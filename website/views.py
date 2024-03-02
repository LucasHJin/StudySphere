from flask import Blueprint, render_template #allows to split defining views


views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('index.html')


