from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# HTML code as a template string
html_code = """
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
        /* Rest of your CSS styles */
    </style>
</head>
<body>
    <div class="container">
        <h1>JSON Converter</h1>
        <h2>Vists: <span id="visitorCount">1555</span></h2>
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
            document.getElementById('copyButton').style.display = 'block';
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

@app.route('/')
def home():
    return render_template_string(html_code)

@app.route('/convert', methods=['POST'])
def convert():
    cookies = request.form.get('cookies')
    if not cookies:
        return jsonify({"error": "No cookies provided"}), 400

    cookie_dict = {}
    for pair in cookies.split(';'):
        if '=' in pair:
            key, value = pair.strip().split('=', 1)
            cookie_dict[key] = value

    return jsonify(cookie_dict)

if __name__ == '__main__':
    app.run(debug=True)
    
