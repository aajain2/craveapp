import openai
import json

class OpenAIProcessor:
    def __init__(self, api_key):
        openai.api_key = api_key

    def process_query(self, query):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key information from restaurant queries."},
                {"role": "user", "content": f"""
                Extract key information from this restaurant query: "{query}"
                Return a JSON object with the following keys:
                - cuisine_type: The type of cuisine mentioned or 'any' if not specified
                - price_level: A number from 1 to 4, where 1 is very cheap, 2 is cheap, 3 is moderate, and 4 is expensive
                - atmosphere: The desired atmosphere or ambiance
                - search_query: A concise search query for Google Places API based on the extracted information
                """}
            ]
        )
        
        try:
            result = json.loads(response.choices[0].message['content'])
            return result
        except json.JSONDecodeError:
            print("Error: Could not parse OpenAI response as JSON")
            return {
                "cuisine_type": "any",
                "price_level": 2,
                "atmosphere": "any",
                "search_query": query
            }