---
name: parallel
description: High-accuracy web search and research via Parallel.ai API. Optimized for AI agents with rich excerpts and citations. Supports authenticated/private sources.
user-invocable: true
disable-model-invocation: true
triggers:
  - parallel
  - deep search
  - research
  - enrich
  - findall
  - monitor
  - extract
metadata:
  clawdbot:
    emoji: "🔬"
    primaryEnv: PARALLEL_API_KEY
    requires:
      bins: [python3]
      env: [PARALLEL_API_KEY, BROWSERUSE_API_KEY]
---

# Parallel.ai 🔬

High-accuracy web research API built for AI agents. Outperforms Perplexity/Exa on research benchmarks.

## APIs Overview

| API | Use Case | Speed |
|-----|----------|-------|
| **Search** | Quick lookups, current events | Fast |
| **Task** | Deep research, enrichment, reports | Medium-Slow |
| **FindAll** | Entity discovery → structured datasets | Slow (async) |
| **Extract** | Clean content from URLs/PDFs | Fast |
| **Monitor** | Continuous tracking with alerts | Recurring |

---

## Search API - Quick web search

```bash
python3 {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5
python3 {baseDir}/scripts/search.py "latest AI news" --json
```

---

## Task API - Deep research & enrichment

```bash
# Simple question → answer
python3 {baseDir}/scripts/task.py "What was France's GDP in 2023?"

# Structured enrichment (company research)
python3 {baseDir}/scripts/task.py --enrich "company_name=Stripe,website=stripe.com" \
  --output "founding_year,employee_count,total_funding"

# Research report (markdown with citations)
python3 {baseDir}/scripts/task.py --report "Market analysis of the HVAC industry in USA"

# With authenticated sources (requires browser-use.com key)
export BROWSERUSE_API_KEY="your-key"
python3 {baseDir}/scripts/task.py "Extract specs from https://nxp.com/products/K66_180"
```

### Processors

| Processor | Speed | Depth | Use Case |
|-----------|-------|-------|----------|
| `base` | Fast | Light | Simple lookups, fact checks |
| `core` | Medium | Standard | Enrichment, structured data |
| `ultra` | Slow | Deep | Reports, multi-hop research |

---

## FindAll API - Entity discovery (NEW Feb 2026)

Turn natural language into structured datasets. "Find all dental practices in Ohio with 4+ star reviews" → enriched list with citations.

```bash
# Basic entity discovery
python3 {baseDir}/scripts/findall.py "Find all AI startups that raised Series A in 2025"

# With enrichment
python3 {baseDir}/scripts/findall.py "portfolio companies of Khosla Ventures" \
  --enrich "funding,employee_count,founder_names" --limit 50

# Lead generation
python3 {baseDir}/scripts/findall.py "residential roofing companies in Charlotte, NC" --generator pro

# Check status of running job
python3 {baseDir}/scripts/findall.py --status findall_abc123
```

### Generators

| Generator | Coverage | Cost | Use Case |
|-----------|----------|------|----------|
| `base` | Limited | Low | Quick discovery, prototyping |
| `core` | Balanced | Medium | Most use cases |
| `pro` | Comprehensive | High | Maximum recall (61% benchmark) |

### How it works
1. **Ingest**: Converts natural language → entity type + match conditions
2. **Generate**: Searches web for candidate entities
3. **Evaluate**: Validates each candidate against match conditions
4. **Enrich**: Extracts additional fields for matched entities

---

## Extract API - Clean content extraction (NEW Feb 2026)

Convert any URL into clean markdown - handles JS-heavy pages, PDFs, paywalls.

```bash
# Basic extraction with excerpts
python3 {baseDir}/scripts/extract.py https://stripe.com/docs/api

# Full content (not just excerpts)
python3 {baseDir}/scripts/extract.py https://arxiv.org/pdf/2301.00000.pdf --full

# Focused extraction
python3 {baseDir}/scripts/extract.py https://sec.gov/10-K.htm --objective "Extract risk factors"

# Multiple URLs at once
python3 {baseDir}/scripts/extract.py https://url1.com https://url2.com --json
```

### Use Cases
- **API documentation** - Pull complete references and code examples
- **PDF research papers** - Extract methodology, results, citations
- **SEC filings** - Extract specific sections from 10-Ks, earnings reports
- **News articles** - Get clean text without ads/nav/paywalls

---

## Monitor API - Continuous tracking (NEW Feb 2026)

Set up recurring queries - get alerts when things change.

```bash
# Create a monitor
python3 {baseDir}/scripts/monitor.py create "Track AI funding news" --cadence daily
python3 {baseDir}/scripts/monitor.py create "Alert when AirPods drop below $150" --cadence hourly

# With webhook notifications
python3 {baseDir}/scripts/monitor.py create "OpenAI product announcements" \
  --cadence daily --webhook https://your-endpoint.com/webhook

# List all monitors
python3 {baseDir}/scripts/monitor.py list

# Get events (detected changes)
python3 {baseDir}/scripts/monitor.py events monitor_abc123
python3 {baseDir}/scripts/monitor.py events monitor_abc123 --lookback 10d

# Delete a monitor
python3 {baseDir}/scripts/monitor.py delete monitor_abc123
```

### Cadences
- `hourly` - Fast-moving topics, stock/price tracking
- `daily` - News, competitive intel (most common)
- `weekly` - Slower changes, policy updates

### Example queries
- **News**: "Let me know when someone mentions Parallel Web Systems"
- **Competitive**: "Alert me when Apple announces new MacBook models"
- **Price**: "Notify me when PS5 Pro is back in stock at Best Buy"
- **Policy**: "Track changes to OpenAI's terms of service"

---

## Authenticated Sources (Jan 2026)

Task API supports **authentication-gated private data sources** via MCP servers:
- Internal wikis & dashboards
- Industry databases (NXP, IEEE, etc.)
- CRM systems & subscription services

Uses [browser-use.com](https://browser-use.com) MCP integration:

### Setup
1. Get API key from [browser-use.com](https://browser-use.com)
2. Create a **profile** with saved login sessions
3. Set `BROWSERUSE_API_KEY` env var

### Usage
```bash
export BROWSERUSE_API_KEY="your-key"
python3 {baseDir}/scripts/task.py "Extract migration guide from NXP K66 docs"
```

---

## When to Use Each API

| Scenario | API | Why |
|----------|-----|-----|
| Quick fact lookup | Search | Fast, simple |
| Company enrichment | Task | Structured output with citations |
| Build a prospect list | FindAll | Discovers + validates + enriches |
| Extract content from URL | Extract | Handles JS, PDFs, paywalls |
| Ongoing tracking | Monitor | Set once, get alerts |
| Deep research report | Task (--report) | Multi-hop with citations |
| Access gated content | Task + MCP | Authenticated browsing |

---

## API Reference

- Docs: https://docs.parallel.ai
- Platform: https://platform.parallel.ai
- Changelog: https://parallel.ai/blog

---

## Security & Permissions

**What this skill does:**
- Makes API calls to `api.parallel.ai` for web search, research, extraction, and monitoring
- All scripts are read-only research tools — they do not modify any local or remote data
- The `BROWSERUSE_API_KEY` (optional) is only used for authenticated source access via browser-use.com

**What this skill does NOT do:**
- Does not send your API key to any endpoint other than `api.parallel.ai`
- Does not access local files, databases, or system resources
- Does not write to disk (except JSON output when using `--json`)
- Cannot be invoked autonomously by the agent (`disable-model-invocation: true`)

Review `scripts/` before first use to verify behavior.
