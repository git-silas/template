import os

from flask import Flask, g, session
from flask_wtf.csrf import CSRFProtect
from typing import Optional, Any, Dict, cast

from ..repo.base import AbstractRepository, ConnectionAPI

from webtemplate.repo import create_repository
from webtemplate.repo.models import User
 
from webtemplate.web.core import utils

from webtemplate.web.main import views as main_views
from webtemplate.web.auth import views as auth_views


class Template(Flask):

    def __init__(self, name: str):
        super().__init__(name)
        self._repository: Optional[AbstractRepository] = None

    def setup_config(self, config_mapping: Dict[str, Any] = None):
        self.config.from_pyfile('config.py')
        if config_mapping:
            if config_mapping.get('TESTING', False):
                self.config.from_mapping(
                    SECRET_KEY='dev',
                    REPOSITORY='ram://',
                    WTF_CSRF_ENABLED=False
                )
            self.config.from_mapping(config_mapping)

        for key, value in self.config.items():
            new_value = os.environ.get(key, None)
            if new_value is None:
                continue
            if isinstance(value, str):
                self.config[key] = new_value
            elif isinstance(value, bool):
                self.config[key] = utils.to_bool(new_value)

        self.config['DATABASE_URL'] = {
            "type": self.config["DB_TYPE"],
            "host": self.config["DB_HOST"],
            "database": self.config["DB_DATABASE"],
            "user": self.config["DB_USER"],
            "pw": self.config["DB_PW"],
            "port": self.config["DB_PORT"],
        }

        self.config["AUTH_CASE"] = utils.to_bool(
            self.config.get("AUTH_CASE", None)
        )

    def setup_repository(self):
        self._repository = create_repository(self.config['DATABASE_URL'])

        def close_connection(_exc: BaseException = None):
            connection = g.pop('connection', None)
            if connection:
                connection.close()

        self.teardown_request(close_connection)

    def get_connection(self) -> ConnectionAPI:
        if 'connection' not in g:
            if self._repository is None:
                raise TypeError('Repository not set.')
            g.connection = self._repository.create()
        return cast(ConnectionAPI, g.connection)

    def login(self, user: User):
        self._clear_session()
        session['user'] = user
    
    def logout(self):
        self._clear_session()

    @staticmethod
    def _clear_session():
        keys = set(session.keys()) - {"connection_messages"}
        for key in keys:
            del session[key]
    
    def _set_template_folder(self):
        template_folder = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        template_folder = os.path.join(template_folder, "webtemplate")
        template_folder = os.path.join(template_folder, "web")
        template_folder = os.path.join(template_folder, "templates")
        self.template_folder = template_folder
    
    def setup(self) -> None:
        self.setup_repository()



def create_app(config_mapping: Dict[str, Any] = None) -> Template:

    app = Template('webtemplate.web')
    app.setup_config(config_mapping)

    csrf = CSRFProtect(app)

    csrf.init_app(app)

    app.add_url_rule('/', 'home', main_views.home, methods=['GET', 'POST'])
    

    app.add_url_rule('/registration', 'registration', auth_views.registration, methods=['GET', 'POST'])
    app.add_url_rule('/registration/user', 'register_user', auth_views.register_user, methods=['GET', 'POST'])
    app.add_url_rule('/login', 'login', auth_views.login, methods=['GET', 'POST'])
    app.add_url_rule('/login/user', 'login_user', auth_views.login_user, methods=['GET', 'POST'])
    app.add_url_rule('/logout', 'logout', auth_views.logout, methods=['GET', 'POST'])

    app.setup()

    return app