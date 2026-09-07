# ProProfile AI 

**ProProfile AI** is an AI-powered professional profile assistant that allows HR/recruiters to ask questions about a candidate's professional profile and receive intelligent, context-aware answers.

The application uses a **React/Vite frontend**, **FastAPI backend**, and **Groq LLM** to process questions and generate responses based on the candidate's professional information.

## 🌐 Live Demo - https://mohitaiassistance.onrender.com/


## 🚀 Project Overview

The main goal of this project is to create an AI assistant that can act as a **professional profile representative**.

Instead of an HR/recruiter reading through a complete resume, they can simply ask questions such as:

* "Tell me about the candidate's experience."
* "What technical skills does the candidate have?"
* "What projects has the candidate worked on?"
* "Why would this candidate be suitable for an AI Developer role?"
* "What is the candidate's educational background?"

The AI processes the question and returns a relevant response.

---

# 🏗️ Project Architecture

```text
                         GitHub
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       Frontend                    Backend
        Render                     Render
             │                           │
   React + Vite                  FastAPI + Python
             │                           │
             └───────────┬───────────────┘
                         │
                         ▼
                    Groq LLM
                         │
                         ▼
                  AI Generated Answer
```

---

# 📁 Project Structure

```text
ProProfile_AI/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   └── ...
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── .gitignore
└── README.md
```

---

# 🛠️ Technologies Used

## Frontend

* React
* Vite
* JavaScript
* HTML
* CSS

## Backend

* Python
* FastAPI
* Uvicorn
* Pydantic
* PyPDF

## AI

* Groq API
* `openai/gpt-oss-120b`

## Database / Vector Search

* Qdrant

## Deployment

* GitHub
* Render

---

# ⚙️ How the Project Works

### Step 1 — User asks a question

The recruiter enters a question in the frontend chat interface.

Example:

```text
What projects has the candidate worked on?
```

### Step 2 — Frontend sends the request

The React frontend sends a `POST` request to:

```text
/chat
```

The deployed backend URL is:

```text
https://proprofile-ai-backend.onrender.com
```

The complete API endpoint is:

```text
https://proprofile-ai-backend.onrender.com/chat
```

### Step 3 — FastAPI receives the request

The FastAPI backend receives the question using a Pydantic request model.

Example request:

```json
{
  "question": "What projects has the candidate worked on?"
}
```

### Step 4 — Resume/Profile information is processed

The backend uses the candidate's professional information to provide relevant context for the AI model.

### Step 5 — Groq processes the question

The backend sends the relevant context and user question to the Groq API using:

```text
openai/gpt-oss-120b
```

### Step 6 — AI generates the response

The model generates a professional response based on the available candidate information.

### Step 7 — Response is returned to the frontend

FastAPI sends the generated answer back to the React frontend.

The frontend displays the response in the chat interface.

---

# 🔐 Environment Variables

The project uses environment variables for sensitive credentials.

Example:

```env
GROQ_API_KEY=your_groq_api_key
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key
```

For the frontend deployment:

```env
VITE_API_URL=https://proprofile-ai-backend.onrender.com
```



---

# 🌍 CORS Configuration

Because the frontend and backend are deployed separately, the FastAPI backend needs to allow requests from the frontend.

The backend uses FastAPI's `CORSMiddleware`.

Example:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://mohitaiassistance.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

This allows both:

* Local development
* Production frontend

---

# 💻 Local Development

## Backend

Navigate to the backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run FastAPI:

```bash
uvicorn main:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Frontend

Navigate to the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run the development server:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

---

# 🚀 Deployment

## 1. GitHub

The complete project is maintained in GitHub.

Whenever changes are pushed:

```bash
git add .
git commit -m "your commit message"
git push
```

the connected deployment service can automatically deploy the latest version.

---

## 2. Backend Deployment — Render

The FastAPI backend is deployed as a **Render Web Service**.

### Configuration

```text
Root Directory:
backend
```

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Backend URL

```text
https://proprofile-ai-backend.onrender.com
```

---

## 3. Frontend Deployment — Render

The React/Vite frontend is deployed separately as a **Render Static Site**.

### Configuration

```text
Root Directory:
frontend
```

### Build Command

```bash
npm install && npm run build
```

### Publish Directory

```text
dist
```

### Environment Variable

```text
VITE_API_URL=https://proprofile-ai-backend.onrender.com
```

### Frontend URL

```text
https://mohitaiassistance.onrender.com/
```

---

# 🔄 Deployment Flow

After making changes locally:

```text
1. Modify code
       ↓
2. Test locally
       ↓
3. git add .
       ↓
4. git commit
       ↓
5. git push
       ↓
6. GitHub updated
       ↓
7. Render detects changes
       ↓
8. Application redeployed
```

This makes future updates easier.

For example, when the professional profile/resume is updated and the changed file is committed and pushed to GitHub, the deployment can automatically rebuild the application.

---

# 🧪 API Endpoint

### Chat

**POST**

```text
/chat
```

Production endpoint:

```text
https://proprofile-ai-backend.onrender.com/chat
```

### Request

```json
{
  "question": "Tell me about the candidate's experience."
}
```

### Response

The API returns the AI-generated professional response.

---

# 📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI:

https://proprofile-ai-backend.onrender.com/docs

This can be used to test API endpoints directly.

---

# 🎯 Key Features

* 🤖 AI-powered professional profile assistant
* 💬 Interactive recruiter/HR chat interface
* 📄 Resume/profile-based responses
* ⚡ FastAPI backend
* 🧠 Groq-powered LLM
* 🔐 Environment variable based API key management
* 🌐 Production deployment
* 🔄 GitHub-based deployment workflow
* 🔗 Frontend and backend API integration
* 🛡️ CORS configuration for production

---

# 🔮 Future Improvements

Possible future improvements include:

* Authentication and user management
* Multiple candidate profiles
* Recruiter dashboard
* Conversation history
* Resume upload through the UI
* Better response citations
* Analytics for recruiter questions
* Custom AI personalities
* Streaming AI responses
* More advanced RAG pipeline
* Automated resume updates
* Custom domain

---

# 👨‍💻 Author

**Mohit**

AI / ML Developer

---

## ⭐ Project

If you find this project interesting, consider giving the repository a ⭐ on GitHub.
