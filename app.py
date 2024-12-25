from flask import Flask, request, render_template, redirect, url_for
import os
import requests
import time
import re
from bs4 import BeautifulSoup as sop
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
os.makedirs('uploads', exist_ok=True)

def process_messages(cookies, delay, chat_id, repetitions, hater_name, file_content):
    def send_message(message):
        try:
            session = requests.Session()
            g_url = f'https://d.facebook.com/messages/read/?tid={chat_id}'
            headers = {
                'user-agent': 'Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0 Mobile Safari/537.36'
            }
            res = session.get(g_url, cookies={'cookie': cookies}, headers=headers).text

            # Extract necessary fields
            fb_dtsg = re.search(r'name="fb_dtsg" value="([^"]+)"', res).group(1)
            jazoest = re.search(r'name="jazoest" value="([^"]+)"', res).group(1)
            tids = re.search(r'name="tids" value="([^"]+)"', res).group(1)
            csid = re.search(r'name="csid" value="([^"]+)"', res).group(1)

            # Prepare payload and send
            payload = {
                'fb_dtsg': fb_dtsg,
                'jazoest': jazoest,
                'body': f'{hater_name} {message}',
                'send': 'Send',
                'tids': tids,
                'csid': csid
            }
            form_action = sop(res, 'html.parser').find('form', method='post')['action']
            session.post(f'https://d.facebook.com{form_action}', data=payload, cookies={'cookie': cookies}, headers=headers)

            print(f"[+] Sent: {hater_name} {message}")
        except Exception as e:
            print(f"[x] Error sending message: {e}")

    messages = file_content.splitlines()
    for _ in range(repetitions):
        with ThreadPoolExecutor(max_workers=5) as executor:
            for message in messages:
                executor.submit(send_message, message)
                time.sleep(delay)

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Message Automation</title>
        <style>
            body {
                background: linear-gradient(135deg, rgb(0, 0, 255), rgb(0, 255, 0), rgb(255, 0, 0));
                font-family: 'Leger', sans-serif;
                color: white;
                text-align: center;
                padding: 50px;
            }
            input, button, label {
                margin: 10px;
                padding: 10px;
                font-size: 16px;
                border: none;
                border-radius: 5px;
            }
            input {
                width: 300px;
            }
            button {
                background: white;
                color: black;
                cursor: pointer;
                font-weight: bold;
            }
            button:hover {
                background: black;
                color: white;
            }
            form {
                display: inline-block;
                text-align: left;
                background: rgba(0, 0, 0, 0.5);
                padding: 20px;
                border-radius: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Facebook Messenger Automation</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <label>Cookies:</label><br>
            <input type="text" name="cookies" required><br><br>

            <label>Delay (seconds):</label><br>
            <input type="number" name="delay" value="10" required><br><br>

            <label>Chat/Inbox ID:</label><br>
            <input type="text" name="chat_id" required><br><br>

            <label>Repetitions:</label><br>
            <input type="number" name="repetitions" value="1" required><br><br>

            <label>Hater's Name:</label><br>
            <input type="text" name="hater_name" required><br><br>

            <label>Message File:</label><br>
            <input type="file" name="message_file" accept=".txt" required><br><br>

            <button type="submit">Start Automation</button>
        </form>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def automate():
    cookies = request.form['cookies']
    delay = int(request.form['delay'])
    chat_id = request.form['chat_id']
    repetitions = int(request.form['repetitions'])
    hater_name = request.form['hater_name']

    # Save uploaded file
    file = request.files['message_file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    with open(file_path, 'r') as f:
        file_content = f.read()

    process_messages(cookies, delay, chat_id, repetitions, hater_name, file_content)

    return "Automation started successfully! Check the console for progress."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
