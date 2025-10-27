import shutil

from openai import BadRequestError


def error_is_streaming_not_supported(e: BadRequestError) -> bool:
    error_type = e.body.get("type")
    error_param = e.body.get("param")
    return error_type == "invalid_request_error" and error_param == "stream"


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
        f"[tokens: "
        f"input={input_tokens} ({cached_input_tokens_percent}% cached); "
        f"output={output_tokens}; "
        f"total={total_tokens}]"
    )


def print_separator() -> None:
    term_width = shutil.get_terminal_size().columns
    sep_width = min(term_width, 50)
    print("-" * sep_width)
