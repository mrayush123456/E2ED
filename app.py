from flask import Flask, request, render_template_string, flash, redirect, url_for
from fbchat import Client
from fbchat.models import Message
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FB Messenger Group Chat</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
            width: 400px;
        }
        h1 {
            text-align: center;
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin: 10px 0 5px;
            font-weight: bold;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        button {
            background-color: #007bff;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .info {
            font-size: 12px;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Messenger Group</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label for="c_user">Session Cookie (c_user):</label>
            <input type="text" id="c_user" name="c_user" required>

            <label for="xs">Session Cookie (xs):</label>
            <input type="text" id="xs" name="xs" required>

            <label for="group_id">Group Chat ID:</label>
            <input type="text" id="group_id" name="group_id" required>

            <label for="message_file">Message File:</label>
            <input type="file" id="message_file" name="message_file" required>
            <p class="info">Upload a .txt file containing messages (one per line).</p>

            <label for="delay">Delay (in seconds):</label>
            <input type="number" id="delay" name="delay" min="1" required>

            <button type="submit">Send Messages</button>
        </form>
    </div>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def messenger_group():
    if request.method == "POST":
        try:
            # Get form data
            c_user = request.form["c_user"]
            xs = request.form["xs"]
            group_id = request.form["group_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Read messages from file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("messenger_group"))

            # Initialize FBChat Client with session cookies
            session_cookies = {"c_user": c_user, "xs": xs}
            client = Client(session_cookies=session_cookies)
            print("[INFO] Logged in successfully!")

            # Send messages to group chat
            for message in messages:
                print(f"[INFO] Sending message to group {group_id}: {message}")
                client.send(Message(text=message), thread_id=group_id, thread_type=client.THREAD_TYPE_GROUP)
                time.sleep(delay)

            client.logout()
            flash("Messages sent successfully!", "success")
            return redirect(url_for("messenger_group"))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for("messenger_group"))

    return render_template_string(HTML_TEMPLATE)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
