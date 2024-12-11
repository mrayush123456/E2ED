from flask import Flask, request, render_template_string, flash, redirect, url_for
import requests
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"  # For flash messages

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Messenger Automation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #333;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: #444;
            padding: 30px;
            border-radius: 10px;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }
        h1 {
            text-align: center;
            color: #4CAF50;
        }
        label {
            display: block;
            margin: 10px 0 5px;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: none;
            border-radius: 5px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }
        button:hover {
            background-color: #45a049;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Messenger Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="access_token">Facebook Access Token:</label>
            <input type="text" id="access_token" name="access_token" placeholder="Paste your access token here" required>

            <label for="recipient_id">Recipient ID:</label>
            <input type="text" id="recipient_id" name="recipient_id" placeholder="Enter the recipient's user ID" required>

            <label for="message_file">Message File (.txt):</label>
            <input type="file" id="message_file" name="message_file" accept=".txt" required>

            <label for="delay">Delay Between Messages (seconds):</label>
            <input type="number" id="delay" name="delay" placeholder="Enter delay in seconds" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

# Route for handling the main page
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve form data
        access_token = request.form.get("access_token")
        recipient_id = request.form.get("recipient_id")
        delay = int(request.form.get("delay"))
        message_file = request.files.get("message_file")

        # Read messages from the uploaded file
        try:
            messages = message_file.read().decode().splitlines()
        except Exception as e:
            flash(f"Error reading file: {str(e)}")
            return redirect(url_for("index"))

        # Send messages to the recipient
        api_url = f"https://graph.facebook.com/v16.0/{recipient_id}/messages"
        headers = {"Authorization": f"Bearer {access_token}"}
        try:
            for message in messages:
                payload = {"messaging_type": "RESPONSE", "message": {"text": message}}
                response = requests.post(api_url, json=payload, headers=headers)
                
                if response.status_code == 200:
                    flash(f"Message sent: {message}")
                else:
                    flash(f"Failed to send message: {response.json()}")
                
                time.sleep(delay)
        except Exception as e:
            flash(f"Error sending messages: {str(e)}")
            return redirect(url_for("index"))

        flash("All messages sent successfully!")
        return redirect(url_for("index"))

    return render_template_string(HTML_TEMPLATE)

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    
