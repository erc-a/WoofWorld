import requests

try:
    print("Testing server connectivity...")
    response = requests.get("http://localhost:6544/api/facts", timeout=5)
    print(f"✓ Server responding: {response.status_code}")
    print(f"✓ Response headers: {dict(response.headers)}")
    if response.status_code == 200:
        facts = response.json()
        print(f"✓ Found {len(facts)} facts")
    else:
        print(f"✗ Error response: {response.text}")
except requests.exceptions.ConnectionError:
    print("✗ Server not running on localhost:6544")
except Exception as e:
    print(f"✗ Error: {e}")
