[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/mvanhorn-clawdbot-skill-parallel-badge.png)](https://mseep.ai/app/mvanhorn-clawdbot-skill-parallel)

# Parallel Skill for OpenClaw

High-accuracy web research platform via [Parallel.ai](https://parallel.ai), built for AI agents. 7 APIs covering search, extraction, deep research, chat, entity discovery, monitoring, and batch execution.

## What it does

- **Search** - high-accuracy web search with 3 modes: one-shot, fast (~1s), agentic (multi-hop)
- **Extract** - pull clean content from URLs, JS-rendered pages, and PDFs
- **Task (Deep Research)** - 8 processor tiers (lite through ultra8x), MCP tool calling, authenticated browsing
- **Chat** - OpenAI-compatible chat completions with web grounding and basis citations
- **FindAll** - entity discovery at web scale with 4 generator tiers (preview, base, core, pro)
- **Monitor** - scheduled web change tracking with webhook notifications
- **Task Groups** - batch up to 1,000 research tasks per POST with SSE streaming

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
- "Find all AI startups that raised Series A in the last 6 months"
- "Monitor AI safety news daily and alert me"
- "Chat with web grounding about recent funding rounds"
- "Batch research the top 10 cloud providers"

## APIs

| API | Endpoint | Description |
|-----|----------|-------------|
| Search | `POST /v1/search` | Web search with one-shot, fast, agentic modes |
| Extract | `POST /v1beta/extract` | Content extraction from URLs and PDFs |
| Task | `POST /v1/tasks/runs` | Deep research with 8 processor tiers |
| Chat | `POST /v1/chat/completions` | OpenAI-compatible with web grounding |
| FindAll | `POST /v1beta/findall/runs` | Entity discovery at scale |
| Monitor | `POST /v1alpha/monitors` | Scheduled web change tracking |
| Task Groups | `POST /v1beta/tasks/groups` | Batch up to 1,000 tasks |

## SDK and CLI

- **Python:** `pip install parallel-web` (v0.4.2)
- **TypeScript:** `npm install parallel-web`
- **CLI:** `brew install parallel-web/tap/parallel-cli`
- **Vercel AI SDK:** `npm install @parallel-web/ai-sdk-tools`

## Security

- API key is loaded from the `PARALLEL_API_KEY` environment variable only - never hardcoded
- All user input is safely escaped before being sent to the API (no JSON injection)
- Dependencies are pinned in `requirements.txt`
- When using authenticated sources (BROWSERUSE_API_KEY), be aware that your key is transmitted to Parallel.ai's servers which proxy it to browser-use.com

## Links

- Docs: https://docs.parallel.ai
- Platform: https://platform.parallel.ai

## License

MIT
