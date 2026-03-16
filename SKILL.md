---
name: parallel
version: "3.0.0"
description: High-accuracy web research platform with 7 APIs - Search, Extract, Task (Deep Research), Chat, FindAll, Monitor, and Task Groups. Fast mode, 8 processor tiers, MCP tool calling, authenticated browsing, SSE streaming, and OpenAI-compatible chat. OpenClaw skill.
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-parallel
homepage: https://parallel.ai
triggers:
  - parallel
  - deep search
  - research
  - fact check
  - web research
  - search with citations
  - find companies
  - find startups
  - extract content
  - monitor web
  - accurate search
  - cross-reference
  - evidence-based search
  - batch search
  - chat with web
  - task group
  - findall
  - entity discovery
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      env:
        - PARALLEL_API_KEY
      optionalEnv:
        - BROWSERUSE_API_KEY
    primaryEnv: PARALLEL_API_KEY
    tags:
      - search
      - research
      - web
      - parallel
      - citations
      - deep-research
      - agentic
      - fact-checking
      - accurate
      - benchmarks
      - extraction
      - monitoring
      - findall
      - batch
      - chat
      - task-groups
      - fast-mode
      - mcp
---

# Parallel.ai - High-Accuracy Web Research Platform

Deep web research platform with 7 APIs built for AI agents. Outperforms Perplexity and Exa on research benchmarks with rich excerpts, citations, and source provenance.

## Setup

```bash
pip install -r {baseDir}/requirements.txt
```

Requires `PARALLEL_API_KEY` environment variable. Get a key at https://platform.parallel.ai

Optional: `BROWSERUSE_API_KEY` for authenticated page access via browser-use.com (see Authenticated Sources section below).

## Security Notes

- API keys are loaded from environment variables only - never hardcoded in scripts
- User input is safely escaped before API calls (no JSON injection)
- Dependencies are pinned in `requirements.txt` to prevent supply chain attacks
- When using `BROWSERUSE_API_KEY`, your key is transmitted to Parallel.ai servers which proxy it to browser-use.com. Both services see your queries and credentials. Only enable this if you understand and accept that data flow.

---

## Search API

`POST /v1/search`

The primary search interface. Use for most research queries.

### Modes

| Mode | Latency | Use Case | Tradeoff |
|------|---------|----------|----------|
| `one-shot` | ~3-5s | Default, balanced accuracy | Best for most queries |
| `fast` | ~1s | Quick lookups, cost-sensitive | Lowest latency, may sacrifice depth (added Feb 2026) |
| `agentic` | ~10-30s | Complex multi-hop research | Highest accuracy, token-efficient, more expensive |

### Source Policy

Control which sources are searched using `source_policy`:

- **Domain include list** - restrict to specific domains
- **Domain exclude list** - block specific domains
- **`after_date` freshness filtering** - only return results published after a given date

### When to use each mode

- **one-shot**: Single-topic factual queries, company lookups, person research, current events
- **fast**: Simple fact checks, quick lookups where 1-second latency matters, cost-sensitive batch jobs
- **agentic**: Questions requiring cross-referencing multiple sources, comparative analysis, claims that need multi-hop verification, complex "why" and "how" questions

### Basic search

```bash
# Default one-shot search
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5

# Fast mode - ~1 second latency (Feb 2026)
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "latest AI news" --mode fast

# Agentic mode - complex multi-hop research, token-efficient
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "compare transformer architectures for long-context tasks" --mode agentic

# Source policy - domain filtering
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "AI regulation" --include-domains "reuters.com,bloomberg.com" --after-date 2026-01-01

# Exclude domains
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "AI safety" --exclude-domains "reddit.com,twitter.com"

# JSON output for programmatic use
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "latest AI news" --json
```

### Example 1: Company research

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Anthropic company overview funding valuation" --max-results 8
```

Sample output:
```
Search ID: search_abc123

