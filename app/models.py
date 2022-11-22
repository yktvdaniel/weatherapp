from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Result(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    location = db.Column(db.Text(), nullable=False)
    temp = db.Column(db.Float(), nullable=False)
    feels_like = db.Column(db.Float(), nullable=False)
    timestamp = db.Column(db.Integer(), nullable=False)
    icon_url = db.Column(db.Text(), nullable=False)
    weather = db.Column(db.Text(), nullable=False)
    temp_min = db.Column(db.Float(), nullable=False)
    temp_max = db.Column(db.Float(), nullable=False)
    created = db.Column(db.Float(), nullable=False)
    created_url = db.Column(db.String(), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'location': self.location,
            'temp': self.temp,
            'feels_like': self.feels_like,
            'timestamp': self.feels_like,
            'icon_url': self.icon_url,
            'weather': self.weather,
            'temp_min': self.temp_min,
            'temp_max': self.temp_max,
            'created': self.created,
            'created_url': self.created_url
        }

