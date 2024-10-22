import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = os.getenv("NVIDIA_API_KEY")

class ChatNode:
    def call(self, query):
        # OpenAI handles the chat conversation
        response = openai.ChatCompletion.create(
            model="gpt-4",
            #model="nvidia/llama-3.1-nemotron-70b-instruct"
            messages=[
                {"role": "system", "content": "You are a helpful assistant be polite and give accurate response to the user query."},
                {"role": "user", "content": query}
            ],
            max_tokens=1024
        )
        return response.choices[0].message['content'].strip()
