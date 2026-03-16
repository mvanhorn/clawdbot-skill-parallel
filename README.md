# Parallel Skill for OpenClaw

High-accuracy web search via [Parallel.ai](https://parallel.ai), built for AI agents. Outperforms Perplexity and Exa on research benchmarks.

## What it does

- **Deep research** - cross-referenced facts with citations and excerpts
- **Multiple search modes** - one-shot (balanced), fast (quick lookups), agentic (multi-hop reasoning)
- **Rich results** - URLs, titles, relevant excerpts, publish dates
- **Batch search** - run multiple queries in parallel for comparison research
- **Deep research mode** - break complex questions into sub-queries, synthesize findings
- **Source filtering** - include/exclude specific domains, focus on academic or news sources
- **Content extraction** - pull clean text from any URL with targeted objectives
- **FindAll** - natural language to structured datasets (e.g., "AI startups that raised Series A")
- **Monitoring** - continuous web tracking with webhook alerts

## Quick start

### Install the skill

```bash
git clone https://github.com/mvanhorn/clawdbot-skill-parallel.git ~/.openclaw/skills/parallel
cd ~/.openclaw/skills/parallel
pip install -r requirements.txt
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
- "Find all AI startups that raised Series A in the last 6 months"
- "Monitor AI safety news daily and alert me"

## Search modes

| Mode | Use case | Tradeoff |
|------|----------|----------|
| `one-shot` | Default, most queries | Balanced accuracy and speed |
| `fast` | Quick lookups, cost-sensitive | Lower latency, may sacrifice depth |
| `agentic` | Complex multi-hop research | Higher accuracy, more expensive |

## Security

- API key is loaded from the `PARALLEL_API_KEY` environment variable only - never hardcoded
- All user input is safely escaped before being sent to the API (no JSON injection)
- Dependencies are pinned in `requirements.txt`
- When using authenticated sources (BROWSERUSE_API_KEY), be aware that your key is transmitted to Parallel.ai's servers which proxy it to browser-use.com

## How it works

Uses the Parallel Python SDK (`parallel-web`). The skill provides scripts for search, task-based research, content extraction, entity discovery (FindAll), and continuous monitoring. Results include URLs, titles, excerpts, publish dates, and usage stats for cost tracking.

- Docs: https://docs.parallel.ai
- Platform: https://platform.parallel.ai

## License

MIT
