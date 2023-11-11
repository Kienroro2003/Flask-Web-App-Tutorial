from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from . import db
import json
from flask_login import current_user, login_required
from .models import Note
from website.scraping_word import *

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')  # Gets the note from the HTML

        if len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            # new_note = Note(data=note, user_id=current_user.id)  #providing the schema for the note
            # db.session.add(new_note) #adding the note to the database
            # db.session.commit()
            text = ' '.join(note.split('\r\n')).translate({ord(i): None for i in '.(),?!:+-*/@#$%^&<>'}).lower().split(
                ' ')
            print(text)
            notes = current_user.notes
            print(notes)
            for word in text:
                word = add(word, notes)
                if word is not None:
                    word.user_id = current_user.id
                    db.session.add(word)  # adding the note to the database

                db.session.commit()

            print(notes)

            flash('Note added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-word', methods=['POST'])
def delete_note():
    word = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
    wordId = word['wordId']
    word = Word.query.get(wordId)
    if word:
        if word.user_id == current_user.id:
            word.isUsed = False
            db.session.commit()

    return jsonify({})


@views.route('/infor-word/<id>', methods=['GET'])
def infor_word(id):
    word = Word.query.get(int(id))
    if word:
        print(word)
        return render_template("infor.html", user=current_user, word=word)


@views.route('/dictionary', methods=['GET'])
def dictionary():
    return render_template("dictionary.html", user=current_user)

@views.route('/game', methods=['GET'])
def game():
    return render_template('game.html', user=current_user)

@views.route('/trash', methods=['GET', 'POST'])
def trash():
    if request.method == 'POST':
        word = json.loads(request.data)  # this function expects a JSON from the INDEX.js file
        wordId = word['wordId']
        print(wordId)
        word = Word.query.get(wordId)
        print(word)
        if word:
            if word.user_id == current_user.id:
                word.isUsed = True
                db.session.commit()

        return jsonify({})
    return render_template("trash.html", user=current_user)
