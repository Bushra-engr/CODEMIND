# AI Powered Coding Assistant Frontend

This is a lightweight vanilla HTML/CSS/JavaScript frontend for the FastAPI backend.

## How to run

1. Start the FastAPI backend from the project root:

```bash
uvicorn backend.app:app --reload
```

2. Open this file in your browser:

```text
frontend/index.html
```

The frontend expects the backend at:

```text
http://127.0.0.1:8000
```

If your backend runs on another URL, change `API_BASE_URL` in `frontend/app.js`.

## Connected backend endpoints

- `POST /auth/register`
- `POST /auth/login`
- `POST /assistant/analyze`
- `GET /assistant/me`
- `GET /auth/github/login`

No backend logic was changed for this UI.
