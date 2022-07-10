from flask import Flask, render_template
app = Flask(__name__)

@app.route('/decode')
def decode() -> str:
    return render_template("decode.html")

@app.route('/')
def index() -> str:
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)