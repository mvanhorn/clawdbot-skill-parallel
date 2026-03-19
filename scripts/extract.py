#!/usr/bin/env python3
"""
URL content extraction via Parallel.ai or Tavily.

Usage:
  python3 extract.py https://stripe.com/docs/api  # Extract with excerpts
  python3 extract.py https://example.com/paper.pdf --full  # Full content
  python3 extract.py https://sec.gov/10-K.htm --objective "Extract risk factors"
  python3 extract.py https://example.com --provider tavily  # Use Tavily extract
"""

import os
import sys
import json
import argparse

from parallel import Parallel

API_KEY = os.environ.get("PARALLEL_API_KEY")


def extract(
    client: Parallel,
    urls: list,
    objective: str = None,
    full_content: bool = False,
) -> dict:
    """Extract content from URLs."""
    params = {
        "urls": urls,
    }
    
    if objective:
        params["objective"] = objective
    
    if full_content:
        params["full_content"] = {"enabled": True}
    
    result = client.beta.extract(**params)
    return result


def tavily_extract(urls: list, full_content: bool = False, objective: str = None) -> dict:
    """Extract content from URLs using Tavily."""
    tavily_key = os.environ.get("TAVILY_API_KEY")
    if not tavily_key:
        print("Error: TAVILY_API_KEY environment variable is required when --provider=tavily", file=sys.stderr)
        sys.exit(1)

    from tavily import TavilyClient

    client = TavilyClient(api_key=tavily_key)

    params = {"urls": urls[:20]}

    if full_content:
        params["extract_depth"] = "advanced"

    if objective:
        params["query"] = objective

    result = client.extract(**params)

    # Normalize into the structure format_result() expects
    class _Item:
        def __init__(self, url, raw_content):
            self.url = url
            self.title = url
            self.publish_date = None
            self.excerpts = None
            self.content = raw_content

    class _Result:
        def __init__(self, items, failed):
            self.extract_id = "tavily"
            self.results = items
            self.failed = failed

    items = []
    for r in result.get("results", []):
        items.append(_Item(r.get("url", ""), r.get("raw_content", "")))

    failed = result.get("failed_results", [])
    if failed:
        print(f"⚠️  {len(failed)} URL(s) failed to extract", file=sys.stderr)

    return _Result(items, failed)


def format_result(result) -> str:
    """Format extraction result for display."""
    output = []
    
    output.append(f"📄 Extract ID: {result.extract_id}")
    output.append("")
    
    for i, item in enumerate(result.results, 1):
        url = item.url
        title = getattr(item, 'title', 'No title')
        date = getattr(item, 'publish_date', None)
        
        date_str = f" ({date})" if date else ""
        output.append(f"**{i}. {title}**{date_str}")
        output.append(f"   URL: {url}")
        
        # Show excerpts or content
        excerpts = getattr(item, 'excerpts', None)
        content = getattr(item, 'content', None)
        
        if content:
            # Full content mode
            preview = content[:2000]
            if len(content) > 2000:
                preview += f"\n\n... [{len(content)} chars total]"
            output.append(f"\n{preview}")
        elif excerpts:
            # Excerpt mode
            output.append("")
            for excerpt in excerpts[:3]:
                excerpt_clean = excerpt.replace("\n", " ").strip()[:500]
                output.append(f"   > {excerpt_clean}")
        
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="URL content extraction via Parallel.ai or Tavily")
    parser.add_argument("urls", nargs="+", help="URLs to extract content from")
    parser.add_argument("--provider", "-p", choices=["parallel", "tavily"],
                       default="parallel", help="Extraction provider (default: parallel)")
    parser.add_argument("--objective", "-o", metavar="TEXT",
                       help="Focus extraction on specific content (e.g., 'Extract API endpoints')")
    parser.add_argument("--full", "-f", action="store_true",
                       help="Return full page content instead of excerpts")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output raw JSON")

    args = parser.parse_args()

    try:
        if args.provider == "tavily":
            if args.objective:
                print("⚠️  --objective is passed as query hint for Tavily (no direct equivalent)", file=sys.stderr)
            result = tavily_extract(
                urls=args.urls,
                full_content=args.full,
                objective=args.objective,
            )
        else:
            if not API_KEY:
                print("Error: PARALLEL_API_KEY environment variable is required", file=sys.stderr)
                sys.exit(1)
            client = Parallel(api_key=API_KEY)
            result = extract(
                client,
                urls=args.urls,
                objective=args.objective,
                full_content=args.full,
            )
        
        if args.json:
            output = {
                "extract_id": result.extract_id,
                "results": [
                    {
                        "url": r.url,
                        "title": getattr(r, 'title', None),
                        "publish_date": getattr(r, 'publish_date', None),
                        "excerpts": getattr(r, 'excerpts', None),
                        "content": getattr(r, 'content', None),
                    }
                    for r in result.results
                ]
            }
            print(json.dumps(output, indent=2, default=str))
        else:
            print(format_result(result))
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
