from flask import (
    abort,
    Blueprint,
    render_template,
    request,
    session,
    url_for
)
from app.util import reddit
from app.jobs.raffle_job import raffle
from app.db.models import User

raffles = Blueprint('raffles', __name__)


@raffles.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('raffles/create.html',
                               title='create a raffle',
                               reddit_login_url=reddit.get_auth_url())
    elif request.method == 'POST':
        form = request.form.copy()
        if 'submissionUrl' in form:
            form['submissionUrl'] = _ensure_protocol(form['submissionUrl'])
        if not _validate_raffle_form(form):
            abort(422)

        user = _try_get_user_from_session()
        sub_id = reddit.submission_id_from_url(form.get('submissionUrl'))
        raffle_params = {
            'submission_url': form.get('submissionUrl'),
            'winner_count': form.get('winnerCount', type=int),
            'min_account_age': form.get('minAge', type=int),
            'min_comment_karma': form.get('minComment', type=int),
            'min_link_karma': form.get('minLink', type=int)
        }

        raffle.queue(raffle_params=raffle_params,
                     user=user,
                     job_id=sub_id)
        return 'ok'


def _validate_raffle_form(form):
    # Validate presence of required keys.
    REQUIRED_KEYS = {'submissionUrl', 'winnerCount', 'minAge', 'minComment',
                     'minLink'}
    if not REQUIRED_KEYS.issubset(form.keys()):
        return False

    # Validate integer-value keys.
    # All values must be non-negative. winnerCount must be at least 1.
    INT_KEYS = {'minAge', 'winnerCount', 'minComment', 'minLink'}
    for key in INT_KEYS:
        val = form.get(key, type=int)
        if (not isinstance(val, int)) or (val < 0) or \
           (key == 'winnerCount' and val < 1):
            return False

    # Validate that the submission exists
    url = _ensure_protocol(form.get('submissionUrl'))
    if not reddit.get_submission(sub_url=url):
        return False

    return True


def _ensure_protocol(url):
    if url.startswith('http'):
        return url
    return 'https://' + url


def _try_get_user_from_session():
    if 'reddit_username' in session:
        return User.query \
                   .filter_by(username=session['reddit_username']) \
                   .first()
    else:
        return None
