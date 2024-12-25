from flask import Flask, request, render_template_string, redirect, url_for
import os
import datetime
import time
from bs4 import BeautifulSoup
import mechanize

# Flask App Setup
app = Flask(__name__)

# Mechanize Browser Setup
browser = mechanize.Browser()
browser.set_handle_robots(False)
cookies = mechanize.CookieJar()
browser.set_cookiejar(cookies)
browser.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/45.0.2454.85 Safari/537.36')]
browser.set_handle_refresh(False)

# Facebook Login URL
login_url = 'https://m.facebook.com/login.php'

# HTML Template (Inline for simplicity)
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Automation</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px; }
        .container { max-width: 600px; margin: auto; background: #fff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); }
        h2 { text-align: center; color: #333; }
        label { display: block; margin: 10px 0 5px; font-weight: bold; }
        input, textarea, button { width: 100%; padding: 10px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 4px; }
        button { background-color: #007BFF; color: #fff; border: none; }
        button:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Facebook Automation Tool</h2>
        <form method="POST" action="/" enctype="multipart/form-data">
            <label for="email">Facebook Email/Phone:</label>
            <input type="text" id="email" name="email" required>
            
            <label for="password">Facebook Password:</label>
            <input type="password" id="password" name="password" required>
            
            <label for="chat_link">Chat Link:</label>
            <input type="text" id="chat_link" name="chat_link" required>
            
            <label for="haters_name">Hater's Name:</label>
            <input type="text" id="haters_name" name="haters_name" required>
            
            <label for="notepad_file">Upload Message File (.txt):</label>
            <input type="file" id="notepad_file" name="notepad_file" accept=".txt" required>
            
            <label for="delay">Delay (seconds):</label>
            <input type="number" id="delay" name="delay" value="5" required>
            
            <button type="submit">Start Automation</button>
        </form>
    </div>
</body>
</html>
"""

# Helper Functions
def login_facebook(email, password):
    """Log in to Facebook using Mechanize."""
    browser.open(login_url)
    browser.select_form(nr=0)
    browser.form['email'] = email
    browser.form['pass'] = password
    browser.submit()
    # Check for login errors
    response_title = browser.title()
    if "login" in response_title.lower():
        raise Exception("Failed to log in to Facebook. Please check credentials.")

def send_message(chat_url, hater_name, messages, delay):
    """Send messages to the specified chat URL."""
    for count, message in enumerate(messages, start=1):
        try:
            browser.open(chat_url)
            browser.select_form(nr=1)
            browser.form['body'] = f"{hater_name} {message.strip()}"
            browser.submit()
            print(f"Message {count}: Sent at {datetime.datetime.now()}")
            time.sleep(delay)
        except Exception as e:
            print(f"Error sending message {count}: {e}")
            time.sleep(10)

# Flask Routes
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        chat_link = request.form.get("chat_link")
        hater_name = request.form.get("haters_name")
        delay = int(request.form.get("delay"))
        
        notepad_file = request.files["notepad_file"]
        messages = notepad_file.read().decode("utf-8").splitlines()
        
        try:
            login_facebook(email, password)
            send_message(chat_link, hater_name, messages, delay)
            return "Messages sent successfully!"
        except Exception as e:
            return f"Error: {e}"
    
    return render_template_string(html_template)

# Run the App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
