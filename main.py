from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/wiki')
def wiki():
    return render_template("wiki/index.html")

@app.route('/api/admin', methods=['GET'])
def admin():
    
    responseHtml = ""

    with open("lockedPages/admin.html", 'r') as html:
        responseHtml = html.read()

    path = request.path
    reqData = request.get_json

    if (path == "/api/admin"):

        return Response(responseHtml, content_type="text/html")
    
        

    return(jsonify("Invalid request path"))

if __name__ == "__main__":
    app.run(debug=True, port=80)