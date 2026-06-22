from functools import wraps
from flask import request, session, redirect, url_for, flash

def login_necessario(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            flash('Efetue login para prosseguir', 'erro')
            return redirect(url_for('homepage'))
        return func(*args, **kwargs)
    return wrapper