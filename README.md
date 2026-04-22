# 🔍 Browser API — AI-Powered Search Service

A FastAPI backend that combines **DuckDuckGo web search** with **OpenRouter AI** to answer questions using live web data. Includes a beautiful Streamlit frontend with glassmorphism design.

---

## 🏗️ Project Structure

```
Browser-API/
├── main.py                  → FastAPI server + AI logic + memory
├── searchtool.py            → DuckDuckGo web search utility
├── frontend/
│   ├── app.py               → Streamlit UI entry point
│   ├── api_client.py        → API calls to FastAPI backend
│   ├── ui_components.py     → UI rendering + custom CSS
│   └── config.py            → Settings & constants
├── .env                     → API keys (never commit)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/Browser-API.git
cd Browser-API
```

### 2. Create virtual environment
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```
Get your free API key at: https://openrouter.ai

---

## 🚀 Running the Project

### Backend only
```bash
uvicorn main:app --reload
```
API will be live at: http://127.0.0.1:8000

Interactive docs at: http://127.0.0.1:8000/docs

### Backend + Frontend together

**Terminal 1 — Start backend:**
```bash
uvicorn main:app --reload
```

**Terminal 2 — Start frontend:**
```bash
cd frontend
streamlit run app.py
```
Frontend will be live at: http://localhost:8501

---

## 📡 API Endpoints

| Method | Endpoint  | Description               |
|--------|-----------|---------------------------|
| GET    | `/`       | Check API status          |
| GET    | `/health` | Health check + timestamp  |
| POST   | `/ask`    | Ask a question            |

### Example request
```bash
curl -X POST http://127.0.0.1:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Bitcoin price today"}'
```

### Example response
```json
{
  "answer": "Bitcoin is currently trading at $85,000...",
  "sources": [
    "https://coinmarketcap.com/...",
    "https://coindesk.com/..."
  ],
  "latency": "2.34s"
}
```

---

## 🔄 How It Works

```
User Question
     ↓
FastAPI /ask endpoint
     ↓
DuckDuckGo Search (3 results)
     ↓
Build prompt with search context + chat memory
     ↓
OpenRouter AI (openrouter/free)
     ↓
Return answer + sources + latency
```

---

## 🧠 Features

- **Live web search** — fetches real-time results via DuckDuckGo
- **AI synthesis** — OpenRouter free models generate accurate answers
- **Chat memory** — remembers last 5 queries for context-aware answers
- **CORS enabled** — frontend can call backend without issues
- **Beautiful UI** — dark gradient theme with Poppins font, glassmorphism cards
- **Clickable sources** — domain names shown as hoverable links
- **Latency tracking** — shows response time per query
- **Retry logic** — handles rate limiting gracefully
- **Structured logging** — logs to both console and `prod.log`

---

## 🛠️ Tech Stack

| Technology      | Purpose                          |
|-----------------|----------------------------------|
| FastAPI         | Backend API framework            |
| DuckDuckGo      | Live web search (ddgs)           |
| OpenRouter      | Free AI model access             |
| Pydantic        | Data validation & schemas        |
| Uvicorn         | ASGI server                      |
| Streamlit       | Frontend UI                      |
| Python-dotenv   | Environment variable management  |
| Certifi         | SSL certificate handling         |
| CORS Middleware | Cross-origin request support     |

---

## ❗ Common Issues & Fixes

| Error | Fix |
|-------|-----|
| `429 RESOURCE_EXHAUSTED` | Gemini quota exhausted — switched to OpenRouter |
| `No endpoints found` | Model removed — use `openrouter/free` |
| `ConnectionError` | Make sure backend is running on port 8000 |
| `ddgs` import error | Run `pip install ddgs` |
| `SSL Error` | Already handled via `certifi` |
| `NoneType has no attribute strip` | API returned empty response — retry |

---

## 📦 Requirements

```
fastapi
uvicorn[standard]
ddgs
google-genai
openai
pydantic
certifi
python-dotenv
streamlit
requests
```

---

## 🔐 Security Notes

- Never commit your `.env` file
- Never hardcode API keys in source code
- `.gitignore` already excludes `.env` and logs
- API keys loaded via `python-dotenv`

---

## 📈 Problems Solved During Development

| # | Problem | Solution |
|---|---------|----------|
| 1 | Wrong `google.generativeai` import | Switched to `from google import genai` |
| 2 | `duckduckgo_search` package renamed | Reinstalled as `ddgs` |
| 3 | Gemini model 404 not found | Updated to correct model name |
| 4 | Gemini 429 quota exhausted | Switched to OpenRouter free |
| 5 | OpenRouter model endpoint not found | Used `openrouter/free` auto-router |
| 6 | API key hardcoded in source | Moved to `.env` with python-dotenv |
| 7 | No chat context between queries | Added `chat_memory` with max history |
| 8 | Frontend-backend CORS issues | Added `CORSMiddleware` to FastAPI |

---

## 🔜 Future Improvements

- [ ] Deploy backend on Railway or Render
- [ ] Add user authentication
- [ ] Persist chat history to database
- [ ] Add more search engines as fallback
- [ ] Stream AI responses in real-time

---

## 📄 License

MIT License — free to use and modify.

---

## 👨‍💻 Author

Built with FastAPI + OpenRouter + DuckDuckGo + Streamlit
