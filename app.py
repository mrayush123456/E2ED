from flask import Flask, request, redirect, url_for
import time
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '''
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Inbox Message Sender</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    background: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                input, button, label {
                    width: 100%;
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ccc;
                }
                button {
                    background-color: #4CAF50;
                    color: white;
                    cursor: pointer;
                }
                button:hover {
                    background-color: #45a049;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Facebook Inbox Message Sender</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="conversationId">Conversation ID:</label>
                    <input type="text" id="conversationId" name="conversationId" placeholder="Enter target conversation ID" required>
                    
                    <label for="token">Access Token:</label>
                    <input type="text" id="token" name="token" placeholder="Paste your Facebook access token here" required>
                    
                    <label for="clientId">Client ID:</label>
                    <input type="text" id="clientId" name="clientId" placeholder="Enter your client ID here" required>
                    
                    <label for="messageFile">Upload Messages File (TXT):</label>
                    <input type="file" id="messageFile" name="messageFile" accept=".txt" required>
                    
                    <label for="delay">Delay Between Messages (Seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" min="1" required>
                    
                    <button type="submit">Submit</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    # Retrieve form data
    conversation_id = request.form.get('conversationId')
    token = request.form.get('token')
    client_id = request.form.get('clientId')
    delay = int(request.form.get('delay'))

    # Read the messages from the uploaded TXT file
    message_file = request.files['messageFile']
    messages = message_file.read().decode().splitlines()

    # Facebook API URL for sending messages
    url = f"https://graph.facebook.com/v15.0/{conversation_id}/messages"

    # Headers for the HTTP request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Client-ID': client_id
    }

    success_count = 0

    # Loop through the messages and send them
    for i, message in enumerate(messages):
        data = {
            "messaging_type": "RESPONSE",
            "message": {"text": message}
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"[{i+1}/{len(messages)}] Message sent successfully: {message}")
                success_count += 1
            else:
                print(f"[{i+1}/{len(messages)}] Failed to send message: {message}")
                print(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[{i+1}/{len(messages)}] Exception occurred: {e}")

        # Wait for the specified delay before sending the next message
        time.sleep(delay)

    print(f"Finished. {success_count}/{len(messages)} messages sent successfully.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
