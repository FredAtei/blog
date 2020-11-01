from flask import render_template,request,redirect,url_for,abort,flash
from . import main
from flask.views import View,MethodView

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    
    title = 'Blog'
    
    return render_template('index.html', title = title)