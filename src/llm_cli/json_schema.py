from textwrap import dedent

JSON_SCHEMA_TEMPLATE = dedent(
    """
    # === JSON Schema Template ===
    # See here for details:
    # https://platform.openai.com/docs/guides/structured-outputs
    # Remove this and above lines before using.

    {
        "name": "user_data",
        "strict": true,
        "schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the user"
                },
                "username": {
                    "type": "string",
                    "description": "The username of the user. Must start with @",
                    "pattern": "^@[a-zA-Z0-9_]+$"
                },
                "email": {
                    "type": "string",
                    "description": "The email of the user",
                    "format": "email"
                }
            },
            "additionalProperties": false,
            "required": [
                "name", "username", "email"
            ]
        }
    }
    """
).strip()


def print_json_schema_template():
    print(JSON_SCHEMA_TEMPLATE)
