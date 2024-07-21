# my_api_project/token_generator.py

import json
import requests

def generate_m2m_token(grant_type, client_id, client_secret, audience):
    url = "https://id-shadow.sage.com/oauth/token"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "grant_type": grant_type,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": audience
    }
    
    response = requests.post(url, json=body, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        response.raise_for_status()

def generate_token(environment):
    grant_type = "client_credentials"
    client_id = "8JIpa0ybrPwz3moWiqUoc6EmKaVy4NZO"
    client_secret = "_q9nUnj96Ppx4r1R32ut1dncJNbpfeDtW6GPBXQ-KJk1YgAjfHOMjPH-deBFAjdy"
    audience = "snet-dev/network/api"
    
    token = generate_m2m_token(grant_type, client_id, client_secret, audience)
    
    with open("m2m_token.json", "w") as file:
        json.dump({"token": token}, file)

if __name__ == "__main__":
    environment = input("Enter the environment (qa02, qa01, int, pp, SBX, Prod): ")
    generate_token(environment)
