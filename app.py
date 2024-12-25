from flask import Flask, request, redirect, url_for, render_template_string
import requests
import time
import threading
import os

app = Flask(__name__)
stop_flag = False

HTML_TEMPLATE = """
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Automation</title>
    <style>
        body {
            background: linear-gradient(90deg, red, orange, yellow, green, cyan, blue, violet);
            background-size: 400% 400%;
            animation: gradient 5s infinite;
            color: white;
            font-family: Arial, sans-serif;
            text-align: center;
        }
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        .container {
            max-width: 600px;
            margin: 50px auto;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 0 10px rgba(255, 255, 255, 0.7);
            background: rgba(0, 0, 0, 0.6);
        }
        .form-control {
            width: 100%;
            height: 40px;
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid white;
            background: transparent;
            color: white;
        }
        .btn {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 20px;
            cursor: pointer;
        }
        .btn:hover {
            background: red;
        }
        h3, label {
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h3>Facebook Automation</h3>
        <form action="/" method="post" enctype="multipart/form-data">
            <label for="email">Facebook Email/Mobile:</label>
            <input type="text" class="form-control" id="email" name="email" required>
            
            <label for="password">Facebook Password:</label>
            <input type="password" class="form-control" id="password" name="password" required>
            
            <label for="groupId">Target Group/Chat ID:</label>
            <input type="text" class="form-control" id="groupId" name="groupId" required>
            
            <label for="hatersName">Hater's Name:</label>
            <input type="text" class="form-control" id="hatersName" name="hatersName" required>
            
            <label for="txtFile">Message File (.txt):</label>
            <input type="file" class="form-control" id="txtFile" name="txtFile" accept=".txt" required>
            
            <label for="delay">Message Delay (in seconds):</label>
            <input type="number" class="form-control" id="delay" name="delay" value="60" required>
            
            <button type="submit" class="btn">Start Sending</button>
        </form>
        <br>
        <form action="/stop" method="post">
            <button type="submit" class="btn" style="background: red;">Stop</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    global stop_flag
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        group_id = request.form.get('groupId')
        haters_name = request.form.get('hatersName')
        delay = int(request.form.get('delay'))

        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        # Create a folder for logs
        folder_name = f"Facebook_Automation_{group_id}"
        os.makedirs(folder_name, exist_ok=True)

        with open(os.path.join(folder_name, "messages.txt"), "w") as f:
            f.write("\n".join(messages))

        # Start sending messages in a separate thread
        threading.Thread(target=send_messages, args=(email, password, group_id, haters_name, messages, delay)).start()
        return redirect(url_for('index'))
    return render_template_string(HTML_TEMPLATE)


@app.route('/stop', methods=['POST'])
def stop():
    global stop_flag
    stop_flag = True
    return redirect(url_for('index'))


def send_messages(email, password, group_id, haters_name, messages, delay):
    global stop_flag
    stop_flag = False

    try:
        # Placeholder for login process
        session_token = "dummy_session_token"  # Replace with actual Facebook login logic

        # Simulated API URL (adjust as needed)
        post_url = f"https://graph.facebook.com/{group_id}/messages"

        for i, message in enumerate(messages):
            if stop_flag:
                print("Process stopped by the user.")
                break

            # Prepare the message
            full_message = f"{haters_name} {message}"

            # Simulated API request
            parameters = {"access_token": session_token, "message": full_message}
            response = requests.post(post_url, data=parameters)

            if response.status_code == 200:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message {i+1} sent successfully: {full_message}")
            else:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Failed to send message {i+1}: {response.text}")

            time.sleep(delay)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
