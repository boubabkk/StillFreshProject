import csv
from datetime import datetime
from flask_login import login_required, current_user, logout_user, login_user, LoginManager
from flaskmusic import app, db
from flask import render_template, url_for, redirect, flash, request
from flaskmusic.forms import LoginForm, Registration, UpdateAccountForm, RequestResetForm, ResetPasswordForm, ArtistForm
from flaskmusic.models import User, Artist
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ** HOME **
@app.route('/')
@app.route('/home')
def home():
    return render_template('stillFresh.html')


@app.route('/home/browse')
@login_required
def browse():
    return render_template('home/browse.html')


@app.route('/home/premium')
def premium():
    file_name = 'data/plans.csv'
    try:
        with open(file_name) as f:
            list_plans = list(csv.reader(f))[1:]
            headers = list_plans[0:1]
            prices = list_plans[1:2]
            return render_template('home/premium.html', list_plans=list_plans, prices=prices, headers=headers)
    except IOError:
        return 'Problem opening file: ' + file_name


# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Password Reset Request', sender=app.config['MAIL_USERNAME'], recipients=[user.email])
#     msg.body = f'''To reset your password, visit the folling link:
# {url_for('reset_password', token=token, _external=True)}
# If you didn't make this request then discard this email.
# '''
#     mail.send(msg)


@app.route("/home/reset_request", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('logout'))

    form = RequestResetForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            print('Fail')
            return render_template('home/reset_request.html', title='Reset Password', form=form)
        else:
            print('Success')
            user = User.query.filter_by(email=form.email.data).first()
            # send_reset_email(user)
            flash('Check you email for instruction on resetting your password', 'success')
            return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('home/reset_request.html', title='Reset Password', form=form)


@app.route("/home/reset_password/<token>", methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        # Hash password before putting it in the DB
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()

        flash(f'Your password has been successfully reset', 'success')
        return redirect(url_for('login'))
    return render_template('home/reset_password.html', title='Reset Password', form=form)


# ** AUTHENTICATE **
@app.route('/authenticate/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))

    form = LoginForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            flash('Login Unsuccessful. Please check email an password', 'danger')
            return render_template("authentication/login.html", title='Login', form=form)
        else:
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('liked_song'))

        flash('Login Unsuccessful. Please check email an password', 'danger')
        return render_template("authentication/login.html", title='Login', form=form)
    if request.method == 'GET':
        return render_template("authentication/login.html", title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return render_template('stillFresh.html')


@app.route('/authenticate/signup', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('browse'))

    form = Registration()
    if request.method == 'POST':
        if not form.validate_on_submit():
            print("Fail")
            return render_template("authentication/signup.html", title='Register', form=form)
        else:
            print("Success")

            # Hash password before putting it in the DB
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()

            flash(f'Account created for {form.username.data}', 'success')
            return redirect(url_for('login'))
    if request.method == 'GET':
        return render_template("authentication/signup.html", title='Register', form=form)


# ** MY LIBRARY  **
@app.route('/my-library/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            print("Fail")
            return render_template('my-library/account.html', form=form)
        else:
            print("Success")
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        return render_template('my-library/account.html', form=form)


@app.route('/my-library/artist')
@login_required
def artist():
    return render_template('my-library/artist.html')


@app.route('/my-library/spotify')
@login_required
def spotify():
    return render_template('my-library/spotify.html')


@app.route('/my-library/likedSong')
@login_required
def liked_song():
    artists = Artist.query.all()
    return render_template('my-library/liked-song.html', artists=artists)


@app.route('/my-library/create/artist', methods=['GET', 'POST'])
@login_required
def create_artist():
    form = ArtistForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            print("Fail")
            return render_template('my-library/create/create-artist.html', title='Create Artist', form=form)
        else:
            print("Success")
            artistDB = Artist(artist=form.artist.data, song=form.song.data, album=form.album.data,
                              song_release_date=datetime.utcnow())
            db.session.add(artistDB)
            db.session.commit()

            flash('Your artist has been created!', 'success')
            return redirect(url_for('liked_song'))
    if request.method == 'GET':
        return render_template('my-library/create/create-artist.html', title='Create Artist', form=form)


@app.route('/my-library/details/artist-detail/<int:artist_id>', methods=['GET', 'POST'])
@login_required
def artist_details(artist_id):
    form = ArtistForm()
    artistDetails = Artist.query.get_or_404(artist_id)
    if request.method == 'GET':
        form.artist.data = artistDetails.artist
        form.song.data = artistDetails.song
        form.album.data = artistDetails.album
        return render_template('my-library/details/artist-detail.html', artist=artistDetails, form=form)
    elif request.method == 'POST':
        artistDetails.artist = form.artist.data
        artistDetails.song = form.song.data
        artistDetails.album = form.album.data
        db.session.commit()
        flash('Your artist has been updated!', 'success')
        return redirect(url_for('liked_song'))


@app.route('/my-library/delete/<int:artist_id>', methods=['POST'])
@login_required
def delete_artist(artist_id):
    artistToBeDeleted = Artist.query.get_or_404(artist_id)
    db.session.delete(artistToBeDeleted)
    db.session.commit()
    flash('Your artist has been successfully deleted!', 'success')
    return redirect(url_for('liked_song'))


@app.route('/my-library/album')
@login_required
def album():
    return render_template('my-library/album.html')


@app.route('/test')
def test():
    return render_template('/test.html')