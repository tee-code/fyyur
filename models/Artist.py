from app import db

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    # genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
  
    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    website = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String(120)))

        #relationship
    shows = db.relationship('Show', backref=db.backref('artist', cascade='all, delete', lazy='dynamic'))

    def __repr__(self) -> str:
        return super().__repr__()