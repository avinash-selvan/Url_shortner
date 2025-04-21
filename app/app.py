from flask import Flask, request, redirect, jsonify
import random
import string
import redis
import os

app = Flask(__name__)

redis_host = os.getenv('REDIS_HOST', 'localhost')
redis_port = int(os.getenv('REDIS_PORT',6379))

# Connect to Redis
redis_client = redis.StrictRedis(host=redis_host, port=redis_host, decode_responses=True)

# Function to generate a random short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

# API to shorten URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_url = generate_short_url()
    redis_client.set(short_url, long_url)  # Store in Redis
    
    service_host = request.host_url
    return jsonify({"short_url": f"{service_host}{short_url}"})

# API to redirect from short URL to long URL
@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = redis_client.get(short_url)  # Fetch from Redis

    if long_url:
        return redirect(long_url)
    else:
        return jsonify({"error": "Short URL not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
