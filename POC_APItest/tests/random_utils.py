import random
import uuid

def get_random_character():
    characters = [
        "Harry Potter",
        "Sherlock Holmes",
        "Katniss Everdeen",
        "Frodo Baggins",
        "Hermione Granger",
        # Add more fictional characters here...
    ]
    return random.choice(characters)

def get_random_company():
    companies = [
            "Acme Corporation",
            "Globex Corporation",
            "Wayne Enterprises",
            "Stark Industries",
            "Umbrella Corporation",
            # Add more fictional companies here...
    ]
    return random.choice(companies)

def generate_random_uuid():
    return str(uuid.uuid4())
def get_random_sage_products():
    sage_products = [
            "sage50uk",
            "Intacct",
            "sage100fr",
            "sage100us",
            "sage200fr",
            # Add more products here...
    ]
    return random.choice(sage_products)