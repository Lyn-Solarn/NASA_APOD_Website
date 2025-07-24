import os
from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import DateField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
import requests
# Loads variables in the .env
from dotenv import load_dotenv

# Note: Run app with 'flask --app app --debug run'

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SPACESPACESPACESPACESPACE'
bootstrap = Bootstrap5(app)

NASA_API_KEY = os.getenv("NASA_API_KEY")

def fetch_apod_images():
    """
    Creates a difference of NUM_Days - 1 (i.e. if NUM_DAYS=10 then it becomes timedelta(days=4)). It then subtracts that
    from the current day to get the starting date. Finally it formats the date into "20XX-XX-XX". That format is required for
    NASA's API parameters. The end date is the current day.

    After getting the ending and starting dates, it sets up the NASA's API request and calls it.
    """
    NUM_DAYS = 10
    today = datetime.today()
    start_date = (today - timedelta(days=NUM_DAYS - 1)).strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    url = "https://api.nasa.gov/planetary/apod"
    params = {
        "api_key": NASA_API_KEY,
        "start_date": start_date,
        "end_date": end_date
    }

    response = requests.get(url, params=params)

    # Checks to see if the API call was successful
    if response.status_code == 200:
        # Reverse to show newest first
        return response.json()[::-1]
    else:
        return []

class SearchAction(FlaskForm):
    search_input = DateField('Search',validators=[DataRequired()])

class ImageSave(FlaskForm):
    pass # filler method because I don't know what to do here...

favorites_album = []

def favorite_picture(my_image):
    favorites_album.append(my_image)
    
def remove_favorite_picture(my_image):
     my_image.remove(my_image)


@app.route('/', methods=['POST', 'GET'])
@app.route('/')
def gallery():
	images = fetch_apod_images()

	form = SearchAction()
	if form.validate_on_submit():
		return redirect('search'+form.search_input.data)
	return render_template('galleryview.html', form=form, images=images)

@app.route('/favorites')
def favorites():
	form = SearchAction()
	if form.validate_on_submit():
		return redirect('search'+form.search_input.data)
	return render_template('favoritesview.html', form=form, favorites_album=favorites_album)


if __name__ == "__main__":
    app.run(debug=True)