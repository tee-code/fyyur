from app import db

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#Show Model - it shows the relationship (many to many) between Artist and Vendor models
class Show(db.Model):
  __tablename__ = 'shows'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime())
  artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
