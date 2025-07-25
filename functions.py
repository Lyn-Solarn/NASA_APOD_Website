from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField, HiddenField, RadioField
from wtforms.validators import DataRequired
from datetime import datetime
import requests, json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SPACESPACESPACESPACESPACE'
bootstrap = Bootstrap5(app)
my_key = 'DX3uWsjt0CtEQDSScmJutQhzQcdivrQU4dddT0C3'


class SearchAction(FlaskForm):
	search_input = DateField('Search',validators=[DataRequired()])

class ImageSave(FlaskForm):
	image_title = HiddenField()
	date_of_image = HiddenField()
	decision = RadioField('',
				choices=[('yes', 'Yes'), ('no', 'No')],
				validators=[DataRequired()]
	)

favorites_album = []



@app.route('/', methods=('POST', 'GET'))
def gallery():
	form = SearchAction()
	error= None
	if form.validate_on_submit():
		endpoint = 'https://api.nasa.gov/planetary/apod'
		payload = {
                'api_key': my_key,
                'date': form.search_input.data
            }
		r = requests.get(endpoint, params=payload)
		data = r.json()
		if data['media_type'] == 'image':
			return render_template('searchview.html', data=data, form=ImageSave())
		elif data['media_type'] == 'video':
			error = 'Did not retrieve an image try another date'
	return render_template('galleryview.html', form=form, error=error)

@app.route('/favorites', methods=('POST', 'GET'))
def favorites():
	form = ImageSave()
	if form.validate_on_submit():
		if form.decision.data == 'yes':
			image_date = form.date_of_image.data
			image_title = form.image_title.data
			if image_date not in [item[0] for item in favorites_album]:
				favorites_album.append([image_date,image_title])
		return redirect('/gallery')
	return redirect('/')

@app.route('/gallery')
def your_favorites():
	images = []
	for date, title in favorites_album:
		endpoint = 'https://api.nasa.gov/planetary/apod'
		payload = {
                'api_key': my_key,
                'date': date
            }
		r = requests.get(endpoint, params=payload)
		data = r.json()
		images.append(data)
	return render_template('favoritesview.html', images=images)