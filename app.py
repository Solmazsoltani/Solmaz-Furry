#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import distutils
import json
from urllib import response
from xmlrpc.client import boolean
from click import Abort
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.types import Boolean, String
from sqlalchemy.util import OrderedDict
from sqlalchemy import TypeDecorator, true
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venues(db.Model):
    __tablename__ = 'Venue'

    id    = db.Column(db.Integer, primary_key=True)
    name  = db.Column(db.String)
    city  = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default=False,nullable=True)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Show', backref='Venue', lazy=True)
    def __repr__(self):
         return f'<Venues {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artists(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    Website_link  = db.Column(db.String(120))
    Looking_for_Venues = db.Column(db.Boolean(),default=False, nullable=True)
    Seeking_Description = db.Column(db.String(120))  
    shows = db.relationship('Show', backref='Artist', lazy=True)

    def __repr__(self):
        return f'<Artists {self.id} {self.name}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.now(), nullable=False)

    def __repr__(self):
        return f'<Show {self.id} {self.artist_id} {self.venue_id} {self.start_time}>'
# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.
#db.create_all()

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
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # num_upcoming_shows should be aggregated based on number of upcoming shows per venue.


    #search_result = db.session.query(Venue).filter(Venue.name.ilike(f'%{search_term}%')).all()
    # len(db.session.query(Show).filter(Show.venue_id == result.id).filter(Show.start_time > datetime.now()).all())
    # Querying for cites and states of all venues and unique them
    areas = db.session.query(Venues.city, Venues.state).distinct( Venues.city , Venues.state)
    response = []
    for area in areas:

        # Querying venues and filter them based on area (city, venue)
        result = Venues.query.filter(Venues.state == area.state).filter(Venues.city == area.city).all()

        venue_data = []

        # Creating venues' response
        for Venue in result:
            venue_data.append({
                'id': Venue.id,
                'name': Venue.name,
                'num_upcoming_shows': len(db.session.query(Show).filter(Show.start_time > datetime.now()).all())
            })

        response.append({
                'city': area.city,
                'state': area.state,
                'venues': venue_data
            })

#------------------------------
# data=[{
 #   "city": "San Francisco",
 #   "state": "CA",
  #  "venues": [{
   #   "id": 1,
   #   "name": "The Musical Hop",
   #   "num_upcoming_shows": 0,
   # }, {
   #   "id": 3,
   #   "name": "Park Square Live Music & Coffee",
   #   "num_upcoming_shows": 1,
   # }]
 # }, {
  #  "city": "New York",
  #  "state": "NY",
   # "venues": [{
   #   "id": 2,
   #   "name": "The Dueling Pianos Bar",
   #   "num_upcoming_shows": 0,
   # }]
 # }]
  #-------------------------------------------------------
    return render_template('pages/venues.html', areas=response)
@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

    search_term = request.form.get('search_term', '')
    result = db.session.query(Venues).filter(Venues.name.ilike(f'%{search_term}%')).all()
    count = len(result)
    response = {
        "count": count,
        "data": result
    }
    return render_template('pages/search_venues.html', results=response,search_term=request.form.get('search_term', ''))
  
