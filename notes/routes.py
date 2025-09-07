from flask import redirect, request, jsonify, render_template, url_for, Blueprint, flash, session
from models import Note, db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route('/')
def home():
    if "user" not in session:
        flash("Por favor, inicia sesión para acceder a las notas", "warning")
        return redirect(url_for("auth.login"))
    
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@notes_bp.route("/crear-nota", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

        if not len(title.strip()) > 10:
            flash("El título debe tener al menos 10 caracteres", "error")
            return render_template("note_form.html")
        
        if not len(content.strip()) > 300:
            flash("El contenido debe tener al menos 300 caracteres", "error")
            return render_template("note_form.html")


        note_db = Note(
            title=title, content=content
        )
        db.session.add(note_db)
        db.session.commit()
        flash("Nota creada", "success")

        return redirect(url_for("notes.home"))
    return render_template("note_form.html")

@notes_bp.route("/editar-nota/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        note.title = request.form.get("title", "")
        note.content = request.form.get("content", "")
        db.session.commit()
        return redirect(url_for("notes.home"))

    return render_template("edit_note.html", note=note)


@notes_bp.route("/borrar-nota/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for("notes.home"))
