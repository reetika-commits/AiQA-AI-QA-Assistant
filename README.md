# AiQA – AI-Powered QA Automation Assistant

AiQA is an AI-powered QA automation system that combines browser automation,
vision-language models, LLMs and workflow orchestration to generate
application-specific test cases.

## What it does

Given:

- Application URL
- Feature screenshot
- QA requirement

AiQA:

1. Opens the application and extracts page text + DOM.
2. Uses a Vision-Language Model to identify the UI elements shown in the screenshot.
3. Maps those elements to the actual DOM.
4. Generates structured QA test cases using an LLM.
5. Stores generated test cases in SQLite.

## Architecture

```text
User
  │
  ▼
FastAPI Route
  │
  ▼
QA Agent
  │
  ▼
LangGraph
  │
  ├── Browser Node
  │      └── Page Text + DOM
  │
  └── Vision Node
         └── Screenshot + DOM
                │
                ▼
          Qwen2.5-VL:3B
                │
                ▼
          Relevant DOM
                │
                ▼
          Prompt Builder
                │
                ▼
           AIService
                │
                ▼
           Qwen2.5:3B
                │
                ▼
          Test Cases
                │
                ▼
             SQLite
---

# Output

- AI provider selected dynamically
- Test cases generated successfully
- JSON response parsed
- Test cases stored in SQLite
- Story information stored with provider details

---

# Key Components

BrowserService:
Uses Selenium to open the application and collect:
- Visible page text
- Full DOM

VisionService:
Uses Qwen2.5-VL:3B to correlate the feature screenshot with the actual DOM and return only the relevant UI elements.

LangGraph:
Orchestrates the dependency between browser inspection and visual analysis, passing the DOM through graph state.

AIService:
Handles LLM-based test case generation using the selected AI provider.

SQLite:
Stores generated test cases and provides the foundation for future test-case retrieval.

---

# Tech Stack

- Python
- FastAPI
- Seenium
- Pytest
- LangChain
- LangGraph
- Ollama
- Qwen2.5:3B
- Qwen2.5-VL:3B
- Pydantic
- SQLite

---

# Current Status

- Browser inspection
- DOM extraction
- Screenshot analysis
- Vision + DOM correlation
- LangGraph workflow
- LLM test case generation
- SQLite persistence
- End-to-end execution from main

---

## Next: RAG
The next phase is Test Case Intelligence using RAG.
The planned workflow:
New Request
    │
    ▼
Search Existing Test Cases
    │
    ├── Exact Match ──► Reuse
    │
    ├── Similar Match ─► Retrieve + Adapt
    │
    └── No Match ─────► Generate with LLM
                              │
                              ▼
                           SQLite

The goal is to reduce unnecessary LLM calls and reuse existing QA
knowledge.
Future versions may also use saved screenshots for duplicate/similarity
detection.

---

## Running Locally
- Create and activate a virtual environment:
       python -m venv .venv
       .venv\Scripts\activate

- Install dependencies:
       pip install -r requirements.txt

- Make sure Ollama is running with:
       qwen2.5:3b
       qwen2.5vl:3b

- Start the application using the project's FastAPI entry point.

---

## Author
Reetika Srivastava
QA Automation Engineer | Python | FastAPI | AI Applications
