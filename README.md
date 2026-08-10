# 🤖 AiQA – AI-Powered QA Assistant

## 📌 Overview

*AiQA* is an AI-powered QA assistant that generates software test cases from user requirements.

The project combines *FastAPI, LLMs, LangChain, and SQLite* to create an extensible AI-based test case generation system.

The application is designed with a *multi-provider architecture*, allowing different AI providers to be used without changing the API or database layer.

Currently supported:

- Local LLM using *Ollama*
- Cloud LLM using *Hugging Face Inference API*
- *LangChain + ChatOllama*

The long-term goal is to extend AiQA into an AI-powered testing assistant capable of understanding application features, inspecting live web applications, generating test cases, and eventually executing tests through browser automation.

---

# 🎯 Project Goal

The goal of AiQA is to reduce the manual effort involved in creating software test cases.

Instead of manually converting a requirement into multiple test scenarios, the user can provide a requirement such as:

```text
User Registration
---

# Features

- Added Langchain integration with ChatOllama
- Added Hugging Face cloud integration
- Created huggingface_service.py
- Used huggingface_hub.InferenceClient
- Added provider selection using AI_PROVIDER
- Stored API key securely in .env
- Configured model name through environment variables
- Successfully generated test cases using Hugging Face hosted models
- Saved generated test cases into SQLite database
- Added provider tracking in Story table
- Improved architecture for supporting multiple AI providers

---

# Environment Variables

env
AI_PROVIDER=langchain

OLLAMA_MODEL=qwen2.5:3b

HF_API_KEY=your_huggingface_api_key
HF_MODEL=Qwen/Qwen3-Coder-30B-A3B-Instruct


---

# Supported AI Providers

| Provider | Type | Status |
|----------|------|--------|
| Ollama | Local LLM | ✅ Completed |
| Hugging Face | Cloud LLM | ✅ Completed |
| LangChain | Framework | ✅ Completed |

---

# Architecture


                        API Request
                           │
                           ▼
                     FastAPI Route
                           │
                           ▼
                      AI Service
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
          Ollama      Hugging Face   LangChain
          Service       Service      + ChatOllama
             │             │             │
             └─────────────┼─────────────┘
                           │
                           ▼
                     Prompt Builder
                           │
                           ▼
                         LLM
                           │
                           ▼
                    JSON Response
                           │
                           ▼
                    Response Parsing
                           │
                           ▼
                    SQLite Database


---


# Postman Test

*Endpoint*


POST /generate_testcases


*Request Body*

json
{
    "requirements": "User Registration"
}


---

# Output

- AI provider selected dynamically
- Test cases generated successfully
- JSON response parsed
- Test cases stored in SQLite
- Story information stored with provider details

---

# Challenges Faced

- Modified response parsing to support LAngchain output

---

# Learning

- Hugging Face Inference API
- InferenceClient
- Cloud-hosted LLM integration
- Fine-Grained API Tokens
- Dynamic provider selection using environment variables
- Provider-specific response handling

---

# Next Steps

- Integrate LangAgent


---

## Project Progress

- ✅ Phase 1 – FastAPI Setup
- ✅ Phase 2 – Ollama Integration
- ✅ Phase 3 – Dynamic AI Provider Architecture
- ✅ Phase 4 – Hugging Face Integration
- ✅ Phase 5 – LangChain Integration

## Author
Reetika Srivastava
QA Automation Engineer | Python | FastAPI | AI Applications
