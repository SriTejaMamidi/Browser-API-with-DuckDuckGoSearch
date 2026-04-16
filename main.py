import logging
import time
import certifi
import os
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from openai import OpenAI
from searchtool import get_results
from dotenv  import load_dotenv

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()

#Step 1: Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("prod.log")
    ]
)
logger = logging.getLogger("API_GATEWAY")

#Step 2: App + OpenRouter client
app = FastAPI(title="Professional AI Search Service")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

#Free models on OpenRouter
MODEL = "openrouter/free"

#Step 3: Schemas
class SearchRequest(BaseModel):
    question: str

class SearchResponse(BaseModel):
    answer:  str
    sources: list[str]
    latency: str

#Step 4: Routes
@app.get("/")
async def root():
    return {"status": "online", "message": "Welcome to the AI Search API"}

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/ask", response_model=SearchResponse)
async def ask_ai(request: SearchRequest, raw_request: Request):
    start_time = time.time()
    logger.info(f"Request from {raw_request.client.host} → query: '{request.question}'")

    # Step A: Fetch web context
    web_data = get_results(query=request.question, max_results=3)
    if not web_data:
        logger.warning(f"No results for: {request.question}")
        raise HTTPException(status_code=404, detail="No results found for query")

    # Step B: Build prompt
    context_text = "\n\n".join([
        f"Source: {r['title']}\nSnippet: {r['body']}"
        for r in web_data
    ])

    prompt = (
        f"Using the following search results, answer the user's question accurately.\n\n"
        f"Results:\n{context_text}\n\n"
        f"Question: {request.question}"
    )

    # Step C: Call OpenRouter (free, no quota issues)
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI assistant that answers questions based on web search results."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        answer   = response.choices[0].message.content
        duration = f"{time.time() - start_time:.2f}s"
        logger.info(f"Query processed in {duration}")

        return SearchResponse(
            answer  = answer,
            sources = [r["link"] for r in web_data],
            latency = duration
        )

    except Exception as e:
        logger.critical(f"OpenRouter failure: {e}")
        raise HTTPException(status_code=500, detail=f"AI engine error: {str(e)}")
