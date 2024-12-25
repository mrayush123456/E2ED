from flask import Flask, request, redirect, url_for
import os
import time
import requests
import threading

app = Flask(__name__)
stop_flag = threading.Event()  # Stop flag for halting the process

# RGB Laser Light Background Animation CSS
laser_background = """
    <style>
        body {
            margin: 0;
            height: 100vh;
            background: black;
            overflow: hidden;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .laser {
            position: absolute;
            width: 100%;
            height: 100%;
            z-index: -1;
            animation: laser 10s infinite;
        }
        @keyframes laser {
            0% { background: radial-gradient(circle, red, transparent 50%); }
            25% { background: radial-gradient(circle, blue, transparent 50%); }
            50% { background: radial-gradient(circle, green, transparent 50%); }
            75% { background: radial-gradient(circle, yellow, transparent 50%); }
            100% { background: radial-gradient(circle, red, transparent 50%); }
        }
        .container {
            background-color: rgba(0, 0, 0, 0.8);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            max-width: 500px;
        }
        .form-control {
            margin: 10px 0;
            padding: 10px;
            border-radius: 5px;
            border: 1px solid white;
            width: 100%;
        }
        .btn {
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            color: white;
            cursor: pointer;
        }
        .btn-submit {
            background-color: green;
        }
        .btn-stop {
            background-color: red;
        }
    </style>
"""

# HTML Template
html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Automation</title>
    {laser_background}
</head>
<body>
    <div class="laser"></div>
    <div class="container">
        <h2>Facebook Automation</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <input class="form-control" type="text" name="cookie" placeholder="Enter Cookie" required>
            <input class="form-control" type="file" name="token_file" accept=".txt" required>
            <input class="form-control" type="file" name="message_file" accept=".txt" required>
            <input class="form-control" type="text" name="haters_name" placeholder="Enter Hater's Name" required>
            <input class="form-control" type="number" name="delay" placeholder="Delay (seconds)" required>
            <button class="btn btn-submit" type="submit">Start Automation</button>
        </form>
        <form method="POST" action="/stop">
            <button class="btn btn-stop" type="submit">Stop Automation</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    global stop_flag
    if request.method == "POST":
        stop_flag.clear()  # Reset the stop flag

        # Get form data
        cookie = request.form["cookie"]
        delay = int(request.form["delay"])
        haters_name = request.form["haters_name"]

        # Read uploaded files
        token_file = request.files["token_file"]
        tokens = token_file.read().decode().splitlines()

        message_file = request.files["message_file"]
        messages = message_file.read().decode().splitlines()

        # Start automation in a separate thread
        threading.Thread(target=automation_process, args=(cookie, tokens, messages, haters_name, delay)).start()

        return redirect(url_for("index"))

    return html_template

@app.route("/stop", methods=["POST"])
def stop():
    global stop_flag
    stop_flag.set()  # Signal the process to stop
    return redirect(url_for("index"))

def automation_process(cookie, tokens, messages, haters_name, delay):
    global stop_flag
    post_url = "https://graph.facebook.com/v15.0/me/messages"

    for index, (token, message) in enumerate(zip(tokens, messages)):
        if stop_flag.is_set():
            print("[!] Stopped by User")
            break

        headers = {
            "Authorization": f"Bearer {token}",
            "Cookie": cookie
        }
        data = {
            "message": f"{haters_name} {message}",
        }

        try:
            response = requests.post(post_url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"[+] Message {index + 1} sent successfully.")
            else:
                print(f"[x] Failed to send message {index + 1}: {response.text}")
        except Exception as e:
            print(f"[!] Error: {e}")

        time.sleep(delay)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
