import shutil
from math import ceil, floor

from openai import BadRequestError

ANSI_FORMAT_BOLD = "\033[1m"
ANSI_FORMAT_RESET = "\033[0m"


def bold(text: str) -> str:
    return ANSI_FORMAT_BOLD + text + ANSI_FORMAT_RESET


def error_is_streaming_not_supported(e: BadRequestError) -> bool:
    error_type = e.body.get("type")
    error_param = e.body.get("param")
    return error_type == "invalid_request_error" and error_param == "stream"


def get_term_width() -> int:
    return shutil.get_terminal_size().columns


def print_header(header: str, bar_char: str = "=", max_width: int = 50) -> None:
    term_width = get_term_width()
    bar_width = min(term_width, max_width) - len(header) - 2
    bar_width = max(bar_width, 3)

    left_bar_width = floor(bar_width / 2)
    right_bar_width = ceil(bar_width / 2)

    left_bar = bar_char * left_bar_width
    right_bar = bar_char * right_bar_width

    print(bold(f"{left_bar} {header} {right_bar}"))


def print_token_usage(token_usage) -> None:
    input_tokens = token_usage.prompt_tokens

    try:
        cached_input_tokens = token_usage.prompt_tokens_details.cached_tokens
    except AttributeError:
        cached_input_tokens = 0

    cached_input_tokens_percent = round(100 * cached_input_tokens / input_tokens)

    output_tokens = token_usage.completion_tokens

    total_tokens = input_tokens + output_tokens

    print(
        f"[Tokens: "
        f"input={input_tokens} ({cached_input_tokens_percent}% cached); "
        f"output={output_tokens}; "
        f"total={total_tokens}]"
    )
