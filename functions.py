import requests
import json
from TOKEN_API import COURS_API

COURS_URL = f"https://v6.exchangerate-api.com/v6/{COURS_API}/latest/USD"
response = requests.get(COURS_URL)

if response.status_code == 200:
    data = response.json()
    with open("COURS.json", 'w') as f:
        json.dump(data, f, indent=4)
else:
    print(f"Error: {response.status_code}")
    
exchange_rate_to_dollar = data["conversion_rates"]
