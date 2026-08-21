import sys
import json
import time
import requests
from typing import List, Dict, Tuple, Any
from pydantic import BaseModel, Field

from course_db import search_courses_by_skills, load_all_courses

# ── Pydantic Structured Output Schemas ───────────────────────────────────────
class CuratedSkills(BaseModel):
    skills: List[str] = Field(description="Exactly 3 progressive skills the user must learn to bridge the gap.")
    gap_explanation: str = Field(description="Brief explanation of the gap between user background and target role.")

class CourseMatchSelection(BaseModel):
    selected_course_ids: List[str] = Field(description="A list of exactly 3 course IDs matching the required skills.")
    explanation: str = Field(description="Brief rationale for why these courses were selected.")

class EvaluationResult(BaseModel):
    is_beginner_friendly_for_user: bool = Field(description="True if all selected courses suit the user's background, False if any is too advanced.")
    rejected_course_id: str = Field(default="", description="ID of the course that is too advanced. Empty if all approved.")
    rejection_reason: str = Field(default="", description="Why the course was rejected based on the user's lack of prerequisites.")
    suggested_skill_replacement: str = Field(default="", description="A simpler foundational skill to search for instead (e.g. 'Basic Math', 'Intro to Coding').")


# ── Groq API Caller ───────────────────────────────────────────────────────────
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-20b"

def _call_groq(api_key: str, prompt: str, schema_class: type, temperature: float = 0.2) -> str:
    """
    Calls Groq's OpenAI-compatible API.
    Uses schema-in-prompt for structured JSON output natively supported by Groq.
    """
    schema = schema_class.model_json_schema()

    full_prompt = f"""{prompt}

IMPORTANT INSTRUCTION: You MUST respond with ONLY valid, raw JSON that strictly matches this schema:
{json.dumps(schema, indent=2)}

Do NOT include markdown code blocks (no ```json). Only return the raw JSON object.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": full_prompt}],
        "temperature": temperature,
        "response_format": {"type": "json_object"}
    }

    max_retries = 4
    for attempt in range(max_retries):
        response = requests.post(GROQ_URL, headers=headers, json=body)
        if response.status_code == 429:
            time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s, 8s
            continue
            
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
        
    response.raise_for_status()
    return ""


# ── Agents ────────────────────────────────────────────────────────────────────
class CuratorAgent:
    """Agent 1: Analyzes the target role and user background, extracts 3 core skills needed."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def curated_skills(self, target_job: str, user_background: str) -> CuratedSkills:
        prompt = f"""
        You are the 'Curator Agent' for an educational learning platform.
        Analyze the user's Target Role and their current Background to identify exactly 3 core skills they need to bridge the gap.
        
        Target Role: {target_job}
        User Current Background: {user_background}
        
        Identify exactly 3 progressive skills they need to learn for a successful transition.
        Provide a brief explanation of the skill gap.
        
        CRITICAL INSTRUCTION: Write the gap_explanation addressing the user directly in the second-person (using 'your' / 'you' / 'you need'). Never refer to the user in the third-person (like 'the user', 'the user's background', 'they', 'them', 'their'). For example, write "Your background in sales..." instead of "The user's sales background...".
        """
        text = _call_groq(self.api_key, prompt, CuratedSkills, temperature=0.2)
        return CuratedSkills.model_validate_json(text)


