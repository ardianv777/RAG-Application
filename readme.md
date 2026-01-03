# RAG Demo Application

A simple Retrieval-Augmented Generation (RAG) system built with FastAPI, LangGraph, and Qdrant. This application allows you to store documents and ask questions, with the system retrieving relevant information to generate answers.

## Features

- 📄 Add documents to the system
- 🔍 Ask questions and get relevant answers
- 💾 Dual storage mode: Qdrant vector database or in-memory fallback
- ⚡ Fast response with workflow orchestration using LangGraph
- 🎯 Clean architecture with separation of concerns

## Project Structure

```
rag-demo/
├── app/
│   ├── api/
│   │   └── endpoints.py          # API route handlers
│   ├── services/
│   │   ├── embedding_service.py  # Text embedding generation
│   │   └── rag_workflow.py       # RAG workflow logic
│   ├── storage/
│   │   └── document_store.py     # Document storage management
│   ├── main.py                   # Application entry point
│   └── models.py                 # Pydantic models
├── notes.md                      # Refactoring explanation
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pydantic
- LangGraph
- Qdrant Client

## Installation

### 1. Install Dependencies

```bash
pip install fastapi uvicorn pydantic langgraph qdrant-client
```

Or install from requirements.txt:

```bash
pip install -r requirements.txt
```

### 2. (Optional) Run Qdrant

If you want to use Qdrant vector database instead of in-memory storage:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

**Note:** If Qdrant is not available, the application will automatically fall back to in-memory storage.

## How to Run

Start the application with Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at: `http://localhost:8000`

**API Documentation:**
- Swagger UI: `http://localhost:8000/docs` - Interactive interface to test API endpoints directly
- ReDoc: `http://localhost:8000/redoc` - Clean documentation interface

**Note:** You can use either `/docs` or `/redoc` to interact with the API without using curl commands. Simply open the URL in your browser, and you can test all endpoints interactively.

## API Endpoints

### 1. Check System Status

**GET** `/status`

Check if the system is ready and which storage mode is active.

```bash
curl http://localhost:8000/status
```

**Response:**
```json
{
  "qdrant_ready": true,
  "in_memory_docs_count": 0,
  "graph_ready": true
}
```

### 2. Add Document

**POST** `/add`

Add a new document to the system.

```bash
curl -X POST http://localhost:8000/add \
  -H "Content-Type: application/json" \
  -d '{"text": "Python is a high-level programming language known for its simplicity and readability."}'
```

**Response:**
```json
{
  "id": 0,
  "status": "added"
}
```

### 3. Ask Question

**POST** `/ask`

Ask a question and get an answer based on stored documents.

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Python?"}'
```

**Response:**
```json
{
  "question": "What is Python?",
  "answer": "I found this: 'Python is a high-level programming language known for its simplicity and readability....'",
  "context_used": [
    "Python is a high-level programming language known for its simplicity and readability."
  ],
  "latency_sec": 0.045
}
```

## Usage Example

### Method 1: Using Interactive Documentation (Recommended for Beginners)

1. **Start the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Open Swagger UI in your browser:**
   ```
   http://localhost:8000/docs
   ```

3. **Test the endpoints interactively:**
   - Click on any endpoint (e.g., `/add`)
   - Click "Try it out"
   - Fill in the request body
   - Click "Execute"
   - See the response immediately

**Or use ReDoc for a cleaner view:**
   ```
   http://localhost:8000/redoc
   ```

### Method 2: Using cURL Commands

If you prefer command line:

1. **Start the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

2. **Add some documents:**
   ```bash
   # Add document about Python
   curl -X POST http://localhost:8000/add \
     -H "Content-Type: application/json" \
     -d '{"text": "Python is a programming language created by Guido van Rossum in 1991."}'
   
   # Add document about FastAPI
   curl -X POST http://localhost:8000/add \
     -H "Content-Type: application/json" \
     -d '{"text": "FastAPI is a modern web framework for building APIs with Python."}'
   ```

3. **Ask questions:**
   ```bash
   # Ask about Python
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "Who created Python?"}'
   
   # Ask about FastAPI
   curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"question": "What is FastAPI?"}'
   ```

4. **Check the status:**
   ```bash
   curl http://localhost:8000/status
   ```

## Architecture

The application follows a clean architecture pattern with clear separation of concerns:

- **API Layer** (`app/api/`): Handles HTTP requests and responses
- **Services Layer** (`app/services/`): Contains business logic (embeddings, RAG workflow)
- **Storage Layer** (`app/storage/`): Manages data persistence
- **Models** (`app/models.py`): Defines data structures and validation

## How It Works

1. **Document Storage:** When you add a document, it's converted into a numerical vector (embedding) and stored in either Qdrant or in-memory storage.

2. **Question Processing:** When you ask a question:
   - The question is converted into a vector
   - The system searches for similar documents
   - Relevant documents are retrieved as context
   - An answer is generated based on the retrieved context

3. **Workflow:** LangGraph orchestrates the retrieve → answer workflow to ensure consistent processing.

## Development

### Running Tests

Currently, there are no automated tests. The structure is designed to be easily testable, each component can be tested independently.

### Adding New Features

- **New endpoints:** Add to `app/api/endpoints.py`
- **New services:** Create in `app/services/`
- **New storage backends:** Extend `app/storage/document_store.py`

## Notes

- This is a demo application using a fake embedding function for simplicity
- For production use, replace `fake_embed()` with a real embedding model (e.g., Sentence Transformers, OpenAI embeddings)
- The application uses a simple answer generation - in production, integrate with an LLM for better responses

## Troubleshooting

**Problem:** Qdrant connection error

**Solution:** Make sure Qdrant is running on port 6333, or let the application use in-memory fallback.

**Problem:** Module not found errors

**Solution:** Make sure all dependencies are installed: `pip install -r requirements.txt`

**Problem:** Port 8000 already in use

**Solution:** Use a different port: `uvicorn app.main:app --port 8001`