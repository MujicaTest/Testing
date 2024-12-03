import random
import uuid
import json
import string

def generate_random_string(length=8):
    """Generate a random alphanumeric string."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_email():
    """Generate a random email address."""
    return f"{generate_random_string(6)}@example.com"

def generate_random_id():
    """Generate a random UUID."""
    return str(uuid.uuid4())

def generate_random_country():
    """Return a random country code."""
    countries = ['GB', 'US', 'CA', 'FR', 'DE', 'AU']
    return random.choice(countries)

def generate_random_date(start_year=2025, end_year=2035):
    """Generate a random expiry date."""
    year = random.randint(start_year, end_year)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Avoiding complications with month lengths
    return f"{year:04d}-{month:02d}-{day:02d}"

def generate_json():
    """Generate JSON with fully random values."""
    json_body = {
        "data": {
            "type": generate_random_string(10),  # Randomize type
            "attributes": {
                "name": generate_random_string(),
                "Country": generate_random_country(),
                "externalId": generate_random_id(),
                "externalSource": generate_random_string(12)
            },
            "license": {
                "managingAccountId": generate_random_string(6),
                "subscriptionId": generate_random_string(6),
                "backOfficeId": generate_random_string(6),
                "backOfficeSource": generate_random_string(15),
                "product": generate_random_string(20),
                "type": generate_random_string(25),
                "expiry": generate_random_date()
            },
            "relationships": {
                "administrators": [
                    {
                        "data": {
                            "type": generate_random_string(8),
                            "attributes": {
                                "email": generate_random_email(),
                                "locale": generate_random_country(),
                                "identityId": generate_random_id(),
                                "provider": generate_random_string(10)
                            }
                        }
                    }
                ]
            }
        }
    }
    return json_body

# Generate and print the random JSON
random_json = generate_json()
print(json.dumps(random_json, indent=4))
# Generate and save to file
random_json = generate_json()
with open("contextual_random_json.txt", "w") as file:
    file.write(json.dumps(random_json, indent=4))