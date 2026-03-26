"""Legal Researcher — Search Indian Kanoon, analyze statutes, find case law."""

import re
from typing import Optional
import requests
from bs4 import BeautifulSoup


INDIAN_KANOON_SEARCH = "https://indiankanoon.org/search/?formInput={query}"
INDIAN_KANOON_DOC = "https://indiankanoon.org/doc/{doc_id}/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml",
}


def search_indian_kanoon(query: str, max_results: int = 10) -> list:
    """Search Indian Kanoon for case law."""
    try:
        url = INDIAN_KANOON_SEARCH.format(query=requests.utils.quote(query))
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return [{"error": f"HTTP {resp.status_code}", "suggestion": "Try searching directly on indiankanoon.org"}]

        soup = BeautifulSoup(resp.text, "html.parser")
        results = []

        for item in soup.select(".result")[:max_results]:
            title_el = item.select_one(".result_title a")
            if not title_el:
                continue

            title = title_el.get_text(strip=True)
            href = title_el.get("href", "")
            doc_id = href.split("/doc/")[-1].rstrip("/") if "/doc/" in href else ""

            snippet_el = item.select_one(".result_text")
            snippet = snippet_el.get_text(strip=True)[:300] if snippet_el else ""

            court_el = item.select_one(".docsource")
            court = court_el.get_text(strip=True) if court_el else ""

            results.append({
                "title": title,
                "doc_id": doc_id,
                "url": f"https://indiankanoon.org{href}" if href.startswith("/") else href,
                "court": court,
                "snippet": snippet,
            })

        if not results:
            return [{"info": "No results found", "suggestion": f"Try different keywords or search directly: {url}"}]

        return results

    except requests.RequestException as e:
        return [{"error": str(e), "suggestion": "Check internet connection or try indiankanoon.org directly"}]


def search_statutes(query: str) -> list:
    """Search for statute references in Indian Kanoon."""
    return search_indian_kanoon(f"{query} statute act section", max_results=5)


def format_research_results(results: list) -> str:
    """Format search results as a readable text block."""
    if not results:
        return "No results found."

    lines = []
    for i, r in enumerate(results, 1):
        if "error" in r:
            lines.append(f"Error: {r['error']}")
            if "suggestion" in r:
                lines.append(f"  Suggestion: {r['suggestion']}")
            continue

        if "info" in r:
            lines.append(r["info"])
            continue

        lines.append(f"\n{i}. {r.get('title', 'Untitled')}")
        if r.get("court"):
            lines.append(f"   Court: {r['court']}")
        if r.get("url"):
            lines.append(f"   Link: {r['url']}")
        if r.get("snippet"):
            lines.append(f"   Summary: {r['snippet'][:200]}...")

    return "\n".join(lines)
