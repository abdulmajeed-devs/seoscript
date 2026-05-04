#!/usr/bin/env python3
"""
Test script to verify the RapidAPI Google Search API connection
"""

import http.client
import json
import ssl

def test_api():
    """Test the Google Search API with correct endpoint"""
    
    print("Testing RapidAPI Google Search API...")
    print("=" * 60)
    
    # API credentials
    api_key = "653b90312dmsh9219d00db599bf4p1e3706jsn8f0ba5f7b11b"
    api_host = "google-search116.p.rapidapi.com"
    
    # Test query
    query = "google ads for epoxy flooring"
    country = "us"
    limit = 10
    
    try:
        # Create SSL context
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Create connection
        conn = http.client.HTTPSConnection(api_host, context=context)
        
        # Set headers
        headers = {
            'x-rapidapi-key': api_key,
            'x-rapidapi-host': api_host
        }
        
        # Build endpoint - NOTE: Use / not /search
        from urllib.parse import quote
        endpoint = f"/?query={quote(query)}&country={country}&limit={limit}&gl=us&hl=en&proxy_location=us"
        
        print(f"Query: {query}")
        print(f"Country: {country}")
        print(f"Limit: {limit}")
        print(f"Endpoint: {endpoint}")
        print("=" * 60)
        
        # Make request
        print("\nSending request...")
        conn.request("GET", endpoint, headers=headers)
        
        # Get response
        res = conn.getresponse()
        data = res.read()
        
        # Parse JSON
        result = json.loads(data.decode("utf-8"))
        
        # Display results
        print(f"\nStatus: {res.status} {res.reason}")
        print("=" * 60)
        
        if "results" in result:
            print(f"\n[SUCCESS] Found {len(result['results'])} results!")
            print("\nFirst 3 results:")
            for i, item in enumerate(result['results'][:3], 1):
                print(f"\n{i}. {item.get('title', 'No title')}")
                print(f"   URL: {item.get('url', 'No URL')}")
                print(f"   Position: {item.get('position', 'N/A')}")
        else:
            print(f"\n[ERROR] No results found")
            print(f"Response: {json.dumps(result, indent=2)}")
        
        conn.close()
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_api()
