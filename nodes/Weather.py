import requests
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")
#openai.api_key = os.getenv("NVIDIA_API_KEY")

class WeatherNode:
    def call(self, query):
        city = self.extract_city(query)
        if not city:
            return "Please specify a city to get the weather information."
        
        weather_info = self.get_weather_info(city)
        if weather_info:
            return self.generate_llm_response(weather_info)
        else:
            return "I couldn't fetch the weather information. Please try again later."

    def get_weather_info(self, city):
        # Request weather data from the WeatherAPI
        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={os.getenv('WEATHER_API_KEY')}&q={city}")
        if response.status_code == 200:
            weather_data = response.json()
            return {
                'city': city,
                'condition': weather_data['current']['condition']['text'],
                'temp_c': weather_data['current']['temp_c'],
                'humidity': weather_data['current']['humidity'],
            }
        else:
            return None

    def extract_city(self, query):
        # Extract city name from the query
        if "in" in query:
            return query.split("in")[-1].strip()
        return None  # No default city

    def generate_llm_response(self, weather_info):
        # Generate a conversational response using OpenAI LLM
        prompt = f"The current weather in {weather_info['city']} is {weather_info['condition']}. The temperature is {weather_info['temp_c']}°C with a humidity of {weather_info['humidity']}%."
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            #model="nvidia/llama-3.1-nemotron-70b-instruct"
            messages=[
                {"role": "system", "content": "You are a helpful assistant providing accurate and best answers to user queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1024
        )
        return response.choices[0].message['content'].strip()
