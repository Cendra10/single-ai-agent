# Single AI Agent

A command-line AI agent that plans, calls tools, remembers the conversation, and reviews its own answers.

## Description

Single AI Agent is a small Python agent built on top of an OpenAI-compatible API (Groq). Given a question, the agent decides whether a tool is needed, runs the selected tool, sends the result back to the model, and continues until it has enough information to produce a final answer. A separate reviewer then checks the answer and gives the agent one chance to improve it if something is missing.

## Features

- The agent creates a short plan before using tools and is instructed not to guess calculations or time-related information.
- The model can choose between the available tools (`calculator` and `get_current_time`) through JSON schemas, and the application executes the selected tool.
- The agent can call tools multiple times in a single request, with a hard limit (`MAX_STEPS = 5`) to prevent endless loops.
- Tool errors and unknown tools are handled and returned to the model instead of crashing the application.
- Conversation history is kept in memory, allowing follow-up questions such as "divide the result by 2".
- A separate reviewer checks whether the final answer addresses all parts of the user's question using recent conversation context.
- If the reviewer finds something missing, the agent retries the answer exactly once.

## Tech Stack

- Python 3
- Groq API (OpenAI-compatible), model `openai/gpt-oss-20b`
- `openai` (client library)
- `python-dotenv` (environment variables)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Cendra10/single-ai-agent.git
cd single-ai-agent
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv

# Windows (PowerShell)
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root folder:

```env
GROQ_API_KEY=your_api_key_here
```

The `.env` file is ignored by Git and must never be committed.

## Usage

Run the agent:

```bash
python agent.py
```

Type a question at the `You:` prompt. Type `exit` to quit.

## Example

```text
You: Calculate 8 multiply 7
The result of 8 × 7 is 56.
[Reflection] OK

You: What is the result divided by 2?
The result of dividing 56 by 2 is 28.
[Reflection] OK
```

The second question works because the agent keeps the previous conversation in memory. The `[Reflection]` line shows the reviewer's result for each final answer.

## Project Structure

```text
single-ai-agent/
    agent.py           # Agent loop, memory, reflection, CLI
    tools.py           # Tool functions and their JSON schemas
    requirements.txt   # Python dependencies
    .gitignore
    LICENSE
    README.md
```

## Future Improvement

- Add more tools such as web search and file reading.
- Persist conversation memory across sessions.
- Add token management and context trimming for long conversations.
- Improve reviewer logic based on the tools available to the agent.
- Add automated tests for the tools and the agent loop.
- Add streaming responses.

## License

MIT