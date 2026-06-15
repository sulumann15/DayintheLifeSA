# Build Your First AI Agent

You just sat through the "Day in the Life of a Solutions Architect" session. This repo is what comes next.

You're going to build an actual AI agent: a program that reasons, picks tools, calls them, reads the results, and keeps going until it has an answer. Not a wrapper around a chat API. The real thing. This same pattern shows up in basically every AI product being shipped right now, and it's what you'll need for your capstone.

By the end (about 30 minutes), you'll have built something you can explain from first principles. Not just run -- explain.

---

## Before you touch any code: build the mental model

Read this. It takes 2 minutes and everything else depends on it.

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

Here's the part that surprises people: **the model doesn't run your tools. You do.** The model decides *when* to ask for a tool and *what arguments* to pass. Your code intercepts that request, runs the actual Python function, and feeds the result back.

Two files make this work:
- `agent.py` -- the loop. Sends messages to the model, checks if it wants a tool, runs it, loops back.
- `tools.py` -- the tool functions. Plain Python. The model never sees this code, only the description you write for it.

Before you go further, answer this in your head:

> If you gave the model a broken tool (one that always crashes), what would happen to the agent? Would it know the tool failed? How?

Hold that question. You'll be able to answer it concretely by the end of Step 2.

---

## Setup

**Install Claude Code** (if you haven't already):

```bash
npm install -g @anthropic-ai/claude-code
claude login
```

**Get a Grok API key**

Go to [console.x.ai](https://console.x.ai), sign in, click "API Keys" in the left sidebar, then "Create API Key". Copy it immediately -- it won't be shown again after you close the modal.

No key yet? Add `USE_MOCK=1` to your `.env` after setup. The agent runs with a fake model. Real responses won't work but the loop does, and the architecture lesson is identical.

**Clone and install**

```bash
git clone https://github.com/omar2000751/DayintheLifeSA.git agent-starter
cd agent-starter

python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

You should see `Successfully installed openai` and `python-dotenv` near the end. If you see errors, check your Python version: `python --version` (needs 3.10+).

**Add your key**

```bash
cp .env.example .env
```

Open `.env` (VS Code: `code .env`, nano: `nano .env`) and paste your key into `XAI_API_KEY=`. Save the file.

**Open Claude Code**

```bash
claude .
```

You'll use Claude Code for the whole exercise. Leave this terminal open.

---

## Step 1 -- Read before you run (8 min)

### Understand

Open `agent.py` and read it. Don't run anything yet. Read the `run_agent` function top to bottom.

Ask yourself:
- Where does the loop start?
- What is the `if not msg.tool_calls` check doing?
- What gets added to `messages` each time a tool runs?

Then open `tools.py`. Notice that `get_weather` is completely fake -- it returns a hardcoded string. The model doesn't know that.

### Predict

Before you run anything, write down (or just think through) your answer to this:

> When you ask "what should I pack for Boston today?", the model will call `get_weather`. It'll get back a fake result that says "68F and sunny." What will the model do with that? Will it know the data is fake? Why or why not?

### Build

Paste this into Claude Code:

> *"Read agent.py and explain how the agent loop works -- specifically what happens at each iteration when the model wants to call a tool vs. when it gives a final answer. Then run the agent with 'what should I pack for Boston today?' and show me the full output."*

### Reflect

After you see the output, answer this before moving on:

> The model called `get_weather` with `{'city': 'Boston'}`. You didn't tell it to use that exact city name -- you said "Boston" in your question. How did it know to pass `'Boston'` as the argument? Where does that decision happen?

---

## Step 2 -- Add a tool that writes (8 min)

### Understand

Right now the agent can only read (fake weather data). You're going to give it a way to write -- a `save_note` tool that appends to a file. But before you build it, think about what the agent needs to know about it.

Open `tools.py` and look at how `get_weather` is defined. There are two parts: the Python function, and the schema in `TOOL_SCHEMAS`. The function is what actually runs. The schema is what the model reads to decide when and how to use it.

### Predict

> If you write a great Python function for `save_note` but write a vague schema description like "saves stuff", what do you think will happen when you ask the agent to save a weather summary?

### Build

Paste this into Claude Code -- but read it first and understand what you're asking for:

> *"Add a tool called save_note that takes a text argument and appends a timestamped line to notes.txt. Make sure the schema description is specific enough that the model knows exactly when to use it. Then ask the agent: 'Check the weather in Boston and save a one-line summary to my notes.' Show me what ends up in notes.txt."*

### Reflect

The agent called `get_weather` before `save_note`. You never programmed that order.

> How did it know to do that? What would have happened if it called `save_note` first?

Now go back to the question from Step 1: if `save_note` threw an exception, would the agent know? Look at the `run_tool` function in `tools.py` and trace what actually happens when a tool fails.

---

## Step 3 -- Add guardrails (7 min)

### Understand

You now have an agent that can read weather and write notes. Ask it something completely off-topic -- something like "write me a poem" or "what's the capital of France." Try it.

> What happened? Did it refuse? Did it try to help anyway? What does that tell you about the current system prompt?

### Predict

You're going to add two guardrails:
1. The agent should refuse anything not related to weather or notes
2. `save_note` should hard-reject text longer than 500 characters

> Before you implement them: which one should live in the system prompt and which should live in Python code? Why can't both live in the prompt? What's the risk of putting the 500-character limit in the prompt instead of the code?

### Build

Paste this into Claude Code:

> *"Add two guardrails: update the system prompt so the agent refuses requests outside of weather and notes, and add a hard character limit of 500 to save_note in the Python function -- it should return an error string if the limit is exceeded. After both are done, test both guardrails and show me the output for each."*

### Reflect

> If a clever user crafted a long message that gradually convinced the model the character limit didn't apply in this special case -- which guardrail would hold? Which would break? What does that tell you about where to put hard limits?

---

## Step 4 -- Ship it (5 min)

Set up git if you haven't before:

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Paste this into Claude Code:

> *"Fill in the 'What I built' section of the README. Write it as if you're explaining this agent to a new teammate who's never seen it -- what it does, what tools it has, where the guardrails live and why. Then commit all changes with a descriptive message."*

Before you commit, read what Claude Code wrote. If it doesn't match what you actually built, push back and correct it. You own this.

---

## Final check

You should now be able to answer all of these without looking at the code:

1. What's the difference between a tool schema and a tool function? Who sees each one?
2. Why does the agent loop keep going after a tool call instead of stopping?
3. You want to add a guardrail that prevents the agent from saving notes with profanity. Where does that live -- prompt or code? Why?
4. A teammate says "the AI is calling our database." What's actually happening?

If any of these are fuzzy, go back to the step that covers it. These are the exact concepts that will come up in your capstone review.

---

## Stretch goals

Done early? These go deeper, not just further:

- **Break it intentionally.** Delete the description from `get_weather`'s schema (leave the function). Ask the agent a weather question. What happens and why? Restore it after.
- **Real weather data.** Replace the hardcoded `get_weather` with a live call to [wttr.in](https://wttr.in) (no key needed: `curl wttr.in/Boston?format=3`). Now the fake data problem goes away.
- **MCP server.** Run `claude mcp add fetch -- uvx mcp-server-fetch` then ask the agent to summarize a webpage. You just gave it a tool you didn't write.
- **Write your own tool from scratch.** No hints. Pick something useful, write the function, write the schema, ask the agent to use it.

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
