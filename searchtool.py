# Importing the required modules
from ddgs import DDGS
import logging

logger = logging.getLogger(__name__)

def get_results(query: str, max_results: int = 5):
    """
    Core utility to fetch snippets from the live web.
    Separating this allows for easier unit testing.
    """
    results = []
    try:
        with DDGS() as ddgs:
            search_gen = ddgs.text(query, max_results=max_results)
            for r in search_gen:
                results.append({
                    "title": r.get("title"),
                    "body": r.get("body"),
                    "link": r.get("href")
                })

        if not results:
            logger.warning(f"DDGS returned 0 results for the query: {query}")

        return results

    except Exception as e:
        logger.error(f"Search utility failure: {e}")
        return []
