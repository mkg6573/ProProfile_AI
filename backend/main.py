from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
from pypdf import PdfReader
import json
import os
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel

load_dotenv()
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
model = "openai/gpt-oss-120b"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","https://proprofile-ai-backend.onrender.com/"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# parse resume


class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []


class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []


resume_schema = Resume.model_json_schema()


class ChatRequest(BaseModel):
    question: str




def ask_candidate(question: str, resume: Resume):

    system_prompt = f"""
You are HireMeAI, an AI assistant representing a job candidate.

You must answer questions ONLY using information contained
in the candidate's resume.

CANDIDATE RESUME:
{resume.model_dump_json(indent=2)}

STRICT RULES:

1. Use ONLY information present in the resume.

2. NEVER hallucinate, assume, infer, or add information.

3. If the requested information is not available in the resume,
respond exactly:

I don't have enough information to answer that.

4. Do not use your general knowledge.

5. Answer only what the user asked.

6. Keep answers concise and factual.

7. Preserve exact names, numbers, technologies, companies,
roles, dates, and achievements from the resume.

8. Do NOT write the entire answer in one paragraph.

9. Every section, project, experience, and field MUST be
separated by a new line.

10. Leave ONE blank line between different projects,
experiences, or sections.

11. For multiple items, use numbered lists.

12. For projects, ALWAYS use exactly this structure:

Projects

1. Project Name

Description: ...

Technologies: ...

Team Size: ...

Result: ...

2. Project Name

Description: ...

Technologies: ...

Team Size: ...

Result: ...

13. If a project field is missing from the resume,
DO NOT write "not specified", "N/A", "unknown",
or any other placeholder.

Simply omit that field.

14. For skills:

Skills

- Skill
- Skill
- Skill

15. For experience:

Experience

1. Company: ...
Role: ...
Duration: ...
Description: ...
Skills Used: ...

16. For education:

Education

- Education item

17. For certifications:

Certifications

- Certification

18. Do not create tables unless the user explicitly asks
for a table.

19. Do not add introductions such as:
"Below are..."
"According to the profile..."
"Based on the information provided..."

20. Do not add conclusions or summaries unless the user asks.

21. IMPORTANT:
Use actual newline characters between every field.
Do NOT put multiple fields on the same line.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content








def parse_resume(resume_text):
    system_prompt = f"""
    You are an expert resume parser.

    Extract information from the resume based on its meaning,
    not only based on exact section headings.

    Different resumes may use different headings.

    For example:
    - Experience
    - Professional Experience
    - Work History
    - Employment
    - Internships

    These may all contain relevant experience.

    Skills may also appear in the skills section, work experience,
    internships or projects.

    Return ONLY valid JSON matching this schema:

    {resume_schema}

    Important rules:

    1. Do not invent information.
    2. If a value is not available, return null.
    3. If a list has no information, return an empty list.
    4. Include internships inside experiences.
    5. Extract skills mentioned across the entire resume.
    """
    user_prompt = f"""
    Parse the following resume:

    {resume_text}
    """
    message_system = {
        "role": "system",
        "content": system_prompt
    }
    message_user = {
        "role": "user",
        "content": user_prompt
    }
    messages = [message_system, message_user]
    response_format = {
        "type": "json_object"
    }
    response = client.chat.completions.create(
        model=model, messages=messages, response_format=response_format)
    raw_output = response.choices[0].message.content
    data = json.loads(raw_output)
    resume = Resume(**data)
    return resume

# pdf extraction


def read_pdf(file_path: Path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text

# decorater , homepage


@app.get("/")
def home():
    return {
        "messsage": "hiremeAI is running !"
    }


@app.post("/chat")
def chat(request: ChatRequest):
    resume_text = read_pdf(Path("my_resume.pdf"))
    resume = parse_resume(resume_text)
    answer = ask_candidate(request.question, resume)
    return {
        "answer": answer
    }
