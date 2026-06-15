"""
Tools the agent can call.

A "tool" is just a normal Python function plus a JSON schema describing it,
so the model knows what it does and what arguments it takes. Start with the
fake weather tool, then add real ones in the exercise.
"""

# ---- Tool implementations ---------------------------------------------------

def get_weather(city: str) -> str:
    """Fake weather tool. Step 2 of the exercise replaces this with a real one."""
    return f"The weather in {city} is 68F and sunny (this is a hardcoded placeholder)."


def save_note(text: str) -> str:
    """Append a timestamped line to notes.txt."""
    if len(text) > 500:
        return f"Error: note is {len(text)} characters, exceeds the 500-character limit. Shorten it and try again."
    from datetime import datetime, timezone
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    line = f"[{timestamp}] {text}\n"
    with open("notes.txt", "a") as f:
        f.write(line)
    return f"Saved: {line.strip()}"


# ---- Tool schemas (what the model sees) -------------------------------------
# This is the "menu" the model picks from. The description is prompt engineering:
# write it like you're explaining the tool to a new teammate.

TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city. Use when the user asks about weather.",
        "input_schema": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "City name, e.g. 'Boston'"}
            },
            "required": ["city"],
        },
    },
    {
        "name": "save_note",
        "description": (
            "Append a timestamped note to the user's notes.txt file. "
            "Use this when the user explicitly asks to save, log, record, or write something to their notes. "
            "The text argument should be a concise, self-contained sentence — not a full conversation, just the fact worth saving."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "The note text to save, e.g. 'Boston weather: 68F and sunny.'"}
            },
            "required": ["text"],
        },
    },
]

# Maps a tool name to the function that runs it.
TOOL_FUNCTIONS = {
    "get_weather": get_weather,
    "save_note": save_note,
}


def run_tool(name: str, args: dict) -> str:
    """Execute a tool by name. Returns a string result fed back to the model."""
    fn = TOOL_FUNCTIONS.get(name)
    if fn is None:
        return f"Error: no tool named {name}"
    try:
        return str(fn(**args))
    except Exception as e:
        return f"Error running {name}: {e}"
