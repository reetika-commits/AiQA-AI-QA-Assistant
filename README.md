# AiQA – AI-Powered QA Automation Assistant

AiQA is an AI-powered QA automation system that combines browser automation, retrieval-augmented generation (RAG), vision-language models, LLMs, and workflow orchestration to generate application-specific test cases.

## What it does

Given:

- Application URL
- Feature screenshot
- QA requirement

AiQA:

1. Saves the application URL and feature screenshot.
2. Uses RAG to find historically similar requirements and test cases.
3. Calculates semantic similarity using embeddings.
4. Opens the live application using Selenium.
5. Extracts page text, DOM, and a compact QA-oriented DOM representation.
6. Uses LangGraph to orchestrate browser inspection and optional Vision analysis.
7. Uses a Vision-Language Model when the requirement requires visual analysis.
8. Combines the current application UI information with relevant historical test cases.
9. Generates structured QA test cases using an LLM.
10. Returns the generated test cases along with RAG and UI-analysis metadata.

---

## Architecture

User
  │
  ▼
FastAPI Route
  │
  ▼
QA Agent
  │
  ├──────────────────────┐
  │                      │
  ▼                      ▼
RAGService          Save URL / Image
  │
  ├── Create Embedding
  │
  ├── Similarity Search
  │
  ├── Retrieve Historical
  │   Test Cases
  │
  └── Decide needs_vision
             │
             ▼
         LangGraph
             │
             ▼
        Browser Node
             │
             ├── Page Text
             ├── Full DOM
             └── Compact DOM
                    │
                    ▼
              Conditional Route
                 /       \
                /         \
               ▼           ▼
          Vision Node     END
               │
               ▼
        Qwen2.5-VL:3B
               │
               ▼
         Relevant DOM
               │
               └──────────┐
                          ▼
                    Prompt Builder
                          │
                          ▼
                      AIService
                          │
                          ▼
                    Selected LLM
                          │
                          ▼
                     Test Cases
                          │
                          ▼
                        SQLite

---

## RAG / Test Case Intelligence

AiQA uses Retrieval-Augmented Generation to provide historical QA knowledge to the LLM.
The current workflow is:
Current Requirement
        │
        ▼
Create Embedding
        │
        ▼
Compare with Historical Stories
        │
        ▼
Cosine Similarity
        │
        ▼
Top Similar Stories
        │
        ▼
Retrieve Related Test Cases
        │
        ▼
Prompt Builder
        │
        ▼
LLM
        │
        ▼
Current Test Cases

Historical test cases are used as reference material rather than copied directly.
The current application UI, extracted from the live application, remains the source of truth for UI elements and their properties.
This allows AiQA to reuse existing QA knowledge while adapting it to the current requirement and application.

---

## LangGraph Workflow

LangGraph is used to orchestrate the browser and visual analysis workflow.

The graph currently contains:

### Browser Node
Uses Selenium through BrowserService to:
- Open the application URL
- Extract visible page text
- Extract the full DOM
- Build a compact DOM representation focused on QA-relevant elements

The compact DOM reduces unnecessary HTML and provides useful information such as:
- Input fields
- Buttons
- Select/dropdown elements
- Options
- Labels
- Values
- IDs and names
- Relevant ARIA attributes
- Event handlers
- Semantic parent context
- Element state such as checked, disabled, required, and selected

### Conditional Vision Node
LangGraph determines whether visual analysis is required.

Browser Node
     │
     ▼
needs_vision?
   /       \
 Yes       No
  │         │
  ▼         ▼
Vision     END
 Node
  │
  ▼
 END

This demonstrates conditional workflow execution rather than always invoking the Vision model.

---

### VisionService
When visual analysis is required, AiQA uses Qwen2.5-VL:3B.
VisionService receives:
- Feature screenshot
- Compact DOM
- Current QA requirement
It identifies UI elements relevant to the current requirement and returns structured information about those elements.
Example output:

