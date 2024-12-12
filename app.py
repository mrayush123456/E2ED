from flask import Flask, request, render_template_string, flash, redirect, url_for
from fbchat import Client
from fbchat.models import Message
import time

app = Flask(__name__)
app.secret_key = "your_secret_key"

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Messenger Automation</title>
</head>
<body>
    <h1>Facebook Messenger Automation</h1>
    <form method="POST" enctype="multipart/form-data">
        <label for="cookie">Facebook Session Cookie:</label>
        <textarea id="cookie" name="cookie" required></textarea>
        <br><br>
        <label for="thread_id">Thread/Group ID:</label>
        <input type="text" id="thread_id" name="thread_id" required>
        <br><br>
        <label for="message_file">Message File (.txt):</label>
        <input type="file" id="message_file" name="message_file" accept=".txt" required>
        <br><br>
        <label for="delay">Delay (in seconds):</label>
        <input type="number" id="delay" name="delay" required>
        <br><br>
        <button type="submit">Send Messages</button>
    </form>
</body>
</html>
'''

@app.route("/", methods=["GET", "POST"])
def messenger():
    if request.method == "POST":
        try:
            # Get form data
            session_cookies = request.form["cookie"]
            thread_id = request.form["thread_id"]
            delay = int(request.form["delay"])
            message_file = request.files["message_file"]

            # Parse messages from file
            messages = message_file.read().decode("utf-8").splitlines()
            if not messages:
                flash("Message file is empty!", "error")
                return redirect(url_for("messenger"))

            # Initialize Facebook Messenger Client
            client = Client(session_cookies=session_cookies)
            print("[INFO] Logged in to Facebook Messenger")

            # Send messages
            for message in messages:
                print(f"[INFO] Sending message to {thread_id}: {message}")
                client.send(Message(text=message), thread_id=thread_id, thread_type=client.THREAD_TYPE_GROUP)
                print(f"[SUCCESS] Message sent: {message}")
                time.sleep(delay)

            flash("Messages sent successfully!", "success")
            return redirect(url_for("messenger"))

        except Exception as e:
            flash(f"An error occurred: {e}", "error")
            return redirect(url_for("messenger"))

    return render_template_string(HTML_TEMPLATE)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
