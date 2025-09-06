# Langchain Resume Backend

This project is a FastAPI backend powered by Langchain and Gemini LLM, designed to interact with a Supabase/PostgreSQL database of job applications and resumes. It supports natural language queries, resume text extraction, and can be extended for advanced LLM-based analysis.

## Features
- Query job applications and jobs using natural language
- Extract and return resume text from PDF files stored in Supabase
- Handles complex salary parsing and data cleaning for queries
- Easily extensible for LLM-based resume comparison or advanced analytics

## How to Run the Project

### 1. Install dependencies
- If using `requirements.txt`:
  ```sh
  pip install -r requirements.txt
  ```
- If using `pyproject.toml` and uv:
  ```sh
  uv run main.py
  ```

### 2. Set environment variables
Create a `.env` file in the project root with:
```
READ_ONLY_DB_URL=your_postgres_connection_string
GOOGLE_API_KEY=your_gemini_api_key
```

### 3. Start the backend
- For CLI (interactive):
  ```sh
  uv run main.py
  ```
- For API (to connect with frontend):
  ```sh
  uvicorn api_backend:app --reload
  ```

The API will be available at `http://localhost:8000`.

## API Endpoints
- `GET /` — Health check
- `POST /query` — Main endpoint for natural language queries. Send `{ "query": "your question" }` as JSON.

## Example Query
```json
POST /query
{
  "query": "Show all interns with salary expectations less than 10000"
}
```

## Project Structure
- `main.py` — CLI and backend logic
- `api_backend.py` — FastAPI app for frontend integration
- `resumeParser.py` — Resume text extraction tool
- `BACKEND_API_DOC.md` — Full backend API documentation

## Notes
- All queries are read-only (SELECT only)
- CORS is enabled for local development
- For advanced features (like resume comparison), see the backend API doc or contact the backend developer

## Contact
For issues or feature requests, contact the backend developer.
