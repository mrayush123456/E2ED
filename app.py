from flask import Flask, request, redirect, url_for
import os
import time
import threading
import requests

app = Flask(__name__)
active_threads = []

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}


@app.route('/')
def index():
    return '''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Automation</title>
            <style>
                body {
                    background: black;
                    color: white;
                    font-family: Arial, sans-serif;
                    animation: rgb-background 5s infinite;
                }
                @keyframes rgb-background {
                    0% { background-color: red; }
                    25% { background-color: green; }
                    50% { background-color: blue; }
                    75% { background-color: yellow; }
                    100% { background-color: purple; }
                }
                .container {
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    background: rgba(0, 0, 0, 0.7);
                    border-radius: 10px;
                    box-shadow: 0 0 10px white;
                }
                label {
                    display: block;
                    margin-bottom: 10px;
                }
                input, button {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 20px;
                    border-radius: 5px;
                    border: none;
                }
                button {
                    background-color: green;
                    color: white;
                    font-size: 16px;
                    cursor: pointer;
                }
                button:hover {
                    background-color: red;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Facebook Automation</h1>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="groupId">Target Group Chat ID:</label>
                    <input type="text" id="groupId" name="groupId" required>

                    <label for="cookies">Paste Cookies:</label>
                    <textarea id="cookies" name="cookies" rows="4" required></textarea>

                    <label for="txtFile">Upload TXT File:</label>
                    <input type="file" id="txtFile" name="txtFile" accept=".txt" required>

                    <label for="hatersName">Hater's Name:</label>
                    <input type="text" id="hatersName" name="hatersName" required>

                    <label for="delay">Delay (Seconds):</label>
                    <input type="number" id="delay" name="delay" min="1" value="5" required>

                    <button type="submit">Start Automation</button>
                </form>
                <form action="/stop" method="post">
                    <button type="submit">Stop Automation</button>
                </form>
            </div>
        </body>
        </html>
    '''


@app.route('/', methods=['POST'])
def start_automation():
    group_id = request.form['groupId']
    cookies = request.form['cookies']
    delay = int(request.form['delay'])
    haters_name = request.form['hatersName']

    txt_file = request.files['txtFile']
    messages = txt_file.read().decode().splitlines()

    def automation_task():
        try:
            post_url = f'https://graph.facebook.com/v15.0/{group_id}/'
            for message in messages:
                payload = {'message': f"{haters_name}: {message}", 'cookies': cookies}
                response = requests.post(post_url, headers=headers, json=payload)
                if response.ok:
                    print(f"[SUCCESS] Sent message: {message}")
                else:
                    print(f"[FAILED] Message: {message}, Response: {response.text}")
                time.sleep(delay)
        except Exception as e:
            print(f"Error: {e}")

    thread = threading.Thread(target=automation_task)
    active_threads.append(thread)
    thread.start()

    return redirect(url_for('index'))


@app.route('/stop', methods=['POST'])
def stop_automation():
    for thread in active_threads:
        if thread.is_alive():
            thread.join(timeout=1)
    active_threads.clear()
    print("[INFO] Automation stopped.")
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
