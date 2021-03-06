from flask import Flask, render_template
import datetime
from states import states
import requests
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

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
	positives, deaths, date ,death_i, positive_i, hospitalized_cumu, hospitalized_current = [], [], [], [], [], [], []
	for day in cumulative:
		positives.append(day['positive'])
		if 'death' in day:
			deaths.append(day['death'])
		else:
			deaths.append(0)
		date.append(day['date'])
		if not day['deathIncrease']:
			death_i.append(0)
		else:
			death_i.append(day['deathIncrease'])
		if not day['positiveIncrease']:
			positive_i.append(0)
		else:
			positive_i.append(day['positiveIncrease'])
		if 'hospitalizedCumulative' not in day or not day['hospitalizedCumulative']:
			hospitalized_cumu.append(0)
		else:
			hospitalized_cumu.append(day['hospitalizedCumulative'])
		if 'hospitalizedCurrently' not in day or not day['hospitalizedCurrently']:
			hospitalized_current.append(0)
		else:
			hospitalized_current.append(day['hospitalizedCurrently'])
	positives = positives[::-1]
	deaths = deaths[::-1]
	date = date[::-1]
	positive_i = positive_i[::-1]
	death_i = death_i[::-1]
	hospitalized_cumu = hospitalized_cumu[::-1]
	hospitalized_current = hospitalized_current[::-1]
	f = open("static/data/usa_positives.csv", "w")
	f.write("date,Positives\n")
	for i in range(len(positives)):
		if positives[i] == 0:
			continue
		line = str(date[i]) + ',' + str(positives[i]) + '\n'
		f.write(line)
	f.close()
	f = open("static/data/usa_deaths.csv", "w")
	f.write("date,Deaths\n")
	for i in range(len(positives)):
		if deaths[i] == 0:
			continue
		line = str(date[i]) + ',' + str(deaths[i]) + '\n'
		f.write(line)
	f.close()
	f = open("static/data/usa_positives_i.csv", "w")
	f.write("date,Positives (per day)\n")
	i = 0
	while i < len(positive_i) and positive_i[i] == 0:
		i += 1
	while i < len(positive_i):
		line = str(date[i]) + ',' + str(positive_i[i]) + '\n'
		f.write(line)
		i += 1
	f.close()
	f = open("static/data/usa_deaths_i.csv", "w")
	f.write("date,Deaths (per day)\n")
	i = 0
	while i < len(death_i) and death_i[i] == 0:
		i += 1
	while i < len(death_i):
		line = str(date[i]) + ',' + str(death_i[i]) + '\n'
		f.write(line)
		i += 1
	f.close()
	f = open("static/data/usa_hospital_i.csv", "w")
	f.write("date,Hospitalized (current)\n")
	i = 0
	while i < len(hospitalized_current) and hospitalized_current[i] == 0:
		i += 1
	while i < len(hospitalized_current):
		line = str(date[i]) + ',' + str(hospitalized_current[i]) + '\n'
		f.write(line)
		i += 1
	f.close()
	f = open("static/data/usa_hospital_cumu.csv", "w")
	f.write("date,Hospitalized (cumulative)\n")
	for i in range(len(positives)):
		if hospitalized_cumu[i] == 0:
			continue
		line = str(date[i]) + ',' + str(hospitalized_cumu[i]) + '\n'
		f.write(line)
	f.close()
	increases = {'death': cumulative[0]['deathIncrease'], 'positive': cumulative[0]['positiveIncrease'], 'hosp': cumulative[0]['hospitalizedIncrease']}
	return render_template('index.html', table_data = table_data, states = states, increases = increases)

@app.route('/state/<state>')
def state(state=None):
	state_info = requests.get('https://covidtracking.com/api/states?state='+state).json()
	if 'error' in state_info:
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
	filtered = requests.get('https://covidtracking.com/api/v1/states/' + state + '/daily.json').json()
	positives, deaths, date, death_i, positive_i, hosp = [], [], [], [], [], []
	for day in filtered:
		positives.append(day['positive'])
		if not 'death' in day.keys():
			deaths.append(0)
		else:
			deaths.append(day['death'])
		date.append(day['date'])
		if not day['deathIncrease']:
			death_i.append(0)
		else:
			death_i.append(day['deathIncrease'])
		if not day['positiveIncrease']:
			positive_i.append(0)
		else:
			positive_i.append(day['positiveIncrease'])
		if 'hospitalizedCurrently' not in day or not day['hospitalizedCurrently']:
			hosp.append(0)
		else:
			hosp.append(day['hospitalizedCurrently'])
	positives.reverse()
	deaths.reverse()
	date.reverse()
	positive_i.reverse()
	death_i.reverse()
	hosp.reverse()
	f = open("static/data/states_positives.csv", "w")
	f.write("date,Positives\n")
	for i in range(len(positives)):
		if positives[i] == 0:
			continue
		line = str(date[i]) + ',' + str(positives[i]) + '\n'
		f.write(line)
	f.close()
	f = open("static/data/states_deaths.csv", "w")
	f.write("date,Deaths\n")
	for i in range(len(positives)):
		if deaths[i] == 0:
			continue
		line = str(date[i]) + ',' + str(deaths[i]) + '\n'
		f.write(line)
	f.close()
	f = open("static/data/states_positives_i.csv", "w")
	f.write("date,Positives (per day)\n")
	i = 0
	while i < len(positive_i) and positive_i[i] == 0:
		i += 1
	while i < len(positive_i):
		line = str(date[i]) + ',' + str(positive_i[i]) + '\n'
		f.write(line)
		i += 1
	f.close()
	f = open("static/data/states_deaths_i.csv", "w")
	f.write("date,Deaths (per day)\n")
	i = 0
	while i < len(death_i) and death_i[i] == 0:
		i += 1
	while i < len(death_i):
		line = str(date[i]) + ',' + str(death_i[i]) + '\n'
		f.write(line)
		i += 1
	f.close()
	f = open("static/data/states_hosp.csv", "w")
	f.write("date,Hospitalized\n")
	i = 0
	while i < len(hosp) and hosp[i] == 0:
		i += 1
	while i < len(hosp):
		line = str(date[i]) + ',' + str(hosp[i]) + '\n'
		f.write(line)
		i += 1
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
