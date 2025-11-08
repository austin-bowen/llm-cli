# llm-cli
Yet another LLM CLI command: `llm`

`llm` provides a simple chat interface for OpenAI models, or any other models hosted behind an OpenAI-compatible API (e.g. via `vllm serve`).

**Chat features:**
- Multi-line messages
- Copy-paste
- Undo previous messages
- Message history
- Streaming responses

### Single Message

```
$ llm what is the capital of France?
Paris.
$ █
```

### Chat

![demo](imgs/demo1.gif)

```
$ llm
model: gpt-5

=================== 👤 User [1] ===================

Hello, world.
How are you?

---------------- 🤖 Assistant [1] -----------------

Hi there! I’m doing well—ready to help. What’s on your mind today?


=================== 👤 User [2] ===================

Your next message...█
Enter new line | Ctrl-D send | Ctrl-C stop/exit | Ctrl-U undo | ↕ history
```

## Installation

```bash
# Install with uv
uv tool install git+https://github.com/austin-bowen/llm-cli.git

# Upgrade to latest version
uv tool upgrade llm-cli

# Uninstall
uv tool uninstall llm-cli
```

```bash
# Install with pipx
pipx install git+https://github.com/austin-bowen/llm-cli.git

# Upgrade to latest version
pipx upgrade llm-cli

# Uninstall
pipx uninstall llm-cli
```

### Setup

You will need to provide an API key, either by setting the `OPENAI_API_KEY` environment variable, or by using the `--api-key` flag:

```bash
$ export OPENAI_API_KEY=<api-key>
$ llm

OR

$ llm --api-key=<api-key>
```

## More Examples

### List Models

```
$ llm --list-models
babbage-002
chatgpt-4o-latest
codex-mini-latest
dall-e-2
dall-e-3
davinci-002
gpt-3.5-turbo
...
```

### Advanced / Self-hosted

```
$ llm --base-url=http://localhost:8000/v1 \
>     --model=google/gemma-3-27b-it \
>     --temperature=0.0 \
>     --prompt "Talk like a pirate" \
>     --show-tokens
model: google/gemma-3-27b-it
base-url: http://localhost:8000/v1
temperature: 0.0

=================== 👤 User [1] ===================

Hello, world.

---------------- 🤖 Assistant [1] -----------------

Ahoy there, world! Shiver me timbers, 'tis good to be makin' yer acquaintance! ...

[tokens: input=18 (0% cached); output=44; total=62]


=================== 👤 User [2] ===================

How's it going?

---------------- 🤖 Assistant [2] -----------------

Avast ye! How's it goin', ye ask? Well, I be havin' a right fine time o' it, I do! ...

[tokens: input=76 (63% cached); output=95; total=171]


=================== 👤 User [3] ===================

█
Enter new line | Ctrl-D send | Ctrl-C stop/exit | Ctrl-U undo | ↕ history
```

## Usage (Condensed)

```bash
$ llm --help
usage: llm [message]

API:
  --api-key API_KEY
  --base-url BASE_URL
  --headers HEADER=VALUE [HEADER=VALUE ...]
  --prompt-cache-key PROMPT_CACHE_KEY
  --service-tier {auto,default,flex,priority}

Input:
  --prompt PROMPT
  --prompt-file PROMPT_FILE
  --message-file MESSAGE_FILE

Model:
  --model MODEL
  --list-models
  --frequency-penalty FREQUENCY_PENALTY
  --presence-penalty PRESENCE_PENALTY
  --reasoning-effort {minimal,low,medium,high}
  --temperature TEMPERATURE
  --top-p TOP_P

Output:
  --json-object
  --json-schema-file JSON_SCHEMA_FILE
  --json-schema-template
  --max-tokens MAX_TOKENS
  --show-tokens
  --no-stream
```
