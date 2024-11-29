from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    # Получение данных из формы
    username = request.form.get("username")
    return f"<h1>Hello, {username}!</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)