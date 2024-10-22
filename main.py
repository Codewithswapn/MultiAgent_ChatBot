from nodes.Weather import WeatherNode
from nodes.ChitChat import ChatNode
from nodes.Tourist import WebSearchNode
import openai
import os


openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = os.getenv("NVIDIA_API_KEY")


class DecisionNode:
    def call(self, query):
        # Use GPT to decide which node to route the query to
        decision = self.llm_decide(query)
        if "weather" in decision:
            return "Weather"
        elif "tourist" in decision:
            return "Tourist"
        else:
            return "ChitChat"

    def llm_decide(self, query):
        # Using LLM Model to classify the query belong to which node
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            #model="nvidia/llama-3.1-nemotron-70b-instruct"
            messages=[
                {"role": "system", "content": "Decide whether the query is related to weather, tourism, or general chitchat."},
                {"role": "user", "content": query}
            ]
        )
        return response.choices[0].message['content'].strip().lower()

# Instance of all the nodes
Weather = WeatherNode()
ChitChat = ChatNode()
Tourist = WebSearchNode()
decision_node = DecisionNode()

# Main function to route nodes according to user_query
def main():
    while True:
        user_query = input("Enter your query (or 'exit' to stop): ")
        if user_query.lower() == 'exit':
            break

        # Decision node determines which node to route the query to
        node_choice = decision_node.call(user_query)

        # Execute the chosen node
        if node_choice is not None:
            if node_choice == "Weather":
                response = Weather.call(user_query)
            elif node_choice == "Tourist":
                response = Tourist.call(user_query)
            else:
                response = ChitChat.call(user_query)

            print(f"Response: {response}")

if __name__ == "__main__":
    main()

