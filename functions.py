from flask import Flask, render_template, flash, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SPACESPACESPACESPACESPACE'
bootstrap = Bootstrap5(app)

class SearchAction(FlaskForm):
	search_input = DateField('Search',validators=[DataRequired()])

class ImageSave(FlaskForm):
	1+1 #filler method because i dont know what to do here...

favorites_album = []

def favorite_picture(my_image):
	favorites_album.append('')

@app.route('/', methods=['POST', 'GET'])

@app.route('/')
def gallery():
	random_gallery = []

	form = SearchAction()
	if form.validate_on_submit():
		return redirect('search'+form.search_input.data)
	return render_template('galleryview.html', form=form, random_gallery=random_gallery)

@app.route('/favorites')
def favorites():
	form = SearchAction()
	if form.validate_on_submit():
		return redirect('search'+form.search_input.data)
	return render_template('favoritesview.html', form=form, favorites_album=favorites_album)

@app.route('/search/<search_input>')
def search(search_input):
	form = SearchAction()
	if form.validate_on_submit():
		return redirect('search'+form.search_input.data)
	return render_template('searchview.html', form=form, search_results=search_results)