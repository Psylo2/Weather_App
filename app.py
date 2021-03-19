import os
from flask import Flask, render_template, request, redirect, flash

from db.db import db
from models.city import CityModel


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/weather.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.urandom(16).hex()
db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    db.create_all()
    if request.method == 'POST':
        name = request.form.get('city_name')
        all_cities = [city.name for city in CityModel.query.all()]

        if name not in all_cities:
            city = CityModel(name)
            if city.get_weather() != 1:
                city.save_to_db()
            else:
                flash("The city doesn't exist!")
        else:
            flash("The city has already been added to the list!")

    weather = [city.get_weather() for city in CityModel.query.all()]

    if not weather:
        flash("Please Add a CityModel!")
    return render_template('base.html', weather=reversed(weather))

@app.route('/delete/<int:_id>', methods=['POST'])
def remove(_id: int):
    if request.method == 'POST':
        city = CityModel.find_by_id(_id)
        if not city:
            flash("CityModel ID not exists")
        city.delete_from_db()
        flash(f"{city.name.capitalize()} has been removed")
    return redirect('/')

if __name__ == '__main__':
    db.init_app(app)
    app.run(debug=True)
