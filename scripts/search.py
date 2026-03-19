#!/usr/bin/env python3
"""
Parallel.ai / Tavily Search API
Usage: python3 search.py <query> [--max-results N] [--mode one-shot|agentic] [--provider parallel|tavily]
"""

import os
import sys
import json
import argparse

from parallel import Parallel

API_KEY = os.environ.get("PARALLEL_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")

def search(objective: str, max_results: int = 10, mode: str = "one-shot"):
    """Search using Parallel SDK."""
    client = Parallel(api_key=API_KEY)
    return client.beta.search(
        mode=mode,
        max_results=max_results,
        objective=objective
    )

def tavily_search(query: str, max_results: int = 10):
    """Search using Tavily API."""
    from tavily import TavilyClient
    client = TavilyClient(api_key=TAVILY_API_KEY)
    return client.search(
        query=query,
        max_results=max_results,
        search_depth="advanced",
    )

def format_tavily_results(response: dict) -> str:
    """Format Tavily search results for display."""
    output = []
    output.append(f"🔍 Tavily Search\n")

    for i, result in enumerate(response.get("results", []), 1):
        title = result.get("title") or "No title"
        url = result.get("url", "")
        content = result.get("content", "")
        score = result.get("score")

        score_str = f" (score: {score:.2f})" if score is not None else ""
        output.append(f"**{i}. [{title}]({url})**{score_str}")

        if content:
            excerpt = content.replace("\n", " ").strip()[:400]
            output.append(f"   {excerpt}...")
        output.append("")

    return "\n".join(output)

def format_results(response) -> str:
    """Format search results for display."""
    output = []
    output.append(f"🔍 Search ID: {response.search_id}\n")
    
    for i, result in enumerate(response.results, 1):
        title = result.title or "No title"
        url = result.url
        excerpts = result.excerpts or []
        date = f" ({result.publish_date})" if result.publish_date else ""
        
        output.append(f"**{i}. [{title}]({url})**{date}")
        
        if excerpts:
            # Clean and truncate excerpt
            excerpt = excerpts[0].replace("\n", " ").strip()[:400]
            output.append(f"   {excerpt}...")
        output.append("")
    
    if response.usage:
        usage = ", ".join(f"{u.name}: {u.count}" for u in response.usage)
        output.append(f"📊 Usage: {usage}")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Parallel.ai / Tavily Search")
    parser.add_argument("query", nargs="*", help="Search query")
    parser.add_argument("--max-results", "-n", type=int, default=10)
    parser.add_argument("--mode", "-m", default="one-shot", choices=["one-shot", "agentic", "fast"])
    parser.add_argument("--provider", "-p", default="parallel", choices=["parallel", "tavily"])
    parser.add_argument("--json", "-j", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        sys.exit(1)

    query = " ".join(args.query)

    if args.provider == "tavily":
        if not TAVILY_API_KEY:
            print("Error: TAVILY_API_KEY environment variable is required when --provider=tavily", file=sys.stderr)
            sys.exit(1)
        response = tavily_search(query, max_results=args.max_results)
        if args.json:
            print(json.dumps({
                "results": [
                    {
                        "url": r.get("url"),
                        "title": r.get("title"),
                        "content": r.get("content"),
                        "score": r.get("score"),
                    }
                    for r in response.get("results", [])
                ]
            }, indent=2))
        else:
            print(format_tavily_results(response))
    else:
        if not API_KEY:
            print("Error: PARALLEL_API_KEY environment variable is required", file=sys.stderr)
            sys.exit(1)
        response = search(query, max_results=args.max_results, mode=args.mode)
        if args.json:
            print(json.dumps({
                "search_id": response.search_id,
                "results": [
                    {
                        "url": r.url,
                        "title": r.title,
                        "publish_date": r.publish_date,
                        "excerpts": r.excerpts
                    }
                    for r in response.results
                ]
            }, indent=2))
        else:
            print(format_results(response))

if __name__ == "__main__":
    main()
