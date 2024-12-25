from flask import Flask, request, render_template, redirect, url_for
import os
import time
import requests

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
    <title>Facebook Message Sender</title>
    <style>
        body{
            background-color: #f0f0f0;
            font-family: Arial, sans-serif;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
        }
        label {
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 8px;
            display: block;
        }
        input[type="text"], input[type="file"], input[type="number"] {
            width: 100%;
            padding: 10px;
            margin-bottom: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .btn-submit {
            background-color: #4CAF50;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            display: block;
            width: 100%;
            margin-top: 10px;
        }
        .btn-submit:hover {
            background-color: #45a049;
        }
        h2 {
            text-align: center;
            font-size: 18px;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>

<div class="container">
    <h2>Send Message via Facebook</h2>
    <form action="/" method="post" enctype="multipart/form-data">
        <label for="cookie">Select Facebook Cookie File:</label>
        <input type="file" id="cookie" name="cookie" accept=".txt" required>
        
        <label for="target">Target Group Chat or Inbox ID:</label>
        <input type="text" id="target" name="target" placeholder="Enter Target Group Chat ID or Inbox ID" required>
        
        <label for="hatersName">Enter Hater Name:</label>
        <input type="text" id="hatersName" name="hatersName" placeholder="Enter Hater's Name" required>
        
        <label for="delay">Delay Between Messages (in seconds):</label>
        <input type="number" id="delay" name="delay" value="10" required>
        
        <button type="submit" class="btn-submit">Send Messages</button>
    </form>
</div>

</body>
</html>
    '''


@app.route('/', methods=['POST'])
def send_message():
    if request.method == 'POST':
        # Retrieve the form data
        cookie_file = request.files['cookie']
        target = request.form['target']
        haters_name = request.form['hatersName']
        delay = int(request.form['delay'])

        # Save the cookie.txt file to the server for later use
        cookie_path = 'cookie.txt'
        cookie_file.save(cookie_path)

        # Read cookies from the cookie.txt file
        with open(cookie_path, 'r') as file:
            cookies = file.read().splitlines()

        # Set the Facebook token from the cookies file
        access_token = None
        for cookie in cookies:
            if 'c_user' in cookie:
                # Extract the token from the cookie or set it manually
                # For simplicity, we assume the token is within the cookie
                access_token = cookie.split('=')[1]
                break

        if not access_token:
            return "Error: No valid access token found in cookie file."

        # Prepare the Facebook Graph API URL
        post_url = f'https://graph.facebook.com/v15.0/{target}/messages'

        # Loop through and send messages
        try:
            for i in range(10):  # Limit to 10 messages for this example
                message = f"{haters_name} {i+1} - Your message here."
                params = {
                    'access_token': access_token,
                    'message': message
                }

                # Send message via Facebook API
                response = requests.post(post_url, params=params, headers=headers)
                if response.status_code == 200:
                    print(f"Message {i+1} sent successfully!")
                else:
                    print(f"Failed to send message {i+1}: {response.text}")

                # Wait before sending the next message
                time.sleep(delay)

            return redirect(url_for('index'))

        except Exception as e:
            return f"An error occurred: {e}"

    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
