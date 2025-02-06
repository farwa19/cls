import argparse 
import requests
import hashlib
from flask import Flask, request, Response
app = Flask(__name__)


cache = {}

parser = argparse.ArgumentParser()
print("kl")

parser.add_argument("--port", type=int, required=False, help="Port number")
parser.add_argument("--origin", type=str, required=True, help="url")

args = parser.parse_args()

# Access the arguments
print(f"Port: {args.port}")
print(f"Origin: {args.origin}")
if args.port:
    url = f"{args.origin}:{args.port}/api"
else:
    url = args.origin
cach = hashlib.md5((url).encode()).hexdigest()
if cach in cache:
    print(cache[cash])
else:



# Send the request
    response = requests.get(url)

    


# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")