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
	total_hospitalized = str(format(total['hospitalizedCurrently'], ',d'))
	total_conclusive_tested = str(format(total['totalTestResults'], ',d'))
	# updated_time = str(datetime.datetime.strptime(total['lastModified'], "%Y-%m-%dT%H:%M:%S%z"))
	updated_time = total['lastModified']
	table_data = {'positives': total_positive, 'negatives': total_negative, 'tested': total_conclusive_tested, 'hospitalized': total_hospitalized, 'deaths': total_death, 'time': updated_time}
	cumulative = requests.get("https://covidtracking.com/api/us/daily").json()
	positives, deaths, date = [], [], []
	for day in cumulative:
		positives.append(day['positive'])
		deaths.append(day['death'])
		date.append(day['date'])
	positives = positives[::-1]
	deaths = deaths[::-1]
	date = date[::-1]
	f = open("static/data/usa.csv", "w")
	f.write("date,Positives,Deaths\n")
	for i in range(len(positives)):
		line = str(date[i]) + ',' + str(positives[i]) + ',' + str(deaths[i]) + '\n'
		f.write(line)
	f.close()
	increases = {'death': cumulative[0]['deathIncrease'], 'positive': cumulative[0]['positiveIncrease'], 'hosp': cumulative[0]['hospitalizedIncrease']}
	return render_template('index.html', table_data = table_data, states = states, increases = increases)

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
	if not state_info['hospitalizedCurrently']:
		state_hospitalized = "Count not provided"
	else:
		state_hospitalized = str(format(state_info['hospitalizedCurrently'], ',d'))
	state_conclusive_tested = str(format(state_info['totalTestResults'], ',d'))
	# updated_time = str(datetime.datetime.strptime(state_info['dateModified'], "%Y-%m-%dT%H:%M:%S%z"))
	updated_time = state_info['dateModified']
	table_data = {'state': states[state], 'positives': state_positive, 'negatives': state_negative, 'tested': state_conclusive_tested, 'hospitalized': state_hospitalized, 'deaths': state_death, 'time': updated_time, 'pending': state_pending}
	cumulative = requests.get('https://covidtracking.com/api/v1/states/daily.json').json()
	filtered = []
	for i in cumulative:
		if i['state'].lower() == state.lower():
			filtered.append(i)
	positives, deaths, date = [], [], []
	for day in filtered:
		positives.append(day['positive'])
		if not 'death' in day.keys():
			deaths.append(0)
		else:
			deaths.append(day['death'])
		date.append(day['date'])
	positives = positives[::-1]
	deaths = deaths[::-1]
	date = date[::-1]
	f = open("static/data/states.csv", "w")
	f.write("date,Positives,Deaths\n")
	for i in range(len(positives)):
		line = str(date[i]) + ',' + str(positives[i]) + ',' + str(deaths[i]) + '\n'
		f.write(line)
	f.close()
	increases = {'death': filtered[0]['deathIncrease'], 'positive': filtered[0]['positiveIncrease'], 'hosp': filtered[0]['hospitalizedIncrease']}
	return render_template('states.html', table_data = table_data, states = states, increases = increases)

@app.route('/world')
def world(state=None):
	all_countries = requests.get('https://coronavirus-19-api.herokuapp.com/countries').json()
	name, positives, positives_today, deaths, deaths_today, recovered = [], [], [], [], [], []
	for country in all_countries:
		name.append(country['country'])
		positives.append(country['cases'])
		positives_today.append(country['todayCases'])
		deaths.append(country['deaths'])
		deaths_today.append(country['todayDeaths'])
		recovered.append(country['recovered'])
	table_data = {'country': name, 'positives': positives, 'up_positives': positives_today, 'deaths': deaths, 'up_deaths': deaths_today, 'recovered': recovered}
	return render_template('world.html', table_data = table_data, states = states)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html', states = states), 404
