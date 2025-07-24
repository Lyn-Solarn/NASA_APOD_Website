import os
from flask import Flask, render_template
import requests
from datetime import datetime, timedelta
# Loads variables in the .env
from dotenv import load_dotenv

# Note: Run app with 'flask --app app --debug run'

load_dotenv()

app = Flask(__name__)

NASA_API_KEY = os.getenv("NASA_API_KEY")
# The number of days that the API will fetch
NUM_DAYS = 10

def fetch_apod_images():
    """
    Creates a difference of NUM_Days - 1 (i.e. if NUM_DAYS=10 then it becomes timedelta(days=4)). It then subtracts that
    from the current day to get the starting date. Finally it formats the date into "20XX-XX-XX". That format is required for
    NASA's API parameters. The end date is the current day.

    After getting the ending and starting dates, it sets up the NASA's API request and calls it.
    """
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

@app.route("/")
def index():
    images = fetch_apod_images()
    return render_template("index.html", images=images)

if __name__ == "__main__":
    app.run(debug=True)