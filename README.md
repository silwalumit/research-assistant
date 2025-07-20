# Research Assistant Agent

This project implements a mini Agentic RAG. The agent is designed to answer natural-language questions about a local folder of documents using Retrieval-Augmented Generation (RAG) with short-term session memory.

## Problem Statement
Build a mini “Research Assistant” agent that answers natural-language questions about a local folder of documents.

## Functional Requirements
- **Data Ingestion**: CLI/endpoint to load .txt/.md files, embed with sentence-transformers.
- **Vector Store**: Chroma (open-source, in-process), persisted to local disk.
- **LLM Layer**: Local model via Ollama 
- **Agent Orchestration**: 
- **API**: FastAPI`/ask` returns `{answer}`.
- **Observability**: Pretty + JSON logs to stdout.
- **Local Run**: `rye run dev` boots everything offline.


## Deliverables
- `README.md`
- `/src`
- `docker-compose.yaml` + `Dockerfile`
- `docs/`

### Key Components

1. **API Layer**: FastAPI web server with middleware for request processing and monitoring
2. **Agent Orchestration**: LangGraph-based workflow management with session memory
3. **Core Components**: Document processing, vector storage, and LLM integration
4. **Data Layer**: Local file system, persistent vector database, and session storage

## Quick Start

### Prerequisites

- Python 3.11+
- 8GB+ RAM
- Ollama (for local LLM serving)


### Local Development

1. **Install dependencies**:
   ```bash
   rye sync
   ```

2. **Start Ollama server**:
   ```bash
   docker run -d --name ollama_llm -p 11434:11434 -v ollama:/root/.ollama ollama/ollama
   ```
3. **Pull mistral and server mistral model**:
    ```
    docker exec -it ollama_llm ollama pull mistral:7b &&
    docker exec -it ollama_llm ollama server mistral
    ```

3. **Start the API server**:
   ```bash
   rye run dev
   ```

4. **In another terminal, ingest documents**:
   ```bash
   rye run cli ingest docs -r
   ```

## API Endpoints

### Core Endpoints

- `POST /ask` - Ask questions about ingested documents

## CLI Usage

The CLI tool provides convenient access to core functionality:

### Ingest Documents
```bash
# Ingest specific files
rye run cli ingest file1.txt file2.md

# Ingest all files in a directory
rye run cli ingest documents --recursive
```

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# config for vector store
STORE__KIND='Chroma' # Options: Chroma, Faiss
STORE__LOCATION='./data/chroma/'
STORE__COLLECTION_NAME='research_docs'

# config for LLM layer
LLM__OLLAMA__MODEL_NAME='mistral:7b'
LLM__OLLAMA__BASE_URI='http://localhost:11434/'

# LLM__OPENAPI__MODEL__NAME='gpt-3.5-turbo-instruct'
# LLM__OPENAPI__API_KEY=''

# LLM__BEDROCK__MODEL_ARN='amazon.titan-text-express-v1'
# LLM__BEDROCK__CREDENTIAL_PROFILE_NAME='bedrock_admin'


# logging config
LOG__LEVEL='Info'
LOG__FORMAT='Pretty' # Options: Pretty, Json

# text processing config
LOADER__CHUNK_SIZE=500
LOADER__CHUNK_OVERLAP=100
```

## Troubleshooting

### Common Issues

**Ollama Connection Error**:
```bash
# Make sure Ollama is running
ollama serve

# Pull the required model
ollama pull llama3.2:3b

# Check if model is available
ollama list
```

**Memory Issues**:
- Reduce chunk size in configuration
- Use smaller embedding model
- Limit max retrieved documents


## Acknowledgments

- Built with LangChain and LangGraph
- Uses Ollama for local LLM serving
- ChromaDB for vector storage
- FastAPI for web framework
- Sentence Transformers for embeddings

