from flask import Flask, render_template
import datetime
from states import states
import requests
app = Flask(__name__)

@app.route('/')
def index():
	total = requests.get('https://covidtracking.com/api/us').json()[0]
	total_positive = str(format(total['positive'], ',d'))
	total_negative = str(format(total['negative'], ',d'))
	total_death = str(format(total['death'], ',d'))
	total_hospitalized = str(format(total['hospitalized'], ',d'))
	total_conclusive_tested = str(format(total['totalTestResults'], ',d'))
	# updated_time = str(datetime.datetime.strptime(total['lastModified'], "%Y-%m-%dT%H:%M:%S%z"))
	updated_time = total['lastModified']
	table_data = {'positives': total_positive, 'negatives': total_negative, 'tested': total_conclusive_tested, 'hospitalized': total_hospitalized, 'deaths': total_death, 'time': updated_time}
	return render_template('index.html', table_data = table_data, states = states)

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
	state_positive = str(format(state_info['positive'], ',d'))
	state_negative = str(format(state_info['negative'], ',d'))
	state_death = str(format(state_info['death'], ',d'))
	if not state_info['pending']:
		state_pending = 0
	else:
		state_pending = str(format(state_info['pending'], ',d'))
	if not state_info['hospitalized']:
		state_hospitalized = "Count not provided"
	else:
		state_hospitalized = str(format(state_info['hospitalized'], ',d'))
	state_conclusive_tested = str(format(state_info['totalTestResults'], ',d'))
	# updated_time = str(datetime.datetime.strptime(state_info['dateModified'], "%Y-%m-%dT%H:%M:%S%z"))
	updated_time = state_info['dateModified']
	table_data = {'state': states[state], 'positives': state_positive, 'negatives': state_negative, 'tested': state_conclusive_tested, 'hospitalized': state_hospitalized, 'deaths': state_death, 'time': updated_time, 'pending': state_pending}
	return render_template('states.html', table_data = table_data, states = states)
