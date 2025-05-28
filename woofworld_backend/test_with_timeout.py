#!/usr/bin/env python3

import requests
import json
import sys
import time

def test_with_timeout():
    try:
        # First get a valid admin token
        login_url = "http://localhost:6544/api/login"
        login_data = {
            "email": "admin@woofworld.com", 
            "password": "admin123"
        }
        
        print("Getting admin token...")
        login_response = requests.post(login_url, json=login_data, timeout=10)
        
        if login_response.status_code != 200:
            print(f"Login failed: {login_response.status_code}")
            print(f"Response: {login_response.text}")
            return
        
        token = login_response.json().get('token')
        print(f"Got token: {token[:50]}...")
        
        # Now test the POST endpoint
        post_url = "http://localhost:6544/api/admin/facts"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        fact_data = {
            "content": "Test fact from debug script - Dogs have unique nose prints just like humans have fingerprints"
        }
        
        print(f"\nTesting POST to {post_url}")
        print(f"Data: {fact_data}")
        
        response = requests.post(post_url, json=fact_data, headers=headers, timeout=10)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        try:
            json_response = response.json()
            print(f"Parsed JSON: {json.dumps(json_response, indent=2)}")
        except:
            print("Could not parse response as JSON")
            
    except requests.Timeout:
        print("Request timed out!")
    except Exception as e:
        print(f"Request failed with exception: {e}")

if __name__ == "__main__":
    test_with_timeout()
