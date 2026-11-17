import json
import os
import re

SYSTEM = (
    "You are a football broadcast analyst. Write a 3-4 sentence match recap "
    "using ONLY the facts in the JSON provided. After every claim about a goal "
    "or chance, cite its event id in the form (event N). Do not invent players, "
    "events, stats or minutes. If a fact is not in the JSON, do not state it."
)


def _client():
    if os.getenv("AZURE_OPENAI_ENDPOINT") and os.getenv("AZURE_OPENAI_API_KEY"):
        from openai import AzureOpenAI

        client = AzureOpenAI(
            azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
            api_key=os.environ["AZURE_OPENAI_API_KEY"],
            api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21"),
        )
        return client, os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini")
    if os.getenv("OPENAI_API_KEY"):
        from openai import OpenAI

        return OpenAI(), os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return None, None


def generate_narrative(facts: dict):
    """Return an LLM recap whose citations are all valid, else None."""
    client, model = _client()
    if client is None:
        print("LLM: no credentials found, using template recap")
        return None
    try:
        resp = client.chat.completions.create(
            model=model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": json.dumps(facts, default=str)},
            ],
        )
        text = resp.choices[0].message.content.strip()
    except Exception as e:
        print(f"LLM call failed: {e}")
        return None

    valid = {m["event_id"] for m in facts["moments"]}
    cited = {int(n) for n in re.findall(r"event (\d+)", text)}
    if not cited or not cited <= valid:
        print(f"LLM output rejected, bad or missing citations: {cited}")
        return None
    return text
