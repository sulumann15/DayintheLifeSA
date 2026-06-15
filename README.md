# Build Your First AI Agent

You just sat through the "Day in the Life of a Solutions Architect" session. This repo is what comes next.

You're going to build an actual AI agent: a program that reasons, picks tools, calls them, reads the results, and keeps going until it has an answer. Not a wrapper around a chat API. The real thing. This same pattern shows up in basically every AI product being shipped right now, and it's what you'll need for your capstone.

One rule for this exercise: if you can't explain what you just built to someone who wasn't in the room, you haven't finished the step. That's the Feynman bar -- and it's the bar that matters on a real team.

---

## The mental model (read before you touch anything)

Under every "agent" is a loop:

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

**The model doesn't run your tools. You do.** The model decides *when* to ask for a tool and *what arguments* to pass. Your code intercepts that, runs the Python function, and feeds the result back.

This loop is built on a concept Anthropic calls **context engineering**: the model can only work with what's in its context window at any given moment -- the system prompt, the conversation history, tool results, everything. Every decision the agent makes is based entirely on what you've put in that window. You are the curator. Good agents are built by people who think carefully about what information the model needs, when it needs it, and what to leave out.

Two files make this work today:
- `agent.py` -- the loop itself
- `tools.py` -- the tool functions (plain Python) and their schemas (what the model reads to decide when to use them)

---

## Setup

