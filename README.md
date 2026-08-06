<div align="center">

# 🚀 InterviewIQ

### AI-Powered Interview Preparation Platform

Analyze resumes, generate personalized technical interviews, evaluate answers using AI, and receive detailed hiring feedback.

Built with **FastAPI • React • PostgreSQL • Celery • Redis • Supabase • Gemini AI**

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis)
![Celery](https://img.shields.io/badge/Celery-37814A?style=for-the-badge&logo=celery)
![Gemini](https://img.shields.io/badge/Gemini_AI-4285F4?style=for-the-badge)
![Railway](https://img.shields.io/badge/Railway-000000?style=for-the-badge)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge)

</div>

---

# 📖 Overview

InterviewIQ is an AI-powered interview preparation platform designed to simulate real technical interviews.

The platform analyzes a candidate's resume, generates personalized interview questions using AI, evaluates every response, and produces a detailed interview report including strengths, weaknesses, hiring recommendation, and personalized improvement plan.

The backend is built using production-ready architecture with FastAPI, PostgreSQL, Celery, Redis, JWT Authentication, Background Workers, and Supabase Storage.

---

# ✨ Features

## 🔐 Authentication

- User Registration
- Login
- JWT Authentication
- Refresh Token Rotation
- Email Verification
- Forgot Password
- Password Reset
- Protected Routes
- HttpOnly Cookie Authentication

---

## 📄 Resume Analysis

- Upload Resume (PDF)
- Resume stored in Supabase
- AI Resume Parsing
- ATS Score Generation
- Skills Extraction
- Resume Summary
- Background Processing using Celery

---

## 🤖 AI Interview

- Personalized Questions
- Resume-Based Questions
- Dynamic Follow-up Questions
- Difficulty Levels
- Progress Tracking
- AI Answer Evaluation

---

## 📊 Interview Reports

- Overall Score
- Technical Score
- Communication Score
- Problem Solving Score
- Strengths
- Weaknesses
- Hiring Recommendation
- Improvement Plan
- Question-wise Analysis
- Ideal Answers
- Learning Points

---

## ⚙ Backend Features

- REST API
- SQLAlchemy ORM
- Alembic Migrations
- Celery Workers
- Redis Queue
- PostgreSQL Database
- Supabase Storage
- Brevo Email Service
- Railway Deployment

---

# 🏗 Architecture

```
                    React Frontend
                           │
                     Axios + Cookies
                           │
                   FastAPI Backend
             ┌─────────────┼─────────────┐
             │             │             │
        PostgreSQL      Redis       Supabase
             │             │             │
             │         Celery Worker     │
             │             │             │
             │        Gemini AI          │
             └─────────────┴─────────────┘
```

---

# 🛠 Tech Stack

| Category | Technologies |
|----------|--------------|
| Frontend | React, Redux Toolkit, React Router, Axios |
| Backend | FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL |
| Authentication | JWT, Refresh Tokens, HttpOnly Cookies |
| AI | Google Gemini |
| Queue | Celery |
| Cache | Redis |
| Storage | Supabase |
| Email | Brevo |
| Deployment | Railway |
| Documentation | Swagger / OpenAPI |

---

# 📸 Screenshots

## Login

![Login](screenshots/login.png)

---

## Register

![Register](screenshots/register.png)

---

## Email Verification

![Verification](screenshots/email.png)

---

## Resume Upload

![Resume Upload](screenshots/upload.png)

---

## Resume Analysis

![Resume Analysis](screenshots/resume-analysis.png)

---

## AI Interview

![Interview](screenshots/interview.png)

---

## AI Report

![Report](screenshots/report.png)

---

## Question Analysis

![Question Analysis](screenshots/question-analysis.png)

---

## Reports Dashboard

![Reports](screenshots/reports.png)

---

## Swagger Documentation

![Swagger](screenshots/swagger.png)

---

# 📂 Folder Structure

```
InterviewIQ
│
├── backend
│   ├── app
│   ├── alembic
│   ├── tests
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── public
│   └── package.json
│
└── README.md
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/yourusername/InterviewIQ.git

cd InterviewIQ
```

---

## Backend Setup

```bash
cd backend

python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

alembic upgrade head

uvicorn app.main:app --reload
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

```env
DATABASE_URL=

SECRET_KEY=

AI_API_KEY=

AI_MODEL=

AI_PROVIDER=

REDIS_HOST=

REDIS_PORT=

REDIS_PASSWORD=

SUPABASE_URL=

SUPABASE_KEY=

SUPABASE_BUCKET=

BREVO_API_KEY=

BREVO_FROM_EMAIL=

FRONTEND_URL=
```

---

# 📚 API Documentation

Swagger UI

```
/docs
```

Main Endpoints

```
/api/v1/auth
/api/v1/users
/api/v1/resumes
/api/v1/interviews
/api/v1/dashboard
```

---

# 🌍 Deployment

| Service | Platform |
|----------|----------|
| Frontend | Railway |
| Backend | Railway |
| Database | Railway PostgreSQL |
| Redis | Railway Redis |
| Storage | Supabase |
| Email | Brevo |

---

# 🔮 Future Improvements

- Google OAuth Login
- Voice-Based Interviews
- PDF Report Download
- Analytics Dashboard
- Interview Search
- Dark Mode
- WebSocket Streaming
- Multi-language Interviews

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Rohit Sonar**

- LinkedIn
- GitHub
- Email

---

⭐ If you found this project useful, consider giving it a star.