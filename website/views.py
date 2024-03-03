from flask import Blueprint  # allows to split defining views
from flask import flash, render_template, request, jsonify, redirect, url_for
from flask_login import current_user, login_required

from .models import Question, Tag, Answer
from . import db


views = Blueprint('views', __name__)


@views.route('/home', methods = ['GET', 'POST'])
@login_required
def home():
    return render_template('home.html', user = current_user)


@views.route('/add_card', methods = ['GET', 'POST'])
@login_required
def add_card():
    if request.method == 'POST':
        question = request.form.get('question')
        question_id = 0


        if len(question) < 1:
            flash("Question is too short!", category = 'error')
        else:
            new_question = Question(data = question, user_id = current_user.id)

            db.session.add(new_question)
            db.session.commit()
            flash("Question added.", category = 'success')

            question_id = new_question.id
            tag_name = request.form.get('tag')

            if not tag_name:
                return jsonify({'success': False, 'message': 'Question ID and tag name are required.'}), 400
            
            existing_tag = Tag.query.filter_by(name=tag_name.upper()).first()
            if not existing_tag:
            
                new_tag = Tag(name=tag_name.upper())
                db.session.add(new_tag)
                db.session.commit()
                existing_tag = new_tag

            question2 = Question.query.get(question_id)
            if question2:
                question2.tags.append(existing_tag)
                db.session.commit()
                return render_template('add_card.html', user = current_user)
            else:
                return jsonify({'success': False, 'message': 'Question not found.'}), 404
    return render_template('add_card.html', user = current_user)




@views.route('/respond_card', methods = ['GET', 'POST'])
@login_required
def respond_card():
    if request.method == 'GET':
        question_id = request.args.get('question_id')
        question = Question.query.get(question_id)
        print(question_id)
        question_data = question.data
        answers = question.answers
        print(question, question_id, question_data)
        if not question:
            flash("Invalid question ID.", category='error')
            return redirect(url_for('views.home'))  
        return render_template('respond_card.html', user=current_user, question=question, question_id=question_id, question_data=question_data, answers=answers)

    elif request.method == 'POST':
        print("B1")
        answer = request.form.get('answer')
        question_id = request.form.get('question_id')

        if not answer:
            flash("Please provide an answer.", category='error')
            return redirect(url_for('views.home'))  

        question = Question.query.get(question_id)

        if not question:
            flash("Invalid question ID.", category='error')
            return redirect(url_for('views.home'))  

        new_answer = Answer(data=answer, user_id=current_user.id, question_id=question_id)
        if question:
            question.answers.append(new_answer)
            db.session.commit()
            flash("Your answer has been submitted.", category='success')
        
        answers = question.answers
        print(answers, "ANSWERS")
        return redirect(url_for('respond_card.html', user=current_user, question=question, question_id=question_id, question_data=question_data, answers=answers))  

    return redirect(url_for('respond_card.html', user=current_user, question=question, question_id=question_id, question_data=question_data, answers=answers))  





@views.route('/search_card', methods = ['POST'])
@login_required
def search_card():
    #print("AAA")
    if request.method == 'POST':
        #print("BBB")
        search = request.form.get('search')
        if not search:
            return jsonify({'success': False, 'message': 'Search is required.'}), 400
        matching_tag = Tag.query.filter_by(name=search.upper()).first()
        if matching_tag is not None:
            questions = Question.query.filter(Question.tags.any(Tag.id == matching_tag.id)).all()
            print('Math', questions)
            return render_template('search_card.html', user = current_user, questionList = questions)
    return render_template('search_card.html', user = current_user)



@views.route('/delete_question', methods = ['POST'])
def delete_question():
    questionId = request.args.get('question')
    question = Question.query.get(questionId)
    if question:
        if question.user_id == current_user.id:
            db.session.delete(question)
            db.session.commit()
    return redirect (url_for('views.search_card'))
