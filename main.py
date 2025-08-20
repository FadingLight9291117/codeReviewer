from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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",
)

completion = client.chat.completions.create(
  model="openai/gpt-4o",
  messages=[
    {
      "role": "user",
      "content": "What is the meaning of life?"
    }
  ]
)

print(completion.choices[0].message.content)
