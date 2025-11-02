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
    get_term_width,
    print_header,
    print_token_usage,
)

Message = dict[str, str]


def chat(args: argparse.Namespace, client: OpenAI) -> None:
    system_message = get_system_message(args)
    messages: list[Message] = [system_message] if system_message else []

    print_settings(args)
    print()

    while True:
        turn = 1 + len(messages) // 2

        # User turn

        print_header(f"👤 User [{turn}]", bar_char="=")
        print()
        try:
            user_message = get_user_message()
        except UndoCommand:
            if messages:
                messages.pop()
                messages.pop()
                print("[Last message dropped]")
            else:
                print("[No messages to drop]")
            print()
            continue
        messages.append(user_message)
        print()

        # Assistant turn

        print_header(f"🤖 Assistant [{turn}]", bar_char="-")
        print()
        try:
            assistant_response = get_assistant_response(args, client, messages)
        except (KeyboardInterrupt, OpenAIError) as e:
            print()
            if isinstance(e, KeyboardInterrupt):
                print("[Stopped]")
            else:
                traceback.print_exc()

            messages.pop()
            print("[Last message dropped]")
        else:
            messages.append(assistant_response)
        print()
        print()


def single_message(args: argparse.Namespace, client: OpenAI) -> None:
    system_message = get_system_message(args)
    messages = [system_message] if system_message else []
    messages.append(dict(role="user", content=args.message))
    get_assistant_response(args, client, messages)


def get_system_message(args: argparse.Namespace) -> Optional[Message]:
    if args.prompt and args.prompt_file:
        raise ValueError("Cannot specify both --prompt and --prompt-file.")

    if args.prompt:
        return dict(role="system", content=args.prompt)

    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            return dict(role="system", content=f.read())

    return None


def get_user_message() -> Message:
    session = get_prompt_session()
    content = session.prompt(
        bottom_toolbar=bottom_toolbar,
    ).strip()

    return dict(role="user", content=content)


@lru_cache(maxsize=1)
def get_prompt_session() -> PromptSession:
    kb = KeyBindings()

    # Ctrl-D
    @kb.add("c-d")
    def submit(event):
        event.current_buffer.validate_and_handle()

    # Ctrl-U
    @kb.add("c-u")
    def undo(event):
        # Add any in-progress text to history
        if event.current_buffer.text.strip():
            event.current_buffer.append_to_history()

        event.app.exit(exception=UndoCommand())

    return PromptSession(
        multiline=True,
        auto_suggest=AutoSuggestFromHistory(),
        history=InMemoryHistory(),
        key_bindings=kb,
    )


def bottom_toolbar() -> HTML:
    term_width = get_term_width()
    return (
        BOTTOM_TOOLBAR_LONG
        if term_width >= BOTTOM_TOOLBAR_LONG_WIDTH
        else BOTTOM_TOOLBAR_SHORT
    )


BOTTOM_TOOLBAR_LONG_WIDTH = 73

BOTTOM_TOOLBAR_LONG = HTML(
    "<b>Enter</b> new line | "
    "<b>Ctrl-D</b> send | "
    "<b>Ctrl-C</b> stop/exit | "
    "<b>Ctrl-U</b> undo | "
    "<b>↕</b> history"
)

BOTTOM_TOOLBAR_SHORT = HTML(
    "<b>^D</b> send | <b>^C</b> stop/exit | <b>^U</b> undo | <b>↕</b> history"
)


class UndoCommand(Exception):
    pass


def get_assistant_response(
    args: argparse.Namespace,
    client: OpenAI,
    messages: list[Message],
) -> Message:
    request_kwargs = dict(
        messages=messages,
        model=args.model,
        frequency_penalty=args.frequency_penalty,
        max_completion_tokens=args.max_tokens,
        presence_penalty=args.presence_penalty,
        reasoning_effort=args.reasoning_effort,
        response_format=args.response_format,
        service_tier=args.service_tier,
        temperature=args.temperature,
        top_p=args.top_p,
    )

    if not args.no_stream:
        try:
            message = get_assistant_message_streaming(args, client, request_kwargs)
        except BadRequestError as e:
            if error_is_streaming_not_supported(e):
                print(
                    f"[Streaming not supported. Error message: {e.body.get('message')}]"
                )
                print()
                args.no_stream = True
            else:
                raise

    if args.no_stream:
        message = get_assistant_message_no_streaming(args, client, request_kwargs)

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

    if args.show_tokens and token_usage:
        print()
        print_token_usage(token_usage)

    assistant_message = "".join(message_chunks)

    return assistant_message


def get_assistant_message_no_streaming(
    args: argparse.Namespace,
    client: OpenAI,
    request_kwargs: dict[str, Any],
) -> str:
    response = client.chat.completions.create(**request_kwargs)

    assistant_message = response.choices[0].message.content.strip()

    print(assistant_message)

    if args.show_tokens:
        print()
        print_token_usage(response.usage)

    return assistant_message
