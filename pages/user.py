from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from .auth import login_required
from ..forms import UserPageForm

bp = Blueprint('user', __name__)


@bp.route('/user/profile', methods=('GET', 'POST'))
@login_required
def profile():
    form = UserPageForm()
    if request.method == 'POST':
        return redirect(url_for('auth.reset_password'))
    
    return render_template('user/profile.html', form=form)
