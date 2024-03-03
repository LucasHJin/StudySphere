from flask import Blueprint  # allows to split defining views
from flask import flash, render_template, request, jsonify
from flask_login import current_user, login_required

from .models import Question, Tag, Answer
from . import db

import json

views = Blueprint('views', __name__)


@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user = current_user)


@views.route('/add_card', methods = ['GET', 'POST'])
@login_required
def add_card():
    if request.method == 'POST':
        if 'action' in request.form:
            action = request.form['action']
            if action == 'add_card':
                question = request.form.get('question')
                if len(question) < 1:
                    flash("Question is too short!", category = 'error')
                else:
                    new_question = Question(data = question, user_id = current_user.id)
                    db.session.add(new_question)
                    db.session.commit(new_question)
                    flash("Question added.", category = 'success')
            elif action == 'add_tag':
                question_id = request.form.get('question_id')
                tag_name = request.form.get('tag_name')

                if not question_id or not tag_name:
                    return jsonify({'success': False, 'message': 'Question ID and tag name are required.'}), 400

                existing_tag = Tag.query.filter_by(name=tag_name.upper()).first()
                if existing_tag:
                    return jsonify({'success': False, 'message': 'Tag already exists.'}), 400

                new_tag = Tag(name=tag_name.upper())
                db.session.add(new_tag)
                db.session.commit()

                question = Question.query.get(question_id)
                if question:
                    question.tags.append(new_tag)
                    db.session.commit()
                    return jsonify({'success': True, 'message': 'Tag created successfully.', 'tag': new_tag.name}), 200
                else:
                    return jsonify({'success': False, 'message': 'Question not found.'}), 404
    return render_template('add_card.html', user = current_user)



@views.route('/respond_card')
@login_required
def respond_card():
    return render_template('respond_card.html', user = current_user)


@views.route('/search_card')
@login_required
def search_card():
    return render_template('search_card.html', user = current_user)



@views.route('/delete_question', methods = ['POST'])
def delete_question():
    question = json.loads(request.data)
    questionId = question['question']
    question = Question.query.get(questionId)
    if question:
        if question.user_id == current_user.id:
            db.session.delete(question)
            db.session.commit()
            return jsonify({})
