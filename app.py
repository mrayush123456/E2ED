from flask import Flask, request, render_template_string, flash, redirect, url_for
from cryptography.fernet import Fernet
import os
import time

# Flask App
app = Flask(__name__)
app.secret_key = 'a_secure_random_key'

# Encryption Key (याद रखें कि यह key secret होनी चाहिए)
ENCRYPTION_KEY = Fernet.generate_key()
cipher_suite = Fernet(ENCRYPTION_KEY)

# HTML Template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Encrypted Messenger</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 500px;
            margin: auto;
            padding: 20px;
            background: white;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.3);
        }
        h2 {
            text-align: center;
            color: #333;
        }
        input, button {
            width: 100%;
            padding: 10px;
            margin: 10px 0;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
        button {
            background-color: #28a745;
            color: white;
            border: none;
        }
        button:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2>Encrypted Messenger</h2>
        <form method="POST" enctype="multipart/form-data">
            <input type="text" name="username" placeholder="Enter your username" required>
            <input type="password" name="password" placeholder="Enter your password" required>
            <input type="text" name="receiver" placeholder="Enter receiver username" required>
            <input type="file" name="message_file" accept=".txt" required>
            <input type="number" name="delay" placeholder="Delay in seconds" required>
            <button type="submit">Send Message</button>
        </form>
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Step 1: Get User Inputs
        username = request.form['username']
        password = request.form['password']
        receiver = request.form['receiver']
        delay = int(request.form['delay'])
        message_file = request.files['message_file']
        
        # Step 2: Read Message File
        try:
            message_content = message_file.read().decode('utf-8')
        except Exception as e:
            flash("Error reading the file: " + str(e), 'error')
            return redirect(url_for('index'))
        
        # Step 3: Encrypt the Message
        encrypted_message = cipher_suite.encrypt(message_content.encode())
        flash(f"Encrypted Message Sent Successfully to {receiver}", 'success')
        
        # Simulate Delay
        time.sleep(delay)
        
        print(f"[DEBUG] Encrypted Message Sent: {encrypted_message}")
        return redirect(url_for('index'))
    
    return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
