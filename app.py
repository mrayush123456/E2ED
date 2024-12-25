from flask import Flask, request, render_template, redirect, url_for
import os
import time
import requests
import threading

app = Flask(__name__)

# Static headers
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

stop_flag = False

@app.route('/')
def index():
    return '''
        <html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Automation</title>
    <style>
        /* CSS for styling elements */
        body {
            background-color: black;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
            padding-top: 50px;
        }
        .container {
            margin-top: 50px;
            max-width: 600px;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
            background: linear-gradient(to right, rgba(0, 255, 255, 0.5), rgba(255, 0, 255, 0.5));
        }
        .form-control {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border-radius: 5px;
            border: 1px solid white;
            background: transparent;
            color: white;
        }
        .btn-submit {
            background-color: #4CAF50;
            color: white;
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            border: none;
        }
        .btn-submit:hover {
            background-color: #45a049;
        }
        .btn-stop {
            background-color: red;
            color: white;
            padding: 12px 24px;
            border-radius: 10px;
            cursor: pointer;
            border: none;
        }
        .btn-stop:hover {
            background-color: darkred;
        }
        .laser-light {
            color: rgb(255, 0, 0);
            text-shadow: 0 0 10px rgb(255, 0, 0), 0 0 20px rgb(255, 0, 0);
            font-size: 50px;
            animation: laser 1.5s infinite alternate;
        }
        @keyframes laser {
            0% { text-shadow: 0 0 10px rgb(255, 0, 0), 0 0 20px rgb(255, 0, 0); }
            100% { text-shadow: 0 0 20px rgb(255, 255, 0), 0 0 30px rgb(255, 255, 0); }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="laser-light">Facebook Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <div>
                <input type="text" name="thread_id" class="form-control" placeholder="Thread ID" required>
                <input type="file" name="cookie_file" class="form-control" required>
                <input type="file" name="messages_file" class="form-control" accept=".txt" required>
                <input type="text" name="hater_name" class="form-control" placeholder="Hater Name" required>
                <input type="number" name="delay" class="form-control" placeholder="Delay in seconds" required>
            </div>
            <button type="submit" class="btn-submit">Start Messaging</button>
        </form>
        <form action="/stop" method="POST">
            <button type="submit" class="btn-stop">Stop Messaging</button>
        </form>
    </div>
</body>
</html>
    '''

@app.route('/', methods=['POST'])
def send_message():
    global stop_flag
    stop_flag = False

    # Retrieve form data
    thread_id = request.form['thread_id']
    cookie_file = request.files['cookie_file']
    messages_file = request.files['messages_file']
    hater_name = request.form['hater_name']
    delay = int(request.form['delay'])

    # Read cookie
    cookies = cookie_file.read().decode().splitlines()

    # Read messages
    messages = messages_file.read().decode().splitlines()

    # Define post URL
    post_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'

    # Send messages in a separate thread to avoid blocking
    def message_thread():
        for message_index, message in enumerate(messages):
            if stop_flag:
                print("[x] Stopping message sending.")
                break

            # Choose a cookie for this message
            cookie = cookies[message_index % len(cookies)]
            params = {'access_token': cookie, 'message': f"{hater_name} {message}"}

            # Send the message
            response = requests.post(post_url, json=params, headers=headers)
            if response.ok:
                print(f"[+] Sent Message No. {message_index + 1}: {message}")
            else:
                print(f"[x] Failed to Send Message No. {message_index + 1}: {message}")

            time.sleep(delay)

    # Start the message sending thread
    thread = threading.Thread(target=message_thread)
    thread.start()

    return redirect(url_for('index'))

@app.route('/stop', methods=['POST'])
def stop_sending():
    global stop_flag
    stop_flag = True
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
