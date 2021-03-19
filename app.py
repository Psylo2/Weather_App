import os
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import requests
from datetime import datetime, timezone, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/weather.db'
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = os.urandom(16).hex()
API_KEY = "092e16492935f7d7e893c67b0912701f"
db = SQLAlchemy(app)


class City(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return '<City %r>' % self.name

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def get_weather(self):
        params = {'q': self.name, 'appid': API_KEY, 'units': 'metric', 'lang': 'en'}
        try:
            resp = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
            resp.raise_for_status()
            info = resp.json()
            tz_info = timezone(timedelta(seconds=info['timezone']))
            time = datetime.now(tz_info).hour
            time = 'night' if time < 6 else 'day' if 14 <= time < 20 else 'evening-morning'

            return {
                'time': time,
                'degrees': round(info['main']['temp']),
                'state': info['weather'][0]['main'],
                'city': info['name'].capitalize(),
                'id': self.id
            }

        except requests.HTTPError:
            # flash("Invalid request, city name must be valid and exist!")
            return 1

        except requests.RequestException:
            flash("Unable to connect to Weather API site, please try later!")
            self.delete_from_db()
            return redirect('/')

        except FileNotFoundError:
            flash("Error occurred while processing, API unavailable")
            self.delete_from_db()
            return redirect('/')

    @classmethod
    def find_by_city(cls, name: str) -> "City":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_city_params(cls):
        return cls.get_weather(cls.find_by_city(cls.name))

    @classmethod
    def find_by_id(cls, _id: int) -> "City":
        return cls.query.filter_by(id=_id).first()


db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('city_name').lower()
        all_cities = [city.name for city in City.query.all()]

        if name not in all_cities:
            city = City(name)
            if city.get_weather() != 1:
                city.save_to_db()
            else:
                flash("The city doesn't exist!")
        else:
            flash("The city has already been added to the list!")

    weather = [city.get_weather() for city in City.query.all()]

    if not weather:
        flash("Please Add a City!")
    return render_template('base.html', weather=reversed(weather))

@app.route('/delete/<int:_id>', methods=['POST'])
def remove(_id: int):
    if request.method == 'POST':
        city = City.find_by_id(_id)
        if not city:
            flash("City ID not exists")
        city.delete_from_db()
        flash(f"{city.name.capitalize()} has been removed")
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
