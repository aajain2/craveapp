class UserInterface:
    def get_user_query(self):
        return input("What kind of restaurant are you looking for? ")

    def display_results(self, restaurants):
        print("\nHere are some restaurant recommendations:")
        for i, restaurant in enumerate(restaurants, 1):
            print(f"{i}. {restaurant['name']}")
            print(f"   Address: {restaurant['address']}")
            print(f"   Rating: {restaurant['rating']}")
            print(f"   Price Level: {restaurant['price_level']}")
            print()