@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
    venue = Venues.query.filter(Venues.id == venue_id).first()

    past = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
      Show.start_time < datetime.now()).join(Artists, Show.artist_id == Artists.id).add_columns(Artists.id, Artists.name,
                                                                                               Artists.image_link,
                                                                                                Show.start_time).all()

    upcoming = db.session.query(Show).filter(Show.venue_id == venue_id).filter(
        Show.start_time > datetime.now()).join(Artists, Show.artist_id == Artists.id).add_columns(Artists.id, Artists.name,
                                                                                                Artists.image_link,Show.start_time).all()

    upcoming_shows = []

    past_shows = []

    for i in upcoming:
        upcoming_shows.append({
            'artist_id': i[1],
            'artist_name': i[2],
            'artist_image_link': i[3],
            'start_time': str(i[4])
        })

    for i in past:
        past_shows.append({
            'artist_id': i[1],
            'artist_name': i[2],
            'artist_image_link': i[3],
            'start_time': str(i[4])
        })

    if venue is None:
        Abort(404)

    response = {
        "id": venue.id,
        "name": venue.name,
        "genres": [venue.genres],
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past),
        "upcoming_shows_count": len(upcoming),
    }
    return render_template('pages/show_venue.html', venue=response)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    try:
        venues = Venues(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            address=request.form['address'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            website=request.form['website_link'],
            seeking_talent=bool(request.form['seeking_talent']),
            seeking_description=request.form['seeking_description']
        )
        db.session.add(venues)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully added!')
    except Exception as e:
        print(e)
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be added')
        db.session.rollback()
    finally:
        db.session.close()
        return render_template('pages/home.html')
    
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
 

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
        Venues.query.filter(Venues.id == venue_id).delete()
        db.session.commit()
  except : 
        db.session.rollback()
  finally :
        db.session.close()
  return render_template('pages/home.html')



#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  response = Artists.query.all()
  return render_template('pages/artists.html', artists=response)
  

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term', '')
    result = db.session.query(Artists).filter(Artists.name.ilike(f'%{search_term}%')).all()
    count = len(result)
    response = {
        "count": count,
        "data": result
    }
    return render_template('pages/search_artists.html', results=response, search_term=search_term)



@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
      artist = Artists.query.filter(Artists.id == artist_id).first()

      past = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
        Show.start_time < datetime.now()).join(Venues, Show.venue_id == Venues.id).add_columns(Venues.id, Venues.name,
                                                                                             Venues.image_link,
                                                                                             Show.start_time).all()

      upcoming = db.session.query(Show).filter(Show.artist_id == artist_id).filter(
        Show.start_time > datetime.now()).join(Venues, Show.venue_id == Venues.id).add_columns(Venues.id, Venues.name,
                                                                                             Venues.image_link,
                                                                                             Show.start_time).all()

      upcoming_shows = []

      past_shows = []

      for i in upcoming:
        upcoming_shows.append({
            'venue_id': i[1],
            'venue_name': i[2],
            'venue_image_link': i[3],
            'start_time': str(i[4])
        })

      for i in past:
        past_shows.append({
            'venue_id': i[1],
            'venue_name': i[2],
            'venue_image_link': i[3],
            'start_time': str(i[4])
        })

        if artist is None:
         Abort(404)

      response = {
        "id": artist.id,
        "name": artist.name,
        "genres": [artist.genres],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.Website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.Looking_for_Venues,
        "seeking_description": artist.Seeking_Description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past),
        "upcoming_shows_count": len(upcoming),
    }
      return render_template('pages/show_artist.html', artist=response)
 # data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  #return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form=ArtistForm(request.form)
  
  [artist] = Artists.query.filter(Artists.id == artist_id).first()
 
  #form.city.data= artist.city
  #form.id.data= artist.id,
  form.name.data= artist.name,
  form.genres.data= [artist.genres],
  form.city.data= artist.city,
  form.state.data= artist.state,
  form.phone.data= artist.phone,
  form.website_link.data= artist.Website_link,
  form.facebook_link.data= artist.facebook_link,
  form.seeking_venue.data= artist.Looking_for_Venues,
  form.seeking_description.data= bool(artist.Seeking_Description),
  form.image_link.data= artist.image_link,
  response = {
        "id": artist.id,
        "name": artist.name,
       # "genres": [artist.genres],
         #form.city.raw_data: artist.city,
       # "state": artist.state,
       # "phone": artist.phone,
       # "website_link": artist.Website_link,
       # "facebook_link": artist.facebook_link,
       # "seeking_venue": artist.Looking_for_Venues,
        #"seeking_description": artist.Seeking_Description,
        #"image_link": artist.image_link,
        
    }
  
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html',form=form,artist=response)
  # TODO: populate form with fields from artist with ID <artist_id>
 

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
    form=ArtistForm(request.form)
 #try:
    artist=Artists.query.get(artist_id)
    
    artist.name==request.form['name'],
    artist.city=request.form['city'],
    artist.state=request.form['state'],
    artist.phone=request.form['phone'],
    artist.genres=request.form.getlist('genres'),
    artist.image_link=request.form['image_link'],
    artist.facebook_link=request.form['facebook_link'],
    #artist.Looking_for_Venues=request.form['seeking_venue'],
    artist.Website_link=request.form['website_link'].strip(),
    artist.Seeking_Description=request.form['seeking_description']
        

    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully edited!')
  #except Exception as e:
        #print(e)
        #flash('An error occurred. Artist ' + request.form['name'] + ' could not be edited')
        #db.session.rollback()
  #finally:
    db.session.close()
    return redirect(url_for('show_artist',artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venues.query.filter(Venues.id == venue_id).first()
  #form.city.data= artist.city
  #form.id.data= artist.id,
  s=venue.name
  form.name.data= s.strip(),
  form.genres.data= [venue.genres],
  form.city.data= venue.city,
  form.state.data= venue.state,
  form.phone.data= venue.phone,
  form.website_link.data= venue.website,
  form.facebook_link.data= venue.facebook_link,
  form.seeking_talent.data= venue.seeking_talent,
  #form.seeking_description.data= bool(venue.seeking_description),
  form.image_link.data= venue.image_link,
  response = {
    "id": venue.id,
    "name": venue.name,
    #"genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    #"address": "1015 Folsom Street",
    #"city": "San Francisco",
    #"state": "CA",
    #"phone": "123-123-1234",
    #"website": "https://www.themusicalhop.com",
    #"facebook_link": "https://www.facebook.com/TheMusicalHop",
    #"seeking_talent": True,
    #"seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    #"image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60" 
    }



  
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=response)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])

