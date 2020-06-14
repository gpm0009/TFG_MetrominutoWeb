"""
    metrominuto_app.utils.decorators
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module contains function decorators useful for the application.

"""
from functools import wraps
from flask import flash, redirect, url_for
from flask import session


def log_in(controller):
    """
    Decorator that assures only logged in users can access some routes
    in the applicaction.

    Parameters
    ----------
    controller : function
        Controller (route) to be decorated.

    Returns
    -------
    function
        Decorated function.

    """

    @wraps(controller)
    def decorated_function(*args, **kwargs):
        if session.get('email') is None:
            flash('Página con acceso restringido a usuarios autenticados. '
                  'Necesita iniciar sesión primero para continuar.', 'warning')
            return redirect(url_for('main.widget'))
        else:
            return controller(*args, **kwargs)

    return decorated_function
