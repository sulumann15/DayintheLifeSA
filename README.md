# Agent Starter — Build Your First AI Agent in 30 Minutes

A follow-along repo for the **"Day in the Life of a Solutions Architect"** session.
You'll use **Claude Code** to build a small but real AI **agent**: an LLM in a loop
that decides when to call tools, calls them, reads the results, and answers.

By the end you'll have:
- a working agent loop (the thing under every "AI agent")
- two real tools the model can call
- a guardrail that keeps the agent in its lane
- a committed git repo you can show off

This is a miniature of the agent you'll build for your capstone. Same muscles.

---

## The big idea (read this once, 60 seconds)

An **agent** is not magic. It's a loop:

```
observe  ->  think  ->  act  ->  check   (repeat until done)
```

1. You give the model a list of **tools** (functions you wrote, each with a name + description).
2. The model replies either with a final answer OR "call tool X with these arguments."
3. Your code runs the tool, hands the result back to the model.
4. Repeat until the model answers or you hit a step cap.

That's it. The rest is detail. You'll build exactly this.

---

## Setup (do this first — 5 minutes)

You need **Python 3.10+** and a **Grok (xAI) API key** — it's free. Grab one at
https://console.x.ai (sign in, create an API key). Grok is OpenAI-compatible, so
this same code works with OpenAI too if you'd rather.

```bash
# 1. clone your fork
git clone <your-fork-url> agent-starter
cd agent-starter

# 2. make a virtualenv
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 3. install deps
pip install -r requirements.txt

# 4. set your key
cp .env.example .env
# then edit .env: paste your key into XAI_API_KEY
```

Provider options in `.env`:
- **Grok / xAI (default):** set `XAI_API_KEY` (free at console.x.ai)
- **OpenAI:** set `OPENAI_API_KEY` and `PROVIDER=openai`

No key handy? You can still build and run the whole thing in **mock mode**
(`USE_MOCK=1` in `.env`) — the agent runs with a fake model so the architecture
lesson works even offline.

---

## The exercise — let Claude Code do the building

You will mostly **prompt Claude Code**, not hand-type code. That's the point:
you're directing an agent to build an agent.

Open Claude Code in this folder and work through the steps. Each step has a
copy-paste prompt. The finished reference code is in `agent.py` if you get stuck.

### Step 1 — Make the loop real (8 min)
> Prompt Claude Code:
> "Open agent.py. It has a tool-calling loop with one fake tool, get_weather.
> Walk me through how the loop works line by line, then run it with the
> question 'what should I pack for Boston today?' and show me the tool call."

You're looking for: the model decides to call `get_weather`, you see the result
go back in, then a final answer. That's the agent loop.

### Step 2 — Add a real tool (8 min)
> Prompt Claude Code:
> "Add a second tool called save_note(text) that appends a line to notes.txt.
> Then ask the agent to look up the weather and save a one-line summary to my notes."

Now the agent **chains two tools**: read something, then write something.

### Step 3 — Add a guardrail (7 min)
> Prompt Claude Code:
> "Add two guardrails: the agent should politely refuse anything not about
> weather or notes, and save_note must reject text longer than 500 characters.
> Tell me which guardrail you put in the prompt and which you put in code, and why."

This is the real lesson: some rules live in the prompt, hard limits live in code.

### Step 4 — Ship it (5 min)
> Prompt Claude Code:
> "Update the README's 'What I built' section to describe my agent, then commit
> everything to git with a sensible message."

Done. You built and shipped an agent.

---

## Stretch goals (if you finish early)

- **Add an MCP server** so your agent gets a tool you didn't have to write:
  `claude mcp add fetch -- uvx mcp-server-fetch` then ask the agent to read a web page.
- **Package it as a Claude Code skill** in `.claude/skills/` so the behavior is reusable.
- **Write your own tool**: pick anything (dice roller, stock price, unit converter)
  and have the agent call it.

---

## What I built

_(You'll fill this in at Step 4.)_

---

## How the files fit together

```
agent-starter/
├── README.md            <- this guide
├── requirements.txt     <- dependencies
├── .env.example         <- copy to .env, add your key
├── agent.py             <- the agent loop + tools (you extend this)
├── tools.py             <- tool functions live here
└── .claude/
    └── skills/          <- (stretch) package your agent as a skill
```
