AiQA

AI-powered Test Case Generator for QA Engineers

Overview
AiQA is a REST API built with FastAPI that uses Google's Gemini LLM to generate software test cases from plain English requirements.
The application accepts a requirement, sends it to Gemini, receives structured test cases, and stores the request and response for future reference.

Features
AI-powered test case generation
FastAPI REST API
Interactive Swagger UI
Structured JSON responses
SQLite database integration
Input validation using Pydantic
Clean project architecture

Tech Stack
Python
FastAPI
Google Gemini API
Pydantic
SQLite
Uvicorn
Swagger UI

Project Structure
AiQA/
│
├── app/
├── config/
├── database/
├── models/
├── prompts/
├── routes/
├── services/
├── tests/
│
├── .env
├── requirements.txt
└── README.md

Installation
git clone <repository-url>

cd AiQA

python -m venv .venv

source .venv/bin/activate
Windows
.venv\Scripts\activate

Install dependencies
pip install -r requirements.txt
Environment Variables
Create a .env file.
GOOGLE_API_KEY=your_api_key_here
Run the Application
uvicorn app.main:app --reload
Swagger UI
Open
http://127.0.0.1:8000/docs
API Endpoint
Generate Test Cases
POST
/generate-testcases
Example Request
{
  "requirement": "User should be able to login using email and password."
}

Future Enhancements
API test case generation
Selenium script generation
Export to Excel
Jira integration
Authentication
Docker support

Author
Reetika Srivastava
QA Automation Engineer | Python | FastAPI | AI Applications