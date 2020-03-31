from flask import Flask
import requests
app = Flask(__name__)

@app.route('/')
def index():
	total = requests.get('https://covidtracking.com/api/us').json()[0]
	total_positive = str(total['positive'])
	total_negative = str(total['negative'])
	total_death = str(total['death'])
	total_hospitalized = str(total['hospitalized'])
	total_conclusive_tested = str(total['totalTestResults'])
	updated_time = str(total['lastModified'])
	return 'Positives: ' + total_positive + '<br>' + 'Negatives: ' + total_negative + '<br>' + 'Hospitalized: ' + total_hospitalized + '<br>' + 'Tested (with results): ' + total_conclusive_tested + '<br>' + 'Deaths: ' + total_death + '<br>' + 'Last updated time: ' + updated_time