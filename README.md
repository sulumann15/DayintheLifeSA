# Build Your First AI Agent

You just sat through the "Day in the Life of a Solutions Architect" session. This repo is what comes next.

You're going to build an actual AI agent: a program that reasons, picks tools, calls them, reads the results, and keeps going until it has an answer. Not a wrapper around a chat API. The real thing. This same pattern shows up in basically every AI product being shipped right now, and it's also what you'll need for your capstone. The scale will be different. The concepts are the same.

By the end (about 30 minutes), you'll have:
- A working agent loop you can read and explain
- Two tools the model can call and chain together
- A guardrail that keeps the agent in scope
- Code committed to a repo you own

---

## What you're actually building

Most people assume AI is a black box. It isn't. Under every "agent" is a loop:

```
user message
     ↓
  model thinks
     ↓
  "I need to call a tool"  -->  your code runs the tool  -->  result goes back to model
     ↓
  model thinks again
     ↓
  final answer
```

Here's the part that surprises people: the model doesn't run your tools. You do. The model decides *when* to ask for a tool and *what arguments* to pass. Your code intercepts that, runs the actual Python function, and feeds the result back. Once you see that happen once, the whole space of "AI agents" gets a lot less mysterious.

What you're building today:
- `agent.py` — the loop. Sends messages to the model, checks if it wants a tool, runs it, loops back.
- `tools.py` — the tool functions. Plain Python. The model never sees this code, only the description you write for it.

---

## Setup

You need Python 3.10+ and an API key. We're using Grok (xAI) because it's free and takes about 2 minutes to get a key.

**Get your API key first**

Go to [console.x.ai](https://console.x.ai), sign in, and create an API key. Have it ready before you run anything.

No key yet? Set `USE_MOCK=1` in your `.env` and the agent runs with a fake model. You won't get real responses but the loop works and the architecture is the same. Swap in a real key whenever.

**Clone and install**

```bash
git clone https://github.com/omar2000751/DayintheLifeSA.git agent-starter
cd agent-starter

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

**Add your key**

```bash
cp .env.example .env
```

Open `.env` and paste your key into `XAI_API_KEY`. Leave everything else alone.

**Check that it works**

```bash
python agent.py "what should I pack for Boston today?"
```

You should see `-> calling tool: get_weather({'city': 'Boston'})` in the output before the final answer. If that line shows up, the loop is running correctly.

Using OpenAI instead? Set `OPENAI_API_KEY` and change `PROVIDER=openai` in `.env`. The rest of the code doesn't change since Grok uses the same API format.

---

## The exercise

You'll use Claude Code to extend this agent rather than hand-writing everything. That's intentional. The skill here is knowing what to ask for, not grinding out boilerplate. Open Claude Code in this folder (`claude .`) and work through the steps. Each one has a prompt you can paste in directly.

---

### Step 1 -- Understand the loop (8 min)

Before changing anything, make sure you know what's running.

> Paste this into Claude Code:
> *"Open agent.py and walk me through the agent loop line by line. Explain what happens when the model decides to call a tool versus when it gives a final answer. Then run it with 'what should I pack for Boston today?' and show me the tool call in the output."*

Look for `-> calling tool: get_weather({'city': 'Boston'})` before the final answer. That's your code intercepting the model's request, running the Python function, and handing the result back.

---

### Step 2 -- Add a tool that writes (8 min)

Right now the agent can only read (fake weather data). Give it something to write to.

> Paste this into Claude Code:
> *"Add a second tool called save_note(text) that appends a timestamped line to notes.txt. Add it to TOOL_SCHEMAS and TOOL_FUNCTIONS in tools.py. Then ask the agent: 'Check the weather in Boston and save a one-line summary to my notes.' Show me the notes.txt output."*

The agent should call `get_weather` first, then `save_note`. Two tools, chained automatically. You didn't program that order -- the model figured it out.

---

### Step 3 -- Add guardrails (7 min)

An agent without guardrails will eventually do something you didn't want. There are two types, and where they live matters.

> Paste this into Claude Code:
> *"Add two guardrails: (1) the agent should politely refuse any request that isn't about weather or notes -- put this in the system prompt, (2) save_note should hard-reject any text longer than 500 characters with an error -- put this in the Python function. After implementing both, explain in a comment why each guardrail lives where it does."*

Behavioral rules ("stay on topic") belong in the prompt because they're soft and contextual. Hard limits ("never write more than 500 chars") belong in code because the model shouldn't be able to reason its way around them.

---

### Step 4 -- Ship it (5 min)

> Paste this into Claude Code:
> *"Fill in the 'What I built' section of the README with 3-4 sentences describing this agent -- what it does, what tools it has, and what guardrails protect it. Then commit everything to git with a clear message."*

---

## Stretch goals

If you finish early, pick one:

- **Real weather data.** Replace the hardcoded `get_weather` with a call to [wttr.in](https://wttr.in) (no key needed: `curl wttr.in/Boston?format=3`).
- **MCP server.** Run `claude mcp add fetch -- uvx mcp-server-fetch` and ask the agent to read a webpage. You just added a tool you didn't write.
- **Your own tool.** Dice roller, unit converter, file reader. Add the schema and the function and ask the agent to use it.
- **Claude Code skill.** The `.claude/skills/` folder is set up. Flesh out the research-agent skill so it runs as a slash command.

---

## What I built

_(Fill this in at Step 4.)_

---

## Files

```
agent-starter/
├── agent.py             <- the loop: messages, tool calls, looping back
├── tools.py             <- tool functions + schemas (what the model sees)
├── requirements.txt     <- openai SDK + dotenv
├── .env.example         <- copy to .env, add your key
└── .claude/
    └── skills/
        └── research-agent/   <- stretch goal starter
```
