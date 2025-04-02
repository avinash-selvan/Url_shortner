from flask import Flask, request, redirect, jsonify
import random
import string

app = Flask(__name__)

# In-memory key-value store for URLs
url_mapping = {}

# Function to generate a short URL (random 6-character string)
def generate_short_url():
    characters = string.ascii_letters + string.digits  # a-z, A-Z, 0-9
    return ''.join(random.choices(characters, k=6))

# API: Shorten a URL
@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    long_url = data.get("url")

    if not long_url:
        return jsonify({"error": "URL is required"}), 400

    short_url = generate_short_url()
    url_mapping[short_url] = long_url  # Store mapping

    return jsonify({"short_url": f"http://localhost:5000/{short_url}"})

# API: Redirect to original URL
@app.route('/<short_url>')
def redirect_url(short_url):
    long_url = url_mapping.get(short_url)

    if long_url:
        return redirect(long_url)  # Redirect to the original URL
    else:
        return jsonify({"error": "Short URL not found"}), 404

# Run the Flask app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
