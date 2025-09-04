from flask import Flask, request, jsonify


app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

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