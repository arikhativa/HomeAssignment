from openai import OpenAI


def call_openai(prompt):
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            # NOTE - max_tokens must be less than 200 since this is the size reserved in the DB
            max_tokens=200,
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        msg = completion.choices[0].message.content
        if len(msg) > 200:
            return "Response is too long", False
        return msg, True

    except Exception as e:
        return f"An error occurred: {e}", False
