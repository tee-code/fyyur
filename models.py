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
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    website_link = db.Column(db.String(500))
    genres = db.Column(db.ARRAY(db.String(120)))

        #relationship
    shows = db.relationship('Show', lazy='dynamic', backref=db.backref('artist', cascade='all, delete', lazy='dynamic', uselist=True))

    def __repr__(self) -> str:
        return super().__repr__()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

    # TODO: implement any missing fields, as a database migration using Flask-Migrate
    genres = db.Column(db.ARRAY(db.String(120)))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.String(500))
    website_link = db.Column(db.String(500))

    #relationship
    shows = db.relationship('Show', lazy='dynamic', backref=db.backref('venue', cascade='all, delete', lazy='dynamic', uselist=True))

    def __repr__(self) -> str:
        return super().__repr__()

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#Show Model - it shows the relationship (many to many) between Artist and Vendor models
class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime())
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()


