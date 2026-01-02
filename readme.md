
# RAG Application

A Retrieval-Augmented Generation (RAG) application built with FastAPI, LangGraph, and Qdrant vector database.

## Prerequisites

- Python 3.8+
- pip

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd RAG-Application
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install uvicorn fastapi pydantic langgraph qdrant-client
```

## Running the Application

### Option 1: Direct Python Execution
```bash
python main.py
```

### Option 2: Using Uvicorn
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Usage

Access the interactive API documentation at `http://localhost:8000/docs`

## Project Structure

- **FastAPI**: REST API framework
- **Pydantic**: Data validation
- **LangGraph**: RAG workflow orchestration
- **Qdrant**: Vector database for semantic search
