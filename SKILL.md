---
name: parallel
version: "1.1.0"
description: High-accuracy web search and research via Parallel.ai API. Optimized for AI agents with rich excerpts and citations. Supports agentic mode for token-efficient multi-step reasoning.
author: mvanhorn
license: MIT
repository: https://github.com/mvanhorn/clawdbot-skill-parallel
homepage: https://parallel.ai
triggers:
  - parallel
  - deep search
  - research
metadata:
  openclaw:
    emoji: "🔬"
    requires:
      env:
        - PARALLEL_API_KEY
    primaryEnv: PARALLEL_API_KEY
    tags:
      - search
      - research
      - web
      - parallel
      - citations
---

# Parallel.ai 🔬

High-accuracy web search API built for AI agents. Outperforms Perplexity/Exa on research benchmarks.

## Setup

```bash
pip install parallel-web
```

API key is configured. Uses Python SDK.

```python
from parallel import Parallel
client = Parallel(api_key="YOUR_KEY")
response = client.beta.search(
    mode="one-shot",  # or "fast" for lower latency/cost, "agentic" for multi-hop
    max_results=10,
    objective="your query"
)
```

## Modes

| Mode | Use Case | Tradeoff |
|------|----------|----------|
| `one-shot` | Default, balanced accuracy | Best for most queries |
| `fast` ⚡ | Quick lookups, cost-sensitive | Lower latency/cost, may sacrifice some accuracy |
| `agentic` | Complex multi-hop research | Higher accuracy, more expensive |

## Quick Usage

```bash
# Default search (one-shot mode)
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "Who is the CEO of Anthropic?" --max-results 5

# Fast mode - lower latency/cost ⚡
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "latest AI news" --mode fast

# Agentic mode - complex research
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "compare transformer architectures" --mode agentic

# JSON output
{baseDir}/.venv/bin/python {baseDir}/scripts/search.py "latest AI news" --json
```

## Response Format

Returns structured results with:
- `search_id` - unique search identifier
- `results[]` - array of results with:
  - `url` - source URL
  - `title` - page title
  - `excerpts[]` - relevant text excerpts
  - `publish_date` - when available
- `usage` - API usage stats

## When to Use

- **Deep research** requiring cross-referenced facts
- **Company/person research** with citations
- **Fact-checking** with evidence-based outputs
- **Complex queries** that need multi-hop reasoning
- Higher accuracy than traditional search for research tasks

## API Reference

Docs: https://docs.parallel.ai
Platform: https://platform.parallel.ai
