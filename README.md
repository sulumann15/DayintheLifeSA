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
     |
  model thinks
     |
  "I need to call a tool"  -->  your code runs the tool  -->  result goes back to model
     |
  model thinks again
     |
  final answer
```

Here's the part that surprises people: the model doesn't run your tools. You do. The model decides *when* to ask for a tool and *what arguments* to pass. Your code intercepts that, runs the actual Python function, and feeds the result back. Once you see that happen once, the whole space of "AI agents" gets a lot less mysterious.

What you're building today:
- `agent.py` -- the loop. Sends messages to the model, checks if it wants a tool, runs it, loops back.
- `tools.py` -- the tool functions. Plain Python. The model never sees this code, only the description you write for it.

---

## Before you start: install Claude Code

If you haven't already, install Claude Code and log in:

```bash
npm install -g @anthropic-ai/claude-code
claude login
```

That's what you'll use to build the agent. All the exercise prompts are designed for Claude Code, not a terminal.

---

## Setup

You need Python 3.10+ and an API key. We're using Grok (xAI) because it's free and takes about 2 minutes to get a key.

**Step 1: Get your API key**

Go to [console.x.ai](https://console.x.ai) and sign in. In the left sidebar, click "API Keys", then "Create API Key". Copy the key that appears -- you won't be able to see it again after you close that modal.

No key right now? That's fine. You can use mock mode (explained below) and swap in a real key later.

**Step 2: Clone and install**

```bash
git clone https://github.com/omar2000751/DayintheLifeSA.git agent-starter
cd agent-starter

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

You should see `Successfully installed openai` and `python-dotenv` at the end. If you see errors instead, make sure you're running Python 3.10 or higher: `python --version`.

**Step 3: Add your key**

```bash
cp .env.example .env
```

Open `.env` in any editor (VS Code: `code .env`, nano: `nano .env`) and paste your API key on the `XAI_API_KEY=` line. Save the file.

If you're using mock mode instead, open `.env` and change `USE_MOCK=0` to `USE_MOCK=1`. You'll get fake responses but the agent loop still runs.

**Step 4: Open Claude Code and verify**

```bash
claude .
```

Once Claude Code opens, paste this in:

> *"Look at agent.py and tell me what it does, then test that my setup is working by asking the agent what I should pack for Boston today. Show me the full output including any tool calls."*

You're looking for a line that says `-> calling tool: get_weather(...)` before the final answer. If you see that, the loop is working and you're ready for the exercise.

Using OpenAI instead of Grok? Set `OPENAI_API_KEY` and change `PROVIDER=openai` in `.env`. The code is identical either way.

---

## The exercise

You'll use Claude Code to extend this agent rather than write everything from scratch. That's intentional -- the skill here is knowing what to ask for, not grinding out boilerplate. Each step below has a prompt you can paste directly into Claude Code.

---

### Step 1 -- Understand the loop (8 min)

Before you change anything, make sure you understand what's running.

> Paste into Claude Code:
> *"Walk me through how the agent loop in agent.py works, step by step. What happens when the model wants to call a tool? What happens when it's ready to give a final answer? Then run the agent with a test question and point out exactly where in the output the tool call happens."*

Look for `-> calling tool: get_weather({'city': 'Boston'})` before the final answer. That line is printed by your code, at the moment it intercepts the model's tool request and runs the Python function. That's the loop in action.

---

### Step 2 -- Add a tool that writes (8 min)

Right now the agent can only read (fake weather data). Give it something to write to.

> Paste into Claude Code:
> *"Add a second tool called save_note that takes a text argument and appends a timestamped line to notes.txt. Wire it up so the agent knows about it. Then ask the agent to check the weather in Boston and save a one-line summary to my notes. Show me what ends up in notes.txt."*

The agent should call `get_weather` first, then `save_note`. Two tools, chained in the right order automatically. You didn't program that order -- the model figured it out from the descriptions you gave each tool.

---

### Step 3 -- Add guardrails (7 min)

An agent without guardrails will eventually do something you didn't want. There are two types, and they live in different places for a reason.

> Paste into Claude Code:
> *"Add two guardrails: first, update the system prompt so the agent politely refuses any request that isn't about weather or notes. Second, make save_note reject any text longer than 500 characters with an error message. After both are done, explain to me why one lives in the prompt and the other lives in code."*

Behavioral rules like "stay on topic" belong in the prompt because they're soft and contextual -- the model can apply judgment. Hard limits like "never store more than 500 chars" belong in code because the model shouldn't be able to reason its way around them.

---

### Step 4 -- Ship it (5 min)

First, make sure git knows who you are (skip this if you've used git on this machine before):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Then paste into Claude Code:

> *"Fill in the 'What I built' section of the README with 3-4 sentences: what this agent does, what tools it has, and what guardrails are in place. Then stage all the changed files and commit with a descriptive message."*

---

## Stretch goals

Done early? Pick one:

- **Real weather data.** Replace the hardcoded `get_weather` with a live call to [wttr.in](https://wttr.in) -- no key needed (`curl wttr.in/Boston?format=3` to see the format).
- **MCP server.** Run `claude mcp add fetch -- uvx mcp-server-fetch` and ask the agent to read a webpage. You just gave it a tool you didn't write.
- **Your own tool.** Dice roller, unit converter, file reader -- anything. Add the function and tell the agent what it does. Ask it to use it.
- **Claude Code skill.** The `.claude/skills/` folder is set up. Flesh out the research-agent skill so it runs as a slash command.

---

## What I built

_(Fill this in at Step 4.)_

---

## Files

```
agent-starter/
├── agent.py             -- the loop: messages, tool calls, looping back
├── tools.py             -- tool functions + schemas (what the model sees)
├── requirements.txt     -- openai SDK + dotenv
├── .env.example         -- copy to .env, add your key
└── .claude/
    └── skills/
        └── research-agent/   -- stretch goal starter
```
