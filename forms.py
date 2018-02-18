from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField
from wtforms.validators import DataRequired


### Form on web page to upload file with ip range ###
### Given also possibility to manually set ip range
class Start(FlaskForm):
	name = StringField('Person scanning the network:',validators=[DataRequired()])
	submit=SubmitField('Start')
