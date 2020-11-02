from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,OpinionForm,CommentForm
from ..models import User,Opinion,Comment
from flask_login import login_required,current_user
from .. import db,photos

@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''

    title = 'Blog website'

    return render_template('index.html', title = title)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)


@main.route('/user/<uname>/update',methods = ['GET','opinion'])
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

    return render_template('profile/update.html',form =form, quote=quote)

@main.route('/user/<uname>/update/pic',methods= ['opinion'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/opinion/new_opinion', methods = ['GET','opinion'])
@login_required
def new_opinion():

    form = OpinionForm()

    if form.validate_on_submit():
        opinion= form.description.data
        title=form.opinion_title.data

        # Updated opinion instance
        new_opinion = Opinion(opinion_title=title,description= opinion,user_id=current_user.id)

        title='New Blog'

        new_opinion.save_opinion()

        return redirect(url_for('main.index'))

    return render_template('opinion.html',form= form)

@main.route('/opinion/all', methods=['GET', 'opinion'])
@login_required
def all():
    opinions = Opinion.query.all()

    return render_template('opinions.html', opinions=opinions)

@main.route('/comments/<id>')
@login_required
def comment(id):
    '''
    function to return the comments
    '''
  
    comm =Comment.get_comments(id)
    title = 'comments'
    return render_template('comments.html',comment = comm,title = title)

@main.route('/new_comment/<int:opinion_id>', methods = ['GET', 'opinion'])
@login_required
def new_comment(opinion_id):
  
    opinions = Opinion.query.filter_by(id = opinion_id).first()
    form = CommentForm()

    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment=comment,user_id=current_user.id, opinion_id=opinion_id)

        new_comment.save_comment()

        return redirect(url_for('main.index'))
    title='New comment'
    return render_template('new_comment.html',title=title,comment_form = form,opinion_id=opinion_id)

@main.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    opinion = Opinion.query.get_or_404(id)
    opinion_comments = Comment.query.filter_by(opinion_id=id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(opinion_id=id, comment=comment_form.comment.data, username=current_user)
        new_comment.save_comment()

    return render_template('view.html', opinion=opinion, opinion_comments=opinion_comments, comment_form=comment_form)     