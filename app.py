from flask import Flask, render_template, request, redirect, url_for, jsonify
import time
import os
import requests
from threading import Thread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import base64

app = Flask(__name__)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}

@app.route('/')
def index():
    return '''
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Automation</title>
        <style>
            body {
                background: rgb(0,0,0);
                background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(255,0,150,1) 35%, rgba(0,255,255,1) 100%);
                animation: gradient 3s ease infinite;
                height: 100vh;
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }
            @keyframes gradient {
                0% {background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(255,0,150,1) 35%, rgba(0,255,255,1) 100%);}
                50% {background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(255,0,255,1) 35%, rgba(0,255,0,1) 100%);}
                100% {background: linear-gradient(90deg, rgba(0,0,0,1) 0%, rgba(255,0,150,1) 35%, rgba(0,255,255,1) 100%);}
            }
            .container {
                width: 400px;
                padding: 30px;
                background: rgba(0, 0, 0, 0.5);
                border-radius: 10px;
                box-shadow: 0 0 20px rgba(0, 0, 0, 0.7);
            }
            label, button, input {
                width: 100%;
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 5px;
                border: 1px solid white;
            }
            button {
                background-color: #4CAF50;
                color: white;
                cursor: pointer;
            }
            button:hover {
                background-color: #45a049;
            }
            input[type="file"] {
                background-color: transparent;
                border: none;
                color: white;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Automation</h2>
            <form action="/start" method="POST" enctype="multipart/form-data">
                <label for="cookies">Paste Cookies Here:</label>
                <textarea name="cookies" rows="4" placeholder="Enter Facebook Cookies"></textarea>

                <label for="target_group">Target Group Chat/Inbox URL:</label>
                <input type="text" name="target_group" placeholder="Group/Inbox URL">

                <label for="file">Select a Message File (.txt):</label>
                <input type="file" name="file" accept=".txt" required>

                <label for="haters_name">Enter Hater's Name:</label>
                <input type="text" name="haters_name" placeholder="Hater's Name" required>

                <label for="delay">Delay (in seconds):</label>
                <input type="number" name="delay" value="5" required>

                <button type="submit">Start Automation</button>
            </form>
            <button onclick="window.location.href='/stop'">Stop Automation</button>
        </div>
    </body>
    </html>
    '''

@app.route('/start', methods=['POST'])
def start_automation():
    cookies = request.form['cookies']
    target_group = request.form['target_group']
    delay = int(request.form['delay'])
    file = request.files['file']
    hater_name = request.form['haters_name']

    # Save the uploaded file
    file_path = os.path.join('uploads', file.filename)
    os.makedirs('uploads', exist_ok=True)
    file.save(file_path)

    # Start a background thread for the automation
    thread = Thread(target=facebook_automation, args=(cookies, target_group, file_path, hater_name, delay))
    thread.start()

    return redirect(url_for('index'))

@app.route('/stop')
def stop_automation():
    # Implement logic to stop the automation (use shared flags or manage threads)
    return jsonify({"status": "Automation Stopped"}), 200

def facebook_automation(cookies, target_group, file_path, hater_name, delay):
    # Load Facebook cookies into the WebDriver
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    driver = webdriver.Chrome(options=options)

    driver.get('https://www.facebook.com/')
    driver.add_cookie({'name': 'cookie_name', 'value': cookies})

    driver.get(target_group)

    # Read the message file
    with open(file_path, 'r') as file:
        messages = file.readlines()

    # Send messages with delay
    for message in messages:
        # Find the message input field and send the message
        message_box = driver.find_element_by_xpath("//textarea")
        message_box.send_keys(f"{hater_name}: {message}")
        
        send_button = driver.find_element_by_xpath("//button[@type='submit']")
        send_button.click()

        time.sleep(delay)

    driver.quit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
        
