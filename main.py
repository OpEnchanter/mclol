from flask import Flask, render_template, request, jsonify, Response
import random
from mcrcon import MCRcon

app = Flask(__name__)

rconIp = "127.0.0.1"
rconPort = 25566
rconPassword = "rcon"

mcr = None

sessionKeys = []

class session():
    def __init__(self, key):
        self.key = key


def create_session():
    key = random.randint(1111111111, 9999999999)
    sessionKeys.append(key)
    return session(key)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/wiki')
def wiki():
    return render_template("wiki/index.html")

@app.route('/admin')
def admin():
    return render_template("admin/index.html")

@app.route('/api/admin', methods=['POST'])
def api_admin():
    responseHtml = ""

    # Load the HTML file
    with open("lockedPages/admin.html", 'r') as html:
        responseHtml = html.read()

    # Get JSON data from request
    reqData = request.get_json()

    # Check if reqData is valid
    if reqData is None:
        return jsonify({"error": "Invalid JSON data"}), 400
    
    if reqData["key"] == "test":
        session = create_session()

        return jsonify({
            "response": True,
            "skey": session.key,
            "html": responseHtml
        })

    return jsonify({
        "response": False
    })

@app.route('/api/command', methods=['POST'])
def api_command():
    global mcr
    reqData = request.get_json()

    print(reqData)

    if reqData["skey"] in sessionKeys:

        if mcr is None:
            mcr = MCRcon(rconIp, rconPassword, rconPort)
            mcr.connect()

        result = mcr.command(reqData["command"])
        return jsonify({
            "response": True,
            "result": result
        })

    return jsonify({
        "response": False
    })

if __name__ == "__main__":
    app.run(debug=True, port=80)