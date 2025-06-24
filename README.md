# QUIZ_APP_USING_FASTAPI_REACTJS

# 🧠 Quiz Application (React + FastAPI)

A full-stack quiz web application where users can select categories, answer timed questions with dynamic validation (string, numeric, boolean), and receive their score and result by email.

---

## 📌 Features

- ✅ Dynamic question types (String, Numeric, Boolean)
- ⏱️ Countdown timer (auto-submits when time ends)
- 📝 Save & Mark for Review
- 📧 Result emailed to the user
- 🧠 Question type validation (type, min/max limits)
- 📊 Score and detailed result analysis (correct/incorrect)
- 📂 Admin can manage categories and questions via API

---

## ⚙️ Technologies Used

### 🖥️ Frontend
- React.js
- CSS

### 🧪 Backend
- FastAPI
- SQLAlchemy (SQLite DB)
- Pydantic (Validation)
- SMTP (Email via Gmail)

**Run with specific host and port**
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

**Run the FastAPI Server (development mode)**
uvicorn main:app --reload

**requirements.txt**
fastapi
uvicorn
sqlalchemy
pydantic
email-validator
