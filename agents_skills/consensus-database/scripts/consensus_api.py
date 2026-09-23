#!/usr/bin/env python3
import os
import sys
import json
import argparse
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any

DEFAULT_API_KEY = os.environ.get("CONSENSUS_API_KEY", "ak_5JBYVR8YMEN55A9HQE41J1NGDQQ120XW")
BASE_URL = "https://api.consensus.app/v1/search"

def search_consensus(
    query: str,
    page: Optional[int] = None,
    page_size: Optional[int] = None,
    api_key: Optional[str] = None
) -> Dict[str, Any]:
    key = api_key or DEFAULT_API_KEY
    if not key:
        raise ValueError("Consensus API Key missing")

    params = {"query": query}
    if page is not None and page > 1:
        params["page"] = page
    if page_size is not None:
        params["page_size"] = page_size

    encoded_url = f"{BASE_URL}?{urllib.parse.urlencode(params)}"
    headers = {"x-api-key": key, "User-Agent": "Antigravity-Consensus/1.0"}

    req = urllib.request.Request(encoded_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "details": e.read().decode("utf-8", errors="ignore")}
    except Exception as e:
        return {"error": str(e)}

def format_results_markdown(data: Dict[str, Any], query: str, limit: int = 5) -> str:
    if "error" in data:
        err = data.get("error", "")
        details = data.get("details", "")
        return f"### Error: {err}\n{details}"

    results = data.get("results", [])
    if not results:
        return f"No results found for query: *{query}*"

    displayed = results[:limit]
    lines = [
        f"## Consensus.app Scientific Evidence: *{query}*",
        f"**Total Retrieved:** {len(results)} papers | **Showing Top:** {len(displayed)}\n"
    ]

    for i, p in enumerate(displayed, 1):
        title = p.get("title", "Untitled")
        authors = ", ".join(p.get("authors", []))
        year = p.get("publish_year", "")
        journal = p.get("journal_name", "")
        doi = p.get("doi", "")
        url = p.get("url", "")
        takeaway = p.get("takeaway", "")
        citations = p.get("citation_count", 0)
        sjr = p.get("sjr_best_quartile", None)
        sjr_badge = f"Q{sjr}" if sjr else "N/A"
        is_preprint = "Preprint" if p.get("is_preprint") else "Peer-Reviewed"

        link = url if url else (f"https://doi.org/{doi}" if doi else "#")
        lines.append(f"### {i}. [{title}]({link})")
        lines.append(f"- **Authors:** {authors} ({year})")
        lines.append(f"- **Journal:** {journal} | **Impact:** SJR {sjr_badge} | **Type:** {is_preprint}")
        lines.append(f"- **Citations:** {citations} | **DOI:** {doi}")
        if takeaway:
            lines.append(f"- **Consensus Key Takeaway:**\n  > {takeaway}")
        lines.append("")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Query Consensus.app API")
    parser.add_argument("query", help="Scientific search query")
    parser.add_argument("--limit", type=int, default=5, help="Number of papers to display (default: 5)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    parser.add_argument("--api-key", default=None)

    args = parser.parse_args()
    data = search_consensus(args.query, api_key=args.api_key)

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(format_results_markdown(data, args.query, limit=args.limit))

if __name__ == "__main__":
    main()
