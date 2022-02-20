import os

from application_core.services import AppConfigurationService


class AppConfigurations(AppConfigurationService):
    def __init__(self, app):
        self._app = app
        self.add_configurations()

    @property
    def app(self):
        return self._app

    def add_configurations(self) -> None:
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('REPOSITORY_URI')
        self.app.config['PROPAGATE_EXCEPTIONS'] = True
        self.app.secret_key = os.environ.get('APP_SECRET_KEY')
