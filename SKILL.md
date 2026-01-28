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

# With authenticated sources (NEW - Jan 2026)
python3 {baseDir}/scripts/task.py --auth-session cookies.json \
  "Extract key specs from internal wiki at wiki.company.com/product"
```

## Authenticated Sources (NEW)

Task API now supports **authentication-gated private data sources**:
- Internal wikis
- Industry databases (NXP, IEEE, etc.)
- Niche forums
- Paywalled content

Provide a browser session/cookies to access gated content:
```python
task_run = client.beta.task_run.create(
    input="Extract migration guide from NXP K66 docs",
    processor="ultra",
    auth_session={
        "cookies": [{"name": "session", "value": "...", "domain": ".nxp.com"}]
    }
)
```

**Use cases:**
- Research behind login walls
- Extract from internal documentation
- Industry database enrichment

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
