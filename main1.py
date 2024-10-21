from flask import Blueprint, render_template, request, redirect, flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from . import db
from .models import User, Post, Comment, Like

main = Blueprint('main', __name__)




@main.route("/<int:post_id>/readmore")
def readmore(post_id):
    post = Post.query.get(post_id)
    return render_template('readmore.html', post=post,user=current_user)

@main.route('/home')
@main.route('/')
def home():
    return render_template('home.html',user=current_user)

@main.route('/aboutme')
def aboutme():
    return render_template('aboutme.html',user=current_user)

@main.route('/contact')
def contact():
    return render_template('contact.html',user=current_user)

@main.route('/admin')
@login_required
def admin():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('admin.html', posts=posts,user=current_user)

@main.route('/index')
def index():
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('index.html', posts=posts,user=current_user)

@main.route('/create-comment/<post_id>',methods=['POST'])
@login_required
def create_comment(post_id):
    text = request.form.get('text')

    if not text:
        flash('Comment cannot be empty!',category='error')
    else:
        post = Post.query.get(post_id)
        if post:
            comment = Comment(text=text,author=current_user.id,post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash('Post does not exist',category='error')

    return redirect(f'/{post_id}/readmore')


@main.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        file = request.files['img']
        filename = file.filename
        post = Post(title=title, body=body, img_name=filename,author=current_user.id)

        if file and filename != '':
            save_path = os.path.join(os.path.join(os.getcwd(), 'static/img'), filename)
            file.save(save_path)
            db.session.add(post)
            db.session.commit()
            return redirect('/admin')
        else:
            db.session.add(post)
            db.session.commit()
            return redirect('/admin')
    elif request.method == 'GET':
        return render_template('create.html',user=current_user)

@main.route('/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update(post_id):
    post = Post.query.get(post_id)
    if request.method == 'POST':
        post.title = request.form.get('title')
        post.body = request.form.get('body')
        db.session.commit()
        return redirect('/admin')
    elif request.method == 'GET':
        return render_template('update.html', post=post,user=current_user)

@main.route('/<int:post_id>/delete', methods=['GET'])
@login_required
def delete(post_id):
    post = Post.query.get(post_id)
    if not post:
        flash('Post not found',category='error')
    elif current_user.id != post.author:
        flash('You are not allowed to delete this post',category='error')
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Post deleted',category='success')
    return redirect('/admin')

@main.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pass = generate_password_hash(password)

        email_exits = User.query.filter_by(username=username).first()
        if email_exits:
            flash('Username already exit',category='error')
        elif len(username) < 2:
            flash('Username is too short',category='error')
        elif len(password) < 6:
            flash('Password is too short',category='error')
        else:
            new_user = User(username=username, password=hashed_pass)
            db.session.add(new_user)
            db.session.commit()
            flash('You are now registered',category='success')
            return redirect('/login')

    elif request.method == 'GET':
        return render_template('signup.html',user=current_user)

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password=password):
            flash('You are now logged in',category='success')
            login_user(user,remember=True)
            return redirect('/admin')
        else:
            flash('Invalid username or password',category='error')
            return redirect('/login')
    elif request.method == 'GET':
        return render_template('login.html',user=current_user)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@main.route('/delete-comment/<comment_id>')
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get(comment_id)
    if not comment:
        flash('Comment not found',category='error')
    elif current_user.id != comment.author and current_user.id != comment.post.author and current_user.id != 1:
        flash('You are not allowed to delete this comment',category='error')
    elif current_user.id == 1 or comment.author or comment.post.author:
        db.session.delete(comment)
        db.session.commit()
        return redirect(f'/{comment.post_id}/readmore')


@main.route('/like-post/<post_id>',methods=['GET'])
@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    like = Like.query.filter_by(author=current_user.id, post_id=int(post_id)).first()
    if not post:
        flash('Post not found',category='error')
    elif like:
        db.session.delete(like)
        db.session.commit()
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    return redirect(f'/{post_id}/readmore')
