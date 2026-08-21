import csv
import os
from typing import List, Dict

# Path to the data directory and courses.json file
DATA_DIR = os.path.dirname(os.path.abspath(__file__))
COURSES_FILE = os.path.join(DATA_DIR, "data", "courses.csv")

def load_all_courses() -> List[Dict]:
    """
    Loads all courses defined in data/courses.csv.
    Falls back to a default course list if the file is missing or invalid.
    """
    if os.path.exists(COURSES_FILE):
        try:
            courses = []
            with open(COURSES_FILE, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    skills = [s.strip() for s in row.get("skills_addressed", "").split(",") if s.strip()]
                    prereqs = [p.strip() for p in row.get("prerequisites", "").split(",") if p.strip()]
                    
                    course = {
                        "id": row.get("id"),
                        "title": row.get("title"),
                        "platform": row.get("platform"),
                        "skills_addressed": skills,
                        "difficulty": row.get("difficulty"),
                        "prerequisites": prereqs,
                        "description": row.get("description"),
                        "url": row.get("url")
                    }
                    courses.append(course)
            return courses
        except Exception:
            pass
            
    # Fallback default courses if json load fails or is missing
    return [
        {
            "id": "ibm-python-basics",
            "title": "Python for Data Science, AI & Development",
            "platform": "IBM SkillsBuild / Coursera",
            "skills_addressed": ["Python", "Coding", "Programming"],
            "difficulty": "Beginner",
            "prerequisites": [],
            "description": "Learn python programming basics, control structures, list manipulations, and functions.",
            "url": "https://www.coursera.org/learn/python-for-applied-data-science-ai"
        },
        {
            "id": "ibm-data-analyst-basics",
            "title": "Introduction to Data Analytics",
            "platform": "IBM SkillsBuild / Coursera",
            "skills_addressed": ["Data Analysis", "Excel", "Data Visualization"],
            "difficulty": "Beginner",
            "prerequisites": [],
            "description": "Understanding data analytics processes, types of data, and working with Excel spreadsheet basics.",
            "url": "https://skillsbuild.org/students/career-paths/data-analyst"
        },
        {
            "id": "khan-pre-algebra",
            "title": "Pre-Algebra & Arithmetic Foundations",
            "platform": "Khan Academy",
            "skills_addressed": ["Basic Math", "Pre-Algebra", "Mathematics"],
            "difficulty": "Beginner",
            "prerequisites": [],
            "description": "Learn core arithmetic, fractions, decimals, negative numbers, and foundations of algebraic representation.",
            "url": "https://www.khanacademy.org/math/pre-algebra"
        },
        {
            "id": "coursera-sql-basics",
            "title": "SQL for Data Science",
            "platform": "Coursera (UC Davis)",
            "skills_addressed": ["SQL", "Databases", "Data Analysis"],
            "difficulty": "Beginner",
            "prerequisites": [],
            "description": "Learn fundamentals of SQL querying, filtering, sorting, joins, and aggregates.",
            "url": "https://www.coursera.org/learn/sql-for-data-science"
        },
        {
            "id": "edx-advanced-machine-learning",
            "title": "Machine Learning and Deep Learning Foundations",
            "platform": "edX (MIT)",
            "skills_addressed": ["Machine Learning", "Artificial Intelligence", "Deep Learning"],
            "difficulty": "Advanced",
            "prerequisites": ["Python", "Calculus", "Linear Algebra", "Statistics"],
            "description": "Explore heavy statistical machine learning formulations, neural networks, loss functions, and backpropagation.",
            "url": "https://www.edx.org/course/machine-learning-with-python-from-linear-models-to-deep-learning"
        },
        {
            "id": "khan-linear-algebra",
            "title": "Linear Algebra (Vectors, Matrices, Spaces)",
            "platform": "Khan Academy",
            "skills_addressed": ["Linear Algebra", "Mathematics"],
            "difficulty": "Intermediate",
            "prerequisites": ["Algebra"],
            "description": "Master vectors, matrix transformations, eigenvalues, and vectors spaces necessary for advanced data science.",
            "url": "https://www.khanacademy.org/math/linear-algebra"
        }
    ]

def search_courses_by_skills(skills: List[str]) -> List[Dict]:
    """
    Finds courses that address any of the skills in the list (case-insensitive keyword matching).
    """
    all_courses = load_all_courses()
    matched = []
    
    # Normalize skills for searching
    search_skills = [s.lower().strip() for s in skills]
    
    for course in all_courses:
        course_skills = [c.lower() for c in course.get("skills_addressed", [])]
        title = course.get("title", "").lower()
        description = course.get("description", "").lower()
        
        match_found = False
        for skill in search_skills:
            if any(skill in cs for cs in course_skills):
                match_found = True
                break
            if skill in title or skill in description:
                match_found = True
                break
                
        if match_found:
            matched.append(course)
            
    return matched
