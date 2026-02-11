#!/usr/bin/env python3
"""
Parallel.ai Task API - Deep research, enrichment, and authenticated sources.

Usage:
  python3 task.py "What was France's GDP in 2023?"
  python3 task.py --enrich "company_name=Stripe" --output "founding_year,funding"
  python3 task.py --report "Market analysis of HVAC industry"
  
  # Authenticated page access (requires browser-use.com API key)
  export BROWSERUSE_API_KEY="your-key"
  python3 task.py "Extract migration docs from https://nxp.com/products/K66_180"
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


def create_task(
    client: Parallel,
    input_data,
    processor: str = "core",
    task_spec: dict = None,
    include_domains: list = None,
    exclude_domains: list = None,
    mcp_servers: list = None,
) -> dict:
    """Create and run a task."""
    params = {
        "input": input_data,
        "processor": processor,
    }
    
    if task_spec:
        params["task_spec"] = task_spec
    
    # Source policy
    if include_domains or exclude_domains:
        source_policy = {}
        if include_domains:
            source_policy["include_domains"] = include_domains
        if exclude_domains:
            source_policy["exclude_domains"] = exclude_domains
        params["source_policy"] = source_policy
    
    # MCP servers for authenticated browsing (Jan 2026 feature)
    if mcp_servers:
        params["mcp_servers"] = mcp_servers
        params["betas"] = ["mcp-server-2025-07-17"]
    
    # Create task run
    task_run = client.beta.task_run.create(**params)
    return task_run


def poll_task(client: Parallel, run_id: str, timeout: int = 300) -> dict:
    """Poll until task completes."""
    start = time.time()
    while time.time() - start < timeout:
        result = client.beta.task_run.retrieve(run_id)
        if result.run.status == "completed":
            return result
        elif result.run.status == "failed":
            raise Exception(f"Task failed: {result.run}")
        time.sleep(2)
    raise TimeoutError(f"Task {run_id} did not complete within {timeout}s")


def build_enrichment_spec(input_fields: str, output_fields: str) -> tuple:
    """Build input/output schemas for enrichment."""
    # Parse input: "company_name=Stripe,website=stripe.com"
    input_data = {}
    input_props = {}
    for pair in input_fields.split(","):
        if "=" in pair:
            key, val = pair.split("=", 1)
            input_data[key.strip()] = val.strip()
            input_props[key.strip()] = {"type": "string"}
    
    # Parse output: "founding_year,employee_count,funding"
    output_props = {}
    for field in output_fields.split(","):
        field = field.strip()
        if field:
            output_props[field] = {
                "type": "string",
                "description": f"The {field.replace('_', ' ')} of the entity"
            }
    
    task_spec = {
        "input_schema": {
            "type": "json",
            "json_schema": {
                "type": "object",
                "properties": input_props,
                "required": list(input_props.keys()),
                "additionalProperties": False
            }
        },
        "output_schema": {
            "type": "json",
            "json_schema": {
                "type": "object",
                "properties": output_props,
                "required": list(output_props.keys()),
                "additionalProperties": False
            }
        }
    }
    
    return input_data, task_spec


def format_result(result) -> str:
    """Format task result for display."""
    output = []
    
    run = result.run
    output.append(f"🔬 Task: {run.run_id}")
    output.append(f"   Status: {run.status} | Processor: {run.processor}")
    output.append("")
    
    if hasattr(result, 'output') and result.output:
        content = result.output.content
        output_type = result.output.type
        
        if output_type == "json" and isinstance(content, dict):
            output.append("**Results:**")
            for key, val in content.items():
                # Truncate long values
                val_str = str(val)
                if len(val_str) > 200:
                    val_str = val_str[:200] + "..."
                output.append(f"  • {key}: {val_str}")
        elif output_type == "text":
            output.append("**Report:**")
            output.append(content[:2000] + "..." if len(content) > 2000 else content)
        else:
            output.append(f"**Output ({output_type}):**")
            output.append(str(content)[:2000])
        
        # Show basis/citations if available
        if hasattr(result.output, 'basis') and result.output.basis:
            output.append("")
            output.append("**Citations:**")
            for basis in result.output.basis[:5]:  # Limit to 5
                field = basis.field if hasattr(basis, 'field') else 'result'
                confidence = basis.confidence if hasattr(basis, 'confidence') else 'unknown'
                output.append(f"  [{field}] confidence: {confidence}")
                if hasattr(basis, 'citations'):
                    for cite in basis.citations[:2]:
                        output.append(f"    - {cite.title}: {cite.url}")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Parallel.ai Task API")
    parser.add_argument("query", nargs="*", help="Research query or question")
    parser.add_argument("--processor", "-p", default="core", 
                       choices=["base", "core", "ultra"],
                       help="Processor tier (base=fast, core=standard, ultra=deep)")
    parser.add_argument("--enrich", "-e", metavar="FIELDS",
                       help="Enrichment mode: key=value pairs (e.g., 'company_name=Stripe,website=stripe.com')")
    parser.add_argument("--output", "-o", metavar="FIELDS",
                       help="Output fields for enrichment (e.g., 'founding_year,employee_count')")
    parser.add_argument("--report", "-r", action="store_true",
                       help="Generate markdown report with citations")
    parser.add_argument("--include-domains", metavar="DOMAINS",
                       help="Comma-separated domains to include")
    parser.add_argument("--exclude-domains", metavar="DOMAINS",
                       help="Comma-separated domains to exclude")
    parser.add_argument("--browseruse-key", metavar="KEY",
                       help="browser-use.com API key for authenticated page access")
    parser.add_argument("--timeout", "-t", type=int, default=300,
                       help="Timeout in seconds (default: 300)")
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output raw JSON")
    parser.add_argument("--no-wait", action="store_true",
                       help="Don't wait for completion, just return run_id")
    
    args = parser.parse_args()
    
    client = Parallel(api_key=API_KEY)
    
    # Determine input and task spec
    input_data = None
    task_spec = None
    processor = args.processor
    
    if args.enrich:
        if not args.output:
            print("Error: --enrich requires --output fields", file=sys.stderr)
            sys.exit(1)
        input_data, task_spec = build_enrichment_spec(args.enrich, args.output)
    elif args.report:
        query = " ".join(args.query) if args.query else None
        if not query:
            print("Error: --report requires a query", file=sys.stderr)
            sys.exit(1)
        input_data = query
        task_spec = {"output_schema": {"type": "text"}}
        processor = "ultra"  # Reports need deep processing
    else:
        query = " ".join(args.query) if args.query else None
        if not query:
            parser.print_help()
            sys.exit(1)
        input_data = query
    
    # Parse domain filters
    include_domains = None
    exclude_domains = None
    if args.include_domains:
        include_domains = [d.strip() for d in args.include_domains.split(",")]
    if args.exclude_domains:
        exclude_domains = [d.strip() for d in args.exclude_domains.split(",")]
    
    # Build MCP servers for authenticated browsing
    mcp_servers = None
    browseruse_key = args.browseruse_key or os.environ.get("BROWSERUSE_API_KEY")
    if browseruse_key:
        mcp_servers = [{
            "type": "url",
            "url": "https://api.browser-use.com/mcp",
            "name": "browseruse",
            "headers": {"Authorization": f"Bearer {browseruse_key}"}
        }]
    
    # Create task
    try:
        task_run = create_task(
            client,
            input_data,
            processor=processor,
            task_spec=task_spec,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            mcp_servers=mcp_servers,
        )
        
        run_id = task_run.run.run_id if hasattr(task_run, 'run') else task_run.run_id
        
        if args.no_wait:
            print(f"Task created: {run_id}")
            return
        
        # Poll for completion
        print(f"⏳ Running task {run_id}...", file=sys.stderr)
        result = poll_task(client, run_id, timeout=args.timeout)
        
        if args.json:
            # Convert to dict for JSON output
            output = {
                "run_id": result.run.run_id,
                "status": result.run.status,
                "processor": result.run.processor,
            }
            if hasattr(result, 'output') and result.output:
                output["output"] = {
                    "type": result.output.type,
                    "content": result.output.content,
                }
                if hasattr(result.output, 'basis'):
                    output["basis"] = [
                        {
                            "field": b.field if hasattr(b, 'field') else None,
                            "confidence": b.confidence if hasattr(b, 'confidence') else None,
                            "citations": [
                                {"title": c.title, "url": c.url}
                                for c in (b.citations if hasattr(b, 'citations') else [])
                            ]
                        }
                        for b in result.output.basis
                    ]
            print(json.dumps(output, indent=2, default=str))
        else:
            print(format_result(result))
            
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
