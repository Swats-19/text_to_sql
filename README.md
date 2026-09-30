On-Device AI Text-to-SQL Agent
An AI-powered, 100% local database intelligence agent running on Qualcomm Snapdragon hardware via Ollama. It enables users to query e-commerce databases using natural language without sending sensitive schema or enterprise data to cloud APIs.

Why This Project?
SQL is powerful, but querying enterprise databases usually requires deep knowledge of table schemas, relationships, joins, and SQL syntax. While Cloud LLMs can generate SQL, passing live database structures over the internet poses major privacy and data security risks. Furthermore, standard single-shot LLM queries often fail silently—producing syntactically valid but logically incorrect SQL.

This project addresses two core challenges:

Privacy & Offline Edge AI: Running small, quantized code models (SLMs) locally on Snapdragon hardware via Ollama so zero data leaves the local machine.

Reliability via Agentic Workflows: Moving from a single fragile LLM call to a controlled, self-correcting LangGraph pipeline that validates, heals, and approves queries before execution.

Architecture Comparison
1. Monolithic Baseline (Local Single-Shot)
A standard local baseline that passes the prompt directly to an edge SLM:

User Question ──► Ollama (Local SLM) ──► Generated SQL ──► Database ──► Result
Simple and low-latency, but lacks independent verification or recovery if the local model misinterprets a complex join.

2. Agentic Architecture (Self-Healing Edge Pipeline)
A multi-step LangGraph workflow optimized for running small, fast local models with strict validation guardrails:

User Question
      ↓
Database Connection
      ↓
Schema Loading & Filtering (Keeps context slim for edge SLMs)
      ↓
SQL Generator (Ollama / Local Qwen2.5-Coder or Llama-3.2)
      ↓
SQL Judge (Independent local validation step)
     ↙         ↘
Reject         Approve
  ↓               ↓
Regenerate     Human Approval (Pro Mode)
                   ↓
             ┌─────┴─────┐
           Reject     Approve
             ↓           ↓
         Regenerate   Execute (Read-Only Safety Guard)
                         ↓
                   Explain Result
Key Advantages for Snapdragon Edge AI
100% Privacy & Zero Cloud Dependency: Powered locally by Ollama, keeping database credentials, sensitive rows, and schema metadata entirely on-device.

Optimized for Snapdragon ARM64: Leverages lightweight, quantized Small Language Models (such as qwen2.5-coder:1.5b or llama3.2:3b) running natively on Snapdragon X Elite / Copilot+ PC architectures.

Context-Aware Schema Filtering: Prunes large database schemas dynamically so local SLMs process only relevant tables, maximizing token generation speed and reducing NPU/CPU memory consumption.

SQL Judge & Self-Healing: Smaller edge models occasionally make syntax errors. The SQL Judge catches failures locally and feeds error traces back to the model for automatic self-correction.

Human-in-the-Loop & Read-Only Safety: Pauses execution for user approval in Pro Mode while strictly enforcing read-only SQL statements to protect local storage from corruption.

Multi-Provider Fallback: Defaults to local Ollama execution while retaining optional fallback support for cloud providers (Gemini, Groq, Cohere) when internet connectivity is available.

Tech Stack
Local Inference Engine: Ollama (Qwen2.5-Coder 1.5B/7B, Llama 3.2 3B)

Target Hardware: Qualcomm Snapdragon X Elite / Copilot+ PC (ARM64 Native)

Agentic Framework: LangGraph, LangChain

Backend & API: Python 3.12, FastAPI, Server-Sent Events (SSE)

Databases: SQLite (Default Local) / PostgreSQL

Frontend: React + Tailwind UI / Streamlit

Observability & Safety: LangSmith Tracing, Read-Only SQL Interceptor

Run Locally
1. Start Local Ollama Model
Ensure Ollama is installed and run your preferred code model locally:

PowerShell
ollama run qwen2.5-coder:1.5b
2. Environment Setup
Create and activate an isolated Python 3.12 environment:

PowerShell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy .env.example to .env and configure your local Ollama endpoint and database URL:

Code snippet
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=qwen2.5-coder:1.5b
DATABASE_URL=sqlite:///./database/ecommerce.db
3. Launch Application
Start the API backend and React UI using the automated script:

PowerShell
.\start-app.ps1
Access the application at [http://127.0.0.1:5173](http://127.0.0.1:5173).

To stop all background services:

PowerShell
.\stop-app.ps1
Project Structure
text_to_sql/
├── database/         # Local SQLite sample datasets & migrations
├── skills/           # Schema extraction & pruning utilities
├── ui/               # React frontend with SSE streaming
├── api.py            # FastAPI streaming backend endpoints
├── llm.py            # Ollama & local provider abstraction
├── prompt.py         # System prompts optimized for edge SLMs
├── text_to_sql.py    # Main LangGraph agentic state machine
├── execute.py        # Safe read-only SQL execution engine
├── mon.py            # Monolithic baseline runner
└── start-app.ps1     # One-click launcher script
Developer: Swati Muttin

Built For: Snapdragon AI Hackathon (Edge AI & On-Device Innovation)
