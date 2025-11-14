from openai import OpenAI

client = OpenAI(api_key="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")

def analyze_with_gpt(prompt):
    """
    A clean separation of GPT logic so tasks remain simple.
    """
    response =  client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are an F1 race analyst."},
                {"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response["choices"][0]["message"]["content"]