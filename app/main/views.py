from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,AddBlog
from ..models import User,Comment,Blog
from flask_login import login_required,current_user
from .. import db,photos


# Views
@main.route('/')
def index():

    '''
    View root page function that returns the index page and its data
    '''
    return render_template('index.html')

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

@main.route('/blogs')
def blogs():
    title = 'Blogs Added'
    blogs = Blog.query.order_by(
        Blog.posted_on.desc())

    

    return render_template('blogs.html',blogs = blogs, title=title)

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

@main.route('/view_comments/<id>')
@login_required
def view_comments(id):
    comment = Comment.get_comments(id)
    title = 'View Comments'
    return render_template('comment.html', comment=comment, title=title)

@main.route('/comment/new/<int:blog_id>', methods = ['GET','POST'])
@login_required
def new_comment(blog_id):
    form = CommentForm()
    title = 'Add a comment'
    blog = Blog.query.filter_by(id=blog_id).first()
    if form.validate_on_submit():
        comment = form.comment.data

        new_comment = Comment(comment = comment,blog_id = blog_id, user_id=current_user.id)
        db.session.add(new_comment)
        db.session.commit()
        

        return redirect(url_for('.view_comments', id= blog.id))

    
    return render_template('add_comment.html', form = form,blog = blog,title=title  )


@main.route('/blog/<blog_id>/update', methods = ['GET','POST'])

def updateblog(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    form = AddBlog()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.content = form.content.data
        db.session.commit()
       
        return redirect(url_for('main.blogs',id = blog.id)) 
    if request.method == 'GET':
        form.title.data = blog.title
        form.content.data = blog.content
    return render_template('add_blog.html', form = form)


