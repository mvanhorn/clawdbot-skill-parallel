---
name: parallel
version: "2.0.0"
description: High-accuracy web search and deep research via Parallel.ai API. Outperforms Perplexity and Exa on benchmarks. Rich excerpts, citations, source filtering, batch search, agentic mode, content extraction, entity discovery, and continuous monitoring. OpenClaw skill.
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
---

# Parallel.ai - High-Accuracy Web Research

Deep web research API built for AI agents. Outperforms Perplexity and Exa on research benchmarks with rich excerpts, citations, and source provenance.

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

The primary search interface. Use for most research queries.

### Modes

| Mode | Use Case | Tradeoff |
|------|----------|----------|
| `one-shot` | Default, balanced accuracy | Best for most queries |
| `fast` | Quick lookups, cost-sensitive | Lower latency/cost, may sacrifice some depth |
| `agentic` | Complex multi-hop research | Highest accuracy, uses more tokens, more expensive |

### When to use each mode

- **one-shot**: Single-topic factual queries, company lookups, person research, current events
- **fast**: Simple fact checks, quick lookups where speed matters more than depth, cost-sensitive batch jobs
- **agentic**: Questions requiring cross-referencing multiple sources, comparative analysis, claims that need multi-hop verification, complex "why" and "how" questions

### Basic search

```bash
# Default one-shot search
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5

# Fast mode - lower latency/cost
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "latest AI news" --mode fast

# Agentic mode - complex multi-hop research
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "compare transformer architectures for long-context tasks" --mode agentic

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

**3. [Anthropic's Claude 3.5 Sonnet tops benchmarks](https://example.com/claude-benchmarks)**  (2025-11-20)
   The latest Claude model achieves state-of-the-art results on MMLU, HumanEval, and GPQA benchmarks while maintaining strong safety properties...

Usage: search_units: 1, result_count: 8
```

### Example 2: Fact-checking with agentic mode

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Is it true that GPT-4 was trained on over 1 trillion parameters? Verify with sources." --mode agentic --max-results 10
```

Sample output:
```
Search ID: search_def456

