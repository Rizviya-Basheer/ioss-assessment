from flask import Flask, render_template, request, redirect, jsonify
import string, random, datetime

app = Flask(__name__)

# In-memory URL storage
url_store = {}

def generate_short_code(length=6):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    original_url = data.get("url")
    if not original_url:
        return jsonify({"error": "URL required"}), 400

    short_code = generate_short_code()
    url_store[short_code] = {
        "url": original_url,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url})

@app.route("/<short_code>")
def redirect_to_url(short_code):
    entry = url_store.get(short_code)
    if entry:
        return redirect(entry["url"])
    return jsonify({"error": "Short URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)