from flask import Blueprint, render_template, request


city_blueprint = Blueprint('city', __name__)
city_blueprint.handler = None


@city_blueprint.get('/')
def city_weather_get():
    all_weathers = city_blueprint.handler.get_all_cities_current_weather()
    return render_template('base.html', weather=reversed(all_weathers))


@city_blueprint.post('/')
def city_weather_post():
    city_name = request.form.get('city_name')
    city_blueprint.handler.register_city(city_name=city_name)
    return city_weather_get()


@city_blueprint.post('/delete/<int:_id>')
def city_weather_remove(_id: int):
    city_blueprint.handler.remove_city(_id=_id)
    return city_weather_get()
