# Async RAG API

An asynchronous Retrieval-Augmented Generation (RAG) API built with FastAPI, Redis Queue, and LangChain. This system processes PDF documents and answers questions based on their content using OpenAI's GPT models and vector similarity search.

## Features

- **Asynchronous Processing**: Jobs are queued and processed in the background, keeping the API responsive
- **PDF Document Processing**: Automatically chunks and indexes PDF documents
- **Vector Search**: Uses Qdrant for efficient similarity search
- **Job Tracking**: Monitor job status and retrieve results when ready
- **Scalable Architecture**: Separate API and worker processes for better resource management

## Architecture

![Architecture](./Async%20RAG%20API%20(Architecture).png)

## Tech Stack

- **FastAPI**: Web framework for the API
- **Redis Queue (RQ)**: Background job processing (using Valkey)
- **LangChain**: Document processing and RAG orchestration
- **Qdrant**: Vector database for similarity search
- **OpenAI**: Embeddings and chat completions
- **PyPDF**: PDF document loading

## Prerequisites

- Python 3.8+
- Redis/Valkey server
- Docker (for Qdrant)
- OpenAI API key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/10Vaibhav/Async-RAG-API.git
cd async-rag-api
```

2. Create a virtual environment:
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

5. Start Qdrant and Valkey using Docker:
```bash
docker-compose up -d
```

6. Verify Valkey is running:
```bash
python -c "from redis import Redis; r = Redis(host='localhost', port=6379); print(r.ping())"
```
Should return `True` if Valkey is running correctly.

## Usage

### 1. Verify Services are Running

Check that Valkey is accessible:
```bash
python -c "from redis import Redis; r = Redis(host='localhost', port=6379); print(r.ping())"
```

### 2. Index Your PDF Document

First, place your PDF file in the project directory and update the path in `index.py`:

```bash
python index.py
```

This will:
- Load the PDF
- Split it into chunks
- Create embeddings
- Store vectors in Qdrant

### 3. Start the Worker

The worker processes background jobs:

```bash
python run_worker.py
```

### 4. Start the API Server

In a separate terminal:

```bash
python main.py
```

The API will be available at `http://127.0.0.1:8000`

### 5. Make Requests

**Submit a query:**
```bash
POST http://127.0.0.1:8000/chat?query=What is Node.js?
```

Response:
```json
{
  "status": "queued",
  "job_id": "e3bc9337-5026-4e07-9ddf-cdf3ffa55d09"
}
```

**Check job status:**
```bash
GET http://127.0.0.1:8000/job-status?job_id=e3bc9337-5026-4e07-9ddf-cdf3ffa55d09
```

Response:
```json
{
  "result": "Node.js is a JavaScript runtime built on Chrome's V8 engine..."
}
```
## API Endpoints

### `GET /`
Health check endpoint.

**Response:**
```json
{
  "status": "Server is up and running!"
}
```

### `POST /chat`
Submit a query for processing.

**Parameters:**
- `query` (string): The question to ask about the PDF content

**Response:**
```json
{
  "status": "queued",
  "job_id": "string"
}
```

### `GET /job-status`
Retrieve the result of a processed job.

**Parameters:**
- `job_id` (string): The job ID returned from `/chat`

**Response:**
```json
{
  "result": "string or null"
}
```

## How It Works

1. **Document Indexing**: PDFs are loaded, split into chunks, converted to embeddings, and stored in Qdrant
2. **Query Submission**: User submits a question via `/chat` endpoint
3. **Job Queuing**: The query is added to Redis Queue and a job ID is returned immediately
4. **Background Processing**: Worker picks up the job and:
   - Searches for relevant chunks in Qdrant
   - Builds context from retrieved chunks
   - Sends context + query to OpenAI
   - Stores the result
5. **Result Retrieval**: User polls `/job-status` with the job ID to get the answer

## Configuration

### Qdrant
- URL: `http://localhost:6333`
- Collection: `pdf_rag`

### Valkey (Redis-compatible)
- Host: `localhost`
- Port: `6379`

### OpenAI
- Embedding Model: `text-embedding-3-large`
- Chat Model: `gpt-4`

## Windows Compatibility

This project uses `SimpleWorker` from RQ, which is compatible with Windows (standard RQ workers use `os.fork()` which doesn't exist on Windows).

## Troubleshooting

**Worker fails with "module 'os' has no attribute 'fork'":**
- Make sure you're using `run_worker.py` which uses `SimpleWorker`

**Qdrant connection errors:**
- Ensure Docker is running and Qdrant container is up: `docker-compose up -d`

**OpenAI API errors:**
- Verify your API key in `.env`
- Check your OpenAI account has credits

**Valkey/Redis connection errors:**
- Ensure Valkey server is running on `localhost:6379`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
