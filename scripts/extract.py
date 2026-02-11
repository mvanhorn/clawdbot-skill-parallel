#!/usr/bin/env python3
"""
Parallel.ai Extract API - Clean content extraction from any URL.

Usage:
  python3 extract.py https://stripe.com/docs/api  # Extract with excerpts
  python3 extract.py https://example.com/paper.pdf --full  # Full content
  python3 extract.py https://sec.gov/10-K.htm --objective "Extract risk factors"
"""

import os
import sys
import json
import argparse

from parallel import Parallel

API_KEY = os.environ.get("PARALLEL_API_KEY")
if not API_KEY:
    print("Error: PARALLEL_API_KEY environment variable is required", file=sys.stderr)
    sys.exit(1)


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
    parser = argparse.ArgumentParser(description="Parallel.ai Extract API")
    parser.add_argument("urls", nargs="+", help="URLs to extract content from")
    parser.add_argument("--objective", "-o", metavar="TEXT",
                       help="Focus extraction on specific content (e.g., 'Extract API endpoints')")
    parser.add_argument("--full", "-f", action="store_true",
                       help="Return full page content instead of excerpts")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output raw JSON")
    
    args = parser.parse_args()
    
    client = Parallel(api_key=API_KEY)
    
    try:
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
