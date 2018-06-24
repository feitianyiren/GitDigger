import flask
from app import app
from datetime import datetime
from flask_login import current_user

def flash(message, category='info'):
    flask.flash(message, category)

@app.template_global()
def timeago_tag(time, classname=''):
    html = '<time class="timeago {0}" datetime="{1}" title="{1}">{2}</time>'
    return html.format(classname, time.isoformat(), time.ctime())

@app.template_global()
def human_number(num):
    if num > 999:
        return ('%.1f' % (num / 1000.0)).rstrip('0').rstrip('.') + 'k'
    return num

@app.template_global()
def get_copyright_year():
    return datetime.now().year

@app.template_global()
def get_body_class():
    body_class = '-'.join(['page'] + flask.request.endpoint.split('.'))
    if current_user.is_authenticated:
        body_class = body_class + ' logged-in'
    return body_class

@app.template_global()
def url_for_vote(target):
    if not current_user.is_authenticated:
        return ''
    if target.__tablename__ == 'issue':
        return flask.url_for('api.issue_voters', issue_id=target.id,
                            username=current_user.username)
    return ''
