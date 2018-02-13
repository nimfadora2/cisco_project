from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import Required


### Form on web page to upload file with ip range ###
### Given also possibility to manually set ip range
class Start(FlaskForm):
	submit=SubmitField('Start')
