import requests
import json

# Get admin token
login_response = requests.post(
    "http://localhost:6544/api/login",
    json={"email": "admin@woofworld.com", "password": "admin123"}
)

if login_response.status_code == 200:
    token = login_response.json()["token"]
    print(f"Token obtained: {token[:30]}...")
    
    # Test admin facts endpoint
    response = requests.get(
        "http://localhost:6544/api/admin/facts",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Success! Found {len(data.get('facts', []))} facts")
        print("Sample response:", json.dumps(data, indent=2)[:200] + "...")
    else:
        print(f"Error: {response.text}")
else:
    print(f"Login failed: {login_response.status_code} - {login_response.text}")
