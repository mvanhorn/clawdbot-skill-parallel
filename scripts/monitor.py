#!/usr/bin/env python3
"""
Parallel.ai Monitor API - Continuous web tracking with alerts.

Usage:
  python3 monitor.py create "Track AI funding news" --cadence daily
  python3 monitor.py create "Alert when AirPods drop below $150" --cadence hourly --webhook https://...
  python3 monitor.py list  # List all monitors
  python3 monitor.py events monitor_abc123  # Get events for a monitor
  python3 monitor.py delete monitor_abc123  # Delete a monitor
"""

import os
import sys
import json
import argparse
import requests

API_KEY = os.environ.get("PARALLEL_API_KEY")
if not API_KEY:
    print("Error: PARALLEL_API_KEY environment variable is required", file=sys.stderr)
    sys.exit(1)
BASE_URL = "https://api.parallel.ai/v1alpha"


def api_request(method: str, endpoint: str, data: dict = None) -> dict:
    """Make API request to Parallel."""
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json",
    }
    
    url = f"{BASE_URL}{endpoint}"
    
    if method == "GET":
        response = requests.get(url, headers=headers, params=data)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)
    else:
        raise ValueError(f"Unsupported method: {method}")
    
    response.raise_for_status()
    return response.json() if response.text else {}


def create_monitor(
    query: str,
    cadence: str = "daily",
    webhook_url: str = None,
    metadata: dict = None,
) -> dict:
    """Create a new monitor."""
    data = {
        "query": query,
        "cadence": cadence,
    }
    
    if webhook_url:
        data["webhook"] = {
            "url": webhook_url,
            "event_types": ["monitor.event.detected", "monitor.run.completed"]
        }
    
    if metadata:
        data["metadata"] = metadata
    
    return api_request("POST", "/monitors", data)


def list_monitors() -> list:
    """List all monitors."""
    return api_request("GET", "/monitors")


def get_events(monitor_id: str, lookback: str = None) -> dict:
    """Get events for a monitor."""
    params = {}
    if lookback:
        params["lookback"] = lookback
    return api_request("GET", f"/monitors/{monitor_id}/events", params)


def delete_monitor(monitor_id: str) -> bool:
    """Delete a monitor."""
    api_request("DELETE", f"/monitors/{monitor_id}")
    return True


def format_monitor(monitor: dict) -> str:
    """Format a single monitor for display."""
    output = []
    
    monitor_id = monitor.get("monitor_id", "unknown")
    query = monitor.get("query", "")
    status = monitor.get("status", "unknown")
    cadence = monitor.get("cadence", "unknown")
    created = monitor.get("created_at")
    
    output.append(f"📡 {monitor_id}")
    output.append(f"   Query: {query[:100]}")
    output.append(f"   Status: {status} | Cadence: {cadence}")
    if created:
        output.append(f"   Created: {created}")
    
    return "\n".join(output)


def format_events(events_result: dict) -> str:
    """Format events for display."""
    output = []
    
    events = events_result.get("events", [])
    
    if not events:
        return "No events found."
    
    output.append(f"📋 Events ({len(events)} total)")
    output.append("")
    
    for i, event in enumerate(events[:20], 1):
        event_type = event.get("type", "event")
        event_date = event.get("event_date")
        event_output = event.get("output", "")
        sources = event.get("source_urls", [])
        
        date_str = f" ({event_date})" if event_date else ""
        output.append(f"**{i}. {event_type}**{date_str}")
        
        if event_output:
            output.append(f"   {event_output[:200]}")
        
        if sources:
            for src in sources[:2]:
                output.append(f"   🔗 {src}")
        output.append("")
    
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser(description="Parallel.ai Monitor API")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new monitor")
    create_parser.add_argument("query", help="What to monitor")
    create_parser.add_argument("--cadence", "-c", default="daily",
                              choices=["hourly", "daily", "weekly"],
                              help="How often to check")
    create_parser.add_argument("--webhook", "-w", metavar="URL",
                              help="Webhook URL for notifications")
    create_parser.add_argument("--metadata", "-m", metavar="JSON",
                              help="JSON metadata to attach")
    
    # List command
    subparsers.add_parser("list", help="List all monitors")
    
    # Events command
    events_parser = subparsers.add_parser("events", help="Get events for a monitor")
    events_parser.add_argument("monitor_id", help="Monitor ID")
    events_parser.add_argument("--lookback", "-l", metavar="DURATION",
                              help="Lookback duration (e.g., '10d', '1w')")
    
    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a monitor")
    delete_parser.add_argument("monitor_id", help="Monitor ID to delete")
    
    # Global options
    parser.add_argument("--json", "-j", action="store_true",
                       help="Output raw JSON")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == "create":
            metadata = json.loads(args.metadata) if args.metadata else None
            result = create_monitor(
                query=args.query,
                cadence=args.cadence,
                webhook_url=args.webhook,
                metadata=metadata,
            )
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(f"✅ Monitor created!")
                print(format_monitor(result))
                
        elif args.command == "list":
            result = list_monitors()
            monitors = result.get("monitors", result) if isinstance(result, dict) else result
            
            if args.json:
                print(json.dumps(monitors, indent=2))
            else:
                if not monitors:
                    print("No monitors found.")
                else:
                    print(f"📡 Monitors ({len(monitors)} total)\n")
                    for monitor in monitors:
                        print(format_monitor(monitor))
                        print()
                        
        elif args.command == "events":
            result = get_events(args.monitor_id, lookback=args.lookback)
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(format_events(result))
                
        elif args.command == "delete":
            delete_monitor(args.monitor_id)
            print(f"✅ Monitor {args.monitor_id} deleted.")
            
    except requests.exceptions.HTTPError as e:
        print(f"❌ API Error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
