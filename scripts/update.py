import requests
import csv
import yaml
import codecs
import subprocess
import os
from git import Repo
from datetime import datetime
from contextlib import closing

source_url = 'https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv'
countries_to_break_down = ['Australia', 'Canada', 'China', 'US']

last_update = datetime(1970, 1, 1)
confirmed = 0
recovered = 0
deaths = 0
countries = dict()
breakdowns = dict()

for country in countries_to_break_down:
    breakdowns[country] = list()

script_path = os.path.dirname(os.path.realpath(__file__))
repo = Repo(script_path + '/..')
repo.remote(name='origin').pull()

with closing(requests.get(source_url, stream=True)) as r:
    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8') , delimiter=',', quotechar='"')

    header_processed = False
    update_col = None
    confirmed_col = None
    recovered_col = None
    deaths_col = None
    country_col = None
    state_col = None
    
    for row in reader:
        if not header_processed:
            for i in range(0, len(row)):
                if row[i].lower() == 'last_update':
                    update_col = i
                elif row[i].lower() == 'confirmed':
                    confirmed_col = i
                elif row[i].lower() == 'recovered':
                    recovered_col = i
                elif row[i].lower() == 'deaths':
                    deaths_col = i
                elif row[i].lower() == 'country_region':
                    country_col = i
                elif row[i].lower() == 'province_state':
                    state_col = i
            header_processed = True
            continue
        confirmed += int(row[confirmed_col])
        recovered += int(row[recovered_col])
        deaths += int(row[deaths_col])
        if not len(row[update_col]):
            continue
        row_update = datetime.strptime(row[update_col], '%Y-%m-%dT%H:%M:%S.000Z')
        if row_update > last_update:
            last_update = row_update

        country = row[country_col]
        if not country in countries:
            countries[country] = dict()
            countries[country]['name'] = country
            countries[country]['confirmed'] = 0
            countries[country]['recovered'] = 0
            countries[country]['deaths'] = 0
        countries[country]['confirmed'] += int(row[confirmed_col])
        countries[country]['recovered'] += int(row[recovered_col])
        countries[country]['deaths'] += int(row[deaths_col])

        state = row[state_col]
        if country in countries_to_break_down and state is not None:
            breakdown = dict()
            breakdown['name'] = state
            breakdown['confirmed'] = int(row[confirmed_col])
            breakdown['recovered'] = int(row[recovered_col])
            breakdown['deaths'] = int(row[deaths_col])
            breakdowns[country].append(breakdown)

for country in countries_to_break_down:
    breakdowns[country] = sorted(breakdowns[country], key=lambda k: k['name'])

countries_list = list()
for country in countries:
    countries_list.append(countries[country])
countries_list = sorted(countries_list, key=lambda k: k['name'])

new_yaml = None

with open(script_path + '/../_data/covid.yml', 'r') as f:
    s = f.read()
    dict = yaml.safe_load(s)
    if dict['updated'] != last_update:
        dict = {
            'confirmed' : confirmed,
            'recovered' : recovered,
            'deaths' : deaths,
            'countries': countries_list,
            'breakdowns': breakdowns,
            'updated' : last_update,
            'source' : source_url
        }
        new_yaml = yaml.dump(dict, default_flow_style=False, sort_keys=False)

if new_yaml is not None:
    # write data file for website
    with open(script_path + '/../_data/covid.yml', 'w') as f:
        f.write(new_yaml)
    # write global history
    with open(script_path + '/../_data/history.csv', 'a') as f:
        f.write(str(last_update) + ',' + str(confirmed) + ',' + str(recovered) + ',' + str(deaths) + '\n')
    # write country-level history
    for country in countries:
        filename = country.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('*', '').replace(',', '') + '.csv'
        with open(script_path + '/../_data/details/' + filename, 'a') as f:
            if os.stat(script_path + '/../_data/details/' + filename).st_size == 0:
                f.write('timestamp,confirmed,recovered,deaths\n')
            f.write(str(last_update) + ',' + str(countries[country]['confirmed']) + ',' + str(countries[country]['recovered']) + ',' + str(countries[country]['deaths']) + '\n')
    # write state and province level history
    for country in breakdowns:
        folder_name = country.lower().replace(' ', '-').replace('(', '').replace(')', '').replace('*', '').replace(',', '')
        state_list = breakdowns[country]
        for state_data in state_list:
            filename = state_data['name'].lower().replace(' ', '-').replace('(', '').replace(')', '').replace('*', '').replace(',', '') + '.csv'
            with open(script_path + '/../_data/details/' + folder_name + '/' + filename, 'a') as f:
                if os.stat(script_path + '/../_data/details/' + folder_name + '/' + filename).st_size == 0:
                    f.write('timestamp,confirmed,recovered,deaths\n')
                f.write(str(last_update) + ',' + str(state_data['confirmed']) + ',' + str(state_data['recovered']) + ',' + str(state_data['deaths']) + '\n')
    repo.git.add('_data')
    repo.git.commit('-m', 'automatic data update', author='commit robot <noreply@thebigboard.cc>')
    repo.remote(name='origin').push()
