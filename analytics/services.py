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