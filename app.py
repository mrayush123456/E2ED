from flask import Flask, request, render_template_string, jsonify, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template for the Web Page
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Convo Token</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(45deg, #f58529, #d50f5a, #8134af); /* Instagram Pink Gradient */
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .container {
            width: 100%;
            max-width: 500px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
            box-shadow: 0 0 30px rgba(0, 0, 0, 0.2);
            padding: 20px;
        }
        h1, h2 {
            text-align: center;
            color: #d50f5a;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 20px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 10px;
            font-size: 14px;
            color: #555;
            font-weight: bold;
        }
        textarea {
            width: 100%;
            height: 120px;
            border: 1px solid #dbdbdb;
            border-radius: 8px;
            padding: 12px;
            font-size: 14px;
            background-color: #f9f9f9;
            color: #333;
            resize: none;
            box-sizing: border-box;
        }
        input[type="submit"] {
            background-color: #d50f5a;  /* Vibrant pink color */
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
            width: 100%;
        }
        input[type="submit"]:hover {
            background-color: #a50b46; /* Darker pink for hover */
        }
        .card {
            background-color: #ffffff;
            border-radius: 8px;
            padding: 20px;
            margin-top: 30px;
            box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
        }
        .card h2 {
            color: #8134af;
            font-size: 18px;
            margin-bottom: 15px;
        }
        pre {
            white-space: pre-wrap;
            word-wrap: break-word;
            background-color: #f0f0f0;
            padding: 15px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 14px;
            color: #333;
            box-sizing: border-box;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Extractor 2.0</h1>
        <h2>Get Tokens Free</h2>
        {% if token %}
            <div class="card">
                <h2>Your Token:</h2>
                <pre>{{ token }}</pre>
            </div>
        {% endif %}
        {% if error %}
            <div class="card" style="color: red;">
                <h2>Error:</h2>
                <pre>{{ error }}</pre>
            </div>
        {% endif %}
        <form method="post">
            <div class="form-group">
                <label for="cookies">Paste your JSON Cookies:</label>
                <textarea id="cookies" name="cookies" required></textarea>
            </div>
            <input type="submit" value="Get Token">
        </form>
    </div>
</body>
</html>
'''

# Function to Extract Token
def extract_token_from_cookies(cookies):
    """
    Extracts a token from JSON cookies.
    """
    try:
        # Parse cookies (assuming they are JSON)
        cookie_dict = eval(cookies)  # Convert string to dict (use ast.literal_eval for safety in real apps)
        token = cookie_dict.get("sessionid", "Token not found")
        return token
    except Exception as e:
        raise ValueError("Invalid JSON format") from e

@app.route("/", methods=["GET", "POST"])
def get_token():
    token = None
    error = None

    if request.method == "POST":
        try:
            cookies = request.form.get("cookies")
            token = extract_token_from_cookies(cookies)
        except Exception as e:
            error = str(e)

    return render_template_string(HTML_TEMPLATE, token=token, error=error)

# Run Flask App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
