#!/usr/bin/env python3
"""
Parallel.ai FindAll API - Natural language → structured datasets.

Usage:
  python3 findall.py "Find all AI startups that raised Series A in the last 6 months"
  python3 findall.py "dental practices in Ohio with 4+ star Google reviews" --limit 50
  python3 findall.py "portfolio companies of Khosla Ventures" --enrich "funding,employee_count"
  python3 findall.py --status findall_abc123  # Check status of running job
"""

import os
import sys
import json
import argparse
import time

from parallel import Parallel

API_KEY = os.environ.get("PARALLEL_API_KEY")
if not API_KEY:
    print("Error: PARALLEL_API_KEY environment variable is required", file=sys.stderr)
    sys.exit(1)


def ingest_query(client: Parallel, query: str) -> dict:
    """Convert natural language to structured schema."""
    result = client.beta.findall.ingest(objective=query)
    return result


def create_findall(
    client: Parallel,
    objective: str,
    entity_type: str,
    match_conditions: list,
    generator: str = "core",
    match_limit: int = 25,
    enrichments: list = None,
) -> str:
    """Start a FindAll run."""
    params = {
        "objective": objective,
        "entity_type": entity_type,
        "match_conditions": match_conditions,
        "generator": generator,
        "match_limit": match_limit,
    }
    
    if enrichments:
        params["enrichments"] = enrichments
    
    result = client.beta.findall.create(**params)
    return result.findall_id


def poll_findall(client: Parallel, findall_id: str, timeout: int = 600) -> dict:
    """Poll until FindAll completes."""
    start = time.time()
    while time.time() - start < timeout:
        result = client.beta.findall.retrieve(findall_id)
        status = result.status.status if hasattr(result.status, 'status') else result.status
        
        if status == "completed":
            return result
        elif status == "failed":
            raise Exception(f"FindAll failed: {result}")
        
        # Show progress
        if hasattr(result.status, 'metrics'):
            m = result.status.metrics
            gen = getattr(m, 'generated_candidates_count', 0)
            matched = getattr(m, 'matched_candidates_count', 0)
            print(f"⏳ Progress: {matched} matched / {gen} generated", file=sys.stderr)
        
        time.sleep(5)
    raise TimeoutError(f"FindAll {findall_id} did not complete within {timeout}s")


def format_result(result) -> str:
    """Format FindAll result for display."""
    output = []
    
    findall_id = result.findall_id
    status = result.status.status if hasattr(result.status, 'status') else result.status
    metrics = result.status.metrics if hasattr(result.status, 'metrics') else None
    
    output.append(f"🔍 FindAll: {findall_id}")
    output.append(f"   Status: {status}")
    
    if metrics:
        gen = getattr(metrics, 'generated_candidates_count', 0)
        matched = getattr(metrics, 'matched_candidates_count', 0)
        output.append(f"   Candidates: {matched} matched / {gen} generated")
    output.append("")
    
    if hasattr(result, 'candidates') and result.candidates:
        output.append("**Matched Entities:**")
        for i, candidate in enumerate(result.candidates, 1):
            name = getattr(candidate, 'name', 'Unknown')
            url = getattr(candidate, 'url', '')
            desc = getattr(candidate, 'description', '')[:150]
            
            output.append(f"\n**{i}. {name}**")
            if url:
                output.append(f"   URL: {url}")
            if desc:
                output.append(f"   {desc}")
            
            # Show enrichments if present
            if hasattr(candidate, 'enrichments') and candidate.enrichments:
                for key, val in candidate.enrichments.items():
                    val_str = str(val)[:100]
                    output.append(f"   • {key}: {val_str}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Parallel.ai FindAll API")
    parser.add_argument("query", nargs="*", help="Natural language query")
    parser.add_argument("--generator", "-g", default="core",
                       choices=["base", "core", "pro"],
                       help="Generator tier (base=budget, core=balanced, pro=comprehensive)")
    parser.add_argument("--limit", "-l", type=int, default=25,
                       help="Maximum matched entities to return")
    parser.add_argument("--enrich", "-e", metavar="FIELDS",
                       help="Comma-separated enrichment fields (e.g., 'funding,employee_count')")
    parser.add_argument("--status", "-s", metavar="ID",
                       help="Check status of existing FindAll job")
    parser.add_argument("--timeout", "-t", type=int, default=600,
                       help="Timeout in seconds (default: 600)")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output raw JSON")
    parser.add_argument("--no-wait", action="store_true",
                       help="Don't wait for completion, just return findall_id")
    
    args = parser.parse_args()
    
    client = Parallel(api_key=API_KEY)
    
    # Check status of existing job
    if args.status:
        result = client.beta.findall.retrieve(args.status)
        if args.json:
            print(json.dumps(result.__dict__, indent=2, default=str))
        else:
            print(format_result(result))
        return
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    query = " ".join(args.query)
    
    try:
        # Step 1: Ingest - convert natural language to schema
        print(f"📝 Analyzing query...", file=sys.stderr)
        schema = ingest_query(client, query)
        
        entity_type = schema.entity_type
        match_conditions = [
            {"name": c.name, "description": c.description}
            for c in schema.match_conditions
        ]
        
        print(f"   Entity type: {entity_type}", file=sys.stderr)
        print(f"   Match conditions: {len(match_conditions)}", file=sys.stderr)
        
        # Parse enrichments
        enrichments = None
        if args.enrich:
            enrichments = [
                {"name": f.strip(), "description": f"The {f.strip().replace('_', ' ')}"}
                for f in args.enrich.split(",")
            ]
        
        # Step 2: Create FindAll run
        print(f"🚀 Starting FindAll...", file=sys.stderr)
        findall_id = create_findall(
            client,
            objective=schema.objective,
            entity_type=entity_type,
            match_conditions=match_conditions,
            generator=args.generator,
            match_limit=args.limit,
            enrichments=enrichments,
        )
        
        if args.no_wait:
            print(f"FindAll created: {findall_id}")
            return
        
        # Step 3: Poll for completion
        result = poll_findall(client, findall_id, timeout=args.timeout)
        
        if args.json:
            output = {
                "findall_id": result.findall_id,
                "status": result.status.status if hasattr(result.status, 'status') else result.status,
                "candidates": [
                    {
                        "name": getattr(c, 'name', None),
                        "url": getattr(c, 'url', None),
                        "description": getattr(c, 'description', None),
                        "enrichments": getattr(c, 'enrichments', None),
                    }
                    for c in (result.candidates or [])
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
