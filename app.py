import os
from flask import Flask, render_template, redirect, flash, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import DateField, HiddenField, RadioField
from wtforms.validators import DataRequired
from datetime import datetime, timedelta
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SPACESPACESPACESPACESPACE'
bootstrap = Bootstrap5(app)

NASA_API_KEY = os.getenv("NASA_API_KEY")

# --- Forms ---
class SearchAction(FlaskForm):
    search_input = DateField('Search', validators=[DataRequired()])

class ImageSave(FlaskForm):
    image_title = HiddenField()
    date_of_image = HiddenField()
    decision = RadioField('Add to Favorites?',
                          choices=[('yes', 'Yes'), ('no', 'No')],
                          validators=[DataRequired()])

# --- Favorites Store ---
favorites_album = []

# --- Helpers ---
def fetch_apod_images():
    """
    Creates a difference of NUM_Days - 1 (i.e. if NUM_DAYS=10 then it becomes timedelta(days=4)). It then subtracts that
    from the current day to get the starting date. Finally it formats the date into "20XX-XX-XX". That format is required for
    NASA's API parameters. The end date is the current day.

    After getting the ending and starting dates, it sets up the NASA's API request and calls it.
    """
    NUM_DAYS = 25
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
    if response.status_code == 200:
        return response.json()[::-1]  # newest first
    return []

def fetch_apod_by_date(date):
    endpoint = 'https://api.nasa.gov/planetary/apod'
    payload = {
        'api_key': NASA_API_KEY,
        'date': date
    }
    r = requests.get(endpoint, params=payload)
    return r.json()

# --- Routes ---
@app.route('/', methods=['GET', 'POST'])
def gallery():
    form = SearchAction()
    error = None
    images = fetch_apod_images()

    if form.validate_on_submit():
        return redirect(f'/search/{form.search_input.data}')

    return render_template('galleryview.html', form=form, images=images, error=error)

@app.route('/search/<date>', methods=['GET', 'POST'])
def search(date):
    form = ImageSave()
    data = fetch_apod_by_date(date)

    if data.get('media_type') != 'image':
        flash("That date doesn't contain an image. Try another.")
        return redirect('/')

    if form.validate_on_submit():
        if form.decision.data == 'yes':
            image_date = form.date_of_image.data
            image_title = form.image_title.data
            if image_date not in [item[0] for item in favorites_album]:
                favorites_album.append([image_date, image_title])
        return redirect('/favorites')

    # Pre-fill form fields
    form.date_of_image.data = data.get('date')
    form.image_title.data = data.get('title')

    return render_template('searchview.html', data=data, form=form)

@app.route('/favorites', methods=['GET', 'POST'])
def favorites():
    if request.method == 'POST':
        image_title = request.form.get('image_title')
        image_date = request.form.get('date_of_image')
        decision = request.form.get('decision')

        if decision == 'yes' and image_date:
            if image_date not in [item[0] for item in favorites_album]:
                favorites_album.append([image_date, image_title])
        return redirect('/')

    # GET: Show current favorites
    images = []
    for date, _ in favorites_album:
        data = fetch_apod_by_date(date)
        if data.get('media_type') == 'image':
            images.append(data)
    return render_template('favoritesview.html', images=images)

# --- Run ---
if __name__ == "__main__":
    app.run(debug=True)