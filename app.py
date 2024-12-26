from flask import Flask, request, redirect, url_for
import requests
import time
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def send_message():
    if request.method == "POST":
        # Get user inputs
        fb_token = request.form.get("fb_token")
        delay = int(request.form.get("delay", 1))
        message = request.form.get("message", "")

        # Get uploaded TXT file
        inbox_file = request.files["inbox_file"]
        inbox_ids = inbox_file.read().decode("utf-8").splitlines()

        # Create a folder to store logs
        folder_name = "logs"
        os.makedirs(folder_name, exist_ok=True)

        # Log details
        with open(os.path.join(folder_name, "inbox_ids.txt"), "w") as f:
            f.write("\n".join(inbox_ids))

        with open(os.path.join(folder_name, "message.txt"), "w") as f:
            f.write(message)

        # Send messages
        for inbox_id in inbox_ids:
            try:
                url = f"https://graph.facebook.com/v15.0/{inbox_id}/messages"
                payload = {"message": message}
                headers = {"Authorization": f"Bearer {fb_token}"}

                response = requests.post(url, json=payload, headers=headers)

                if response.ok:
                    print(f"[+] Message sent to {inbox_id}")
                else:
                    print(f"[x] Failed to send message to {inbox_id}: {response.text}")

                time.sleep(delay)
            except Exception as e:
                print(f"Error sending message to {inbox_id}: {e}")
                time.sleep(30)  # Wait before retrying

        return redirect(url_for("send_message"))

    # Render the HTML form
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Facebook Automation</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                width: 400px;
            }
            .form-control {
                width: 100%;
                padding: 10px;
                margin: 10px 0;
                border: 1px solid #ccc;
                border-radius: 4px;
            }
            .btn-submit {
                background: #4CAF50;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
            }
            .btn-submit:hover {
                background: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Inbox Automation</h2>
            <form method="POST" enctype="multipart/form-data">
                <label for="fb_token">Enter Facebook Token:</label>
                <input type="text" id="fb_token" name="fb_token" class="form-control" required>

                <label for="inbox_file">Upload Inbox IDs (TXT):</label>
                <input type="file" id="inbox_file" name="inbox_file" class="form-control" accept=".txt" required>

                <label for="message">Message:</label>
                <textarea id="message" name="message" class="form-control" rows="4" required></textarea>

                <label for="delay">Delay (in seconds):</label>
                <input type="number" id="delay" name="delay" class="form-control" min="1" value="1" required>

                <button type="submit" class="btn-submit">Send Messages</button>
            </form>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
            
