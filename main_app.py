import sys
import os
import site

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, site.USER_SITE)

import streamlit as st
import time

# Load API key from Streamlit secrets (set in .streamlit/secrets.toml locally,
# or via the Streamlit Cloud dashboard when deploying publicly)
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", "")

# Page Configuration
st.set_page_config(
    page_title="Lifelong Learning Guide",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom Sleek Premium CSS (Dark Theme, Playfair & Plus Jakarta Sans, Champagne Gold Theme)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;0,700;0,800;1,400&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');
    
    /* Overall page adjustments */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Adjust page width to be wider and elegant */
    .block-container {
        max-width: 1100px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }
    
    .stApp {
        background: radial-gradient(circle at top center, #0F172A 0%, #030712 100%) !important;
        color: #F1F5F9 !important;
    }
    
    /* Header Container styling */
    .title-container {
        text-align: center;
        padding: 3rem 0 2rem 0;
        margin-bottom: 1rem;
    }
    
    .title-text {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 850;
        background: linear-gradient(135deg, #FDFBF7 0%, #E2B857 50%, #B8860B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -1px;
        margin-bottom: 0.75rem;
        text-shadow: 0 4px 20px rgba(212, 175, 55, 0.15);
    }
    
    .subtitle-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1.15rem;
        color: #94A3B8;
        letter-spacing: 0.2px;
        font-weight: 300;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Styled Form Container */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.65) !important;
        border: 1px solid rgba(226, 184, 87, 0.15) !important;
        border-radius: 20px !important;
        padding: 2.5rem !important;
        backdrop-filter: blur(15px) !important;
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.6) !important;
        margin-bottom: 2rem !important;
    }
    
    /* Labels styling */
    label[data-testid="stWidgetLabel"] p {
        color: #E2E8F0 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.3px;
        margin-bottom: 8px !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Text Inputs */
    div[data-baseweb="input"] {
        background-color: rgba(17, 24, 39, 0.8) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        padding: 4px 8px !important;
    }
    
    div[data-baseweb="input"]:focus-within {
        border-color: #E2B857 !important;
        box-shadow: 0 0 12px rgba(226, 184, 87, 0.25) !important;
        background-color: rgba(17, 24, 39, 0.95) !important;
    }
    
    input {
        color: #F8FAFC !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-size: 0.95rem !important;
    }
    
    /* Form Submit Button */
    button[kind="primaryFormSubmit"] {
        background: linear-gradient(135deg, #E2B857 0%, #B8860B 100%) !important;
        color: #030712 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 2rem !important;
        font-size: 1.05rem !important;
        font-weight: 750 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        box-shadow: 0 4px 20px rgba(226, 184, 87, 0.25) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        letter-spacing: 0.5px;
        margin-top: 10px !important;
    }
    
    button[kind="primaryFormSubmit"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(226, 184, 87, 0.45) !important;
        background: linear-gradient(135deg, #FDFBF7 0%, #E2B857 100%) !important;
        cursor: pointer;
    }
    
    button[kind="primaryFormSubmit"]:active {
        transform: translateY(0) !important;
    }

    /* Progress bar style */
    div[data-testid="stProgress"] {
        margin: 25px 0 !important;
    }
    
    div[data-testid="stProgress"] > div > div > div > div {
        background: linear-gradient(90deg, #2563EB 0%, #8B5CF6 50%, #E2B857 100%) !important;
        border-radius: 10px !important;
        height: 6px !important;
    }
    
    /* Notifications and alerts */
    div[data-testid="stNotification"] {
        background-color: rgba(30, 41, 59, 0.45) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-left: 5px solid #2563EB !important;
        backdrop-filter: blur(12px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15) !important;
        padding: 1rem !important;
    }
    
    div[data-testid="stNotification"] div[role="alert"] {
        background: transparent !important;
        color: #F1F5F9 !important;
    }

    /* Custom headers and separators */
    .section-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.1rem;
        font-weight: 750;
        color: #F8FAFC;
        margin-top: 3rem;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
        position: relative;
        display: inline-block;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -6px;
        left: 0;
        width: 60px;
        height: 3px;
        background: linear-gradient(90deg, #E2B857, #B8860B);
        border-radius: 2px;
    }
    
    .gap-box {
        background: rgba(226, 184, 87, 0.06);
        border-left: 4px solid #E2B857;
        border-radius: 4px 16px 16px 4px;
        padding: 1.4rem 1.8rem;
        margin-top: 1.5rem;
        margin-bottom: 2.5rem;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 1rem;
        line-height: 1.6;
        color: #E2E8F0;
        box-shadow: inset 0 0 15px rgba(0, 0, 0, 0.2);
    }
    
    .gap-box strong {
        color: #F3E5AB;
        font-weight: 600;
        font-family: 'Plus Jakarta Sans', sans-serif;
        text-transform: uppercase;
        font-size: 0.8rem;
        letter-spacing: 1px;
        display: block;
        margin-bottom: 4px;
    }
    
    /* Premium Course Cards */
    .card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 1.8rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(15px);
    }
    
    .card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #E2B857 0%, #2563EB 100%);
        opacity: 0.7;
        transition: opacity 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        border-color: rgba(226, 184, 87, 0.35);
        box-shadow: 0 20px 45px rgba(226, 184, 87, 0.08), 0 5px 15px rgba(0, 0, 0, 0.4);
    }
    
    .card:hover::before {
        opacity: 1;
    }
    
    .step-number {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        color: #E2B857;
        font-weight: 750;
        margin-bottom: 0.6rem;
    }
    
    .card-title {
        font-family: 'Playfair Display', serif;
        color: #FFFFFF;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.8rem;
        line-height: 1.35;
    }
    
    .card-meta-row {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-bottom: 1.2rem;
    }
    
    .meta-badge {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        transition: all 0.2s ease;
    }
    
    .badge-platform {
        border: 1px solid rgba(59, 130, 246, 0.3);
        color: #93C5FD;
        background: rgba(59, 130, 246, 0.1);
    }
    
    .badge-difficulty {
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #6EE7B7;
        background: rgba(16, 185, 129, 0.1);
    }
    
    .prereq-text {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.85rem;
        color: #94A3B8;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .prereq-text strong {
        color: #CBD5E1;
        font-weight: 600;
        margin-right: 6px;
    }
    
    .card-desc {
        color: #CBD5E1;
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 0.98rem;
        line-height: 1.6;
        margin-bottom: 1.8rem;
        font-weight: 300;
    }
    
    .card-link {
        display: inline-flex;
        align-items: center;
        background: rgba(226, 184, 87, 0.05);
        border: 1.5px solid #E2B857;
        color: #E2B857 !important;
        text-decoration: none !important;
        padding: 10px 22px;
        font-size: 0.85rem;
        font-weight: 750;
        border-radius: 30px;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        letter-spacing: 0.5px;
    }
    
    .card-link:hover {
        background: #E2B857 !important;
        color: #030712 !important;
        box-shadow: 0 8px 20px rgba(226, 184, 87, 0.35) !important;
        transform: translateY(-1px);
    }
    
    /* Warning Cards (For alternate routes) */
    .card-warning {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(15px);
    }
    
    .card-warning::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #F59E0B 0%, #EF4444 100%);
        opacity: 0.7;
    }
    
    .card-warning:hover {
        transform: translateY(-3px);
        border-color: rgba(245, 158, 11, 0.35);
    }
    
    /* Expander / Developer Console Styling */
    div[data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.45) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2) !important;
        margin-top: 2rem !important;
    }
    
    div[data-testid="stExpander"] details summary {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        color: #94A3B8 !important;
        padding: 14px 20px !important;
        transition: color 0.2s ease !important;
    }
    
    div[data-testid="stExpander"] details summary:hover {
        color: #E2B857 !important;
    }
    
    div[data-testid="stExpander"] details [data-testid="stVerticalBlock"] {
        background-color: #020612 !important;
        border-radius: 10px !important;
        padding: 2rem !important;
        border: 1px solid rgba(255, 255, 255, 0.04) !important;
        box-shadow: inset 0 5px 20px rgba(0,0,0,0.5) !important;
    }
    
    /* Code logs inner text styling */
    div[data-testid="stExpander"] details [data-testid="stVerticalBlock"] p, 
    div[data-testid="stExpander"] details [data-testid="stVerticalBlock"] div {
        font-family: 'Fira Code', 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
        color: #6EE7B7 !important; /* Mint/Emerald color for logs */
        line-height: 1.7 !important;
    }
