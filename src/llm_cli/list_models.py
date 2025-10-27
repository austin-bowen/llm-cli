from openai import OpenAI


def list_models(client: OpenAI) -> None:
    models = client.models.list().data
    models = sorted(m.id for m in models)
    for model in models:
        print(model)
