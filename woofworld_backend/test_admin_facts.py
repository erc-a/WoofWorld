import requests
import json

def test_admin_facts():
    base_url = "http://localhost:6544"
    
    # Login as admin
    login_data = {
        "email": "admin@woofworld.com",
        "password": "admin123"
    }
    
    print("1. Logging in as admin...")
    login_response = requests.post(f"{base_url}/api/login", json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return False
    
    token = login_response.json().get('token')
    print(f"✓ Login successful, got token")
    
    # Test the admin facts endpoint
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print("2. Testing admin facts endpoint...")
    response = requests.get(f"{base_url}/api/admin/facts", headers=headers)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Success! Found {len(data.get('facts', []))} facts")
        return True
    else:
        print(f"❌ Failed with status {response.status_code}")
        return False

if __name__ == "__main__":
    test_admin_facts()
