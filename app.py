from flask import Flask, render_template, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

# Global variables for controlling the process
stop_flag = False
headers = {"User-Agent": "Mozilla/5.0"}

# Facebook Graph API Base URL
FB_GRAPH_API_URL = "https://graph.facebook.com/v16.0"

# HTML template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Messenger Bot</title>
    <style>
        body { font-family: Arial, sans-serif; background: rgb(34, 34, 34); color: white; margin: 0; padding: 0; }
        header { padding: 20px; text-align: center; background: rgb(60, 60, 60); }
        form { padding: 20px; background: rgb(50, 50, 50); max-width: 600px; margin: auto; border-radius: 10px; }
        button { padding: 10px 20px; background: rgb(100, 149, 237); border: none; color: white; border-radius: 5px; }
        button:hover { background: rgb(72, 125, 202); }
        input, textarea { width: 100%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
    </style>
</head>
<body>
    <header>
        <h1>Facebook Messenger Bot</h1>
    </header>
    <form id="messageForm">
        <label for="token">Access Token:</label>
        <input type="text" id="token" name="token" required>

        <label for="group_id">Target Group/Inbox ID:</label>
        <input type="text" id="group_id" name="group_id" required>

        <label for="txt_file">Message File:</label>
        <input type="file" id="txt_file" name="txt_file" accept=".txt" required>

        <label for="hatersname">Haters Name:</label>
        <input type="text" id="hatersname" name="hatersname">

        <label for="delay">Delay (seconds):</label>
        <input type="number" id="delay" name="delay" min="0" value="5">

        <button type="submit">Start Sending</button>
        <button type="button" onclick="stopSending()">Stop</button>
    </form>

    <script>
        function stopSending() {
            fetch('/stop', { method: 'POST' });
            alert('Message sending stopped.');
        }

        document.getElementById('messageForm').onsubmit = async (event) => {
            event.preventDefault();
            const formData = new FormData(event.target);
            const response = await fetch('/send', {
                method: 'POST',
                body: formData
            });
            const result = await response.json();
            alert(result.message);
        };
    </script>
</body>
</html>
"""

@app.route("/")
def home():
    """Render the home page."""
    return HTML_TEMPLATE

@app.route("/stop", methods=["POST"])
def stop():
    """Stop the message sending process."""
    global stop_flag
    stop_flag = True
    return jsonify({"message": "Message sending stopped."})

@app.route("/send", methods=["POST"])
def send_messages():
    """Send messages to the target group or inbox."""
    global stop_flag
    stop_flag = False

    # Get form data
    token = request.form.get("token")
    group_id = request.form.get("group_id")
    haters_name = request.form.get("hatersname")
    delay = int(request.form.get("delay", 5))
    txt_file = request.files.get("txt_file")

    # Read the message content from the TXT file
    if not txt_file:
        return jsonify({"message": "Message file not uploaded."})
    messages = txt_file.read().decode("utf-8").strip().split("\n")

    # Define the worker function for sending messages
    def message_worker():
        nonlocal stop_flag
        for message in messages:
            if stop_flag:
                break
            # Customize the message with haters' name if provided
            final_message = f"Hello {haters_name}, {message}" if haters_name else message

            # Send the message via Facebook Graph API
            response = requests.post(
                f"{FB_GRAPH_API_URL}/{group_id}/messages",
                headers=headers,
                params={
                    "access_token": token,
                    "message": final_message,
                }
            )

            if response.status_code == 200:
                print(f"[SUCCESS] Sent: {final_message}")
            else:
                print(f"[ERROR] Failed to send: {response.json().get('error', {}).get('message', 'Unknown error')}")

            time.sleep(delay)

    # Start the worker thread
    threading.Thread(target=message_worker).start()
    return jsonify({"message": "Messages are being sent."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
            
