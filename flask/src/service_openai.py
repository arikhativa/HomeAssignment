from openai import OpenAI
from .types import HTTPStatusCode


def call_openai(prompt):
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            # NOTE - max_tokens must be less than 2000 for performance reasons
            max_tokens=2000,
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        msg = completion.choices[0].message.content
        if len(msg) >= 2000:
            return (
                f"Response is too long. try asking simpler question.",
                HTTPStatusCode.BAD_REQUEST,
            )
        return msg, HTTPStatusCode.OK

    except Exception as e:
        if e:
            return f"An error occurred: {e}", HTTPStatusCode.INTERNAL_SERVER_ERROR
        return f"An error occurred", HTTPStatusCode.INTERNAL_SERVER_ERROR
