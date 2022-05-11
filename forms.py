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
from enums import Genre, State
from wtforms.fields import TelField
'''
def validate_website(form,field):
    url_regex = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*'
    regex1 = re.compile(url_regex)
    try:

     if not regex1.match(field.data):
        raise ValidationErr('The correct format for the website link was not correct')
    except :
            raise ValidationErr('Invalid phone numberzjgj ')
            flash('Invalid phone number')
    finally:
           return 
'''

def is_valid_phone(number):
    """ Validate phone numbers like:
    1234567890 - no space
    123.456.7890 - dot separator
    123-456-7890 - dash separator
    123 456 7890 - space separator
    Patterns:
    000 = [0-9]{3}
    0000 = [0-9]{4}
    -.  = ?[-. ]
    Note: (? = optional) - Learn more: https://regex101.com/
    """
    regex = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
    return regex.match(number)

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
class VenueForm(Form):
            
    name = StringField('Name', [DataRequired()])
    
    def validate_name(form, field):
        try:                                                                                                              
            if len(field.data)==3:
                 raise ValidationErr('Name has three characters')
        except :
            flash('Invalid phone number')
        finally:
           return 
        
    city = StringField(
        'city', validators=[DataRequired()]
    )
    
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
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
        choices=Genre.choices())
    
    facebook_link = StringField(
        'facebook_link', validators=[Regexp('(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?', message="The correct format for the facebook link was not correct")])
    website_link = StringField(
        'website_link',validators=[URL('Invalid URL')]
    )

    seeking_talent = BooleanField( 'seeking_talent')

    seeking_description = StringField(
        'seeking_description'
    )
    def validate(self):
        """Define a custom validate method in your Form:"""
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True


class ArtistForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )

    city = StringField(
        'city', validators=[DataRequired()]
    )

    state = SelectField(
        'state', validators=[DataRequired()],
        choices=State.choices()
    )

     
    phone = StringField(
        # TODO implement validation logic for state
        
        'phone', validators=[DataRequired(),])
    
    image_link = StringField(
        'image_link'
    )

    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=Genre.choices()
     )
     
    facebook_link = StringField(
        # TODO implement enum restriction
       
        'facebook_link', validators=[Optional(),Regexp('(?:(?:http|https):\/\/)?(?:www.)?facebook.com\/(?:(?:\w)*#!\/)?(?:pages\/)?(?:[?\w\-]*\/)?(?:profile.php\?id=(?=\d.*))?([\w\-]*)?', message="The correct format for the facebook link was not correct")])
     
     
    website_link = StringField(
        'website_link',validators=[Optional(),URL('Invalid URL')]
     )
    
    seeking_venue = BooleanField('seeking_venue')

    seeking_description = StringField(
            'seeking_description'
     )

    def validate(self):
        """Define a custom validate method in your Form:"""
        rv = Form.validate(self)
        if not rv:
            return False
        if not is_valid_phone(self.phone.data):
            self.phone.errors.append('Invalid phone.')
            return False
        if not set(self.genres.data).issubset(dict(Genre.choices()).keys()):
            self.genres.errors.append('Invalid genres.')
            return False
        if self.state.data not in dict(State.choices()).keys():
            self.state.errors.append('Invalid state.')
            return False
        # if pass validation
        return True