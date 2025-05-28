import requests
import json

def test_server_routes():
    """Test if the server is running and routes are accessible"""
    
    base_url = "http://localhost:6544"
    
    print("🔍 Testing WoofWorld Backend Server Routes...")
    print("=" * 60)
    
    # Test basic connectivity
    try:
        # Test a simple public endpoint that should exist
        print("1. Testing public facts endpoint...")
        response = requests.get(f"{base_url}/api/facts", timeout=5)
        print(f"   ✓ GET /api/facts: {response.status_code}")
        if response.status_code == 200:
            facts = response.json()
            print(f"   📊 Found {len(facts)} facts")
        
    except requests.exceptions.ConnectionError:
        print("   ❌ Server not running on localhost:6544")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test login endpoint
    try:
        print("\n2. Testing login endpoint...")
        login_data = {
            "email": "admin@woofworld.com",
            "password": "admin123"
        }
        response = requests.post(
            f"{base_url}/api/login", 
            json=login_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        print(f"   ✓ POST /api/login: {response.status_code}")
        
        if response.status_code == 200:
            login_result = response.json()
            print(f"   🔑 Login successful, token received")
            token = login_result.get('token')
            
            # Test admin endpoint with token
            print("\n3. Testing admin facts endpoint...")
            admin_headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
            
            # Test GET first
            admin_response = requests.get(
                f"{base_url}/api/admin/facts",
                headers=admin_headers,
                timeout=10
            )
            print(f"   ✓ GET /api/admin/facts: {admin_response.status_code}")
            
            if admin_response.status_code == 200:
                admin_facts = admin_response.json()
                print(f"   📊 Admin can access {len(admin_facts)} facts")
                  # Test POST
                print("\n4. Testing admin POST facts endpoint...")
                new_fact_data = {
                    "content": "Server Test Fact - Dogs have an incredible sense of smell"
                }
                
                post_response = requests.post(
                    f"{base_url}/api/admin/facts",
                    json=new_fact_data,
                    headers=admin_headers,
                    timeout=10
                )
                print(f"   ✓ POST /api/admin/facts: {post_response.status_code}")
                
                if post_response.status_code == 200:
                    print("   🎉 SUCCESS! Admin POST endpoint working correctly!")
                    result = post_response.json()
                    print(f"   📝 Created fact: {result}")
                    return True
                else:
                    print(f"   ❌ Admin POST failed: {post_response.text}")
                    return False
            else:
                print(f"   ❌ Admin GET failed: {admin_response.text}")
                return False
        else:
            print(f"   ❌ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error testing routes: {e}")
        return False

if __name__ == "__main__":
    success = test_server_routes()
    if success:
        print("\n🎯 All tests passed! The server is working correctly.")
        print("💡 You can now use your frontend with confidence.")
    else:
        print("\n⚠️  Some tests failed. Check the server configuration.")
