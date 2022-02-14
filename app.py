from dotenv import load_dotenv

load_dotenv(".env", verbose=True)

from flask import Flask
from manager.manager_repository import repository
from manager.app_configurations import AppConfigurations

from factory import Factory
from views.city_view import city_blueprint
from handlers import CityHandler


app = Flask(__name__)
AppConfigurations(app=app)

repository.init_app(app=app)
repository.create_all(app=app)

factory = Factory()
city_handler = CityHandler(factory=factory)
city_blueprint.handler = city_handler

app.register_blueprint(blueprint=city_blueprint)


if __name__ == '__main__':
    app.run(debug=False)
