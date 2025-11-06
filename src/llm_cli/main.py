from openai import OpenAI

from llm_cli.args import parse_args
from llm_cli.chat import chat, single_message
from llm_cli.json_schema import print_json_schema_template
from llm_cli.list_models import list_models


def main() -> None:
    args = parse_args()

    if args.json_schema_template:
        print_json_schema_template()
        return

    client = OpenAI(
        api_key=args.api_key,
        base_url=args.base_url,
        default_headers=args.headers or None,
    )

    if args.list_models:
        list_models(client)
        return

    if args.message:
        try:
            single_message(args, client)
        except KeyboardInterrupt:
            print()
            print("[Stopped]")
        return

    try:
        chat(args, client)
    except KeyboardInterrupt:
        print("[Exit]")


if __name__ == "__main__":
    main()
