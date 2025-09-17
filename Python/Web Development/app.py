from flask import Flask, render_template_string, request, jsonify
import socket

# Configure your OpenAI API key (best to load from env var)
import os
app = Flask(__name__)

# ================== ROUTES ==================
@app.route("/main")
def home():
    return render_template_string(""" 
   <!DOCTYPE html>
        <html>
        <head>      
            <title>My Python Webpage</title>
            <style>
                body {
                    font-family: sans-serif;
                    background-color: black;
                    text-align: center;
                    margin: 50px;
                }
                h1 {
                    color: #f7f7f7;
                    font-family: sans-serif;
                }
                h1 {
                    color:azure;
                    font-family: cursive;
                }
                p {
                    font-size: 18px;
                    color: #ffff
                }
                .button {
                    display: inline-block;
                    padding: 10px 30px;
                    background: #a2bfde;
                    color: white;
                    text-decoration: none;
                    border-radius: 15px;
                }
                .button:hover {
                    background: #5a6d81;
                }
                .button2 {
                    display :inline-block;
                    padding: 10px 20px;
                    background: #a2bfde;
                    color: #ffff;
                    text-decoration: none;
                    border-radius: 20px;
                }
                .button:hover {
                    background: rgb(80, 108, 108)
                }
            </style>
        </head>
        <body>
            <h1><b> Welcome To Bruno Ai...</b></h1>
            <p>An Ai Built By A <u><i>12 Year old Tech Genius</i></u></p>
            <a href="bruno.html" class="button">Start Chatting with Bruno !</a>
            <a href="about.html" class="button">About Me</a>
        </body>
        </html>
    """)

@app.route("/about-me")
def about():
    return render_template_string(""" 
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <style>
        body {
            background: #292727;
            font-family: cursive;
            text-align: center;
        }
        h1 {
            color: #ffff;
            text-align: center;
            font-family: cursive;
            font-style: bold;

        }
        p {
            color: #ffff;
            text-align: center;
            font-family: georgia;
            font-style: italic;
        }
        .button {
            display: inline-block;
            color: #ffffff;
            padding: 10px 20px;
            text-align: left,center;
            border-radius: 15px;
            text-decoration: none;
            background: #383636
        }
        .button:hover {
            background: rgb(80,108,108);
        }
    </style>
    <a href="index.html" class="button">Go Back</a>
    <br>
    <h1>About Me !</h1>
    <p>Hi Guys, I am a 12 Year Old, dev studying in class 7 in __________School(i don't want to give out my school's name though tbh)</p>
    <br>
    <p>This Website is for <u>EDUCATIONAL PURPOSES ONLY</u> no online illegal activity will be a problem for me(thats why i am making you sign-in)</p>
</body>
</html>
    """)

# ✅ Chat page with frontend JS
@app.route("/chat")
def chat():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <title>Bruno AI Chatbot</title>
    <style>
        body { font-family: sans-serif; background-color: #000; text-align: center; margin: 50px; color: white; }
        .chat-container { width: 60%; max-width: 600px; margin: 20px auto; background: #1a1a1a; border-radius: 20px; padding: 20px; }
        .chat-box { height: 300px; overflow-y: auto; border: 1px solid #444; border-radius: 10px; padding: 10px; background: #383131; text-align: left; margin-bottom: 15px; }
        .message { margin: 10px 0; padding: 10px; border-radius: 15px; max-width: 70%; word-wrap: break-word; }
        .user { background: #aaafb5; color: black; margin-left: auto; text-align: right; }
        .bot { background: #242323; color: white; margin-right: auto; text-align: left; }
        .input-container { display: flex; justify-content: space-between; }
        input[type="text"] { flex: 1; padding: 7px; border-radius: 20px; border: none; outline: none; }
        button { padding: 0px 20px; margin-left: 5px; background: #a2bfde; color: white; border: none; border-radius: 20px; cursor: pointer; }
        button:hover { background: #5a6d81; }
    </style>
</head>
<body>
    <div class="chat-container">
        <div id="chatBox" class="chat-box"></div>
        <div class="input-container">
            <input type="text" id="userInput" placeholder="Type your message...">
            <button onclick="sendMessage()">Send</button>
        </div>
    </div>

    <script>
        async function sendMessage() {
            let input = document.getElementById("userInput");
            let message = input.value.trim();
            if (message === "") return;

            // Add user message
            let chatBox = document.getElementById("chatBox");
            let userMsg = document.createElement("div");
            userMsg.className = "message user";
            userMsg.textContent = message;
            chatBox.appendChild(userMsg);

            chatBox.scrollTop = chatBox.scrollHeight;
            input.value = "";

            // Send to backend
            let response = await fetch("/get_response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });

            let data = await response.json();

            // Add bot message
            let botMsg = document.createElement("div");
            botMsg.className = "message bot";
            botMsg.textContent = "Bruno AI: " + data.reply;
            chatBox.appendChild(botMsg);

            chatBox.scrollTop = chatBox.scrollHeight;
        }
    </script>
</body>
</html>
""")

# ✅ Backend endpoint that queries OpenAI
@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can also use "gpt-4"
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response["choices"][0]["message"]["content"]
    except Exception as e:
        reply = f"Error: {str(e)}"

    return jsonify({"reply": reply})


# ================== RUN SERVER ==================
if __name__ == "__main__":
    PORT = 8000
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    print(f"Serving Flask app on http://127.0.0.1:{PORT}")
    print(f"Access from other devices: http://{local_ip}:{PORT}")

    app.run(host="0.0.0.0", port=PORT, debug=True)
