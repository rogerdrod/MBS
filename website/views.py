from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)

@views.route('/movie', methods=['GET','POST'])
@login_required
def movie():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Comment is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Comment Added!', category='success')
    return render_template("movie.html", user=current_user)

@views.route('/catalog', methods=['GET', 'POST'] )
def catalog():
    return render_template("catalog.html", user=current_user)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    #we can manipulate the code at the bottom to only allow certain users to delete comments, such as admins
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})