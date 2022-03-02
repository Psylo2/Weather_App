from flask import Blueprint, render_template, request, redirect

from application.usecases.services import CityUseCaseService

city_blueprint = Blueprint(name='city',
                           import_name=__name__)
city_blueprint.__setattr__("use_case", CityUseCaseService)


@city_blueprint.get(rule='/')
def city_weather_get():
    all_weathers = city_blueprint.use_case.get_all_cities_current_weather()
    return render_template('base.html', weather=reversed(all_weathers))


@city_blueprint.post(rule='/')
def city_weather_post():
    city_name = request.form.get('city_name')
    city_blueprint.use_case.register_city(city_name=city_name)
    return city_weather_get()


@city_blueprint.post(rule='/delete/<int:_id>')
def city_weather_remove(_id: int):
    city_blueprint.use_case.remove_city(_id=_id)
    return redirect('/')