**Install Claude Code** (if you haven't already):

```bash
npm install -g @anthropic-ai/claude-code
claude login
```

**Get a Grok API key**

Go to [console.x.ai](https://console.x.ai), sign in, click "API Keys" in the left sidebar, then "Create API Key". Copy it immediately -- it won't be shown again after you close that modal.

No key yet? Add `USE_MOCK=1` to your `.env` after cloning. The agent runs with a fake model. The loop still works and the concepts are identical.

**Clone and install**

```bash
git clone https://github.com/omar2000751/DayintheLifeSA.git agent-starter
cd agent-starter

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

Look for `Successfully installed openai` and `python-dotenv` at the end. If you see errors: `python --version` should say 3.10 or higher.

**Add your key**

```bash
cp .env.example .env
```

Open `.env` (VS Code: `code .env`, nano: `nano .env`) and paste your key into `XAI_API_KEY=`. Save.

**Open Claude Code**

```bash
claude .
```

You'll use Claude Code for the entire exercise.

---

## Step 1 -- Understand the loop (8 min)

### Read first

Open `agent.py` and read `run_agent` before running anything. Find the line that checks `if not msg.tool_calls`. That's the fork: one path ends the loop, the other continues it.

Then open `tools.py`. `get_weather` returns a hardcoded string -- "68F and sunny" regardless of city or season. The model has no idea.

**Quick question before you run:** when the model gets that fake result back, will it know it's fake? Why or why not?

### Build

Ask Claude Code:

> *"Read agent.py and explain how the agent loop works -- what happens when the model wants a tool vs. when it has a final answer. Then test it with a weather question for Boston and show me the full output."*

### The concept

Look at what's in `messages` by the time the loop finishes. It started with a system prompt and a user message. Now it also has the tool call, the tool result, and the final answer -- all stacked up chronologically. That accumulating list *is* the context window. The model doesn't have memory between turns; it just has that list. Every response is generated from scratch based on everything in it.

This is **thinking in layers**: system prompt at the base, conversation history building on top, tool results added as they come in. When you design an agent, you're designing what each layer contains.

**Before moving on, explain in one sentence:** why does the model call `get_weather` before answering, instead of just answering from its training data?

---

## Step 2 -- Add a tool that writes (8 min)

### Read first

Look at `TOOL_SCHEMAS` in `tools.py`. The `description` field is the only thing the model reads to decide when to use a tool. The Python function is invisible to it.

**Question before you build:** if you write a vague description like "saves stuff", what will the model do when you ask it to save a weather summary?

### Build

Ask Claude Code:

> *"Add a tool called save_note that takes a text argument and appends a timestamped line to notes.txt. Write a specific schema description so the model knows exactly when to use it. Then ask the agent to check the weather in Boston and save a one-line summary to my notes. Show me what ends up in notes.txt."*

### The concept

The agent called `get_weather` first, then `save_note`. You never programmed that order. The model inferred it from the tool descriptions and the user's request -- that's **context engineering** working in practice. The description you wrote for each tool is the signal the model used to decide what to do and when.

**Before moving on:** in `tools.py`, find `run_tool`. What happens if a tool throws an exception? Does the model get told about it? Trace it through the code.

---

## Step 3 -- Add guardrails (7 min)

### Try it first

Before building anything, ask the agent something completely off-topic -- "write me a poem" or "what's 2+2." See what it does.

**Question:** did it refuse or help anyway? What does that tell you about what's currently in the system prompt?

### Build

Ask Claude Code:

> *"Add two guardrails: update the system prompt so the agent refuses anything not related to weather or notes, and add a hard 500-character limit inside the save_note function that returns an error if exceeded. Test both and show me the output."*

### The concept

You just put two limits in two different places on purpose. The system prompt limit is **behavioral** -- it shapes what the model wants to do. The code limit is **structural** -- it doesn't matter what the model wants, the function enforces it regardless.

**Before moving on:** if a user sent a very long, persuasive message that slowly convinced the model the character limit didn't apply in this special case -- which guardrail would hold? Which would break? What does that tell you about where hard limits belong?

---

## Step 4 -- Ship it (5 min)

Set up git if you haven't before:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Ask Claude Code:

> *"Fill in the 'What I built' section of the README. Write it as if you're explaining this agent to a teammate who wasn't here -- what it does, what tools it has, where the guardrails are and why they're there. Then commit everything with a descriptive message."*

Read what it writes before you accept it. If it doesn't match what you actually built, correct it. You own this.

---

## Feynman check

You should be able to answer all of these out loud, without looking at the code:

1. What's the difference between a tool schema and a tool function? Who sees each one?
2. The model doesn't have memory between sessions. So how does it know what happened earlier in a conversation?
3. You want a guardrail that blocks the agent from saving notes containing profanity. Prompt or code? Why?
4. A teammate says "the AI is calling our database." What's actually happening?

If any of these are fuzzy, go back to the step that covers it. These are the concepts that come up in capstone reviews.

---

## Stretch goals

These go deeper, not just further:

- **Break it intentionally.** Delete the `description` field from `get_weather`'s schema (leave the function). Ask the agent a weather question. What happens? Restore it after. This is the fastest way to understand why schema descriptions matter.
- **Real weather data.** Replace the hardcoded `get_weather` with a live call to [wttr.in](https://wttr.in) (no key: `curl wttr.in/Boston?format=3`).
- **MCP server.** Run `claude mcp add fetch -- uvx mcp-server-fetch` and ask the agent to summarize a webpage. You just gave it a tool you didn't write.
- **Build a tool from scratch.** No hints. Pick something useful, write the function and schema, ask the agent to use it.

---

## What I built

This is a minimal AI agent: a language model running in a loop that can call Python tools, read their results, and keep reasoning until it has a final answer. The model never runs tools itself — it decides when to ask for one and what arguments to pass, and the loop in `agent.py` does the actual execution.

**Tools**

Two tools live in `tools.py`. Each has a Python function (what runs) and a JSON schema (what the model reads to decide when to use it — the function is invisible to it):

- `get_weather(city)` — returns current weather for a city. Currently returns a hardcoded placeholder; the schema description tells the model to use it whenever the user asks about weather.
- `save_note(text)` — appends a timestamped line to `notes.txt`. The schema description is deliberately specific: use it only when the user explicitly asks to save, log, record, or write something to their notes, and the text should be a concise, self-contained sentence.

**Guardrails**

Two guardrails, intentionally placed in different layers:

- **System prompt** (`agent.py`): the agent is scoped to weather and notes only. If you ask it to write code, explain a concept, or do anything outside that scope, it refuses before touching any tool. This is a behavioral guardrail — it shapes what the model *wants* to do. It's cheap (no tool round-trips) but soft: a persuasive enough prompt could work around it.
- **Hard character limit** (`tools.py`, inside `save_note`): notes longer than 500 characters return an error string instead of writing to disk. The model sees the error as a tool result and self-corrects by trimming and retrying. This is a structural guardrail — it doesn't matter what the model wants, the Python function enforces it unconditionally. Hard limits belong in code, not in prompts, because code can't be argued with.

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
