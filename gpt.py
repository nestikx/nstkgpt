from g4f.client import Client

client = Client()
messages = []

def question(message: str) -> str:
    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model = "gpt-4o",
        messages = messages
    )
    
    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    
    return answer