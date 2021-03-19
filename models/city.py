import requests
from datetime import datetime, timezone, timedelta
from flask import redirect, flash


from db.db import db, API_KEY


class CityModel(db.Model):
    __tablename__ = 'city'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return '<CityModel %r>' % self.name

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
            time = 'night' if time < 6 else 'day' if 6 <= time < 15 else 'evening-morning'

            return {
                'time': time,
                'degrees': round(info['main']['temp']),
                'state': info['weather'][0]['main'],
                'city': info['name'].capitalize(),
                'id': self.id
            }

        except requests.HTTPError:
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
    def find_by_city(cls, name: str) -> "CityModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_city_params(cls):
        return cls.get_weather(cls.find_by_city(cls.name))

    @classmethod
    def find_by_id(cls, _id: int) -> "CityModel":
        return cls.query.filter_by(id=_id).first()