def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
            venue=Venues.query.get(venue_id)
  #try:
      
            venue.name=request.form['name'],
            venue.city=request.form['city'],
            venue.state=request.form['state'],
            venue.address=request.form['address'],
            venue.phone=request.form['phone'],
            venue.genres=request.form.getlist('genres'),
            venue.image_link=request.form['image_link'],
            venue.facebook_link=request.form['facebook_link'],
            venue.website=request.form['website_link'],
            #venue.seeking_talent=bool(request.form['seeking_talent']),
            venue.seeking_description=request.form['seeking_description']
               
            db.session.commit()
            flash('Venue ' + request.form['name'] + ' was successfully edited!')
  #except Exception as e:
        #print(e)
        #flash('An error occurred. Venue ' + request.form['name'] + ' could not be edited')
        #db.session.rollback()
  #finally:
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

  # on successful db insert, flash success
  #flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  #return render_template('pages/home.html')
  #try:
        form=ArtistForm(request.form)
        artist = Artists(
            name=request.form['name'],
            city=request.form['city'],
            state=request.form['state'],
            phone=request.form['phone'],
            genres=request.form.getlist('genres'),
            image_link=request.form['image_link'],
            facebook_link=request.form['facebook_link'],
            Looking_for_Venues=form.seeking_venue.data,
            Website_link=request.form['website_link'],
            Seeking_Description=request.form['seeking_description']
        )
        db.session.add(artist)
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
  #except Exception as e:
        #print(e)
        #flash('An error occurred. Artist ' + request.form['name'] + ' could not be added')
        #db.session.rollback()
  #finally:
        db.session.close()
        return render_template('pages/home.html')

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data = Show.query.join(Artists, Artists.id == Show.artist_id).join(Venues, Venues.id == Show.venue_id).all()

  response = []
  for show in data:
        response.append({
            "venue_id": show.venue_id,
            "venue_name": show.Venue.name,
            "artist_id": show.artist_id,
            "artist_name": show.Artist.name,
            "artist_image_link": show.Artist.image_link,
            "start_time": str(show.start_time)
        })
  return render_template('pages/shows.html', shows=response)



@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  #flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  #return render_template('pages/home.html')

    try:
        show = Show(
            artist_id=request.form['artist_id'],
            venue_id=request.form['venue_id'],
            start_time=request.form['start_time']
        )
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully added!')
    except Exception as e:
        print(e)
        flash('An error occurred. Show could not be added')
        db.session.rollback()
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
