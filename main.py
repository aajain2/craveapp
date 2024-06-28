from database import Database
from openai_processor import OpenAIProcessor
from google_places_api import GooglePlacesAPI
from user_interface import UserInterface
import os
import json

def main():
    db = Database()
    openai_processor = OpenAIProcessor(os.getenv('OPENAI_API_KEY'))
    
    google_places_api_key = os.getenv('GOOGLE_PLACES_API_KEY')
    if not google_places_api_key:
        print("Error: GOOGLE_PLACES_API_KEY environment variable is not set.")
        return
    
    google_places_api = GooglePlacesAPI(google_places_api_key)
    ui = UserInterface()

    name = input("Enter your name: ")
    dietary_preferences = input("Enter your dietary preferences (e.g., vegetarian, vegan, gluten-free): ")
    city = input("Enter your city: ")
    state = input("Enter your state/province: ")
    country = input("Enter your country: ")
    location = f"{city}, {state}, {country}"

    db.add_user(name, dietary_preferences)
    user_id = 1  # Assuming this is the first user

    print(f"User preferences: {dietary_preferences}")

    query = ui.get_user_query()
    processed_query = openai_processor.process_query(query)
    
    print(f"Processed query: {json.dumps(processed_query, indent=2)}")
    print(f"Location: {location}")

    restaurants = google_places_api.search_restaurants(
        processed_query['search_query'], 
        location, 
        max_price=processed_query['price_level']
    )
    
    print(f"\nTop 5 restaurant recommendations based on your query:")
    for i, restaurant in enumerate(restaurants, 1):
        print(f"{i}. {restaurant['name']}")
        print(f"   Address: {restaurant['address']}")
        print(f"   Rating: {restaurant['rating']}")
        print(f"   Price Level: {restaurant['price_level']}")
        
        # Check if the restaurant matches dietary preferences
        matches_diet = any(dietary_preferences.lower() in review.get('text', '').lower() for review in restaurant['reviews'])
        if matches_diet:
            print(f"   ✓ Matches dietary preference: {dietary_preferences}")
        else:
            print(f"   ✗ May not match dietary preference: {dietary_preferences}")
        print()

    db.close()

if __name__ == "__main__":
    main()