from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)

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
        return jsonify({
            "response": True,
            "html": responseHtml
        })

    return jsonify({
        "response": False
    })
    

if __name__ == "__main__":
    app.run(debug=True, port=80)