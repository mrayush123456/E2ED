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
            <title>Facebook Inbox Messenger</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                    padding: 20px;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    background: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }
                label, input, button, textarea {
                    width: 100%;
                    margin: 10px 0;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ced4da;
                }
                button {
                    background-color: #007bff;
                    color: white;
                    cursor: pointer;
                    border: none;
                }
                button:hover {
                    background-color: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Facebook Inbox Messenger</h2>
                <form action="/" method="post" enctype="multipart/form-data">
                    <label for="conversationId">Conversation ID:</label>
                    <input type="text" id="conversationId" name="conversationId" placeholder="Enter the target conversation ID" required>
                    
                    <label for="token">Access Token:</label>
                    <textarea id="token" name="token" rows="4" placeholder="Paste your Facebook access token here" required></textarea>
                    
                    <label for="messageFile">Messages File (TXT):</label>
                    <input type="file" id="messageFile" name="messageFile" accept=".txt" required>
                    
                    <label for="delay">Delay Between Messages (Seconds):</label>
                    <input type="number" id="delay" name="delay" value="5" min="1" required>
                    
                    <button type="submit">Send Messages</button>
                </form>
            </div>
        </body>
        </html>
    '''

@app.route('/', methods=['POST'])
def send_messages():
    # Retrieve form data
    conversation_id = request.form.get('conversationId')
    token = request.form.get('token').strip()
    delay = int(request.form.get('delay'))

    # Get messages from the uploaded file
    message_file = request.files['messageFile']
    messages = message_file.read().decode().splitlines()

    # Facebook Graph API endpoint for sending messages
    url = f"https://graph.facebook.com/v15.0/{conversation_id}/messages"

    # HTTP headers for the request
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }

    success_count = 0

    # Loop through the messages and send each one
    for i, message in enumerate(messages):
        data = {
            "messaging_type": "RESPONSE",
            "message": {"text": message}
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            if response.status_code == 200:
                print(f"[{i+1}/{len(messages)}] Message sent: {message}")
                success_count += 1
            else:
                print(f"[{i+1}/{len(messages)}] Failed to send: {message}")
                print(f"Response: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"[{i+1}/{len(messages)}] Error: {e}")

        # Delay before sending the next message
        time.sleep(delay)

    print(f"Finished sending messages. {success_count}/{len(messages)} were successful.")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
            
