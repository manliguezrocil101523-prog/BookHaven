import requests
import json

# Test data
test_cart = {
    "The Folly Magic": 2,
    "Love of My Life": 1
}

test_customer = {
    "name": "John Doe",
    "street": "123 Main St",
    "barangay": "Brgy San Jose",
    "city": "Manila",
    "province": "Metro Manila",
    "postal": "1000",
    "payment": "Credit Card"
}

test_total = 950

# Send request to place-order endpoint
url = "http://127.0.0.1:5000/place-order"
payload = {
    "cart": test_cart,
    "customer": test_customer,
    "total": test_total
}

response = requests.post(url, json=payload)
print(f"Status Code: {response.status_code}")
print(f"Response: {response.json()}")
