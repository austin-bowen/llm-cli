import argparse
import json
from importlib.metadata import version as pkg_version
from textwrap import dedent

from openai import Omit, omit

# API defaults
DEFAULT_BASE_URL = None
DEFAULT_SERVICE_TIER = omit

# Model defaults
DEFAULT_MODEL: str = "gpt-5"
DEFAULT_FREQUENCY_PENALTY = omit
DEFAULT_PRESENCE_PENALTY = omit
DEFAULT_REASONING_EFFORT = omit
DEFAULT_TEMPERATURE = omit
DEFAULT_TOP_P = omit

# Output defaults
DEFAULT_MAX_TOKENS = omit


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=dedent(
            """
            Provides a simple chat interface to OpenAI models, or any other models hosted behind an OpenAI-compatible API.

            Chat mode: $ %(prog)s

            Single message mode: $ %(prog)s what is the capital of France?

            Make sure you set the `OPENAI_API_KEY` environment variable, or use the `--api-key` flag.
        """
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    add_api_args(parser)
    add_input_args(parser)
    add_model_args(parser)
    add_output_args(parser)

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


def add_api_args(parser: argparse.ArgumentParser) -> None:
    parser = parser.add_argument_group("API")

    parser.add_argument(
        "--api-key",
        "-k",
        help="""
            API key. If not given, then the `OPENAI_API_KEY` environment variable will be used.
        """,
    )

    parser.add_argument(
        "--base-url",
        default=DEFAULT_BASE_URL,
        help="Override the base URL for the OpenAI API.",
    )

    parser.add_argument(
        "--service-tier",
        default=DEFAULT_SERVICE_TIER,
        choices=("auto", "default", "flex", "priority"),
        help="Specifies the processing type used for serving the request. Default: auto.",
    )


def add_input_args(parser: argparse.ArgumentParser) -> None:
    parser = parser.add_argument_group("Input")

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
        "message",
        nargs="*",
        help="The user message. This will output the assistant's response and exit (no chat).",
    )


def add_model_args(parser: argparse.ArgumentParser) -> None:
    parser = parser.add_argument_group("Model")

    parser.add_argument(
        "--model",
        "-m",
        default=DEFAULT_MODEL,
        help="The model to use. Default: %(default)s",
    )

    parser.add_argument(
        "--list-models",
        "-l",
        action="store_true",
        help="List available models and exit.",
    )

    parser.add_argument(
        "--frequency-penalty",
        default=DEFAULT_FREQUENCY_PENALTY,
        type=float,
        help="""
            Number between -2.0 and 2.0. Default: 0.
            Positive values penalize new tokens based on their existing frequency in the text so far,
            decreasing the model's likelihood to repeat the same line verbatim.
        """,
    )

    parser.add_argument(
        "--presence-penalty",
        default=DEFAULT_PRESENCE_PENALTY,
        type=float,
        help="""
            Number between -2.0 and 2.0. Default: 0.
            Positive values penalize new tokens based on whether they appear in the text so far,
            increasing the model's likelihood to talk about new topics.
        """,
    )

    parser.add_argument(
        "--reasoning-effort",
        default=DEFAULT_REASONING_EFFORT,
        choices=["minimal", "low", "medium", "high"],
        help="""
            Constrains effort on reasoning for reasoning models. Default: medium.
            Reducing reasoning effort can result in faster responses and fewer tokens used on reasoning in a response.
        """,
    )

    parser.add_argument(
        "--temperature",
        "-t",
        default=DEFAULT_TEMPERATURE,
        type=float,
        help="""
            What sampling temperature to use, between 0 and 2. Default: 1.
            Higher values like 0.8 will make the output more random,
            while lower values like 0.2 will make it more focused and deterministic.
            We generally recommend altering this or top_p but not both.
        """,
    )

    parser.add_argument(
        "--top-p",
        default=DEFAULT_TOP_P,
        type=float,
        help="""
            An alternative to sampling with temperature, called nucleus sampling,
            where the model considers the results of the tokens with top_p probability mass.
            So 0.1 means only the tokens comprising the top 10%% probability mass are considered.

            We generally recommend altering this or temperature but not both.
        """,
    )


def add_output_args(parser: argparse.ArgumentParser) -> None:
    parser = parser.add_argument_group("Output")

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
        help="""
            Print a JSON schema template and exit. Use to help create a JSON schema file.
        """,
    )

    parser.add_argument(
        "--max-tokens",
        default=DEFAULT_MAX_TOKENS,
        type=int,
        help="The maximum number of tokens to generate per response.",
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
    print(f"model: {args.model}")

    # API settings

    if args.base_url != DEFAULT_BASE_URL:
        print(f"base-url: {args.base_url}")

    if args.service_tier != DEFAULT_SERVICE_TIER:
        print(f"service-tier: {args.service_tier}")

    # Model settings

    if args.frequency_penalty != DEFAULT_FREQUENCY_PENALTY:
        print(f"frequency_penalty: {args.frequency_penalty}")

    if args.presence_penalty != DEFAULT_PRESENCE_PENALTY:
        print(f"presence_penalty: {args.presence_penalty}")

    if args.reasoning_effort != DEFAULT_REASONING_EFFORT:
        print(f"reasoning_effort: {args.reasoning_effort}")

    if args.temperature != DEFAULT_TEMPERATURE:
        print(f"temperature: {args.temperature}")

    if args.top_p != DEFAULT_TOP_P:
        print(f"top_p: {args.top_p}")

    # Output settings

    if args.max_tokens != DEFAULT_MAX_TOKENS:
        print(f"max_tokens: {args.max_tokens}")
