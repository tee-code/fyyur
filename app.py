#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
from re import S
import sys
import dateutil.parser
import babel
from flask import Flask, jsonify, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#
from models import *

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  venues = Venue.query.order_by(Venue.id).limit(10).all()
  venues.reverse()
  artists = Artist.query.order_by(Artist.id).limit(10).all()
  artists.reverse()
  data = {
    "venues": venues,
    "artists": artists
  }
  return render_template('pages/home.html', data=data)


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  
  venues = Venue.query.all()
  areas = {}
  data = []

  for index,venue in enumerate(venues):
    area = venue.city+":"+venue.state 
    
    if area not in areas.keys():
      areas[area] = index
      data.append({
        "city": venue.city,
        "state": venue.state,
        "venues": [{
          "id": venue.id,
          "name": venue.name,
          "num_upcoming_shows": venue.shows.filter(Show.start_time > datetime.now()).count(),
          }]
      })
    else:
      key = areas[area]
      data[key]['venues'].append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": venue.shows.filter(Show.start_time > datetime.now()).count(),
      })

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"


  query = request.form.get('search_term', '')  #get the search item from request

  venues_by_name = Venue.query.filter(Venue.name.ilike(f"%{query}%")).all()
  venues_by_state = Venue.query.filter(Venue.state.ilike(f"%{query}%")).all()
  venues_by_city = Venue.query.filter(Venue.city.ilike(f"%{query}%")).all()

  response = {
    "name": {
      "count": len(venues_by_name),
      "data": []
    },
    "state": {
      "count": len(venues_by_state),
      "data": []
    },
    "city": {
      "count": len(venues_by_city),
      "data": []
    }
    
  }

  for venue in venues_by_name:
    response["name"]["data"].append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": venue.shows.filter(Show.start_time > datetime.now()).count(),
    })
  for venue in venues_by_state:
    response["state"]["data"].append({
      "id": venue.id,
      "name": venue.name,
      "state": venue.state,
      "num_upcoming_shows": venue.shows.filter(Show.start_time > datetime.now()).count(),
    })
  for venue in venues_by_city:
    response["city"]["data"].append({
      "id": venue.id,
      "name": venue.name,
      "city": venue.city,
      "num_upcoming_shows": venue.shows.filter(Show.start_time > datetime.now()).count(),
    })

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id

  venue = Venue.query.get(venue_id)

  if not venue: 
    return render_template('errors/404.html')

  past_shows = venue.shows.filter(Show.start_time < datetime.now()).all()
  upcoming_shows = venue.shows.filter(Show.start_time > datetime.now()).all()

  past_shows_data = []
  upcoming_shows_data = []

  for past_show in past_shows:
    past_shows_data.append({
      "artist_id": past_show.artist_id,
      "artist_name": past_show.artist.filter_by(id=past_show.artist_id).first().name,
      "artist_image_link": past_show.artist.filter_by(id=past_show.artist_id).first().image_link,
      "start_time": str(past_show.start_time)
    })
  
  for upcoming_show in upcoming_shows:
    upcoming_shows_data.append({
      "artist_id": upcoming_show.artist_id,
      "artist_name": upcoming_show.artist.filter_by(id=upcoming_show.artist_id).first().name,
      "artist_image_link": upcoming_show.artist.filter_by(id=upcoming_show.artist_id).first().image_link,
      "start_time": str(upcoming_show.start_time)
    })
  
  venue.past_shows = past_shows_data
  venue.past_shows_count = len(past_shows_data)
  venue.upcoming_shows = upcoming_shows_data
  venue.upcoming_shows_count = len(upcoming_shows_data)

  return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  
  venue = dict()

  try:
    name = request.form.get('name', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    address = request.form.get('address', '')
    phone = request.form.get('phone', '')
    genres = request.form.getlist('genres')
    image_link = request.form.get('image_link', '')
    facebook_link = request.form.get('facebook_link', '')
    website_link = request.form.get('website_link', '')

    seeking_talent = bool(request.form.get('seeking_talent'))
     
    seeking_description = request.form['seeking_description']

    venue = Venue(name=name, phone=phone, genres=genres, city=city, state=state, address=address, facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_talent=seeking_talent, seeking_description=seeking_description)
    db.session.add(venue)
    db.session.commit()

    flash('Venue ' + venue.name + ' was successfully listed!')

  except:

    venue = request.form.get('name', '')

    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + venue + ' could not be listed.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    db.session.rollback()
    print(sys.exc_info())
    
  finally:
    db.session.close()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  success = True
  try:

    Venue.query.filter_by(id=venue_id).delete()
    db.session.commit()
    flash('Venue ' + venue_id + ' was successfully deleted!')

  except:
    success = False
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + venue_id + ' could not be deleted.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return jsonify({'success': success})

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  success = True
  try:

    Artist.query.filter_by(id=artist_id).delete()
    db.session.commit()
    flash('Artist ' + artist_id + ' was successfully deleted!')

  except:
    success = False
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + artist_id + ' could not be deleted.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return jsonify({'success': success})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()

  return render_template('pages/artists.html', artists=artists)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  
  search_term = request.form.get('search_term', '')
  artists_by_name = Artist.query.filter(Artist.name.ilike(f"%{search_term}%")).all()
  artists_by_state = Artist.query.filter(Artist.state.ilike(f"%{search_term}%")).all()
  artists_by_city = Artist.query.filter(Artist.city.ilike(f"%{search_term}%")).all()
  
  response = {
    "name": {
      "count": len(artists_by_name),
      "data": []
    },
    "state": {
      "count": len(artists_by_state),
      "data": []
    },
    "city": {
      "count": len(artists_by_city),
      "data": []
    }
    
  }

  for artist in artists_by_name:
    response['name']['data'].append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": artist.shows.filter(Show.start_time > datetime.now()).count(),
    })

  for artist in artists_by_state:
    response['state']['data'].append({
    "id": artist.id,
    "name": artist.name,
    "state": artist.state,
    "num_upcoming_shows": artist.shows.filter(Show.start_time > datetime.now()).count(),
  })

  for artist in artists_by_city:
    response['city']['data'].append({
    "id": artist.id,
    "name": artist.name,
    "city": artist.city,
    "num_upcoming_shows": artist.shows.filter(Show.start_time > datetime.now()).count(),
  })


  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id

  artist = Artist.query.get(artist_id)

  if not artist: 
    return render_template('errors/404.html')

  past_shows = artist.shows.filter(Show.start_time < datetime.now()).all()
  upcoming_shows = artist.shows.filter(Show.start_time > datetime.now()).all()

  past_shows_data = []
  upcoming_shows_data = []

  for past_show in past_shows:
    past_shows_data.append({
      "venue_id": past_show.venue_id,
      "venue_name": past_show.venue.filter_by(id=past_show.venue_id).first().name,
      "venue_image_link": past_show.venue.filter_by(id=past_show.venue_id).first().image_link,
      "start_time": str(past_show.start_time)
    })
  
  for upcoming_show in upcoming_shows:
    upcoming_shows_data.append({
      "venue_id": upcoming_show.venue_id,
      "venue_name": upcoming_show.venue.filter_by(id=upcoming_show.venue_id).first().name,
      "venue_image_link": upcoming_show.venue.filter_by(id=upcoming_show.venue_id).first().image_link,
      "start_time": str(upcoming_show.start_time)
    })
  
  artist.past_shows = past_shows_data
  artist.past_shows_count = len(past_shows_data)
  artist.upcoming_shows = upcoming_shows_data
  artist.upcoming_shows_count = len(upcoming_shows_data)


  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = Artist.query.get(artist_id)

  if artist:
    form.name.data = artist.name
    form.city.data = artist.city
    form.state.data = artist.state
    form.phone.data = artist.phone
    form.genres.data = artist.genres
    form.facebook_link.data = artist.facebook_link
    form.image_link.data = artist.image_link
    form.website_link.data = artist.website_link
    form.seeking_venue.data = artist.seeking_venue
    form.seeking_description.data = artist.seeking_description

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  artist = Artist.query.get(artist_id)

  try:
    artist.name = request.form.get('name', '')
    artist.city = request.form.get('city', '')
    artist.state = request.form.get('state', '')
    artist.address = request.form.get('address', '')
    artist.phone = request.form.get('phone', '')
    artist.genres = request.form.getlist('genres')
    artist.image_link = request.form.get('image_link', '')
    artist.facebook_link = request.form.get('facebook_link', '')
    artist.website_link = request.form.get('website_link', '')
    
    artist.seeking_venue = bool(request.form.get('seeking_venue'))
    artist.seeking_description = request.form['seeking_description']

    db.session.commit()

    flash('Artist ' + artist.name + ' was successfully updated!')

  except:

    artist = request.form.get('name', '')
    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + artist + ' could not be updated.')
    db.session.rollback()
    print(sys.exc_info())
    
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  
  # TODO: populate form with values from venue with ID <venue_id>

  venue = Venue.query.get(venue_id)

  if venue: 
    form.name.data = venue.name
    form.city.data = venue.city
    form.state.data = venue.state
    form.phone.data = venue.phone
    form.address.data = venue.address
    form.genres.data = venue.genres
    form.facebook_link.data = venue.facebook_link
    form.image_link.data = venue.image_link
    form.website_link.data = venue.website_link
    form.seeking_talent.data = venue.seeking_talent
    form.seeking_description.data = venue.seeking_description

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  venue = Venue.query.get(venue_id)

  try:
    venue.name = request.form.get('name', '')
    venue.city = request.form.get('city', '')
    venue.state = request.form.get('state', '')
    venue.address = request.form.get('address', '')
    venue.phone = request.form.get('phone', '')
    venue.genres = request.form.getlist('genres')
    venue.image_link = request.form.get('image_link', '')
    venue.facebook_link = request.form.get('facebook_link', '')
    venue.website_link = request.form.get('website_link', '')
    venue.seeking_talent = bool(request.form.get('seeking_talent'))  
    
    venue.seeking_description = request.form['seeking_description']

    db.session.commit()

    flash('Venue ' + venue.name + ' was successfully updated!')
  except:

    venue = request.form.get('name', '')

    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Venue ' + venue + ' could not be updated.')
    db.session.rollback()
    print(sys.exc_info())
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  artist = dict()

  try:

    name = request.form.get('name', '')
    city = request.form.get('city', '')
    state = request.form.get('state', '')
    phone = request.form.get('phone', '')
    genres = request.form.getlist('genres')
    image_link = request.form.get('image_link', '')
    facebook_link = request.form.get('facebook_link', '')
    website_link = request.form.get('website_link', '')

    seeking_venue = bool(request.form.get('seeking_venue'))
    seeking_description = request.form['seeking_description']
    
    artist = Artist(name=name, phone=phone, genres=genres, city=city, state=state, facebook_link=facebook_link, image_link=image_link, website_link=website_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
    db.session.add(artist)
    db.session.commit()

    flash('Artist ' + artist.name + ' was successfully created!')

  except:

    artist = request.form.get('name', '')

    # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    flash('An error occurred. Artist ' + artist + ' could not be created.')

    db.session.rollback()
    #print error message
    print(sys.exc_info())

  finally:
    
    db.session.close()
  
  return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.

  shows = Show.query.all()
  data = []

  for show in shows:
    
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.filter_by(id=show.venue_id).first().name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.filter_by(id=show.artist_id).first().name,
      "artist_image_link": show.artist.filter_by(id=show.artist_id).first().image_link,
      "start_time": str(show.start_time)
    })

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  show = {}
  error = False
  try:

    start_time = request.form.get('start_time', '')
    artist_id = request.form.get('artist_id', '')
    venue_id = request.form.get('venue_id', '')

    show = Show(start_time=start_time, artist_id=artist_id, venue_id=venue_id)
    db.session.add(show)
    db.session.commit()

    flash('Show was successfully listed!')

  except:
    # TODO: on unsuccessful db insert, flash an error instead.
    # e.g., flash('An error occurred. Show could not be listed.')
    flash('An error occurred. Show could not be created.')
    # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

    db.session.rollback()
    print(sys.exc_info())
  finally:

    db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
