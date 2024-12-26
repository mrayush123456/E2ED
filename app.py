from flask import Flask, request, redirect, url_for
import requests
import time
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        # Get user inputs
        token = request.form.get('token')
        delay = int(request.form.get('delay'))
        
        # Upload and read the TXT files
        target_file = request.files['targetFile']
        targets = target_file.read().decode().splitlines()

        message_file = request.files['messageFile']
        messages = message_file.read().decode().splitlines()

        # Create a folder for storing details
        folder_name = "facebook_automation"
        os.makedirs(folder_name, exist_ok=True)

        with open(os.path.join(folder_name, "targets.txt"), "w") as f:
            f.write("\n".join(targets))

        with open(os.path.join(folder_name, "messages.txt"), "w") as f:
            f.write("\n".join(messages))

        with open(os.path.join(folder_name, "token.txt"), "w") as f:
            f.write(token)

        # Send messages
        num_targets = len(targets)
        num_messages = len(messages)

        for index, target in enumerate(targets):
            message = messages[index % num_messages]  # Rotate through messages if targets > messages
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            payload = {
                'recipient': {'id': target},
                'message': {'text': message}
            }

            try:
                response = requests.post(
                    f'https://graph.facebook.com/v15.0/{target}/messages',
                    json=payload,
                    headers=headers
                )

                if response.status_code == 200:
                    print(f"[+] Message sent to {target}: {message}")
                else:
                    print(f"[x] Failed to send message to {target}: {response.text}")

                time.sleep(delay)
            except Exception as e:
                print(f"[!] Error sending message to {target}: {e}")
                time.sleep(30)  # Retry after a delay

        return "Messages sent successfully!"
    else:
        return '''
        <html>
        <head>
            <title>Facebook Inbox Automation</title>
        </head>
        <body>
            <h1>Facebook Inbox Automation</h1>
            <form action="/" method="post" enctype="multipart/form-data">
                <label for="token">Enter Token:</label><br>
                <input type="text" id="token" name="token" required><br><br>
                
                <label for="targetFile">Upload Target File (TXT):</label><br>
                <input type="file" id="targetFile" name="targetFile" accept=".txt" required><br><br>
                
                <label for="messageFile">Upload Messages File (TXT):</label><br>
                <input type="file" id="messageFile" name="messageFile" accept=".txt" required><br><br>
                
                <label for="delay">Enter Delay (Seconds):</label><br>
                <input type="number" id="delay" name="delay" value="5" required><br><br>
                
                <button type="submit">Submit</button>
            </form>
        </body>
        </html>
        '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                    
