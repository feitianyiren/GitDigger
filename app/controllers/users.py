from app.models.user import User
from app import app, db, login_manager
from app.helpers.github_helper import GitHubHelper
from app.helpers.application_helper import flash
from flask import Blueprint, url_for, render_template
from flask import jsonify, request, redirect, session
from wtforms import TextField, TextAreaField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import logout_user, login_required, login_user, current_user
from flask_wtf import FlaskForm as Form

users = Blueprint('users', __name__)
github_helper = GitHubHelper(app)
login_manager.login_view = 'users.login'

class RegistrationForm(Form):
    username = TextField('Username', [validators.Length(min=4, max=32)])
    email = TextField('Email Address', [validators.Length(min=6, max=32)])
    password = PasswordField('New Password', [
        validators.Required(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')

    def validate(self):
        if not Form.validate(self):
            return False
        if User.query.filter_by(username=self.username.data).first():
            self.username.errors.append('Username is already taken')
            return False
        if User.query.filter_by(username=self.email.data).first():
            self.email.errors.append('Email is already taken')
            return False
        return True

class LoginForm(Form):
    user = None
    login = TextField('Username or email address', [
        validators.Required(),
        validators.Length(min=4, max=32)
    ])
    password = PasswordField('Password', [
        validators.Required()
    ])

    def validate(self):
        print 'validate'
        if not Form.validate(self):
            print 'validate False'
            return False
        login = self.login.data
        if login[1:-1].find('@') >= 0:
            user = User.query.filter_by(email=login).first()
            login_type = 'email'
        else:
            user = User.query.filter_by(username=login).first()
            login_type = 'username'
        print user, login_type
        if user is None:
            self.login.errors.append('Unknown %s' % login_type)
            return False
        if not check_password_hash(user.password, self.password.data):
            self.password.errors.append('Invalid password')
            return False
        self.user = user
        return True

class ProfileForm(Form):
    name = TextField('Name', [validators.Length(max=32)])
    bio = TextAreaField('Bio', [validators.Length(max=160)])

@users.route('/join', methods=['GET', 'POST'])
def join():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        pw_hash = generate_password_hash(form.password.data)
        user = User(form.username.data, form.email.data, pw_hash)
        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering')
        return redirect(url_for('users.login'))
    return render_template('join.html', form=form)

@login_manager.user_loader
def load_user(userid):
    return User.query.get(int(userid))

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        login_user(form.user)
        flash('Logged in successfully')
        next = request.args.get('next')
        return redirect(next or url_for('index'))
    return render_template('login.html', form=form)

@users.route('/settings')
@login_required
def settings():
    return redirect(url_for('users.profile'))

@users.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = current_user
    form = ProfileForm(request.form, name=user.name, bio=user.bio)
    if request.method == 'POST' and form.validate_on_submit():
        current_user.name = form.name.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Profile updated successfully')
    return render_template('settings/profile.html', form=form)

@users.route('/settings/account', methods=['GET', 'POST'])
@login_required
def account():
    return render_template('settings/account.html')

@users.route('/settings/repositories', methods=['GET', 'POST'])
@login_required
def repositories():
    return render_template('settings/repositories.html')

@users.route('/settings/github', methods=['GET', 'POST'])
@login_required
def user_github():
    account = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'unlink':
            current_user.github_token = ''
            db.session.commit()
    integration = github_helper.get_integration()
    if current_user.github_token:
        try:
            account = github_helper.get('user')
        except Exception as e:
            pass
    return render_template('settings/github.html',
                            integration=integration, account=account)

@users.route('/settings/github/install', methods=['GET', 'POST'])
@login_required
def user_github_install():
    integration = github_helper.get_integration()
    if integration:
        return redirect(url_for('users.user_github'))
    app_url = 'https://github.com/apps/'
    app_url += app.config['GITHUB_APP_NAME']
    return redirect(app_url)

@users.route('/auth/github')
def auth_github():
    session['next_url'] = request.args.get('next')
    return github_helper.authorize()

@users.route('/auth/github/callback')
@github_helper.authorized_handler
def authorized(access_token):
    next_url = session.get('next_url')
    if next_url is None:
        next_url = url_for('index')
    else:
        session.pop('next_url')
    if access_token is None:
        return redirect(next_url)
    print access_token
    for i in [0]:
        print current_user
        if current_user.is_authenticated:
            current_user.github_token = access_token
            db.session.commit()
            break
        user = User.query.filter_by(github_token=access_token).first()
        print user
        if user is None:
            break
        login_user(user)
    return redirect(next_url)

@github_helper.access_token_getter
def token_getter():
    if current_user is not None:
        return current_user.github_token

@users.route('/api/users/<string:username>', methods=['GET'])
def get(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify(status=0, user=user)
    return jsonify(status=404)

app.register_blueprint(users)