class MatcherAgent:
    """Agent 2: Finds the 3 best-fitting beginner courses from the database."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def match_courses(self, skills: List[str], user_background: str) -> Tuple[List[Dict], str]:
        candidates = search_courses_by_skills(skills)
        if not candidates:
            candidates = load_all_courses()

        catalog_formatted = ""
        for c in candidates:
            catalog_formatted += (
                f"- ID: {c['id']}\n"
                f"  Title: {c['title']}\n"
                f"  Platform: {c['platform']}\n"
                f"  Skills: {', '.join(c['skills_addressed'])}\n"
                f"  Difficulty: {c['difficulty']}\n"
                f"  Prerequisites: {', '.join(c.get('prerequisites', []))}\n"
                f"  Description: {c['description']}\n\n"
            )

        prompt = f"""
        You are the 'Content Matcher Agent'.
        Select the 3 most appropriate course IDs from the catalog below to address the needed skills: {', '.join(skills)}.
        User background: "{user_background}".
        
        Candidate Catalog:
        {catalog_formatted}
        
        Select exactly 3 course IDs that best match the needed skills and user's level.
        
        CRITICAL INSTRUCTION: Write the explanation addressing the user directly in the second-person (using 'your' / 'you' / 'you need'). Never refer to the user in the third-person.
        """
        text = _call_groq(self.api_key, prompt, CourseMatchSelection, temperature=0.2)
        match_result = CourseMatchSelection.model_validate_json(text)

        all_courses = load_all_courses()
        selected_courses = [c for c in all_courses if c['id'] in match_result.selected_course_ids]

        if len(selected_courses) < 3:
            selected_courses = candidates[:min(3, len(candidates))]

        return selected_courses, match_result.explanation


class EvaluatorAgent:
    """Agent 3: Checks if selected courses match the user's level. Triggers self-correction if not."""
    def __init__(self, api_key: str):
        self.api_key = api_key

    def evaluate_courses(self, selected_courses: List[Dict], user_background: str) -> EvaluationResult:
        courses_formatted = ""
        for c in selected_courses:
            courses_formatted += (
                f"- ID: {c['id']}\n"
                f"  Title: {c['title']}\n"
                f"  Difficulty: {c['difficulty']}\n"
                f"  Prerequisites: {', '.join(c.get('prerequisites', []))}\n"
                f"  Description: {c['description']}\n\n"
            )

        prompt = f"""
        You are the 'Evaluator Agent'. Check if any selected course is TOO ADVANCED for the user's background.
        
        User Background: {user_background}
        
        Selected Courses:
        {courses_formatted}
        
        Instructions:
        1. Check Difficulty and Prerequisites of each course.
        2. If a course requires skills (Python, Calculus, Linear Algebra, Statistics) the user does not have based on their background, REJECT it.
        3. If rejected: set is_beginner_friendly_for_user=false, fill rejected_course_id, rejection_reason, and suggested_skill_replacement (e.g. 'Basic Math', 'Intro to Python').
        4. If all courses are suitable for a beginner with user's background: set is_beginner_friendly_for_user=true.
        
        CRITICAL INSTRUCTION: Write the rejection_reason addressing the user directly in the second-person (using 'your' / 'you' / 'you need'). Never refer to the user in the third-person.
        """
        text = _call_groq(self.api_key, prompt, EvaluationResult, temperature=0.1)
        return EvaluationResult.model_validate_json(text)


# ── Orchestrator ──────────────────────────────────────────────────────────────
class AgentOrchestrator:
    """Orchestrates the full agentic self-correction loop and records logs."""
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.curator = CuratorAgent(api_key)
        self.matcher = MatcherAgent(api_key)
        self.evaluator = EvaluatorAgent(api_key)
        self.logs = []

    def log(self, message: str):
        self.logs.append(message)

    def run_workflow(self, target_job: str, user_background: str) -> Dict[str, Any]:
        self.log(f"🚀 Workflow started for: **{target_job}** | Your Background: **{user_background}**")

        self.log("🔍 **Curator Agent** analyzing skill gap...")
        curator_res = self.curator.curated_skills(target_job, user_background)
        self.log(f"💡 Gap assessed: *{curator_res.gap_explanation}*")
        self.log(f"   Skills Required: **{', '.join(curator_res.skills)}**")

        active_skills = list(curator_res.skills)
        max_attempts = 3
        attempt = 1
        courses = []

        while attempt <= max_attempts:
            self.log(f"⚖️ **Attempt {attempt}**: Matcher searching for: {', '.join(active_skills)}")
            courses, match_explanation = self.matcher.match_courses(active_skills, user_background)
            self.log(f"📦 **Matcher** selected {len(courses)} courses:")
            for c in courses:
                self.log(f"   - **{c['title']}** ({c['platform']} | {c['difficulty']})")
            self.log(f"   *Rationale*: {match_explanation}")
            
            time.sleep(1) # Prevent bursting API limits

            self.log("🔬 **Evaluator Agent** checking suitability...")
            eval_res = self.evaluator.evaluate_courses(courses, user_background)

            if eval_res.is_beginner_friendly_for_user:
                self.log("✅ **Evaluator**: PASS — all courses are beginner-friendly for you.")
                return {
                    "success": True,
                    "gap_explanation": curator_res.gap_explanation,
                    "skills_identified": curator_res.skills,
                    "learning_path": courses,
                    "logs": self.logs,
                    "iterations": attempt
                }
            else:
                self.log(f"⚡ **Self-Correction**: Rejected **{eval_res.rejected_course_id}** — {eval_res.rejection_reason}")
                self.log(f"   Swapping with foundational skill: `{eval_res.suggested_skill_replacement}`")

                rejected_course = next((c for c in courses if c['id'] == eval_res.rejected_course_id), None)
                swapped = False
                if rejected_course:
                    for tag in rejected_course.get("skills_addressed", []):
                        for idx, skill in enumerate(active_skills):
                            if tag.lower() in skill.lower() or skill.lower() in tag.lower():
                                active_skills[idx] = eval_res.suggested_skill_replacement
                                swapped = True
                                break
                        if swapped:
                            break
                if not swapped:
                    active_skills[-1] = eval_res.suggested_skill_replacement

                attempt += 1

        self.log("⚠️ Max attempts reached. Returning best available curriculum for you.")
        return {
            "success": False,
            "gap_explanation": curator_res.gap_explanation,
            "skills_identified": curator_res.skills,
            "learning_path": courses,
            "logs": self.logs,
            "iterations": max_attempts
        }
