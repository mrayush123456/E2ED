from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML Template as a Python string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cookies to JSON Converter</title>
    <style>
        /* Global Styles */
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(to right, #f953c6, #b91d73);
            color: #fff;
            margin: 0;
            padding: 20px;
        }

        h1 {
            text-align: center;
            color: #fff;
            font-size: 2.5em;
        }

        .container {
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
        }

        label {
            font-weight: bold;
            margin-top: 10px;
            display: block;
            color: #ffebf1;
        }

        textarea {
            width: 100%;
            height: 100px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 8px;
            margin-top: 5px;
            box-sizing: border-box;
            font-size: 1em;
            color: #333;
        }

        button {
            background: linear-gradient(to right, #f953c6, #b91d73);
            color: white;
            padding: 10px 15px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-top: 15px;
            width: 100%;
            font-size: 1.2em;
            transition: transform 0.3s;
        }

        button:hover {
            background: linear-gradient(to right, #b91d73, #f953c6);
            transform: scale(1.05);
        }

        h2 {
            margin-top: 20px;
            font-size: 1.5em;
        }

        pre {
            background: rgba(255, 255, 255, 0.1);
            color: #fff;
            padding: 10px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 1em;
        }

        .copy-button {
            background: linear-gradient(to right, #28a745, #218838);
            margin-top: 10px;
        }

        .copy-button:hover {
            background: linear-gradient(to right, #218838, #28a745);
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cookies to JSON Converter</h1>
        <form id="cookieForm">
            <label for="cookies">Paste Your Simple Cookie Here:</label>
            <textarea id="cookies" name="cookies" placeholder="datr=V7QPZzH8-GBiYnbp3ZkAksOB; sb=V7QPZwHEDTWR226ath-V0gBi;"></textarea>
            <button type="submit">Convert to JSON</button>
        </form>
        <h2>JSON Result:</h2>
        <pre id="jsonOutput"></pre>
        <button id="copyButton" class="copy-button" style="display:none;">Copy to Clipboard</button>
    </div>

    <script>
        document.getElementById('cookieForm').onsubmit = async function(event) {
            event.preventDefault();
            const cookies = document.getElementById('cookies').value;
            const response = await fetch('/convert', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({ cookies })
            });
            const jsonOutput = await response.json();
            document.getElementById('jsonOutput').textContent = JSON.stringify(jsonOutput, null, 4);
            document.getElementById('copyButton').style.display = 'block'; // Show button
        }

        document.getElementById('copyButton').onclick = function() {
            const jsonText = document.getElementById('jsonOutput').textContent;
            navigator.clipboard.writeText(jsonText).then(() => {
                alert('JSON copied successfully!');
            }).catch(err => {
                alert('Error copying JSON: ', err);
            });
        }
    </script>
</body>
</html>
"""

# Utility function to parse cookies
def parse_cookies(cookie_string):
    """
    Parse cookies into a dictionary format.
    """
    cookies = {}
    for pair in cookie_string.split(";"):
        if "=" in pair:
            key, value = pair.split("=", 1)
            cookies[key.strip()] = value.strip()
    return cookies

# Flask Routes
@app.route("/", methods=["GET"])
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        cookies = request.form.get("cookies", "")
        parsed_cookies = parse_cookies(cookies)
        return jsonify(parsed_cookies)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

