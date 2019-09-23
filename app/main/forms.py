from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField,ValidationError,RadioField
from wtforms.validators import Required,Email
from ..models import User,Pitch


class PitchForm(FlaskForm):
	title = StringField('Title', validators=[Required()])
	description = TextAreaField("Pitch Now :",validators=[Required()])
	category = RadioField('Label', choices=[ ('promotionpitch','promotionpitch'), ('interviewpitch','interviewpitch'),('pickuplines','pickuplines'),('productpitch','productpitch')],validators=[Required()])
	submit = SubmitField('Submit')
	
class CommentForm(FlaskForm):
	description = TextAreaField('Add comment',validators=[Required()])
	submit = SubmitField()

class UpvoteForm(FlaskForm):
	submit = SubmitField()


class Downvote(FlaskForm):
	submit = SubmitField()

# class ReviewForm(FlaskForm):

#  title = StringField('Review title',validators=[Required()])

#  review = TextAreaField('Pitch review')

#  submit = SubmitField('Submit')
 
class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')