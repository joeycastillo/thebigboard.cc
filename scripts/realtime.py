import requests
import csv
import yaml
import codecs
import subprocess
import os
from git import Repo
from datetime import datetime
from contextlib import closing

last_update = datetime(1970, 1, 1)
confirmed = 0
recovered = 0
deaths = 0

with closing(requests.get('https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv', stream=True)) as r:
    reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8') , delimiter=',', quotechar='"')

    header_processed = False
    update_col = None
    confirmed_col = None
    recovered_col = None
    deaths_col = None
    
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
            header_processed = True
            continue
        confirmed += int(row[confirmed_col])
        recovered += int(row[recovered_col])
        deaths += int(row[deaths_col])
        row_update = datetime.strptime(row[update_col], '%Y-%m-%dT%H:%M:%S.000Z')
        if row_update > last_update:
            last_update = row_update

new_yaml = None

script_path = os.path.dirname(os.path.realpath(__file__))

with open(script_path + '/../_data/covid.yml', 'r') as f:
    s = f.read()
    dict = yaml.safe_load(s)
    if dict['updated'] != last_update:
        dict = {
            'confirmed' : confirmed,
            'recovered' : recovered,
            'deaths' : deaths,
            'updated' : last_update
        }
        new_yaml = yaml.dump(dict)

if new_yaml is not None:
    repo = Repo(script_path + "/..")
    repo.remote(name='origin').pull()
    with open(script_path + '/../_data/covid.yml', 'w') as f:
        f.write(new_yaml)
    repo.git.add('_data')
    repo.git.commit('-m', 'automatic data update', author='commit robot <noreply@thebigboard.cc>')
    repo.remote(name='origin').push()
