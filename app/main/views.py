from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile
from ..models import User
from flask_login import login_required,current_user
from .. import db,photos

@main.route('/')
@login_required
def index():

    '''
    View root page function that returns the index page and its data
    '''


    title = 'Home - Shitandi blog wbsite'
    content = "WELCOME TO SHITANDI BLOG WEBSITE"

    return render_template('index.html', title = title,content = content)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)