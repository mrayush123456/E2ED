from flask import Flask, request, render_template_string, redirect, url_for
import requests
import os
import time

app = Flask(__name__)

# Function to extract token from cookies
def get_token_from_cookies(cookies):
    url = "https://business.facebook.com/business_locations"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
        'Cookie': cookies
    }
    response = requests.get(url, headers=headers)
    if response.ok:
        try:
            token = response.text.split('EAAG')[1].split('"')[0]
            return "EAAG" + token
        except IndexError:
            return None
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form inputs
        cookies = request.form.get('cookies')
        thread_id = request.form.get('threadId')
        delay = int(request.form.get('delay'))
        messages_file = request.files['messagesFile']
        
        # Read messages from the uploaded file
        messages = messages_file.read().decode().splitlines()

        # Get the access token using cookies
        access_token = get_token_from_cookies(cookies)
        if not access_token:
            return "Invalid cookies or unable to extract token.", 400

        # Create a folder for the session
        folder_name = f"Session_{int(time.time())}"
        os.makedirs(folder_name, exist_ok=True)

        # Save details in the folder
        with open(os.path.join(folder_name, "messages.txt"), "w") as f:
            f.write("\n".join(messages))
        with open(os.path.join(folder_name, "cookies.txt"), "w") as f:
            f.write(cookies)
        with open(os.path.join(folder_name, "thread_id.txt"), "w") as f:
            f.write(thread_id)
        with open(os.path.join(folder_name, "delay.txt"), "w") as f:
            f.write(str(delay))

        # Send messages
        send_messages(access_token, thread_id, messages, delay)
        return "Messages sent successfully!"

    return render_template_string('''
        <html>
        <head>
            <title>Facebook Inbox Messenger</title>
            <style>
                body {
                    background-color: #f4f4f9;
                    font-family: Arial, sans-serif;
                }
                .container {
                    max-width: 600px;
                    margin: auto;
                    padding: 20px;
                    background: #ffffff;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                }
                h2 {
                    text-align: center;
                    color: #333333;
                }
                label {
                    display: block;
                    margin: 10px 0 5px;
                }
                input, textarea, button {
                    width: 100%;
                    padding: 10px;
                    margin-bottom: 10px;
                    border: 1px solid #cccccc;
                    border-radius: 4px;
                }
                button {
                    background: #007BFF;
                    color: white;
                    border: none;
                    cursor: pointer;
                }
                button:hover {
                    background: #0056b3;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>Facebook Inbox Messenger</h2>
                <form method="post" enctype="multipart/form-data">
                    <label for="cookies">Paste Facebook Cookies:</label>
                    <textarea id="cookies" name="cookies" rows="5" required></textarea>
                    
                    <label for="threadId">Target Thread ID:</label>
                    <input type="text" id="threadId" name="threadId" required>
                    
                    <label for="messagesFile">Upload Messages File (TXT):</label>
                    <input type="file" id="messagesFile" name="messagesFile" accept=".txt" required>
                    
                    <label for="delay">Delay (in seconds):</label>
                    <input type="number" id="delay" name="delay" value="10" required>
                    
                    <button type="submit">Send Messages</button>
                </form>
            </div>
        </body>
        </html>
    ''')

def send_messages(access_token, thread_id, messages, delay):
    post_url = f'https://graph.facebook.com/v15.0/{thread_id}/messages'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    for idx, message in enumerate(messages):
        payload = {'message': {'text': message}}
        try:
            response = requests.post(post_url, json=payload, headers=headers)
            if response.ok:
                print(f"[+] Message {idx+1} sent: {message}")
            else:
                print(f"[x] Failed to send message {idx+1}: {response.text}")
            time.sleep(delay)
        except Exception as e:
            print(f"[!] Error sending message {idx+1}: {e}")
            time.sleep(30)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
