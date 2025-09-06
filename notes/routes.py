from flask import redirect, request, jsonify, render_template, url_for, Blueprint, flash
from models import Note, db

notes_bp = Blueprint("notes", __name__)

@notes_bp.route('/')
def home():
    notes = Note.query.all()
    return render_template("home.html", notes=notes)


@notes_bp.route("/crear-nota", methods=["GET", "POST"])
def create_note():
    if request.method == "POST":
        title = request.form.get("title", "")
        content = request.form.get("content", "")

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
