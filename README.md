<div align="center">

# 🚀 CodeMind

### AI-Powered Multi-Agent Coding Assistant

Built for engineers, by engineers.

CodeMind is an intelligent coding assistant that orchestrates multiple specialized AI agents to perform code review, debugging, optimization, documentation, explanation, and GitHub integration within a single workflow.

---

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![LangGraph](https://img.shields.io/badge/LangGraph-Agentic%20AI-orange?style=for-the-badge)
![LangChain](https://img.shields.io/badge/LangChain-LLM-green?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLM-black?style=for-the-badge)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-blue?style=for-the-badge&logo=postgresql)
![Railway](https://img.shields.io/badge/Railway-Deployed-purple?style=for-the-badge)

### 🌐 Live Demo

https://codemind-production.up.railway.app/

</div>

---

# 📖 Overview

CodeMind is an AI-powered multi-agent software engineering platform that automates common development workflows by coordinating specialized Large Language Model (LLM) agents.

Instead of relying on a single AI model for every task, CodeMind intelligently routes requests to dedicated agents responsible for code review, bug fixing, optimization, documentation, explanation, and GitHub operations.

The platform provides a secure backend powered by FastAPI, PostgreSQL, JWT Authentication, and GitHub OAuth, enabling developers to analyze, improve, and manage code directly from one interface.

---

# ✨ Features

## 🤖 Multi-Agent AI Workflow

- Code Review Agent
- Bug Detection Agent
- Code Optimization Agent
- Documentation Agent
- Code Explanation Agent
- GitHub Repository Agent

---

## 📝 Intelligent Code Analysis

- Detects bugs and logical errors
- Identifies anti-patterns
- Reviews coding style
- Suggests performance improvements
- Generates production-ready documentation
- Explains code execution line-by-line

---

## 📂 GitHub Integration

- GitHub OAuth Authentication
- Repository Access
- Push Generated Code
- Repository Management

---

## 🔒 Secure Authentication

- JWT Authentication
- Protected APIs
- Password Hashing using bcrypt
- PostgreSQL User Management

---

## 📊 History Management

- Stores previous analyses
- Tracks generated reports
- User-specific history

---

## ⚡ Fast API Backend

- Modular architecture
- REST APIs
- Pydantic Validation
- SQLAlchemy ORM

---

# 🏗️ System Architecture

```
                        User
                          │
                          ▼
                  FastAPI Backend
                          │
          JWT Authentication & Authorization
                          │
                          ▼
                  Request Router
                          │
     ┌──────────────┬──────────────┬──────────────┐
     ▼              ▼              ▼
Reviewer Agent   Bug Fix Agent   Optimizer Agent
     │              │              │
     └──────────────┼──────────────┘
                    ▼
          Documentation Agent
                    │
                    ▼
          Code Explanation Agent
                    │
                    ▼
             GitHub Integration
                    │
                    ▼
          PostgreSQL + Analysis History
```

---

# 🧠 AI Workflow

```
User submits source code
          │
          ▼
 AI analyzes programming language
          │
          ▼
 Routes request to specialized agent
          │
          ▼
 Generates analysis
          │
          ▼
 Review
 Bug Detection
 Optimization
 Documentation
 Explanation
          │
          ▼
 Stores history
          │
          ▼
 Returns structured response
```

---

# 🛠️ Tech Stack

## Backend

- FastAPI
- Python
- SQLAlchemy
- PostgreSQL (Neon)

## AI

- LangGraph
- LangChain
- Groq LLM
- Prompt Engineering

## Authentication

- JWT
- bcrypt
- GitHub OAuth

## Database

- PostgreSQL
- Neon Cloud

## Frontend

- HTML
- CSS
- Vanilla JavaScript

## Deployment

- Railway

---

# 📁 Project Structure

```
backend/
│
├── app.py
├── routes/
├── services/
├── databases/
├── schema/
├── models/
├── prompts/
│
frontend/
│
├── templates/
├── static/
│
├── css/
├── js/
├── images/
│
requirements.txt
README.md
```

---

# 🚀 Getting Started

## Clone Repository

```bash
git clone https://github.com/Bushra-engr/CODEMIND.git

cd CODEMIND
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env`

```env
DATABASE_URL=

JWT_SECRET_KEY=

GROQ_API_KEY=

GITHUB_CLIENT_ID=

GITHUB_CLIENT_SECRET=
```

---

## Run

```bash
uvicorn backend.app:app --reload
```

Open

```
http://localhost:8000
```

---

# 🔒 Security

- Passwords hashed using bcrypt
- JWT-secured APIs
- OAuth-secured GitHub integration
- Environment-based secret management

---

# 🌟 Future Enhancements

- Multi-language support
- Code execution sandbox
- CI/CD integration
- AI-generated unit tests
- Pull Request review agent
- Team collaboration workspace
- Docker deployment
- Kubernetes support

# 👩‍💻 Developer

## Bushra Khan

BCA Student • AI/ML Enthusiast • Full Stack AI Developer

- LinkedIn: https://www.linkedin.com/in/bushra-khan-1705ba33b/
- GitHub: https://github.com/Bushra-engr

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates further development.

---

## Built with ❤️ using FastAPI, LangGraph, LangChain and Groq.
