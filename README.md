# GitLab Chatbot

An interactive AI chatbot that provides intelligent answers about GitLab's Handbook and Direction pages using semantic search and optional LLM integration.

## Features

- **Semantic Search**: Intelligent retrieval of relevant information from knowledge base
- **Focused Responses**: Returns specific, relevant content instead of entire documents
- **LLM Integration**: Optional AI-generated responses with OpenAI/HuggingFace support
- **Docker Support**: Easy deployment with Docker Compose
- **Modern UI**: Clean, responsive React frontend

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd gitlab-chat
   ```

2. **Add your knowledge base**
   - Place your GitLab Handbook PDF or text files in the `data/` directory
   - Update `PDF_PATH` in `docker-compose.yml` if needed

3. **Start the application**
   ```bash
   docker compose up --build
   ```

4. **Access the chatbot**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## Configuration

### Knowledge Base
- **PDF Files**: Place in `data/` directory
- **Text Files**: Supported formats (.txt)
- **Update Path**: Modify `PDF_PATH` in `docker-compose.yml`

### LLM Integration (Optional)
Add your API keys to `docker-compose.yml`:
```yaml
environment:
  - OPENAI_API_KEY=sk-your-key-here
  - HF_TOKEN=your-hf-token-here
```

## Usage

### Basic Queries
- "What is GitLab?"
- "How do I set up CI/CD?"
- "What are the security features?"
- "How do I create merge requests?"

### LLM Mode
- Toggle "Use hosted LLM" checkbox
- Requires API keys in backend environment

## API Endpoints

- `POST /chat` - Send message to chatbot
- `GET /docs` - API documentation

## Project Structure

```
gitlab-chat/
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── data/            # Knowledge base files
└── docker-compose.yml
```

## Development

### Backend
- FastAPI with semantic search
- TF-IDF vectorization
- Cosine similarity matching

### Frontend
- React 18
- Axios for API calls
- Modern CSS styling

## Troubleshooting

- **No responses**: Check if knowledge base files are in `data/` directory
- **Docker issues**: Ensure Docker is running and ports 3000/8000 are available
- **LLM errors**: Verify API keys are correctly set in environment variables