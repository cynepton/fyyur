#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form, FlaskForm
from forms import *
from flask_migrate import Migrate
import psycopg2
from app import app, db
from models import Venue, Artist, Shows

#  ----------------------------------------------------------------
#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.

  all_venues = Venue.query.group_by(Venue.id, Venue.city).all()
  data = []
  current_city = "null"

  # Looping over each venue in the database
  for venue in all_venues:
    if current_city == venue.city:
      data[len(data) - 1]["venues"].append({
        "id": venue.id,
        "name":venue.name,
        "num_upcoming_shows": 0 
      })
    else:
      data.append({
        "city":venue.city,
        "state":venue.state,
        "venues": [{
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows": 0
        }]
      })
      current_city = venue.city
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  venue_select = Venue.query
  venue_list = []

  venues = venue_select.filter(Venue.name.ilike('%' + request.form['search_term'] + '%'))

  for venue in venues:
    venue_list.append({
      "id":venue.id,
      "name":venue.name,
      "num_upcoming_shows": 0,
    })

  response={
    "count": len(venue_list),
    "data": venue_list
  }

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  
  venue_in_view = Venue.query.get(venue_id)
  data = {
    "id": venue_in_view.id,
    "name": venue_in_view.name,
    "genres": venue_in_view.genres,
    "address": venue_in_view.address,
    "city": venue_in_view.city,
    "state": venue_in_view.state,
    "phone": venue_in_view.phone,
    "website": venue_in_view.website,
    "facebook_link": venue_in_view.facebook_link,
    "seeking_talent": venue_in_view.seeking_talent,
    "image_link": venue_in_view.image_link
  }

  return render_template('pages/show_venue.html', venue=data)

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
  form = VenueForm(request.form)
  venue = Venue(
    name = form.name.data,
    genres = form.genres.data,
    address = form.address.data,
    city = form.city.data,
    state = form.state.data,
    phone = form.phone.data,
    facebook_link = form.facebook_link.data,
  )
  print(venue)
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  try:
    db.session.add(venue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + form.name.data + ' was successfully listed!')
  except Exception as e:
    print(e)
    flash('An error occurred. Venue ' + form.name.data + ' could not be added.')
  finally:
    db.session.close()
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    venue_to_delete = Venue.query.filter_by(id=venue_id)
    venue_to_delete.delete()
    db.session.commit()
  except:
    db.session.rollback() 
  finally:
    db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  all_artists = Artist.query.all()
  data = []

  # Looping over each venue in the database
  for artist in all_artists:
    data.append({
      "id":artist.id,
      "name":artist.name
    })

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  artist_select = Artist.query
  artist_list = []

  artists = artist_select.filter(Artist.name.ilike('%' + request.form['search_term'] + '%'))

  for artist in artists:
    artist_list.append({
      "id":artist.id,
      "name":artist.name,
      "num_upcoming_shows": 0,
    })

  response={
    "count": len(artist_list),
    "data": artist_list
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  artist_in_view = Artist.query.get(artist_id)
  data = {
    "id": artist_in_view.id,
    "name": artist_in_view.name,
    "genres": artist_in_view.genres,
    "city": artist_in_view.city,
    "state": artist_in_view.state,
    "phone": artist_in_view.phone,
    "seeking_venue": artist_in_view.seeking_venue,
    "image_link": artist_in_view.image_link,
    "facebook_link": artist_in_view.facebook_link
  }
  
  #data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  form = ArtistForm(request.form)
  artist = Artist(
    name = form.name.data,
    genres = form.genres.data,
    city = form.city.data,
    state = form.state.data,
    phone = form.phone.data,
    facebook_link = form.facebook_link.data
  )
  print(artist)
  # on successful db insert, flash success
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  try:
    db.session.add(artist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + form.name.data + ' was successfully listed!')
  except Exception as e:
    print(e)
    flash('An error occurred. Artist ' + form.name.data + ' could not be added.')
  finally:
    db.session.close()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  all_shows = Shows.query.join(Venue).join(Artist).all()

  for each_show in all_shows:
    data.append({
      "venue_id": each_show.venue_id,
      "venue_name": each_show.venue.name,
      "artist_id": each_show.artist_id,
      "artist_name": each_show.artist.name,
      "artist_image_link": each_show.artist.image_link,
      "start_time": each_show.start_time
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
  
  form = ShowForm(request.form)
  show = Shows(
    venue_id = form.venue_id.data,
    artist_id = form.artist_id.data,
    start_time = form.start_time.data
  )
  print(show)
  try:
    db.session.add(show)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')
  except Exception as e:
    print(e)
    flash('An error occurred. Show could not be added.')
  finally:
    db.session.close()
  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')
