from flask import Flask, render_template, request, jsonify, Response
import random, subprocess, json
from mcrcon import MCRcon

config = {}

with open("config.json", "r") as conf:
    config = json.load(conf)

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

@app.route("/home")
def embed_home():
    return render_template("home/index.html")

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

        try:
            result = mcr.command(reqData["command"])
            return jsonify({
                "response": True,
                "result": result
            })
        except Exception as e:
            cmd = reqData["command"]
            return jsonify({
                "response":True,
                "result": f"An unexpected error occurred running command '{cmd}'"
            })

    return jsonify({
        "response": False
    })

@app.route('/api/startmcserve', methods=['POST'])
def api_start():
    reqData = request.get_json()

    if reqData["skey"] in sessionKeys:
        if config["serverType"] == "windows":
            process = subprocess.Popen(["startServer.bat"], stdout=subprocess.PIPE)

            output, error = process.communicate()

            print(output.decode())
        elif config["serverType"] == "linux":
            process = subprocess.Popen(["sudo sh startServer.sh"], stdout=subprocess.PIPE)

            output, error = process.communicate()

            print(output.decode())

        return jsonify({
            "response": True
        })
    
    return jsonify({
        "response": False
    })



if __name__ == "__main__":
    app.run(debug=True, port=80, host="0.0.0.0")
