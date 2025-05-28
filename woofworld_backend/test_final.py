import requests
import json

try:
    # Step 1: Login to get admin token
    print("Step 1: Logging in as admin...")
    login_response = requests.post(
        "http://localhost:6544/api/login",
        json={"email": "admin@woofworld.com", "password": "admin123"},
        timeout=10
    )
    
    if login_response.status_code == 200:
        token = login_response.json()["token"]
        print(f"✅ Login successful! Token: {token[:30]}...")
        
        # Step 2: Test admin facts endpoint
        print("Step 2: Testing admin facts endpoint...")
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        facts_response = requests.get(
            "http://localhost:6544/api/admin/facts",
            headers=headers,
            timeout=10
        )
        
        print(f"Status Code: {facts_response.status_code}")
        
        if facts_response.status_code == 200:
            data = facts_response.json()
            facts_count = len(data.get('facts', []))
            print(f"✅ SUCCESS! Retrieved {facts_count} facts from admin endpoint")
            print(f"Response structure: {list(data.keys())}")
            
            if facts_count > 0:
                print(f"Sample fact: {data['facts'][0]['content'][:50]}...")
            
        else:
            print(f"❌ Failed with status {facts_response.status_code}")
            print(f"Response: {facts_response.text}")
            
    else:
        print(f"❌ Login failed with status {login_response.status_code}")
        print(f"Response: {login_response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
