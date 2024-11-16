import requests
import urllib.parse

# Set up the parameters for the authorization request
authorization_url = "https://id-shadow.sage.com/authorize"
params = {
    "response_type": "code",
    "client_id": "RHKuuhavR0gw1weoKqWasbDGnAiXAYWC",
    "scope": "openid email profile offline_access all",
    "redirect_uri": "https://jwt.io/",
    "code_challenge": "2vX9BoQb0IqiE7HHey-W322AQ89BoLjKXnQn27fClvs",
    "code_challenge_method": "S256",
    "audience": "snet-dev/network/api"
}

# Encode the parameters into the URL
encoded_params = urllib.parse.urlencode(params)
auth_request_url = f"{authorization_url}?{encoded_params}"

# Send the GET request
response = requests.get(auth_request_url)

# Check response status and content
if response.status_code == 200:
    print("Authorization request successful!")
    print(response.url)  # This is the full URL you were redirected to
else:
    print(f"Authorization request failed with status code {response.status_code}")
    print(response.text)
