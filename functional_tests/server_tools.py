from fabric.api import run, env
from fabric.context_managers import settings

_URL = {env.host: "tdd-django.niuroweb.net"}
def _get_manage_dot_py(host):
    return f'~/sites/{_URL[env.host]}/virtualenv/bin/python ~/sites/{_URL[env.host]}/source/manage.py'

def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'juan@{host}'):
        run(f'{manage_dot_py} flush --noinput')

def create_session_on_server(host, email):
    manage_doy_py = _get_manage_dot_py(host)
    with settings(host_string=f'juan@{host}'):
        session_key = run(f'{manage_doy_py} create_session {email}')
        return session_key.strip()

