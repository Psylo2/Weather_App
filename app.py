from flask import Flask
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)


from interface.controllers import city_blueprint

from infrastructure.adapters import repository
from infrastructure.queries import CityRepositoryQuery

from application.core import AppConfigurations
from application.handlers import CityHandler


app = Flask(__name__,
            static_folder='interface/gui/static',
            template_folder='interface/gui/templates')

AppConfigurations(app=app)

repository.init_app(app=app)

city_repository_queries_service = CityRepositoryQuery()
city_handler = CityHandler(city_repository_queries_service=city_repository_queries_service)
city_blueprint.handler = city_handler

app.register_blueprint(blueprint=city_blueprint)

@app.before_first_request
def create_tables():
    repository.create_all(app=app)


if __name__ == '__main__':
    app.run(debug=False)
