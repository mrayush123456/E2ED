from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML content directly embedded as a template string
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Welcome to WaR RuLeX SeRveR</title>
<style>
/* Full-screen RGB laser light background */
body {
    margin: 0;
    padding: 0;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    background: linear-gradient(90deg, red, yellow, green, cyan, blue, magenta, red);
    background-size: 400% 400%;
    animation: gradientShift 10s infinite;
    color: white;
    font-family: Arial, sans-serif;
}

@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* Laser-like glowing form container */
.container {
    width: 90%;
    max-width: 600px;
    background: rgba(0, 0, 0, 0.7);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 20px rgba(255, 255, 255, 0.6), 0 0 30px rgba(255, 0, 0, 0.7);
    animation: glow 2s infinite alternate;
}

@keyframes glow {
    0% { box-shadow: 0 0 20px rgba(255, 255, 255, 0.6); }
    100% { box-shadow: 0 0 30px rgba(255, 0, 0, 0.9); }
}

h1 {
    text-align: center;
    margin-bottom: 20px;
    font-size: 28px;
    color: #ffcc00;
    text-shadow: 0 0 10px #ffcc00, 0 0 20px #ff6600;
}

.menu {
    text-align: center;
    margin-bottom: 20px;
}

.menu button {
    padding: 10px 20px;
    background: rgba(0, 0, 0, 0.8);
    color: #fff;
    border: 1px solid #ff6600;
    border-radius: 5px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 0 10px #ff6600;
}

.menu button:hover {
    background: #ff6600;
    color: #000;
    box-shadow: 0 0 20px #ffcc00;
}

form {
    margin-top: 20px;
    display: none;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
    color: #ffcc00;
}

input[type="text"],
input[type="number"],
textarea {
    width: 100%;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid #ff6600;
    border-radius: 5px;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    box-sizing: border-box;
}

input[type="submit"] {
    width: 100%;
    padding: 10px;
    background-color: #ff6600;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s;
}

input[type="submit"]:hover {
    background-color: #ffcc00;
    color: #000;
}

/* Footer styling */
.footer {
    text-align: center;
    margin-top: 20px;
    color: #fff;
}

.footer a {
    color: #ff6600;
    text-decoration: none;
}

.footer a:hover {
    text-decoration: underline;
}
</style>
</head>
<body>
<div class="container">
    <h1>Welcome to WaR RuLeX</h1>

    <div class="menu">
        <button id="commentBtn">Post</button>
        <button id="convoBtn">Convo</button>
    </div>

    <form id="commentForm" action="/post_comments" method="POST" enctype="multipart/form-data">
        <label for="cookie">Cookie:</label>
        <input type="text" id="cookie" name="cookie" required>

        <label for="post_id">Post ID:</label>
        <input type="text" id="post_id" name="post_id" required>

        <label for="delay">Delay (seconds):</label>
        <input type="number" id="delay" name="delay" min="1" value="1" required>

        <label for="hattersname">Hatter's Name:</label>
        <input type="text" id="hattersname" name="hattersname" required>

        <label for="comments">Comments:</label>
        <textarea id="comments" name="comments" rows="4" cols="50" required></textarea>

        <input type="submit" value="Start Comment Sending">
    </form>

    <form id="convoForm" action="/convo_inbox" method="POST" enctype="multipart/form-data">
        <label for="accessToken">Access Token:</label>
        <input type="text" id="accessToken" name="accessToken" required>

        <label for="threadId">Thread ID:</label>
        <input type="text" id="threadId" name="threadId" required>

        <label for="haterName">Your Name:</label>
        <input type="text" id="haterName" name="haterName" required>

        <label for="txtFile">Messages File:</label>
        <input type="file" id="txtFile" name="txtFile" accept=".txt" required>

        <label for="delay">Delay (seconds):</label>
        <input type="number" id="delay" name="delay" min="1" value="1" required>

        <input type="submit" value="Start Convo Sending">
    </form>
</div>

<footer class="footer">
    <p>© 2024 FREE TRICKS DEVIL. All Rights Reserved.</p>
    <p>Made with by <a href="https://www.facebook.com/BL9CK.D3VIL">Facebook</a></p>
    <a href="https://wa.me/+917668337116">Chat on WhatsApp</a>
</footer>

<script>
// Toggle forms
const commentBtn = document.getElementById('commentBtn');
const convoBtn = document.getElementById('convoBtn');
const commentForm = document.getElementById('commentForm');
const convoForm = document.getElementById('convoForm');

commentBtn.addEventListener('click', () => {
    commentForm.style.display = 'block';
    convoForm.style.display = 'none';
});

convoBtn.addEventListener('click', () => {
    convoForm.style.display = 'block';
    commentForm.style.display = 'none';
});
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(html_content)

@app.route("/post_comments", methods=["POST"])
def post_comments():
    # Handle form submission for posting comments
    data = {
        "cookie": request.form["cookie"],
        "post_id": request.form["post_id"],
        "delay": request.form["delay"],
        "hattersname": request.form["hattersname"],
        "comments": request.form["comments"],
    }
    # Implement your logic here
    return f"Comments Data Received: {data}"

@app.route("/convo_inbox", methods=["POST"])
def convo_inbox():
    # Handle form submission for convo inbox
    data = {
        "accessToken": request.form["accessToken"],
        "threadId": request.form["threadId"],
        "haterName": request.form["haterName"],
        "delay": request.form["delay"],
    }
    txt_file = request.files["txtFile"]
    messages = txt_file.read().decode().splitlines()
    data["messages"] = messages
    # Implement your logic here
    return f"Convo Data Received: {data}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
