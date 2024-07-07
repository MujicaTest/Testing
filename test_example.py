import requests

# Define the base URL for the endpoints
base_url = "https://example.com/api"

# Define the endpoint URLs
endpoint_urls = [
    "/endpoint1",
    "/endpoint2",
    "/endpoint3",
    "/endpoint4",
    "/endpoint5",
    "/endpoint6"
]

# Test the endpoints using GET method
for url in endpoint_urls:
    response = requests.get(base_url + url)
    print(f"Response from {url}: {response.status_code}")

# Test the asynchronous endpoints using POST method
async_urls = [
    "/async_endpoint1",
    "/async_endpoint2"
]

for url in async_urls:
    for _ in range(2):
        response = requests.post(base_url + url)
        print(f"Response from {url}: {response.status_code}")
        # Assert 200 response for GET requests
        assert response.status_code == 200, f"GET request to {url} failed with status code {response.status_code}"

        # Assert 202 and 201 response for POST requests
        assert response.status_code in [202, 201], f"POST request to {url} failed with status code {response.status_code}"