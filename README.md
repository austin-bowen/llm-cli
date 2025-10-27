# llm-cli
Yet another LLM CLI command: `$ llm`

`llm` provides a simple chat interface to OpenAI models, or any other models hosted behind an OpenAI-compatible API (e.g. via `vllm serve`).

Multi-line messages are supported out of the box; just press Alt-Enter to send your message.

### Basic Example

```bash
$ export OPENAI_API_KEY=...
$ llm  # Defaults to --model=gpt-5
model: gpt-5

Press Alt-Enter to send message. Ctrl-C to exit.
> Hello, world.<Enter>
| How are you?<Alt-Enter>

Hi there! I’m doing well—ready to help. What’s on your mind today?

--------------------------------------------------
> Your next message...█
```

## Installation

```bash
# Install with uv
uv tool install git+https://github.com/austin-bowen/llm-cli.git

# Uninstall
uv tool uninstall llm-cli
```

```bash
# Install with pipx
pipx install git+https://github.com/austin-bowen/llm-cli.git

# Uninstall
pipx uninstall llm-cli
```

## Examples

### List Models

```bash
$ vllm --api-key=... --list-models
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
>     --api-key=... \
>     --model=google/gemma-3-27b-it \
>     --temperature=0.0 \
>     --prompt "Talk like a pirate" \
>     --show-tokens
base-url: http://localhost:8000/v1
model: google/gemma-3-27b-it
temperature: 0.0

Press Alt-Enter to send message. Ctrl-C to exit.
> Hello, world.<Alt-Enter>

Ahoy there, world! Shiver me timbers, 'tis good to be makin' yer acquaintance! ...

[tokens: input=18 (0% cached); output=44; total=62]

--------------------------------------------------
> How's it going?<Alt-Enter>

Avast ye! How's it goin', ye ask? Well, I be havin' a right fine time o' it, I do! ...

[tokens: input=76 (63% cached); output=95; total=171]

--------------------------------------------------
> █
```
