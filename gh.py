import argparse
import requests
import hashlib
from flask import Flask, request, Response

app = Flask(__name__)
cache = {}  # In-memory cache: {cache_key: (response_content, headers)}

# Step 1: Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument("--port", type=int, default=3000, help="Port number for the proxy server")
parser.add_argument("--origin", type=str, required=True, help="Base URL to forward requests to")
parser.add_argument("--clear-cache", action="store_true", help="Clear the cache and exit")
args = parser.parse_args()
if args.clear_cache:
    cache.clear()
    print("Cache cleared successfully.")
    sys.exit(0) 
origin = args.origin.rstrip("/")  # Remove trailing slash if present

# Step 2: Define the Flask route to handle all paths
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    # Construct the full URL to forward the request
    forward_url = f"{origin}/{path}" if path else origin
    
    # Step 3: Generate a cache key based on the request URL and method
    cache_key = hashlib.md5((forward_url + request.method).encode()).hexdigest()

    # Step 4: Check if the response is cached
    if cache_key in cache:
        cached_response, headers = cache[cache_key]
        headers["X-Cache"] = "HIT"
        return Response(cached_response, headers=headers)
    
    # Step 5: Forward the request to the origin server
    response = requests.request(
        method=request.method,
        url=forward_url,
        headers=request.headers,
        data=request.get_data(),
        params=request.args
    )
    
    # Cache the response content and headers
    cache[cache_key] = (response.content, dict(response.headers))
    
    # Add custom header indicating the response is from the server
    response_headers = dict(response.headers)
    response_headers["X-Cache"] = "MISS"
    
    return Response(response.content, status=response.status_code, headers=response_headers)

# Step 6: Start the Flask server on the specified port
if __name__ == "__main__":
    app.run(port=args.port)