{
    "feature": "Animal Sound Button",
    "elements": [
        {
            "type": "button",
            "description": "Clicks to play an animal sound",
            "selector": "button:onclick=catSound()",
            "dom": "button:onclick=catSound()",
            "status": "found"
        }
    ]
}

---

## Prompt Engineering

AiQA uses separate prompt-building paths depending on whether Vision analysis was required.

### RAG Prompt
Uses:
- Current QA requirement
- Current application UI
- Retrieved historical test cases
Historical test cases provide testing ideas and coverage, while the current application's UI is treated as the authoritative source for UI elements.

### Vision Prompt
Uses:
- Current QA requirement
- Vision-selected relevant DOM
- Retrieved historical test cases
This allows the final LLM to generate test cases using both visual/UI context and historical QA knowledge.

---

## Key Components

### BrowserService
Uses Selenium to open the application and collect:
- Visible page text
- Full DOM
- Compact QA-oriented DOM

### RAGService
Handles:
- Requirement embeddings
- Semantic similarity
- Historical story retrieval
- Related test-case retrieval
- Vision decision based on similarity

### VisionService
Uses Qwen2.5-VL:3B to correlate:
- Screenshot
- Compact DOM
- Current QA requirement and identify relevant UI elements.

### LangGraph
Orchestrates the dependency between:
- Browser inspection
- Conditional Vision analysis
- Shared workflow state

---

## AIService

Provides the abstraction for LLM-based test-case generation and dynamically selects the configured AI provider.

---

## SQLite

Stores application/story and historical test-case information used by the RAG workflow.

---

## Tech Stack

- Python
- FastAPI
- Selenium
- Pytest
- LangChain
- LangGraph
- Ollama
- Qwen2.5:3B
- Qwen2.5-VL:3B
- Pydantic
- SQLite
- Embeddings
- RAG
- Cosine Similarity


### Current Status

Implemented

- FastAPI API layer
- QA Agent
- Selenium browser inspection
- Page text extraction
- Full DOM extraction
- Compact DOM generation
- Screenshot handling
- Vision + DOM correlation
- Conditional Vision workflow
- LangGraph state and routing
- Embedding generation
- Semantic similarity search
- Historical test-case retrieval
- RAG-based test-case generation
- Requirement-aware prompt building
- LLM test-case generation
- Dynamic AI provider selection
- SQLite persistence

---

## Current Scope

AiQA is currently a showcase/learning project demonstrating an AI-assisted QA workflow rather than a fully autonomous test automation platform.
The focus is on demonstrating how traditional QA automation technologies can be combined with modern AI techniques such as:
QA Automation
     +
Python
     +
Selenium / Pytest
     +
RAG
     +
LLM
     +
Vision
     +
LangChain / LangGraph

---

## Running Locally
Create and activate a virtual environment:
python -m venv .venv
.venv\Scripts\activate
Install dependencies:
pip install -r requirements.txt
Make sure Ollama is running with the required models:
qwen2.5:3b
qwen2.5vl:3b
Start the application using the project's FastAPI entry point.

---

## Testing

AiQA uses pytest for automated testing across the main application layers.

### Test Coverage

- Ollama service — mocked LLM response testing
- AI service — provider and database interaction testing
- RAGService — embedding, cosine similarity, similarity ranking,
  top-2 retrieval, and Vision threshold testing
- QA Agent — Vision and non-Vision orchestration paths
- LangGraph — browser node, Vision node, conditional routing,
  and compiled graph workflow
- FastAPI — successful requests, request validation, file uploads,
  and agent failure handling

External dependencies such as Ollama, Selenium, VisionService, and
database operations are mocked where appropriate to keep unit tests
fast and deterministic.

### Running Tests

```bash
pytest -v
```

## Author
Reetika Srivastava
QA Automation Engineer | Python | FastAPI | AI Applications
