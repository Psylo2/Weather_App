from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from flask import Flask
from manager.manager_repository import repository
from manager.app_configurations import AppConfigurations

from factory import Factory
from infrastructure.views import city_blueprint
from application.handlers import CityHandler


app = Flask(__name__)
AppConfigurations(app=app)

repository.init_app(app=app)

factory = Factory()
city_handler = CityHandler(factory=factory)
city_blueprint.handler = city_handler

try:
    app.register_blueprint(blueprint=city_blueprint)
except Exception as e:
    print(e)

@app.before_first_request
def create_tables():
    repository.create_all(app=app)


if __name__ == '__main__':
    app.run(debug=False)
