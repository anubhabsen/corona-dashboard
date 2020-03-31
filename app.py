from flask import Flask
import datetime
from states import states
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
	# updated_time = str(datetime.datetime.strptime(total['lastModified'], "%Y-%m-%dT%H:%M:%S%z"))
	updated_time = total['lastModified']
	# updated_time = updated_time[:-6] + ' UTC'
	return 'Positives: ' + total_positive + '<br>' + 'Negatives: ' + total_negative + '<br>' + 'Hospitalized: ' + total_hospitalized + '<br>' + 'Tested (with results): ' + total_conclusive_tested + '<br>' + 'Deaths: ' + total_death + '<br>' + 'Last updated time: ' + updated_time

@app.route('/state/<state>')
def state(state=None):
	total = requests.get('https://covidtracking.com/api/states').json()
	state_info = {}
	for i in total:
		if i['state'].lower() == state.lower():
			state_info = i
			break
	if state_info == {}:
		return 'Enter valid 2 alphabet state abbreviation'
	state_positive = str(state_info['positive'])
	state_negative = str(state_info['negative'])
	state_death = str(state_info['death'])
	state_pending = str(state_info['pending'])
	state_hospitalized = str(state_info['hospitalized'])
	state_conclusive_tested = str(state_info['totalTestResults'])
	# updated_time = str(datetime.datetime.strptime(state_info['dateModified'], "%Y-%m-%dT%H:%M:%S%z"))
	updated_time = state_info['dateModified']
	# updated_time = updated_time[:-6] + ' UTC'
	return '<h1>' + states[state.upper()] + '</h1><br>Positives: ' + state_positive + '<br>' + 'Negatives: ' + state_negative + '<br>' + 'Pending: ' + state_pending + '<br>' + 'Hospitalized: ' + state_hospitalized + '<br>' + 'Tested (with results): ' + state_conclusive_tested + '<br>' + 'Deaths: ' + state_death + '<br>' + 'Last updated time: ' + updated_time
