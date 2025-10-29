import argparse
import traceback
from functools import lru_cache
from typing import Any, Optional

from openai import BadRequestError, OpenAI, OpenAIError
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.key_binding import KeyBindings

from llm_cli.args import print_settings
from llm_cli.utils import (
    error_is_streaming_not_supported,
    print_header,
    print_token_usage,
)

Message = dict[str, str]


def chat(args: argparse.Namespace, client: OpenAI) -> None:
    system_message = get_system_message(args)
    messages: list[Message] = [system_message] if system_message else []

    print_settings(args)
    print()

    turn = 0
    while True:
        user_message = get_user_message(turn)
        messages.append(user_message)

        try:
            assistant_response = get_assistant_response(args, client, messages, turn)
        except OpenAIError:
            traceback.print_exc()
            messages.pop()
            print("[Last user message dropped]")
        else:
            messages.append(assistant_response)
            turn += 1


def get_system_message(args: argparse.Namespace) -> Optional[Message]:
    if args.prompt and args.prompt_file:
        raise ValueError("Cannot specify both --prompt and --prompt-file.")

    if args.prompt:
        return dict(role="system", content=args.prompt)

    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            return dict(role="system", content=f.read())

    return None


def get_user_message(turn: int) -> Message:
    print_header(f"User [{turn}]", bar_char="=")
    print()

    session = get_prompt_session()
    content = session.prompt(
        bottom_toolbar=bottom_toolbar,
    ).strip()
    print()

    return dict(role="user", content=content)


@lru_cache(maxsize=1)
def get_prompt_session() -> PromptSession:
    kb = KeyBindings()

    # Ctrl-D
    @kb.add("c-d")
    def submit(event):
        event.current_buffer.validate_and_handle()

    return PromptSession(
        multiline=True,
        auto_suggest=AutoSuggestFromHistory(),
        history=InMemoryHistory(),
        key_bindings=kb,
    )


@lru_cache(maxsize=1)
def bottom_toolbar() -> HTML:
    return HTML(
        "<b>Enter</b> for new line | "
        "<b>Ctrl-D to send</b> | "
        "<b>Ctrl-C</b> to exit | "
        "<b>Up/Down</b> for history"
    )


def get_assistant_response(
    args: argparse.Namespace,
    client: OpenAI,
    messages: list[Message],
    turn: int,
) -> Message:
    print_header(f"Assistant [{turn}]", bar_char="-")

    request_kwargs = dict(
        messages=messages,
        model=args.model,
        temperature=args.temperature,
        frequency_penalty=args.frequency_penalty,
        max_completion_tokens=args.max_tokens,
        reasoning_effort=args.reasoning_effort,
    )

    if not args.no_stream:
        try:
            message = get_assistant_message_streaming(args, client, request_kwargs)
        except BadRequestError as e:
            if error_is_streaming_not_supported(e):
                print(
                    f"[Streaming not supported. Error message: {e.body.get('message')}]"
                )
                args.no_stream = True
            else:
                raise

    if args.no_stream:
        message = get_assistant_message_no_streaming(args, client, request_kwargs)

    print()

    return dict(role="assistant", content=message)


def get_assistant_message_streaming(
    args: argparse.Namespace,
    client: OpenAI,
    request_kwargs: dict[str, Any],
) -> str:
    response_stream = client.chat.completions.create(
        **request_kwargs,
        stream=True,
        stream_options=dict(include_usage=True),
    )

    message_chunks = []
    print_buffer = ""
    token_usage = None
    print()
    for chunk in response_stream:
        # The last chunk should have no choices and should have the token usage
        if not chunk.choices:
            token_usage = chunk.usage
            break

        content = chunk.choices[0].delta.content
        if not content:
            continue

        # Some models like to output a lot of whitespace at the end;
        # use a buffer to avoid printing it
        print_buffer += content

        if not print_buffer.isspace():
            print(print_buffer, end="", flush=True)
            message_chunks.append(print_buffer)
            print_buffer = ""

    print()
    print()

    assistant_message = "".join(message_chunks)

    if args.show_tokens and token_usage:
        print_token_usage(token_usage)
        print()

    return assistant_message


def get_assistant_message_no_streaming(
    args: argparse.Namespace,
    client: OpenAI,
    request_kwargs: dict[str, Any],
) -> str:
    response = client.chat.completions.create(**request_kwargs)

    assistant_message = response.choices[0].message.content.strip()

    print()
    print(assistant_message)
    print()

    if args.show_tokens:
        print_token_usage(response.usage)
        print()

    return assistant_message
