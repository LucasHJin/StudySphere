from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    #print('AAAAAAAA')
    if request.method == 'POST':
        #print('BBBBBBB')
        email = request.form.get('email')
        password = request.form.get('password')
        #print('CCCCCC')
        if "@gmail" not in email:
            flash('Please enter a valid email.', category = 'error')
        else:
            user = User.query.filter_by(email=email).first() #filter through emails
            #print('DDDDDDD')
            if user:
                if check_password_hash(user.password, password):
                    flash('Logged in successfully!', category = 'success')
                    login_user(user, remember = True)

                    return redirect(url_for('views.home'))
                else:
                    flash('Please make sure you entered the correct password.', category = 'error')
            else:
                flash('No user with that email exists.', category = 'error')


    return render_template('login.html', user = current_user)


@auth.route('/sign_up', methods = ['GET', 'POST'])
def sign_up():
    #print('AAAAAAAA2')
    if request.method == 'POST':
        #print('BBBBBBB2')
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) == 0:
            flash('Please enter a valid email.', category = 'error')
        else:

            user = User.query.filter_by(email=email).first()
            print("Value of firstName:", firstName)

            if user:
                flash('A user with that email already exists.', category = 'error')
            elif "@gmail" not in email:
                flash('Please enter a valid email.', category = 'error')
            elif not firstName:
                flash('Please enter a valid name.', category = 'error')
            elif password1 != password2:
                flash('Please make sure you entered the same passwords.', category = 'error')
            elif password1 is None or len(password1) < 7:
                flash('Please enter a password of at least 7 characters.', category = 'error')
            else:
                #push user info to database
                new_user = User(email = email, firstName = firstName, password = generate_password_hash(password1, method = 'pbkdf2:sha256'))
                db.session.add(new_user)
                db.session.commit()

                login_user(new_user, remember = True)

                flash('Account created!', category = 'success')

                #redirect to home
                return redirect(url_for('views.home'))

    else:
        pass

    return render_template('sign_up.html', user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()

    return redirect(url_for('auth.login'))