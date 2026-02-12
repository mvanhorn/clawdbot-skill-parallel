# Parallel.ai Search 🔬

High-accuracy web search API built for AI agents. Outperforms Perplexity/Exa on research benchmarks.

## Features

- **Three search modes** for different use cases:
  - `one-shot` — Default, balanced accuracy
  - `fast` ⚡ — Lower latency/cost for quick lookups
  - `agentic` — Multi-hop reasoning for complex research
- Rich excerpts with citations
- Optimized for LLM context efficiency

## Installation

```bash
# Install via ClawHub
clawhub install parallel
```

## Usage

```bash
# Default search
python3 scripts/search.py "Who founded OpenAI?" --max-results 5

# Fast mode (new!) ⚡
python3 scripts/search.py "latest AI news" --mode fast

# Agentic mode for deep research
python3 scripts/search.py "compare transformer architectures" --mode agentic
```

## API Reference

- Docs: https://docs.parallel.ai
- Platform: https://platform.parallel.ai

## Changelog

### 1.1.0 (2026-02-12)
- Added **fast mode** (`--mode fast`) for lower latency/cost searches
- Added mode comparison table to docs

### 1.0.1
- Initial release with one-shot and agentic modes
