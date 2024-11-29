from flask import Flask, render_template, request, jsonify
import sqlite3
import random

app = Flask(__name__)

# Инициализация базы данных
def init_db():
    with sqlite3.connect("game.db") as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY,
            name TEXT,
            health INTEGER,
            hunger INTEGER,
            happiness INTEGER,
            pet_type TEXT
        )''')
        conn.commit()

# Выбор питомца
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        pet_type = request.form["pet_type"]
        with sqlite3.connect("game.db") as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO pets (name, health, hunger, happiness, pet_type) VALUES (?, ?, ?, ?, ?)",
                           (name, 100, 50, 50, pet_type))
            conn.commit()
        return jsonify({"message": f"Питомец {name} ({pet_type}) добавлен!"})
    return render_template("index.html")

# Статус питомца
@app.route("/status", methods=["GET"])
def status():
    with sqlite3.connect("game.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pets LIMIT 1")
        pet = cursor.fetchone()
    if pet:
        return jsonify({"name": pet[1], "health": pet[2], "hunger": pet[3], "happiness": pet[4], "type": pet[5]})
    return jsonify({"error": "Нет питомца!"})

# Действия с питомцем
@app.route("/action", methods=["POST"])
def action():
    action_type = request.json.get("action")
    with sqlite3.connect("game.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM pets LIMIT 1")
        pet = cursor.fetchone()
        if not pet:
            return jsonify({"error": "Нет питомца!"})

        health, hunger, happiness = pet[2], pet[3], pet[4]

        if action_type == "feed":
            hunger = min(100, hunger + 20)
        elif action_type == "play":
            happiness = min(100, happiness + 20)
        elif action_type == "clean":
            health = min(100, health + 10)

        cursor.execute("UPDATE pets SET health = ?, hunger = ?, happiness = ? WHERE id = ?",
                       (health, hunger, happiness, pet[0]))
        conn.commit()

    return jsonify({"message": f"{action_type.capitalize()} выполнено!"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8080)