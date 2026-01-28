---
name: parallel
description: High-accuracy web search and research via Parallel.ai API. Optimized for AI agents with rich excerpts and citations. Supports authenticated/private sources.
triggers:
  - parallel
  - deep search
  - research
  - enrich
metadata:
  clawdbot:
    emoji: "🔬"
---

# Parallel.ai 🔬

High-accuracy web research API built for AI agents. Outperforms Perplexity/Exa on research benchmarks.

## APIs

### Search API - Quick web search
```bash
python3 {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5
python3 {baseDir}/scripts/search.py "latest AI news" --json
```

### Task API - Deep research & enrichment
```bash
# Simple question → answer
python3 {baseDir}/scripts/task.py "What was France's GDP in 2023?"

# Structured enrichment (company research)
python3 {baseDir}/scripts/task.py --enrich "company_name=Stripe,website=stripe.com" \
  --output "founding_year,employee_count,total_funding"

# Research report (markdown with citations)
python3 {baseDir}/scripts/task.py --report "Market analysis of the HVAC industry in USA"

# With authenticated sources (NEW - Jan 2026, requires browser-use.com key)
export BROWSERUSE_API_KEY="your-key"
python3 {baseDir}/scripts/task.py "Extract specs from https://nxp.com/products/K66_180"
```

## Authenticated Sources (NEW - Jan 2026)

Task API now supports **authentication-gated private data sources** via MCP servers:
- Internal wikis & dashboards
- Industry databases (NXP, IEEE, etc.)
- CRM systems & subscription services
- Paywalled content

Uses [browser-use.com](https://browser-use.com) MCP integration:

### Setup
1. Get API key from [browser-use.com](https://browser-use.com)
2. Create a **profile** with saved login sessions ([Profile Docs](https://docs.cloud.browser-use.com/concepts/profile))
3. Set `BROWSERUSE_API_KEY` env var

### Usage
```bash
# CLI
export BROWSERUSE_API_KEY="your-key"
python3 {baseDir}/scripts/task.py "Extract specs from https://nxp.com/products/K66_180"
```

```python
# Python SDK
task_run = client.beta.task_run.create(
    input="Extract migration guide from NXP K66 docs",
    processor="ultra",
    mcp_servers=[{
        "type": "url",
        "url": "https://api.browser-use.com/mcp",
        "name": "browseruse",
        "headers": {"Authorization": "Bearer YOUR_BROWSERUSE_KEY"}
    }],
    betas=["mcp-server-2025-07-17"]
)
```

```bash
# cURL
curl -X POST "https://api.parallel.ai/v1/tasks/runs" \
  -H "x-api-key: $PARALLEL_API_KEY" \
  -H "Content-Type: application/json" \
  -H "parallel-beta: mcp-server-2025-07-17" \
  --data '{
    "input": "Extract data from internal dashboard",
    "processor": "ultra",
    "mcp_servers": [{
      "type": "url",
      "url": "https://api.browser-use.com/mcp",
      "name": "browseruse",
      "headers": {"Authorization": "Bearer YOUR_KEY"}
    }]
  }'
```

**Requirements:**
- browser-use.com API key + profile with saved credentials
- `parallel-beta: mcp-server-2025-07-17` header
- Processor: `ultra` (supports multiple tool calls)
- Max 10 MCP servers per request

**Capabilities:**
- Navigate SPAs and JS-heavy sites
- Fill forms, click buttons, multi-step workflows
- Combine with Parallel's public web research

## Processors

| Processor | Speed | Depth | Use Case |
|-----------|-------|-------|----------|
| `base` | Fast | Light | Simple lookups, fact checks |
| `core` | Medium | Standard | Enrichment, structured data |
| `ultra` | Slow | Deep | Reports, multi-hop research |

## Response Format

### Search API
- `search_id` - unique identifier
- `results[]` - url, title, excerpts, publish_date
- `usage` - API usage stats

### Task API
- `run_id` - task identifier
- `output.content` - structured result or markdown report
- `output.basis[]` - citations, reasoning, confidence per field

## When to Use

- **Search API**: Quick lookups, current events, simple queries
- **Task API**: 
  - Enrichment at scale (CRM, company lists)
  - Deep research reports with citations
  - Accessing authenticated/gated sources
  - Structured output with confidence levels

## API Reference

Docs: https://docs.parallel.ai
Platform: https://platform.parallel.ai
