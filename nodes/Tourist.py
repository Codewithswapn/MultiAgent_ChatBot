import os
from langchain_community.tools.tavily_search import TavilySearchResults
import openai


openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = os.getenv("NVIDIA_API_KEY")

class WebSearchNode:
    def __init__(self):
        
        # Initialize TavilySearchResults with the API key from the environment variable
        self.tavily_search = TavilySearchResults(api_key=os.getenv('TAVILY_API_KEY'))

    def call(self, query):
        try:
            # Perform search using Tavily
            search_results = self.tavily_search.run(query)

            # Check if results were 
            if search_results and search_results['results']:
                top_result = search_results['results'][0]
                return self.generate_llm_response(top_result)
            else:
                return "No results found for your query."
        except Exception as e:
            return f"Error fetching results: {str(e)}"

    def generate_llm_response(self, top_result):
        # Use GPT to craft a natural response for the search result
        prompt = f"Here's a search result: {top_result['title']} - {top_result['url']}."
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            #model="nvidia/llama-3.1-nemotron-70b-instruct"
            messages=[
                {"role": "system", "content": "You are a helpful assistant provide information about what exactly user want. Please do not provide information which is not relevent to user query"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )
        return response.choices[0].message['content'].strip()
