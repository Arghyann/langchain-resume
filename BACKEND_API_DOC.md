# Langchain Resume Backend API Documentation

This backend provides a FastAPI-based API for interacting with a Supabase/PostgreSQL database using a Langchain agent. It is designed to support a frontend app for querying job applications and related data.

## How to Run the Backend

1. **Install dependencies** (in your virtual environment):

   ```sh
   pip install -r requirements.txt
   # or, if using pyproject.toml and uv:
   uv run main.py
   # or for FastAPI server:
   uvicorn api_backend:app --reload
   ```

2. **Set environment variables** (in a `.env` file or your environment):

   - `READ_ONLY_DB_URL` — PostgreSQL connection string
   - `GOOGLE_API_KEY` — Google Gemini API key

3. **Start the backend**
   - For CLI: `uv run main.py`
   - For API: `uvicorn api_backend:app --reload`

---

## API Endpoints (FastAPI)

### Health Check

- **GET /**
- Returns: `{ "status": "ok" }`

### Query Endpoint

- **POST /query**
- **Body:**
  ```json
  { "query": "your question here" }
  ```
- **Response:**
  ```json
  { "result": "agent's answer or SQL results" }
  ```

---

## Route Details

### 1. `GET /`

- **Purpose:** Health check. Use to verify the backend is running.
- **How to call:**
  - `fetch('http://localhost:8000/')` (JS)
  - `curl http://localhost:8000/`
- **Response:** `{ "status": "ok" }`

### 2. `POST /query`

- **Purpose:** Main endpoint for all natural language queries.
- **How to call:**
  - Send a POST request with JSON body: `{ "query": "your question here" }`
  - Example (JS):
    ```js
    fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: "Show all interns with salary expectations less than 10000",
      }),
    })
      .then((res) => res.json())
      .then((data) => console.log(data.result));
    ```
- **Response:**
  - If the agent can answer directly, returns a string.
  - If the agent generates and executes SQL, returns a list of rows (array of arrays or objects).
  - Example:
    ```json
    {
      "result": [
        ["Harsh Singh", "digital.harshsingh41507@gmail.com", "0"],
        ["Vaidehi Singh", "mahi.vaidehi9756@gmail.com", "1000"]
      ]
    }
    ```

---

## How the Backend Works

- The backend uses Langchain to interpret natural language queries and generate SQL.
- The backend executes the generated SQL and returns the results.
- Handles complex salary parsing and data cleaning for queries.
- All queries are read-only (SELECT only).
- The backend can also extract resume text if requested (see below).

---

## Special Features

- **Resume Text Extraction:**
  - If the query is about extracting text from a resume PDF, the backend will use the `GetResumeText` tool.
  - Example query: `Get the text from resume file resume.pdf`.
  - Response: The plain text content of the PDF.

---

## Example Usage

**Request:**

```json
POST /query
{
  "query": "Show all interns with salary expectations less than 10000"
}
```

**Response:**

```json
{
  "result": [
    ["Harsh Singh", "digital.harshsingh41507@gmail.com", "0"],
    ["Vaidehi Singh", "mahi.vaidehi9756@gmail.com", "1000"]
  ]
}
```

---

## Notes for Frontend Developers

- Always send queries as JSON to `/query`.
- The backend will return either the agent's answer or the actual SQL query results.
- If you need more fields or a different format, specify in your query or contact the backend dev.
- All endpoints are CORS-enabled for local development.

---

## Contact

For backend issues or feature requests, contact the backend developer.
