from functools import wraps
from flask import flash, redirect, session, url_for


def login_necessario(view):
    @wraps(view)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Efetue login para prosseguir', 'erro')
            return redirect(url_for('homepage'))
        return view(*args, **kwargs)
    return wrapper