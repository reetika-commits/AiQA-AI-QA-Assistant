# AiQA-AI-QA-Assistant

AI-powered Test Case Generator for QA Engineers.

## Overview
AiQA is a REST API built with FastAPI that uses Google's Gemini LLM to generate software test cases from plain English requirements. The application accepts a requirement, sends it to Gemini, receives structured test cases, and stores the request and response for future reference.

SQLite Integration & Postman Testing ✅

## Features Implemented

### SQLite Database Integration
- Created SQLite database for persistent storage.
- Designed relational database with two tables:
  - *story*
  - *testcase*
- Established one-to-many relationship using story_id.

### Story Table
Stores information about each AI request.

| Column | Description |
|---------|-------------|
| story_id | Primary Key |
| title | User requirement/story |
| model_used | AI model used to generate test cases |
| status | Success/Failed |
| created_at | Timestamp |

### Testcase Table
Stores generated test cases.

| Column | Description |
|---------|-------------|
| testcase_id | Primary Key |
| story_id | Foreign Key |
| title | Test case title |
| preconditions | Preconditions |
| test_steps | Test execution steps |
| expected_result | Expected result |
| priority | Test priority |

## Functionality Added

- SQLite database connection
- Automatic table creation
- Story insertion
- Test case insertion
- Status tracking (Success / Failed)
- Model name stored with each execution

## API Flow


Client
   │
   ▼
FastAPI Route
   │
   ▼
AI Service
   │
   ▼
Ollama Service
   │
   ▼
Prompt Builder
   │
   ▼
Ollama Model
   │
   ▼
JSON Response
   │
   ▼
SQLite Database


## Testing

### Swagger UI
- Successfully generated AI test cases.
- Verified database insertion.

### Postman
- Successfully tested POST endpoint.
- JSON request accepted.
- AI response received.
- Story and test cases stored in SQLite.

## Technologies Used

- Python
- FastAPI
- Ollama (qwen2.5:3b)
- SQLite
- VS Code
- Postman

## Status

✅ SQLite Integration Complete

✅ Database Persistence Complete

✅ Postman Testing Complete

Next Phase:
- Hugging Face Integration
- LangChain Integration

## Author
Reetika Srivastava
QA Automation Engineer | Python | FastAPI | AI Applications
