# Intra-Group Collaboration Report
## OSSD Final Term Project — QuizGen (Quiz Generator from PDF/Text)

---

### 1. Group Overview

| Detail | Info |
|---|---|
| **Project Title** | QuizGen — AI Quiz Generator from PDF/Text |
| **Technology** | Python Tkinter + GitHub Models API (GPT-4o-mini) + SQLite |
| **Repository** | https://github.com/AyeshCoder/quizgen |

---

### 2. Role Distribution

| Member Name | Role | Feature Branch |
|---|---|---|
| Muhammad Ayesh — **Group Lead** | Project Lead, Home Screen, API Integration | `feature/ayesh/home-screen` |
| Malik Abdul Moeed | Quiz Screen & Navigation | `feature/moeed/quiz-screen` |
| Muhammad Touseef | Results Screen & Scoring | `feature/touseef/results-screen` |
| Ahmed Faizan | History Screen & Database | `feature/faizan/history-db` |

---

### 3. Key Contributions

#### Muhammad Ayesh — Group Lead
- Set up the GitHub repository, branch protection rules.
- Built `home_screen.py`: text/PDF input UI, settings, generate flow.
- Wrote `main.py` (app entry point and screen routing logic).
- Integrated GitHub Models API (GPT-4o-mini) in `utils/quiz_generator.py`.
- Maintained README.md and submitted all reports.

#### Malik Abdul Moeed
- Implemented `quiz_screen.py`: MCQ display, option selection, prev/next navigation, answer map grid, progress bar.

#### Muhammad Touseef
- Implemented `results_screen.py`: score computation, per-question review cards with correct/wrong highlighting, explanations, retry flow.

#### Ahmed Faizan
- Implemented `history_screen.py` and `utils/database.py`: SQLite schema, CRUD operations, session cards with delete/review buttons.

---

### 4. Meeting Schedule & Planning Strategy

| Date | Format | Agenda |
|---|---|---|
| Week 1, Day 1 | In-person | Project selection, role assignment, repo setup |
| Week 1, Day 4 | WhatsApp Group | Screen wireframes, agreed on shared styles |
| Week 2, Day 2 | In-person | Integration testing, merge all branches |
| Week 2, Day 4 | In-person | Final testing, README review, submission prep |

**Communication**: WhatsApp group for quick updates; GitHub Issues for task tracking; weekly in-person sync.

---

### 5. Challenges & Resolution

| Challenge | Resolution |
|---|---|
| Tkinter wraplength not updating on resize | Used `<Configure>` event to dynamically update label width |
| AI API sometimes returns markdown around JSON | Added regex strip before `json.loads()` |
| PDF text extraction varying by PDF type | Implemented PyMuPDF + pypdf two-layer fallback |
| Python 3.13 lambda closure bug | Captured variables explicitly in lambda default args |
| Free API rate limits and region blocks | Switched to GitHub Models API (GPT-4o-mini) — reliable and free |

---

*Report prepared by Muhammad Ayesh on behalf of the team.*
