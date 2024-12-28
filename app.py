from flask import Flask, request, render_template_string, jsonify, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Utility Tools</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #ff7e5f, #feb47b);
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        label {
            font-weight: bold;
            margin-top: 10px;
            display: block;
        }
        textarea, input {
            width: 100%;
            padding: 10px;
            margin-top: 5px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
        }
        button {
            background: linear-gradient(to right, #ff416c, #ff4b2b);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin-top: 10px;
            width: 100%;
        }
        button:hover {
            background: linear-gradient(to right, #ff4b2b, #ff416c);
        }
        pre {
            background: #f9f9f9;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
        .success {
            color: green;
            margin-bottom: 10px;
        }
        .error {
            color: red;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Utility Tools</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
        {% endwith %}

        <!-- Cookie to JSON -->
        <form action="/cookie-to-json" method="POST">
            <label for="cookieInput">Convert Cookie to JSON:</label>
            <textarea id="cookieInput" name="cookie" placeholder="Paste cookies here..." required></textarea>
            <button type="submit">Convert to JSON</button>
        </form>
        
        <h3>JSON Output:</h3>
        <pre>{{ cookie_json }}</pre>

        <hr>

        <!-- Instagram Token Extractor -->
        <form action="/extract-token" method="POST">
            <label for="urlInput">Extract Instagram Token:</label>
            <textarea id="urlInput" name="url" placeholder="Paste Instagram URL with token..." required></textarea>
            <button type="submit">Extract Token</button>
        </form>

        <h3>Token Output:</h3>
        <pre>{{ token }}</pre>

        <hr>

        <!-- JSON Converter -->
        <form action="/convert-to-json" method="POST">
            <label for="textInput">Convert Text to JSON:</label>
            <textarea id="textInput" name="text" placeholder="Enter text here..." required></textarea>
            <button type="submit">Convert to JSON</button>
        </form>

        <h3>Converted JSON:</h3>
        <pre>{{ json_output }}</pre>
    </div>
</body>
</html>
'''

# Utility Functions
def parse_cookies(cookie_string):
    """
    Parse cookies into JSON format.
    """
    cookies = {}
    for pair in cookie_string.split(";"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            cookies[key.strip()] = value.strip()
    return cookies

def extract_instagram_token(url):
    """
    Extract token from Instagram URL or string.
    """
    match = re.search(r"access_token=([a-zA-Z0-9_\-]+)", url)
    if match:
        return match.group(1)
    return None

# Flask Routes
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE, cookie_json="", token="", json_output="")

@app.route("/cookie-to-json", methods=["POST"])
def cookie_to_json():
    try:
        cookie_string = request.form["cookie"]
        cookies = parse_cookies(cookie_string)
        return render_template_string(HTML_TEMPLATE, cookie_json=jsonify(cookies).get_data(as_text=True), token="", json_output="")
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for("home"))

@app.route("/extract-token", methods=["POST"])
def extract_token():
    try:
        url = request.form["url"]
        token = extract_instagram_token(url)
        if token:
            flash("Token extracted successfully!", "success")
            return render_template_string(HTML_TEMPLATE, cookie_json="", token=token, json_output="")
        else:
            flash("No token found in the provided URL or string.", "error")
            return redirect(url_for("home"))
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for("home"))

@app.route("/convert-to-json", methods=["POST"])
def convert_to_json():
    try:
        raw_text = request.form["text"]
        json_output = parse_cookies(raw_text)
        return render_template_string(HTML_TEMPLATE, cookie_json="", token="", json_output=jsonify(json_output).get_data(as_text=True))
    except Exception as e:
        flash(f"Error: {e}", "error")
        return redirect(url_for("home"))

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
        
