  
from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from guess_language import guess_language
from app import db
from app.main.forms import EditProfileForm, EmptyForm, PostForm#, SearchForm, MessageForm
from app.models import User, Post
from app.translate import translate
from app.main import bp
from flask import g


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

    g.locale = str(get_locale())
@bp.before_request
def before_request():
    # ...
    g.locale = str(get_locale())
@bp.route('/translate', methods=['POST'])
@login_required
def translate_text():
    return jsonify({'text': translate(request.form['text'],
                                      request.form['source_language'],
                                      request.form['dest_language'])})
    
    
@bp.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.home'))


@bp.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('main.home'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('main.user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('main.user', username=username))
    else:
        return redirect(url_for('main.home'))

@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.explore', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('home.html', title='Explore', posts=posts.items,
                          next_url=next_url, prev_url=prev_url)

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    
    form = PostForm()
    if form.validate_on_submit():
        language = guess_language(form.post.data)
        if language == 'UNKNOWN' or len(language) > 5:
            language = ''
        post = Post(body=form.post.data, author=current_user,language=language)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        
        return redirect(url_for('main.home'))
    countdowns=[{'NameProject':'Kim 18 Geburtstag','Notes':'Make a collage of pictures','DueDate':'29.01.2021','Countdown':'x days and x minuetes'},{'NameProject':'Nikolaus','Notes':'Small present','DueDate':'06.12.2020','Countdown':'x days and x minuetes'}]
    page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.home', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('main.home', page=posts.prev_num) \
        if posts.has_prev else None
    return render_template('home.html', title='Home', form=form,
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url,countdowns=countdowns)

@bp.route('/about/')

def about():
    return render_template('about.html')
