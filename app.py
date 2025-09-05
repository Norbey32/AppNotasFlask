
from flask import Flask, redirect, request, jsonify, render_template, url_for

app = Flask(__name__)

import os
from flask_sqlalchemy import SQLAlchemy

DB_FILE_PATH = os.path.join(
    os.path.dirname(__file__),
    "notes.sqlite"
)

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_FILE_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    
    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"

@app.route('/')
def home():
    notes = [
        {
            "title": "Nota de prueba",
            "content": "Contenido de la nota de prueba"
        }
    ]
    return render_template("home.html", notes=notes)

@app.route('/acerca-de')
def about():
    return "Esta es una app de notas."


@app.route('/contacto', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return "Formulario enviado correctamente", 201
    return "Pagina de contacto"


@app.route("/api/info")
def api_info():
    data = {
        "version": "1.0.0",
        "author": "David",
        "description": "API de ejemplo con Flask"
    }
    return jsonify(data)


@app.route("/Confirmacion")
def confirmation():
    return "Prueba"

@app.route("/crear-nota", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        note = request.form.get("note", "Nota no encontrada")
        return redirect(url_for("confirmation", note=note))
    return render_template("note_form.html")
