# 🔬 Parallel Skill for OpenClaw

High-accuracy web search via [Parallel.ai](https://parallel.ai), built for AI agents. Outperforms Perplexity and Exa on research benchmarks.

## What it does

- **Deep research** - cross-referenced facts with citations and excerpts
- **Multiple search modes** - one-shot (balanced), fast (quick lookups), agentic (multi-hop reasoning)
- **Rich results** - URLs, titles, relevant excerpts, publish dates
- **Company/person research** - evidence-based outputs with source links

## Quick start

### Install the skill

```bash
git clone https://github.com/mvanhorn/clawdbot-skill-parallel.git ~/.openclaw/skills/parallel
```

### Set up your API key

Get a key from [Parallel.ai](https://platform.parallel.ai), then:

```bash
export PARALLEL_API_KEY="your-key-here"
```

### Example chat usage

- "Use Parallel to research transformer architectures"
- "Deep search for the latest on AI regulation in the EU"
- "Research who's behind Anthropic - founders, funding, board"
- "Fact-check this claim about GPT-5 with sources"

## Search modes

| Mode | Use case | Tradeoff |
|------|----------|----------|
| `one-shot` | Default, most queries | Balanced accuracy and speed |
| `fast` | Quick lookups, cost-sensitive | Lower latency, may sacrifice depth |
| `agentic` | Complex multi-hop research | Higher accuracy, more expensive |

## How it works

Uses the Parallel Python SDK (`parallel-web`). The skill runs a search script that returns structured results with URLs, titles, excerpts, and publish dates. Results include usage stats for cost tracking.

- Docs: https://docs.parallel.ai
- Platform: https://platform.parallel.ai

## License

MIT
