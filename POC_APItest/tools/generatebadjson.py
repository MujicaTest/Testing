import random
import uuid
import json
import string

def generate_random_value():
    """Generate a random value of various types."""
    value_types = [
        lambda: ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(5, 15))),  # Random string
        lambda: random.randint(1, 10000),  # Random integer
        lambda: random.uniform(1.0, 100.0),  # Random float
        lambda: str(uuid.uuid4()),  # Random UUID
        lambda: random.choice([True, False]),  # Random boolean
        lambda: None  # Random None value
    ]
    return random.choice(value_types)()

def generate_random_json(template):
    """Recursively replace all values in a JSON template with random values."""
    if isinstance(template, dict):
        return {key: generate_random_json(value) for key, value in template.items()}
    elif isinstance(template, list):
        return [generate_random_json(item) for item in template]
    else:
        return generate_random_value()

# Define the original JSON structure (template)
template_json = {
    "data": {
        "type": "Dataset",
        "attributes": {
            "name": "{{randomName}}",
            "Country": "GB",
            "externalId": "{{IDfromProduct}}",
            "externalSource": "Intacct"
        },
        "license": {
            "managingAccountId": "C00012",
            "subscriptionId": "C00012",
            "backOfficeId": "C00012",
            "backOfficeSource": "Intacct Backoffice",
            "product": "intacct-network",
            "type": "intacct-network-standard",
            "expiry": "2029-05-22"
        },
        "relationships": {
            "administrators": [
                {
                    "data": {
                        "type": "User",
                        "attributes": {
                            "email": "{{LoggedInUserEmail}}",
                            "locale": "en-GB",
                            "identityId": "{{LoggedInUserAuth0PrincipalId}}",
                            "provider": "Intacct"
                        }
                    }
                }
            ]
        }
    }
}

# Generate completely nonsensical random JSON
random_json = generate_random_json(template_json)
print(json.dumps(random_json, indent=4))
# Generate and save nonsensical random JSON
random_json_nonsensical = generate_random_json(template_json)
with open("nonsensical_random_json.txt", "w") as file:
    file.write(json.dumps(random_json_nonsensical, indent=4))