</style>
""", unsafe_allow_html=True)

# App Title & Subtitle
st.markdown(
    """
    <div class="title-container">
        <div class="title-text">Lifelong Learning Guide</div>
        <div class="subtitle-text">Personalized, beginner-friendly learning paths for career transitioners.</div>
    </div>
    """,
    unsafe_allow_html=True
)

import re

def sanitize_text_to_second_person(text: str) -> str:
    if not text:
        return text
    # Replace key third-person references with second-person
    text = re.sub(r'\b[tT]he user\'s\b', 'your', text)
    text = re.sub(r'\b[uU]ser\'s\b', 'your', text)
    text = re.sub(r'\b[tT]he user\b', 'you', text)
    text = re.sub(r'\btheir current background\b', 'your current background', text)
    text = re.sub(r'\btheir background\b', 'your background', text)
    text = re.sub(r'\bthey need\b', 'you need', text)
    text = re.sub(r'\bthem to learn\b', 'you to learn', text)
    text = re.sub(r'\brequiring them\b', 'requiring you', text)
    text = re.sub(r'\b[tT]he user lacks\b', 'you lack', text)
    text = re.sub(r'\b[tT]he user has\b', 'you have', text)
    text = re.sub(r'\b[tT]he user is\b', 'you are', text)
    text = re.sub(r'\bsuit the user\b', 'suit you', text)
    text = re.sub(r'\b[uU]ser lacks\b', 'you lack', text)
    return text

# Form entry
with st.form("learning_path_form"):
    col1, col2 = st.columns(2)
    with col1:
        target_role_input = st.text_input("Target Career Goal", value="", placeholder="e.g. Data Analyst, Software Engineer")
    with col2:
        user_bg = st.text_input("Your Current Background", value="", placeholder="e.g. Sales, your experience")
        
    submit_btn = st.form_submit_button("Generate Roadmap 🚀", use_container_width=True)

if submit_btn:
    target_role = target_role_input.strip()
    
    if not GROQ_API_KEY:
        st.warning("⚠️ API key not configured. Please set GROQ_API_KEY in your Streamlit secrets.")
    elif not target_role or not user_bg:
        st.warning("⚠️ Please provide both a target career goal and your current background.")
    else:
        from learning_agents import AgentOrchestrator
        
        # Run orchestrator
        orchestrator = AgentOrchestrator(GROQ_API_KEY)
        
        progress_bar = st.progress(10)
        status_text = st.empty()
        
        status_text.write("🔍 Curator Agent analyzing skill gaps...")
        progress_bar.progress(30)
        
        try:
            result = orchestrator.run_workflow(target_role, user_bg)
            progress_bar.progress(80)
            status_text.write("🔬 Checking course applicability and level requirements...")
            time.sleep(0.5)
            progress_bar.progress(100)
            status_text.empty()
            
            if result.get("success"):
                st.markdown('<div class="section-title">🎓 Your Personalized Roadmap</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="gap-box"><strong>Gap Analysis:</strong> {sanitize_text_to_second_person(result.get("gap_explanation"))}</div>', unsafe_allow_html=True)
                
                # Render courses list
                for i, course in enumerate(result.get("learning_path", []), 1):
                    prereqs = "None"
                    if course.get('prerequisites'):
                        prereqs = ', '.join(course.get('prerequisites', []))
                    st.markdown(
                        f"""
                        <div class="card">
                            <div class="step-number">Step {i}</div>
                            <div class="card-title">{course['title']}</div>
                            <div class="card-meta-row">
                                <span class="meta-badge badge-platform">{course['platform']}</span>
                                <span class="meta-badge badge-difficulty">{course['difficulty']}</span>
                            </div>
                            <div class="prereq-text">
                                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right: 6px; display: inline-block; vertical-align: middle;"><path d="M12 22c5.523 0 10-4.477 10-10S17.523 2 12 2 2 6.477 2 12s4.477 10 10 10z"></path><path d="m9 12 2 2 4-4"></path></svg>
                                <strong>Prerequisites:</strong> {prereqs}
                            </div>
                            <div class="card-desc">{course['description']}</div>
                            <a class="card-link" href="{course['url']}" target="_blank">Start Course &nbsp;↗</a>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                # Clean Expander for Logs
                with st.expander("🛠️ Execution Logs & Diagnostics", expanded=False):
                    for log in result.get("logs", []):
                        st.markdown(sanitize_text_to_second_person(log))
            else:
                st.error("Failed to compile a completely beginner-friendly course path within limit.")
                if result.get("learning_path"):
                    st.markdown('<div class="section-title" style="margin-top: 1.5rem;">Closest Available Courses</div>', unsafe_allow_html=True)
                    for i, course in enumerate(result.get("learning_path", []), 1):
                        st.markdown(
                            f"""
                            <div class="card-warning">
                                <div class="step-number" style="color: #F59E0B;">Step {i} (Unverified)</div>
                                <div class="card-title">{course['title']}</div>
                                <div class="card-meta-row">
                                    <span class="meta-badge badge-platform">{course['platform']}</span>
                                    <span class="meta-badge badge-difficulty">{course['difficulty']}</span>
                                </div>
                                <div class="card-desc" style="margin-bottom: 1.2rem;">{course['description']}</div>
                                <a class="card-link" href="{course['url']}" target="_blank" style="border-color: #F59E0B; color: #F59E0B !important;">Start Course &nbsp;↗</a>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
        except Exception as e:
            st.error(f"Execution Error: {str(e)}")
            st.info("Please make sure your Groq API Key is valid. Get one free at console.groq.com")
