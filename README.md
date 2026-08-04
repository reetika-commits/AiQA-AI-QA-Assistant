# AiQA-AI-QA-Assistant

AI-powered Test Case Generator for QA Engineers.

# ✨ Hugging Face AI Provider Integration

## Overview

Added *Hugging Face* as the second AI provider for the AIQA Assistant.

The application now supports both *local* and *cloud* Large Language Models through a common service layer. AI providers can be switched by changing a single environment variable without modifying the application code.

---

# Features

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
AI_PROVIDER=huggingface

OLLAMA_MODEL=qwen2.5:3b

HF_API_KEY=your_huggingface_api_key
HF_MODEL=Qwen/Qwen3-Coder-30B-A3B-Instruct


---

# Supported AI Providers

| Provider | Type | Status |
|----------|------|--------|
| Ollama | Local LLM | ✅ Completed |
| Hugging Face | Cloud LLM | ✅ Completed |
| LangChain | Framework | 🚧 Coming Next |

---

# Architecture


API Request
      │
      ▼
AI Service
      │
      ▼
AI Provider Selection
      │
 ┌────┴─────────────┐
 │                  │
 ▼                  ▼
Ollama        Hugging Face
 │                  │
 └──────┬───────────┘
        ▼
 JSON Response
        ▼
SQLite Database


---

# Database Updates

Enhanced the Story table to record the AI provider used.

New columns:

- provider_name
- model_name

This allows tracking which AI model generated each set of test cases.

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

- Fixed FastAPI module import issue
- Resolved Hugging Face token permission errors
- Learned Hugging Face Fine-Grained Token permissions
- Understood provider-specific response formats
- Modified response parsing to support Hugging Face output

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

- Integrate LangChain
- Standardize response parsing across providers
- Add support for additional LLM providers
- Introduce common AI provider interface for better scalability

---

## Project Progress

- ✅ Phase 1 – FastAPI Setup
- ✅ Phase 2 – Ollama Integration
- ✅ Phase 3 – Dynamic AI Provider Architecture
- ✅ Phase 4 – Hugging Face Integration
- 🚧 Phase 5 – LangChain Integration

## Author
Reetika Srivastava
QA Automation Engineer | Python | FastAPI | AI Applications
