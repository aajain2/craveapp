import requests

class GooglePlacesAPI:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"

    def search_restaurants(self, query, location, max_price=4, radius=160934):  # 160934 meters ≈ 100 miles
        search_url = f"{self.base_url}/textsearch/json"
        params = {
            'query': f"{query} restaurants in {location}",
            'type': 'restaurant',
            'maxprice': max_price,
            'radius': radius,
            'key': self.api_key
        }
        
        try:
            response = requests.get(search_url, params=params)
            response.raise_for_status()
            results = response.json().get('results', [])
            print(f"Total results found: {len(results)}")  # Debug print
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return []

        restaurants = []
        for place in results:
            details = self.get_place_details(place['place_id'])
            restaurant = {
                'name': place['name'],
                'address': place.get('formatted_address', 'Address not available'),
                'rating': place.get('rating', 'N/A'),
                'price_level': '$' * (place.get('price_level', 1) + 1),  # Adjust price level display
                'reviews': details.get('reviews', [])
            }
            restaurants.append(restaurant)
            if len(restaurants) >= 5:
                break

        print(f"Restaurants found: {len(restaurants)}")  # Debug print
        return restaurants

    def get_place_details(self, place_id):
        details_url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'fields': 'name,rating,formatted_address,price_level,reviews',
            'key': self.api_key
        }
        
        try:
            response = requests.get(details_url, params=params)
            response.raise_for_status()
            return response.json().get('result', {})
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while fetching place details: {e}")
            return {}