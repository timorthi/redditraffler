from flask import (
    abort,
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from app.util import reddit

base = Blueprint('base', __name__)


@base.route('/')
def index():
    return render_template('base/index.html',
                           title='Home',
                           reddit_login_url=reddit.get_auth_url())


@base.route('/terms-of-service')
def tos():
    return render_template('base/terms-of-service.html',
                           title='Terms of Service')


@base.route('/privacy-policy')
def privacy_policy():
    return render_template('base/privacy-policy.html',
                           title='Privacy Policy')
