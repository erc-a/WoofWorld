#!/usr/bin/env python3

import requests
import json
import sys

def test_post_fact():
    # First get a valid admin token
    login_url = "http://localhost:6544/api/login"
    login_data = {
        "email": "admin@woofworld.com", 
        "password": "admin123"
    }
    
    print("Getting admin token...")
    login_response = requests.post(login_url, json=login_data)
    
    if login_response.status_code != 200:
        print(f"Login failed: {login_response.status_code}")
        print(f"Response: {login_response.text}")
        return
    
    token = login_response.json().get('token')
    print(f"Got token: {token[:20]}...")
    
    # Now test the POST endpoint
    post_url = "http://localhost:6544/api/admin/facts"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    fact_data = {
        "content": "Test fact from debug script - Dogs have unique nose prints"
    }
    
    print(f"\nTesting POST to {post_url}")
    print(f"Headers: {headers}")
    print(f"Data: {fact_data}")
    
    try:
        response = requests.post(post_url, json=fact_data, headers=headers)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {response.text}")
        
        # Try to parse as JSON
        try:
            json_response = response.json()
            print(f"Parsed JSON: {json.dumps(json_response, indent=2)}")
        except:
            print("Could not parse response as JSON")
            
    except Exception as e:
        print(f"Request failed with exception: {e}")

if __name__ == "__main__":
    test_post_fact()
