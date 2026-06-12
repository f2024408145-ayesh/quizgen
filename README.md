# ⚡ QuizGen — AI Quiz Generator from PDF/Text

> A Tkinter desktop app that uses AI to generate multiple-choice quizzes from any text or PDF in seconds.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📄 PDF Upload | Extract text from any PDF and generate quiz |
| ✏️ Paste Text | Type or paste any notes, articles, or content |
| 🤖 AI Generation | AI crafts 3–20 questions at chosen difficulty |
| 🎯 3 Difficulty Levels | Easy, Medium, Hard |
| 📊 Score & Review | See your score with per-question explanations |
| 📋 History | All past quizzes saved to SQLite, reviewable anytime |
| 🔁 Retry | Retake any quiz from history |

---

## 🛠 Tools & Technologies

- **Frontend**: Python Tkinter
- **AI Backend**: GitHub Models API (GPT-4o-mini)
- **PDF Reading**: PyMuPDF (`fitz`) with `pypdf` fallback
- **Database**: SQLite (via Python `sqlite3`)
- **Version Control**: Git + GitHub

---

## 🚀 Setup & Running

### Prerequisites

- Python 3.10+
- GitHub personal access token (free)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/AyeshCoder/quizgen.git
cd quizgen

# 2. Install dependencies
pip install pymupdf pypdf

# 3. Add your GitHub token in utils/quiz_generator.py line 11

# 4. Run the app
py main.py
```

---

## 📁 Project Structure

```
quiz_generator/
├── main.py                  # App entry point, screen routing
├── requirements.txt
├── quiz_history.db          # Created at runtime (SQLite)
├── screens/
│   ├── home_screen.py       # Input text/PDF, settings, generate
│   ├── quiz_screen.py       # MCQ questions with navigation
│   ├── results_screen.py    # Score summary + answer review
│   └── history_screen.py   # Past quiz sessions
└── utils/
    ├── database.py          # SQLite CRUD for quiz history
    ├── pdf_reader.py        # PDF text extraction
    ├── quiz_generator.py    # AI API call + parsing
    └── styles.py            # Color palette and font constants
```

---

## 👥 Team Contributions

| Member | Role | Contributions |
|---|---|---|
| Muhammad Ayesh | Group Lead & Home Screen | `home_screen.py`, project setup, README, API integration |
| Malik Abdul Moeed | Quiz Screen | `quiz_screen.py`, navigation logic, progress bar |
| Muhammad Touseef | Results Screen | `results_screen.py`, scoring, answer review |
| Ahmed Faizan | History & Database | `history_screen.py`, `database.py`, SQLite schema |

---

## 📄 License

MIT — free to use and modify for educational purposes.
