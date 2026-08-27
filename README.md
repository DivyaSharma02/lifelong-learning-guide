# 🎓 Lifelong Learning Guide

> **Personalized, beginner-friendly learning paths for career transitioners — powered by Groq AI.**

A multi-agent Streamlit app that takes your **target career goal** and **current background**, then generates a step-by-step learning roadmap with real, curated courses.

---

## ✨ Features

- 🔍 **Curator Agent** — analyzes the skill gap between your background and target role
- 📦 **Matcher Agent** — selects the best beginner courses from the database
- 🔬 **Evaluator Agent** — self-corrects the roadmap if any course is too advanced
- 🔄 **Agentic loop** — up to 3 self-correction iterations for quality assurance

---

## 🚀 Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your Groq API key

Copy the example secrets file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Then edit `.streamlit/secrets.toml` and replace the placeholder:
```toml
GROQ_API_KEY = "gsk_YOUR_GROQ_API_KEY_HERE"
```

> 🔑 Get a **free** Groq API key at [console.groq.com](https://console.groq.com)

### 4. Run the app
```bash
streamlit run main_app.py
```

---

## ☁️ Deploy on Streamlit Cloud

1. Push this repo to GitHub (**`secrets.toml` is git-ignored — it will NOT be uploaded**)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app** → select your repo
3. In **Advanced settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "gsk_YOUR_GROQ_API_KEY_HERE"
   ```
4. Click **Deploy** 🎉

---

## 📁 Project Structure

```
PROJECT/
├── main_app.py              # Streamlit UI
├── learning_agents.py       # Curator / Matcher / Evaluator agents + Groq API client
├── course_db.py             # Course database loader & search utility
├── requirements.txt         # Python dependencies
├── data/
│   └── courses.csv          # Course catalog
└── .streamlit/
    ├── secrets.toml         # ⛔ Local only — gitignored
    └── secrets.toml.example # ✅ Safe template to commit
```
