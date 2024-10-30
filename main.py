from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/wiki')
def wiki():
    return render_template("wiki/index.html")

if __name__ == "__main__":
    app.run(debug=True, port=80)