**1. [Anthropic raises $2B Series D at $18B valuation](https://example.com/anthropic-funding)**  (2025-12-15)
   Anthropic, the AI safety company founded by former OpenAI researchers Dario and Daniela Amodei, has closed a $2 billion Series D round led by Lightspeed Venture Partners...

**2. [Anthropic - Company Profile](https://www.crunchbase.com/organization/anthropic)**
   Founded: 2021. Headquarters: San Francisco, CA. Total funding: $7.6B. Key products: Claude AI assistant, Claude API. Investors include Google, Spark Capital, Menlo Ventures...

Usage: search_units: 1, result_count: 8
```

### Example 2: Fact-checking with agentic mode

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Is it true that GPT-4 was trained on over 1 trillion parameters? Verify with sources." --mode agentic --max-results 10
```

---

## Extract API

`POST /v1beta/extract`

Extract clean, structured content from any URL. Supports JS-rendered pages and PDF extraction.

### Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `urls[]` | Yes | One or more URLs to extract from |
| `objective` | No | Targeted extraction instruction |
| `mode` | No | `excerpts` (default) or `full_content` |

### Usage

```bash
# Extract with relevant excerpts
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://stripe.com/docs/api

# Full content extraction
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com/paper.pdf --full

# Targeted extraction with an objective
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://sec.gov/10-K.htm --objective "Extract risk factors"

# Multiple URLs at once
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com/page1 https://example.com/page2

# JS-rendered page (React/Vue/Angular SPAs)
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://app.example.com/dashboard --full

# JSON output
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com --json
```

---

## Task API (Deep Research)

`POST /v1/tasks/runs`

For complex questions that benefit from being broken into sub-queries and synthesized. Supports MCP tool calling, authenticated browsing, SSE streaming, and webhooks.

### Processor Tiers

8 tiers from lightweight to maximum depth:

| Processor | Speed | Depth | Cost | Best for |
|-----------|-------|-------|------|----------|
| `lite` | Fastest | Minimal | Lowest | Simple lookups, quick facts |
| `base` | Fast | Shallow | Low | Basic research queries |
| `core` | Medium | Standard | Medium | Most research queries (default) |
| `core2x` | Medium | Enhanced | Medium-High | Detailed analysis |
| `ultra` | Slow | Deep | High | Reports, multi-hop analysis |
| `ultra2x` | Slower | Very deep | Higher | Comprehensive research |
| `ultra4x` | Slow | Extensive | Very high | Exhaustive coverage |
| `ultra8x` | Slowest | Maximum | Highest | Maximum depth research |

### Output Modes

| Mode | Description |
|------|-------------|
| `auto` | Parallel chooses best format (default) |
| `json` | Structured JSON output - supports `json_schema` for custom schemas |
| `text` | Markdown with inline citations |

### Basic usage

```bash
# Generate a comprehensive research report
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --report "Market analysis of the AI code assistant industry in 2025"

# Deep research with specific processor tier
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "What are the key technical differences between Claude, GPT-4, and Gemini?" --processor ultra

# Use the maximum depth tier
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "Comprehensive geopolitical analysis of AI chip export controls" --processor ultra8x

# JSON output with schema
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "List top 5 AI companies" --output-mode json --json-schema '{"companies": [{"name": "string", "valuation": "string"}]}'

# Text output with citations
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "State of quantum computing 2026" --output-mode text
```

### MCP Tool Calling

Connect up to 10 external MCP servers per task. The task processor can invoke tools from connected servers during research.

```bash
# Task with MCP tools
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "Analyze our Stripe revenue data" --mcp-server "stripe-mcp://localhost:3001"
```

### Authenticated Page Access (Jan 2026)

Use a browser agent to access login-protected content. Requires `BROWSERUSE_API_KEY`.

```bash
export BROWSERUSE_API_KEY="your-browseruse-key"

# Access authenticated pages
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "Extract migration docs from https://nxp.com/products/K66_180"
```

**Data flow warning:** When using authenticated sources, your query and BROWSERUSE_API_KEY flow through: Your machine -> Parallel.ai API -> browser-use.com -> target website. Only use this for non-sensitive queries.

### SSE Streaming

Stream real-time progress updates from long-running tasks:

```bash
# Stream task progress
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "Deep market analysis" --processor ultra --stream
```

### Webhooks

Register webhooks for task completion notifications:

- Event: `task_run.status` - fired when a task run changes status (running, completed, failed)

### Enrichment

Enrich structured data with web research:

```bash
# Enrich a company
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --enrich "company_name=Stripe" --output "founding_year,funding,employee_count,ceo"

# Enrich with domain filtering
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --enrich "company_name=Anthropic,website=anthropic.com" --output "valuation,investors,products" --include-domains "crunchbase.com,pitchbook.com"
```

### Source Filtering

Control which sources are used for research:

```bash
# Only search academic sources
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "latest research on chain-of-thought prompting" --include-domains "arxiv.org,scholar.google.com,semanticscholar.org,acm.org"

# Exclude social media and forums
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "AI regulation updates" --exclude-domains "reddit.com,twitter.com,x.com,quora.com"
```

### Example 3: Deep research report

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --report "State of AI safety research in 2025"
```

Sample output:
```
Task: run_xyz789
   Status: completed | Processor: ultra

**Report:**
# State of AI Safety Research in 2025

## Executive Summary
AI safety research has expanded significantly in 2025, with major labs increasing their safety team headcounts by an average of 40%...

**Citations:**
  [safety_research] confidence: high
    - AI Safety Research Landscape 2025: https://example.com/safety-2025
    - Anthropic Constitutional AI v2 Paper: https://arxiv.org/abs/2025.xxxxx
```

---

## Chat API

`POST /v1/chat/completions`

OpenAI-compatible chat endpoint with built-in web grounding. Added January 15, 2026.

### Research Models

| Model | TTFT | Basis Citations | Best for |
|-------|------|-----------------|----------|
| `speed` | ~3s | No | Fast conversational responses without citations |
| `lite` | ~5s | Yes | Quick research with source attribution |
| `base` | ~10s | Yes | Standard research conversations |
| `core` | ~20s | Yes | Deep research with comprehensive citations |

### Features

- **OpenAI-compatible** - drop-in replacement using standard chat completions format
- **Web grounding** - all models (except `speed`) include `basis` citations in responses
- **`response_format`** - supports JSON schema for structured output
- **Streaming** - SSE streaming with `stream: true`

### Usage

```bash
# Chat with web grounding (uses Python SDK)
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py --chat "What happened in AI this week?" --model base

# Structured JSON response
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py --chat "List the top 3 AI companies by valuation" --model core --response-format json

# Fast response without citations
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py --chat "Explain transformers briefly" --model speed
```

### API format

Standard OpenAI chat completions format:
```json
{
  "model": "base",
  "messages": [{"role": "user", "content": "What is Anthropic's latest funding?"}],
  "stream": true,
  "response_format": {"type": "json_schema", "json_schema": {"name": "result", "schema": {...}}}
}
```

Response includes `basis[]` array with source URLs, titles, and confidence scores (except `speed` model).

---

## FindAll API

`POST /v1beta/findall/runs`

Entity discovery at web scale. Turns natural language queries into structured datasets.

### Generators

| Generator | Candidates | Speed | Best for |
|-----------|-----------|-------|----------|
| `preview` | ~10 | Fast | Quick sampling, testing queries |
| `base` | ~50 | Medium | Standard discovery |
| `core` | ~100 | Slow | Thorough discovery |
| `pro` | ~200+ | Slowest | Comprehensive, exhaustive discovery |

### 4-Step Process

1. **Ingest** - submit your natural language query
2. **Create run** - the API generates candidate entities
3. **Poll** - check status until completed
4. **Retrieve** - get matched and enriched entities

### Entity Exclusion (Feb 2026)

Prevent duplicates across runs by passing previously discovered entity IDs:

```bash
# Exclude entities from a previous run
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "AI startups Series A" --exclude-entities "entity_abc,entity_def"
```

### Usage

```bash
# Find matching entities
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "AI startups that raised Series A in the last 6 months"

# With enrichment fields
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "dental practices in Ohio with 4+ star reviews" --enrich "phone,address,rating" --limit 50

# Pro tier for comprehensive discovery
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "portfolio companies of Khosla Ventures" --generator pro

# Preview tier for quick sampling (~10 candidates)
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "cybersecurity startups" --generator preview

# Check status of a long-running job
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py --status findall_abc123

# Don't wait, get the ID and check later
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "SaaS companies in Europe with 50+ employees" --no-wait
```

### Use Cases

- **Lead generation** - find companies matching your ICP
- **Market mapping** - discover all players in a segment
- **Competitive landscape** - enumerate competitors and their attributes

### Example 4: Entity discovery with enrichment

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "AI safety research labs" --enrich "funding,employee_count,founded_year" --limit 10
```

Sample output:
```
FindAll: findall_abc789
   Status: completed
   Candidates: 10 matched / 47 generated

**Matched Entities:**

**1. Anthropic**
   URL: https://www.anthropic.com
   AI safety company building reliable, interpretable AI systems.
   - funding: $7.6B
   - employee_count: ~1500
   - founded_year: 2021

**2. Redwood Research**
   URL: https://www.redwoodresearch.org
   Non-profit AI alignment research lab focused on mechanistic interpretability.
   - funding: $35M (grants)
   - employee_count: ~30
   - founded_year: 2021
```

---

## Monitor API

`POST /v1alpha/monitors`

Scheduled web change tracking. Monitors run at a configured frequency and fire webhooks when events are detected.

### Frequency

Supported intervals: `1h`, `2h`, `4h`, `8h`, `12h`, `1d`, `7d`, `30d`

### Features

- **Webhook notifications** - event: `monitor.event.detected` fires when a monitored condition triggers
- **Event simulation** (Feb 2026) - test your webhook integrations without waiting for real events
- **Structured outputs** (Jan 2026) - use predefined schemas to get structured event data

### Usage

```bash
# Create a daily monitor
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py create "Track AI funding news" --cadence daily

# Hourly monitor with webhook notifications
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py create "Alert when AirPods Pro drop below $150" --cadence hourly --webhook https://hooks.example.com/notify

# Monitor with structured output schema
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py create "Track competitor pricing changes" --cadence 4h --schema '{"competitor": "string", "old_price": "number", "new_price": "number"}'

# Simulate an event for testing (Feb 2026)
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py simulate monitor_abc123

# List all active monitors
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py list

# Get events from a monitor
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py events monitor_abc123 --lookback 10d

# Delete a monitor
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py delete monitor_abc123
```

### Use Cases

- **Competitor tracking** - monitor product launches, pricing changes, hiring
- **Price monitoring** - track price drops for products or services
- **Regulatory changes** - watch for new regulations, policy updates, compliance requirements

---

## Task Group API

`POST /v1beta/tasks/groups`

Batch up to 1,000 task runs in a single POST. Supports dynamic expansion and SSE streaming.

### Features

- **Batch execution** - submit up to 1,000 runs per POST
- **Dynamic expansion** - add more tasks to an active group while it runs
- **SSE event streaming** - real-time completion events for each task in the group

### Usage

```bash
# Create a task group with multiple queries
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --group \
  "Research Anthropic funding history" \
  "Research OpenAI funding history" \
  "Research Google DeepMind funding history"

# Task group with specific processor
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --group --processor core \
  "Market analysis: cloud computing" \
  "Market analysis: edge computing" \
  "Market analysis: quantum computing"

# Stream group completion events
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --group --stream \
  "Company profile: Stripe" \
  "Company profile: Plaid" \
  "Company profile: Adyen"

# Add tasks to an existing group
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --group-add group_abc123 \
  "Company profile: Square" \
  "Company profile: Marqeta"

# Check group status
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --group-status group_abc123
```

---

## Batch Search

Run multiple queries in parallel for comparison research or bulk fact-checking:

```bash
# Run 3 searches in parallel for comparison research
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Claude 3 capabilities" --json > /tmp/claude.json &
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "GPT-4 capabilities" --json > /tmp/gpt4.json &
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Gemini Ultra capabilities" --json > /tmp/gemini.json &
wait
```

For structured batch entity research, use the FindAll API. For batch task execution, use the Task Group API.

---

## Shell Script (parallel.sh)

Lightweight bash wrapper for the Task API. Requires `jq` and `curl`.

```bash
# General research
{baseDir}/scripts/parallel.sh research "What are the latest developments in AI safety?"

# Company research
{baseDir}/scripts/parallel.sh company "Anthropic"

# Person research
{baseDir}/scripts/parallel.sh person "Dario Amodei"

# Check task status
{baseDir}/scripts/parallel.sh status run_abc123
```

---

## Citation Formatting

Results include source URLs and titles. Format citations based on your needs:

### Inline citations (default)
The output format uses markdown links: `**[Title](URL)**` with excerpts below each result.

### Academic style
When writing reports, reformat results as numbered references:
```
[1] Author/Source. "Title." URL. Published: Date.
[2] Author/Source. "Title." URL. Published: Date.
```

### Markdown links
For embedding in documents, extract URL and title:
```
- [Title](URL) - key excerpt
- [Title](URL) - key excerpt
```

Use `--json` output and post-process for custom citation formats.

---

## Response Formats

### Search API response
- `search_id` - unique search identifier
- `results[]` - array of results with:
  - `url` - source URL
  - `title` - page title
  - `excerpts[]` - relevant text excerpts
  - `publish_date` - when available
- `usage` - API usage stats

### Task API response
- `run_id` - unique task identifier
- `status` - completed/failed/running
- `processor` - lite/base/core/core2x/ultra/ultra2x/ultra4x/ultra8x
- `output` - result content (text or JSON)
- `basis[]` - citations with confidence scores

### Chat API response
- Standard OpenAI chat completions format
- `basis[]` - source citations (except `speed` model)

### FindAll API response
- `findall_id` - unique findall run identifier
- `status` - completed/running/failed
- `candidates` - matched count / generated count
- `entities[]` - matched entities with enrichment fields

### Monitor API response
- `monitor_id` - unique monitor identifier
- `status` - active/paused/deleted
- `events[]` - detected events with timestamps

### Task Group API response
- `group_id` - unique group identifier
- `status` - completed/running/partial
- `runs[]` - individual task run results

---

## SDK and CLI Reference

### Python SDK
```bash
pip install parallel-web  # v0.4.2
```

```python
from parallel import Parallel
client = Parallel(api_key="...")
```

### TypeScript SDK
```bash
npm install parallel-web
```

```typescript
import { Parallel } from 'parallel-web';
const client = new Parallel({ apiKey: '...' });
```

### CLI
```bash
brew install parallel-web/tap/parallel-cli
```

### Vercel AI SDK
```bash
npm install @parallel-web/ai-sdk-tools
```

---

## Error Recovery

### Invalid API key
```
Error: PARALLEL_API_KEY environment variable is required
```
Fix: Set `export PARALLEL_API_KEY="your-key"` in your shell profile. Get a key at https://platform.parallel.ai

### Rate limits
The API may return 429 errors during heavy usage. Wait 30-60 seconds and retry, or reduce `--max-results` to lower request weight.

### Empty results
If search returns no results:
1. Broaden your query - remove specific dates or narrow terms
2. Try a different mode - `agentic` mode searches more broadly than `one-shot`
3. Check if the topic is too recent - very new events may not be indexed yet

### Timeout errors
Task API operations (especially `ultra8x` processor and FindAll `pro` generator) can take minutes:
```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "complex query" --timeout 600
```
Or use `--no-wait` to get the run ID and check status later.

### SDK import errors
If `from parallel import Parallel` fails:
```bash
pip install -r {baseDir}/requirements.txt
```

---

## Example 5: Complete research workflow

Combine multiple Parallel APIs for comprehensive research:

```bash
# Step 1: Quick search to scope the topic (fast mode - ~1s)
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "AI code assistants market 2025" --mode fast --max-results 5

# Step 2: Deep research report (ultra processor)
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --report "Comprehensive analysis of the AI code assistant market: key players, market size, growth trends, and competitive dynamics"

# Step 3: Find specific companies in the space (FindAll)
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "AI code assistant companies" --enrich "funding,product_name,pricing" --limit 20

# Step 4: Extract detailed info from key sources (Extract)
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com/ai-code-tools-report --objective "Extract market size estimates and growth projections"

# Step 5: Batch compare top players (Task Groups)
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --group --processor core \
  "Detailed profile: GitHub Copilot" \
  "Detailed profile: Cursor" \
  "Detailed profile: Windsurf"

# Step 6: Set up monitoring for ongoing tracking (Monitor)
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py create "New AI code assistant launches and funding rounds" --cadence daily
```

---

## Follow-Up Questions

After receiving search results, consider asking follow-up queries to deepen understanding:

- "Tell me more about [specific result]" - drill into a particular finding
- "What are the counterarguments to [claim]?" - get opposing viewpoints
- "Find primary sources for [excerpt]" - trace claims to original research
- "How has [topic] changed in the last year?" - temporal analysis
- "Compare [result A] with [result B]" - comparative analysis

---

## When to Use Parallel vs. Other Tools

| Need | Best tool |
|------|-----------|
| High-accuracy research with citations | **Parallel** (this skill) |
| OpenAI-compatible chat with web grounding | **Parallel Chat API** |
| Entity discovery at scale | **Parallel FindAll API** |
| Batch research (up to 1,000 queries) | **Parallel Task Groups** |
| X/Twitter social sentiment and trends | `/search-x` skill |
| Recency-focused research (last 30 days) | `/last30days` skill |
| Quick web page content | Browser/fetch tools |
| Code search | GitHub search, grep |

Parallel excels at research tasks requiring accuracy, citations, and cross-referencing. For social media analysis or very recent events (hours-old), consider combining with other tools.

---

## API Reference

- Docs: https://docs.parallel.ai
- Platform: https://platform.parallel.ai
- Python SDK: `pip install parallel-web` (v0.4.2)
- TypeScript SDK: `npm install parallel-web`
- CLI: `brew install parallel-web/tap/parallel-cli`
- Vercel AI SDK: `npm install @parallel-web/ai-sdk-tools`
