from ast import pattern
from datetime import datetime
from email.policy import default
from html.entities import html5
from operator import length_hint
from pickle import FALSE
import re
from urllib.error import URLError
from urllib.parse import urlparse
from xml.dom import  VALIDATION_ERR,ValidationErr
from flask import flash
from flask_wtf import Form
import phonenumbers
from sqlalchemy import false, null
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, AnyOf, URL,Regexp,re,length,Optional
from phonenumbers import ValidationResult, timezone


def validate_website(form,field):
  url_regex = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
  regex = re.compile(url_regex)
  if not re.match(field,regex):
      raise ValidationErr('The correct format for the website link was not correct')
      
def validate_phone(form, phone):
        try:
            p = phonenumbers.parse(phone.data)
            if not phonenumbers.is_valid_number(p):
                raise ValueError()
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            raise ValidationErr('Invalid phone number')

       
class ShowForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )
#@app.route('/venues/create', methods=['POST'])
#def create_venue_submission():
 # error = False
 # form = VenueForm()
 # if form.validate_on_submit():
   # try:
   #   name = request.form['name']
  #    city = request.form['city']
  #   ...
   # except:
  #    error = True
   #   db.session.rollback()
  #  finally:
  #    db.session.close()
 # else:
  #  for error in form.errors:
   #   flash(error)
  #return render_template('forms/new_venue.html', form=form)
  #
   

class VenueForm(Form):
    genres_choices= [
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
        
    #def validate_phone(form, field):
        #if not re.search(r"^[0-9]{3}-[0-9]{3}-[0-9]{4}$", field.data):
            #raise ValidationErr("Invalid phone number.")


   # def validate_genres(form, field):
        
        #  genres_values = [choice[1] for choice in field]
        #  for value in field.data:
        #  if value not in genres_values:
        #  raise ValidationErr('Invalid genres value.')


    

    name = StringField('Name', [DataRequired()])
    def validate_name(form, field):
                if len(field.data)==3:
                 raise ValidationErr('Name must be less than 50 characters')
                 
    
    
    city = StringField(
        'city', validators=[DataRequired()]
    )
    
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=genres_choices
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone',validators=[DataRequired(),Regexp(r'^[0-9\-\+]+$',message='Invalid Phone Number')]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        #def coerce_for_enum(enum):
        #def coerce(name):
        #if isinstance(name, enum):
        #return name
        #try:
        #       return enum[name]
        #   except KeyError:
        #       raise ValueError(name)
        #return coerce
#Then add coerce parameter as below:

 
        'genres', validators=[DataRequired()],
          choices= genres_choices  )
    
    facebook_link = StringField(
        'facebook_link', validators=[Regexp('(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?', message="The correct format for the facebook link was not correct")])
    website_link = StringField(
        'website_link',validators=[URL('Invalid URL')]
    )

    seeking_talent = BooleanField( 'seeking_talent')

    seeking_description = StringField(
        'seeking_description'
    )



class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )

    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )

     
    phone = StringField(
        # TODO implement validation logic for state
        
        'phone', validators=[DataRequired(),validate_phone])
    
    image_link = StringField(
        'image_link'
    )

    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
     )
     
    facebook_link = StringField(
        # TODO implement enum restriction
       
        'facebook_link', validators=[Optional(),Regexp('(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?', message="The correct format for the facebook link was not correct")])
     
     
    website_link = StringField(
        'website_link',validators=[Optional(),URL('Invalid URL'),validate_website]
     )
    
    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
            'seeking_description'
     )