**1. [GPT-4 Technical Report - OpenAI](https://cdn.openai.com/papers/gpt-4.pdf)**
   OpenAI has not publicly disclosed the parameter count for GPT-4. The technical report focuses on capabilities and safety evaluations rather than architecture details...

**2. [GPT-4 architecture speculation vs. confirmed details](https://example.com/gpt4-details)**  (2025-08-12)
   While widely reported as a mixture-of-experts model with approximately 1.8 trillion parameters across 8 expert models, OpenAI has never officially confirmed these numbers...

**3. [OpenAI CEO Sam Altman on GPT-4](https://example.com/altman-interview)**  (2025-03-15)
   "People are begging to be disappointed and they will be." Altman declined to confirm parameter count, calling it "not the most important metric"...

Usage: search_units: 3, result_count: 10
```

---

## Deep Research Mode

For complex questions that benefit from being broken into sub-queries and synthesized. Use the Task API with the `ultra` processor.

```bash
# Generate a comprehensive research report
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --report "Market analysis of the AI code assistant industry in 2025"

# Deep research with specific processor tier
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "What are the key technical differences between Claude, GPT-4, and Gemini?" --processor ultra
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
AI safety research has expanded significantly in 2025, with major labs increasing their safety team headcounts by an average of 40%. Key developments include Constitutional AI improvements at Anthropic, red-teaming frameworks from NIST, and the EU AI Act entering enforcement.

## Key Findings

### 1. Constitutional AI and RLHF Advances
Anthropic's Constitutional AI v2 introduced chain-of-thought safety reasoning, reducing harmful outputs by 73% compared to baseline RLHF...

### 2. Regulatory Landscape
The EU AI Act began enforcement in August 2025, requiring risk assessments for foundation models exceeding 10^25 FLOPs in training compute...

### 3. Interpretability Breakthroughs
Research from Anthropic, DeepMind, and academic labs has made progress on mechanistic interpretability, identifying specific circuits responsible for factual recall...

[2847 chars total]

**Citations:**
  [safety_research] confidence: high
    - AI Safety Research Landscape 2025: https://example.com/safety-2025
    - Anthropic Constitutional AI v2 Paper: https://arxiv.org/abs/2025.xxxxx
```

### Processor tiers

| Processor | Speed | Depth | Cost | Best for |
|-----------|-------|-------|------|----------|
| `base` | Fast | Shallow | Low | Simple lookups, quick facts |
| `core` | Medium | Standard | Medium | Most research queries (default) |
| `ultra` | Slow | Deep | High | Reports, multi-hop analysis, comprehensive research |

---

## Batch Search

Run multiple queries in parallel for comparison research or bulk fact-checking. Execute multiple search.py calls concurrently:

```bash
# Run 3 searches in parallel for comparison research
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Claude 3 capabilities" --json > /tmp/claude.json &
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "GPT-4 capabilities" --json > /tmp/gpt4.json &
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Gemini Ultra capabilities" --json > /tmp/gemini.json &
wait
```

For structured batch entity research, use the FindAll API instead (see below).

---

## Content Extraction

Extract clean, structured content from any URL. Useful for pulling specific information from pages, PDFs, or documents.

```bash
# Extract with relevant excerpts
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://stripe.com/docs/api

# Full content extraction
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com/paper.pdf --full

# Targeted extraction with an objective
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://sec.gov/10-K.htm --objective "Extract risk factors"

# Multiple URLs at once
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com/page1 https://example.com/page2

# JSON output
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com --json
```

---

## FindAll - Entity Discovery

Turn natural language queries into structured datasets. Finds and enriches entities matching your criteria.

```bash
# Find matching entities
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "AI startups that raised Series A in the last 6 months"

# With enrichment fields
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "dental practices in Ohio with 4+ star reviews" --enrich "phone,address,rating" --limit 50

# Pro tier for comprehensive discovery
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "portfolio companies of Khosla Ventures" --generator pro

# Check status of a long-running job
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py --status findall_abc123

# Don't wait, get the ID and check later
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "SaaS companies in Europe with 50+ employees" --no-wait
```

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
   AI safety company building reliable, interpretable AI systems. Founded by former OpenAI researchers.
   - funding: $7.6B
   - employee_count: ~1500
   - founded_year: 2021

**2. Redwood Research**
   URL: https://www.redwoodresearch.org
   Non-profit AI alignment research lab focused on mechanistic interpretability and adversarial robustness.
   - funding: $35M (grants)
   - employee_count: ~30
   - founded_year: 2021

**3. ARC (Alignment Research Center)**
   URL: https://alignment.org
   Non-profit researching AI alignment with focus on eliciting latent knowledge and model evaluations.
   - funding: $12M (grants)
   - employee_count: ~20
   - founded_year: 2021
```

---

## Monitoring - Continuous Web Tracking

Set up persistent monitors that track topics and alert you when new information appears.

```bash
# Create a daily monitor
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py create "Track AI funding news" --cadence daily

# Hourly monitor with webhook notifications
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py create "Alert when AirPods Pro drop below $150" --cadence hourly --webhook https://hooks.example.com/notify

# List all active monitors
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py list

# Get events from a monitor
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py events monitor_abc123 --lookback 10d

# Delete a monitor
{baseDir}/.venv/bin/python {baseDir}/scripts/monitor.py delete monitor_abc123
```

---

## Task API - Enrichment

Enrich structured data with web research. Provide input fields and specify what output fields you want.

```bash
# Enrich a company
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --enrich "company_name=Stripe" --output "founding_year,funding,employee_count,ceo"

# Enrich with domain filtering
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --enrich "company_name=Anthropic,website=anthropic.com" --output "valuation,investors,products" --include-domains "crunchbase.com,pitchbook.com"
```

---

## Source Filtering

Control which sources are used for research.

```bash
# Only search academic sources
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "latest research on chain-of-thought prompting" --include-domains "arxiv.org,scholar.google.com,semanticscholar.org,acm.org"

# Exclude social media and forums
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "AI regulation updates" --exclude-domains "reddit.com,twitter.com,x.com,quora.com"

# Focus on news sources only
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "OpenAI latest announcements" --include-domains "reuters.com,bloomberg.com,techcrunch.com,theverge.com,arstechnica.com"
```

---

## Authenticated Sources

Access pages behind login walls using browser-use.com integration. This sends your BROWSERUSE_API_KEY to Parallel.ai, which proxies it to browser-use.com. Both services see your queries and the browsing session data.

```bash
# Set up browser-use key
export BROWSERUSE_API_KEY="your-browseruse-key"

# Extract from authenticated pages
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "Extract migration docs from https://nxp.com/products/K66_180"

# Or pass the key directly
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py "Get pricing details from https://example.com/pricing" --browseruse-key "your-key"
```

**Data flow warning:** When using authenticated sources, your query and BROWSERUSE_API_KEY flow through: Your machine -> Parallel.ai API -> browser-use.com -> target website. Research results flow back through the same chain. Only use this for non-sensitive queries.

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

## Response Format

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
- `processor` - base/core/ultra
- `output` - result content (text or JSON)
- `basis[]` - citations with confidence scores

---

## Error Recovery

### Invalid API key
```
Error: PARALLEL_API_KEY environment variable is required
```
Fix: Set `export PARALLEL_API_KEY="your-key"` in your shell profile. Get a key at https://platform.parallel.ai

### Rate limits
The API may return 429 errors during heavy usage. The scripts will fail with an API error. Wait 30-60 seconds and retry, or reduce `--max-results` to lower request weight.

### Empty results
If search returns no results:
1. Broaden your query - remove specific dates or narrow terms
2. Try a different mode - `agentic` mode searches more broadly than `one-shot`
3. Check if the topic is too recent - very new events may not be indexed yet

### Timeout errors
Task API operations (especially `ultra` processor and FindAll) can take minutes. Increase timeout:
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

Combine multiple Parallel tools for comprehensive research:

```bash
# Step 1: Quick search to scope the topic
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "AI code assistants market 2025" --mode fast --max-results 5

# Step 2: Deep research report
{baseDir}/.venv/bin/python {baseDir}/scripts/task.py --report "Comprehensive analysis of the AI code assistant market: key players, market size, growth trends, and competitive dynamics"

# Step 3: Find specific companies in the space
{baseDir}/.venv/bin/python {baseDir}/scripts/findall.py "AI code assistant companies" --enrich "funding,product_name,pricing" --limit 20

# Step 4: Extract detailed info from key sources
{baseDir}/.venv/bin/python {baseDir}/scripts/extract.py https://example.com/ai-code-tools-report --objective "Extract market size estimates and growth projections"

# Step 5: Set up monitoring for ongoing tracking
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
| X/Twitter social sentiment and trends | `/search-x` skill |
| Recency-focused research (last 30 days) | `/last30days` skill |
| Quick web page content | Browser/fetch tools |
| Code search | GitHub search, grep |

Parallel excels at research tasks requiring accuracy, citations, and cross-referencing. For social media analysis or very recent events (hours-old), consider combining with other tools.

---

## API Reference

- Docs: https://docs.parallel.ai
- Platform: https://platform.parallel.ai
- SDK: `pip install parallel-web`
