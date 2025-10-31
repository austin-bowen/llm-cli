import argparse
import json
from importlib.metadata import version as pkg_version

from openai import Omit, omit

DEFAULT_MODEL: str = "gpt-5"
DEFAULT_TEMPERATURE = omit
DEFAULT_FREQUENCY_PENALTY = omit
DEFAULT_MAX_TOKENS = omit
DEFAULT_REASONING_EFFORT = omit
DEFAULT_BASE_URL = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--api-key",
        "-k",
        help="API key. If not given, then the `OPENAI_API_KEY` "
        "environment variable will be used.",
    )

    parser.add_argument(
        "--list-models",
        "-l",
        action="store_true",
        help="List available models and exit.",
    )

    parser.add_argument(
        "--model",
        "-m",
        default=DEFAULT_MODEL,
        help="The model to use. Default: %(default)s",
    )

    parser.add_argument(
        "--prompt",
        "-p",
        help="The system prompt to use.",
    )

    parser.add_argument(
        "--prompt-file",
        help="The path to a file containing the system prompt.",
    )

    parser.add_argument(
        "--message-file",
        help="The path to a file containing the user message. "
        "This will output the assistant's response and exit (no chat).",
    )

    parser.add_argument(
        "--json-object",
        action="store_true",
        help="Force model to output a JSON object.",
    )

    parser.add_argument(
        "--json-schema-file",
        help="The path to a file containing the JSON schema to use.",
    )

    parser.add_argument(
        "--json-schema-template",
        action="store_true",
        help="Print a JSON schema template and exit. "
        "Use to help create a JSON schema file.",
    )

    parser.add_argument(
        "--temperature",
        "-t",
        default=DEFAULT_TEMPERATURE,
        type=float,
        help="The temperature to use.",
    )

    parser.add_argument(
        "--frequency-penalty",
        default=DEFAULT_FREQUENCY_PENALTY,
        type=float,
        help="The frequency penalty to use.",
    )

    parser.add_argument(
        "--max-tokens",
        default=DEFAULT_MAX_TOKENS,
        type=int,
        help="The maximum number of tokens to generate per response.",
    )

    parser.add_argument(
        "--reasoning-effort",
        default=DEFAULT_REASONING_EFFORT,
        choices=["minimal", "low", "medium", "high"],
        help="The reasoning effort to use.",
    )

    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Override the base URL for the OpenAI API.",
    )

    parser.add_argument(
        "--show-tokens",
        action="store_true",
        help="Show the number of tokens used.",
    )

    parser.add_argument(
        "--no-stream",
        action="store_true",
        help="Do not stream the response.",
    )

    parser.add_argument(
        "message",
        nargs="*",
        help="The user message. This will output the assistant's response and exit (no chat).",
    )

    # Version flag should be at the end
    version = pkg_version("llm_cli")
    parser.add_argument(
        "--version",
        "-V",
        action="version",
        version=f"%(prog)s {version}",
        help="Show program's version number and exit.",
    )

    args = parser.parse_args()
    args.message = get_message(args)
    args.response_format = get_response_format(args)

    return args


def get_message(args: argparse.Namespace) -> str | None:
    cli_message = " ".join(args.message)

    if cli_message and args.message_file:
        raise ValueError("Cannot provide message arg and --message-file")

    if args.message_file:
        with open(args.message_file) as f:
            return f.read()

    return cli_message or None


def get_response_format(args: argparse.Namespace) -> dict[str, str] | Omit:
    if args.json_object and args.json_schema_file:
        raise ValueError("Cannot specify both --json-object and --json-schema-file")

    if args.json_object:
        return dict(type="json_object")

    if args.json_schema_file:
        with open(args.json_schema_file) as f:
            json_schema = json.load(f)

        return dict(
            type="json_schema",
            json_schema=json_schema,
        )

    return omit


def print_settings(args: argparse.Namespace) -> None:
    if args.base_url != DEFAULT_BASE_URL:
        print(f"base-url: {args.base_url}")

    print(f"model: {args.model}")

    if args.temperature != DEFAULT_TEMPERATURE:
        print(f"temperature: {args.temperature}")

    if args.frequency_penalty != DEFAULT_FREQUENCY_PENALTY:
        print(f"frequency_penalty: {args.frequency_penalty}")

    if args.max_tokens != DEFAULT_MAX_TOKENS:
        print(f"max_tokens: {args.max_tokens}")

    if args.reasoning_effort != DEFAULT_REASONING_EFFORT:
        print(f"reasoning_effort: {args.reasoning_effort}")
