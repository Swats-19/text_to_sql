# On-Device AI Text-to-SQL Agent

An AI-powered, 100% local database intelligence agent running on Qualcomm Snapdragon hardware via Ollama. It enables users to query e-commerce databases using natural language without sending sensitive schema or enterprise data to cloud APIs.

## Why This Project?

SQL is powerful, but querying enterprise databases usually requires deep knowledge of table schemas, relationships, joins, and SQL syntax. While Cloud LLMs can generate SQL, passing live database structures over the internet poses major privacy and data security risks. Furthermore, standard single-shot LLM queries can fail silently — producing syntactically valid but logically incorrect SQL.

This project addresses two core challenges:

**Privacy & Offline Edge AI:** Running small, quantized code models (SLMs) locally on Snapdragon hardware via Ollama so database credentials, schema metadata, queries, and sensitive data remain on-device.

**Reliability via Agentic Workflows:** Moving from a single fragile LLM call to a controlled, self-correcting LangGraph pipeline that validates, heals, and optionally approves queries before execution.

## Architecture Comparison

### 1. Monolithic Baseline (Local Single-Shot)

A standard local baseline that passes the prompt directly to an edge SLM:

```text
User Question
      ↓
Ollama (Local SLM)
      ↓
Generated SQL
      ↓
Database
      ↓
Result
```

Simple and low-latency, but lacks independent verification or recovery if the local model misinterprets a complex join or database relationship.

### 2. Agentic Architecture (Self-Healing Edge Pipeline)

A multi-step LangGraph workflow optimized for running small, fast local models with strict validation guardrails:

```text
User Question
      ↓
Database Connection
      ↓
Schema Loading & Filtering
      ↓
SQL Generator
(Ollama / Local SLM)
      ↓
SQL Judge
   ↙       ↘
Reject    Approve
  ↓          ↓
Regenerate  Human Approval
               ↓
         ┌─────┴─────┐
       Reject      Approve
         ↓             ↓
     Regenerate     Execute
                   (Read-Only)
                       ↓
                 Explain Result
```

## Key Advantages for Snapdragon Edge AI

**100% Privacy & Zero Cloud Dependency:** Powered locally by Ollama, keeping database credentials, sensitive data, and schema metadata entirely on-device.

**Optimized for Snapdragon ARM64:** Leverages lightweight, quantized Small Language Models such as `qwen2.5-coder:1.5b` and `llama3.2:3b`, designed for local inference on Snapdragon X Elite / Copilot+ PC architectures.

**Context-Aware Schema Filtering:** Dynamically filters large database schemas so local SLMs process only relevant tables, reducing context size and memory usage while improving generation efficiency.

**SQL Judge & Self-Healing:** The local SQL Judge validates generated queries and provides feedback when a query is rejected, allowing the generator to automatically regenerate and correct the SQL.

**Human-in-the-Loop & Read-Only Safety:** Pro Mode pauses execution for user approval while the execution layer enforces read-only SQL operations to protect the local database from modification.

**Multi-Provider Fallback:** Defaults to local Ollama execution while retaining optional support for cloud providers such as Gemini, Groq, and Cohere when internet connectivity is available.

## Why AI?

Natural language provides a more accessible interface to databases than requiring every user to understand SQL, schemas, joins, and database relationships.

For example, a user can ask:

```text
Show me the top 5 customers by total spending.
```

The agent translates the question into SQL using the available database schema, validates the generated query, and executes it only after the required safety checks.

The challenge is not simply generating SQL — it is making the translation reliable, controllable, and observable.

## Tech Stack

**Local Inference Engine:** Ollama — Qwen2.5-Coder 1.5B/7B, Llama 3.2 3B

**Target Hardware:** Qualcomm Snapdragon X Elite / Copilot+ PC (ARM64)

**Agentic Framework:** LangGraph, LangChain

**Backend & API:** Python 3.12, FastAPI, Server-Sent Events (SSE)

**Databases:** SQLite / PostgreSQL

**Frontend:** React + Tailwind CSS

**Alternative UI:** Streamlit

**Observability:** LangSmith

**Safety:** Read-Only SQL Interceptor

## Run Locally

### Step 1: Start Local Ollama Model

Ensure Ollama is installed and run your preferred code model locally:

```bash
ollama run qwen2.5-coder:1.5b
```

### Step 2: Environment Setup

Create and activate an isolated Python 3.12 environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Copy `.env.example` to `.env` and configure your local Ollama endpoint and database URL:

```env
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=qwen2.5-coder:1.5b
DATABASE_URL=sqlite:///./database/ecommerce.db
```

### Step 3: Install Frontend Dependencies

```powershell
Set-Location ui
npm install
```

### Step 4: Launch Application

Start the API backend and React UI using the automated script:

```powershell
.\start-app.ps1
```

Access the application at:

```text
http://127.0.0.1:5173
```

To stop all background services:

```powershell
.\stop-app.ps1
```

The React interface communicates with the LangGraph workflow through Server-Sent Events (SSE). Pro Mode pauses for human approval, while Non-Pro Mode automatically approves the generated query. Both modes enforce read-only SQL execution.

## Project Structure

```text
text_to_sql/
├── database/         # Local SQLite datasets & migrations
├── skills/           # Schema extraction & filtering utilities
├── ui/               # React frontend with SSE streaming
├── api.py             # FastAPI streaming backend endpoints
├── llm.py             # Ollama & local provider abstraction
├── prompt.py          # Prompts optimized for edge SLMs
├── text_to_sql.py     # Main LangGraph agentic state machine
├── execute.py         # Safe read-only SQL execution engine
├── mon.py             # Monolithic baseline runner
├── skills.py          # Schema discovery & filtering utilities
├── start-app.ps1      # One-click application launcher
└── stop-app.ps1       # Stops backend and frontend services
```

## Privacy & Safety

The local inference architecture is designed to keep sensitive database information on-device.

The local workflow can keep the following entirely within the machine:

* Database credentials
* Database schema
* Table metadata
* User questions
* Generated SQL
* Query results
* Local database contents

The execution layer also applies a read-only SQL policy before allowing queries to reach the database.

Optional cloud-provider support can be enabled when required. When using cloud providers, the relevant data sent to those providers is subject to their respective services and privacy policies.

## Developer

**Swati Muttin**

## Built For

**Snapdragon AI Hackathon — Edge AI & On-Device Innovation**
