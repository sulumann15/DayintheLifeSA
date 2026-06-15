"""
A minimal AI agent: an LLM in a loop that can call tools.

Run it:
    python agent.py "what should I pack for Boston today?"

How it works (the whole idea in 4 steps):
    1. Send the user message + the list of tools to the model.
    2. The model replies with either a final answer OR a tool call.
    3. If it's a tool call, run the tool and send the result back.
    4. Repeat until the model answers or we hit MAX_STEPS.

Default provider is Grok (xAI), which is OpenAI-compatible, so the same code
also works with OpenAI and Azure OpenAI. Get a free key at https://console.x.ai
and put it in .env. No key? Set USE_MOCK=1 to run with a fake model.
"""

import os
import sys
import json

from dotenv import load_dotenv

import tools

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "grok").lower()
USE_MOCK = os.getenv("USE_MOCK", "0") == "1"
MAX_STEPS = 5

SYSTEM_PROMPT = (
    "You are a helpful assistant that can call tools. "
    "Use a tool when it helps answer the user. "
    "When you have enough information, give a short, direct final answer."
)


def make_client():
    """Return an OpenAI-compatible client + model name for the chosen provider."""
    from openai import OpenAI

    if PROVIDER == "grok":
        return (
            OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1"),
            os.getenv("XAI_MODEL", "grok-4.3"),
        )
    if PROVIDER == "openai":
        return OpenAI(), os.getenv("OPENAI_MODEL", "gpt-4o")
    raise ValueError(f"Unsupported PROVIDER for this starter: {PROVIDER}")


# OpenAI/Grok-format tool definitions, derived from the schemas in tools.py.
def openai_tools():
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t["description"],
                "parameters": t["input_schema"],
            },
        }
        for t in tools.TOOL_SCHEMAS
    ]


def run_agent(user_message: str) -> str:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    if USE_MOCK:
        return _run_mock(messages)

    client, model = make_client()

    for _ in range(MAX_STEPS):
        resp = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=openai_tools(),
        )
        msg = resp.choices[0].message

        # No tool calls -> we have our final answer.
        if not msg.tool_calls:
            return (msg.content or "").strip() or "(no answer)"

        # Record the assistant's tool-call turn.
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        })

        # Run each tool and append a tool result message.
        for tc in msg.tool_calls:
            args = json.loads(tc.function.arguments or "{}")
            print(f"  -> calling tool: {tc.function.name}({args})")
            output = tools.run_tool(tc.function.name, args)
            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": output,
            })

    return "(hit step cap without a final answer)"


def _run_mock(messages):
    """No-key fallback: pretend to call get_weather once, then answer."""
    user = messages[-1]["content"].lower()
    if "weather" in user or "pack" in user or "wear" in user:
        print("  -> calling tool: get_weather({'city': 'Boston'})")
        result = tools.run_tool("get_weather", {"city": "Boston"})
        return f"[mock] {result} So pack a light jacket."
    return "[mock] I can help with weather. Try asking what to pack for a city."


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What should I pack for Boston today?"
    print(f"Q: {question}\n")
    print(f"A: {run_agent(question)}")
