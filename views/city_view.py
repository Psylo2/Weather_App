from flask import Blueprint, render_template, flash, request

from models import CityEntity

city_blueprint = Blueprint('city', __name__)
city_blueprint.handler = None


@city_blueprint.get('/')
def city_weather_get():
    weathers = city_blueprint.handler.get_all_cities_current_weather()

    if not weathers:
        flash("Please Add a City!")
    return render_template('base.html', weather=reversed(weathers))


@city_blueprint.post('/')
def city_weather_post():
    city_name = request.form.get('city_name')
    all_cities_registered = city_blueprint.handler.get_all_cities_from_repository()

    is_city_registered = city_name in all_cities_registered
    if is_city_registered:
        flash("The city has already been added to the list!")
        return city_weather_get()

    city = CityEntity(name=city_name)
    is_valid_city_name = city_blueprint.handler.get_weather(city=city.dict())

    if not is_valid_city_name:
        flash("The city doesn't exist!")
        return city_weather_get()

    city_blueprint.handler.register_city(city=city)
    return city_weather_get()


@city_blueprint.post('/delete/<int:_id>')
def city_weather_remove(_id: int):
    city = city_blueprint.handler.remove_city(_id=_id)
    if not city:
        flash("City ID not exists")
        return city_weather_get()

    flash("City has removed")
    return city_weather_get()
