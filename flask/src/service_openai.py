from openai import OpenAI


def call_openai(prompt):
    client = OpenAI()
    try:
        completion = client.chat.completions.create(
            # NOTE - max_tokens must be less than 200 since this is the size reserved in the DB
            max_tokens=150,
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return completion.choices[0].message.content

    except Exception as e:
        # TODO log
        print(f"An error occurred: {e}")
        return ""
