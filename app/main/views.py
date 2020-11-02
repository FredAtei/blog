from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,AddBlog,CommentForm
from ..models import User,Blog
from flask_login import login_required,current_user
from .. import db,photos

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Home'

    return render_template('index.html', title = title)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)    

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))    

@main.route('/blogs/new', methods = ['GET','POST'])
@login_required
def new_blog():
    title = 'New | Blog '
    form = AddBlog()
    
    if form.validate_on_submit():
        blog = Blog(title=form.title.data, content=form.content.data,user=current_user)
       
        db.session.add(blog)
        db.session.commit()
        
        return redirect(url_for('main.blogs'))
        
    
    return render_template('add_blog.html',form=form, title = title)    