# llm-cli
Yet another LLM CLI command: `$ llm`

`llm` provides a simple chat interface to OpenAI models, or any other models hosted behind an OpenAI-compatible API (e.g. via `vllm serve`).

### Single Message

```bash
$ llm what is the capital of France?
Paris.
$ █
```

### Basic Chat

Multi-line messages and copy-paste are supported out of the box; just press Ctrl-D to send your message.

```bash
$ llm
model: gpt-5

==================== User [0] ====================

Hello, world.<Enter>
How are you?<Ctrl-D>

----------------- Assistant [0] ------------------

Hi there! I’m doing well—ready to help. What’s on your mind today?


==================== User [1] ====================

Your next message...█
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

## Examples

### List Models

```bash
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

```bash
$ llm --base-url=http://localhost:8000/v1 \
>     --model=google/gemma-3-27b-it \
>     --temperature=0.0 \
>     --prompt "Talk like a pirate" \
>     --show-tokens
model: google/gemma-3-27b-it
base-url: http://localhost:8000/v1
temperature: 0.0

==================== User [0] ====================

Hello, world.<Ctrl-D>

----------------- Assistant [0] ------------------

Ahoy there, world! Shiver me timbers, 'tis good to be makin' yer acquaintance! ...

[tokens: input=18 (0% cached); output=44; total=62]


==================== User [1] ====================

How's it going?<Ctrl-D>

----------------- Assistant [1] ------------------

Avast ye! How's it goin', ye ask? Well, I be havin' a right fine time o' it, I do! ...

[tokens: input=76 (63% cached); output=95; total=171]


==================== User [2] ====================
█
```

## Usage

```bash
$ llm --help
usage: llm [-h] [--api-key API_KEY] [--list-models] [--model MODEL] [--prompt PROMPT] [--prompt-file PROMPT_FILE] [--json-object] [--json-schema-file JSON_SCHEMA_FILE] [--json-schema-template] [--temperature TEMPERATURE]
           [--frequency-penalty FREQUENCY_PENALTY] [--max-tokens MAX_TOKENS] [--reasoning-effort {minimal,low,medium,high}] [--base-url BASE_URL] [--show-tokens] [--no-stream] [--message-file MESSAGE_FILE] [--version]
           [message ...]

positional arguments:
  message               The user message. This will output the assistant's response and exit (no chat).

options:
  -h, --help            show this help message and exit
  --api-key API_KEY, -k API_KEY
                        API key. If not given, then the `OPENAI_API_KEY` environment variable will be used.
  --list-models, -l     List available models and exit.
  --model MODEL, -m MODEL
                        The model to use. Default: gpt-5
  --prompt PROMPT, -p PROMPT
                        The system prompt to use.
  --prompt-file PROMPT_FILE
                        The path to a file containing the system prompt.
  --message-file MESSAGE_FILE
                        The path to a file containing the user message. This will output the assistant's response and exit (no chat).
  --json-object         Force model to output a JSON object.
  --json-schema-file JSON_SCHEMA_FILE
                        The path to a file containing the JSON schema to use.
  --json-schema-template
                        Print a JSON schema template and exit. Use to help create a JSON schema file.
  --temperature TEMPERATURE, -t TEMPERATURE
                        The temperature to use.
  --frequency-penalty FREQUENCY_PENALTY
                        The frequency penalty to use.
  --max-tokens MAX_TOKENS
                        The maximum number of tokens to generate per response.
  --reasoning-effort {minimal,low,medium,high}
                        The reasoning effort to use.
  --base-url BASE_URL   Override the base URL for the OpenAI API.
  --show-tokens         Show the number of tokens used.
  --no-stream           Do not stream the response.
  --version, -V         Show program's version number and exit.
```
