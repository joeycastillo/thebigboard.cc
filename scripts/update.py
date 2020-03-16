import requests
import csv
import yaml
import codecs
from datetime import datetime
from contextlib import closing

def get_total(url):
    with closing(requests.get(url, stream=True)) as r:
        reader = csv.reader(codecs.iterdecode(r.iter_lines(), 'utf-8') , delimiter=',', quotechar='"')
        total = 0
        date = None
        for row in reader:
            if date is None:
                date = row[-1]
            else:
                total += int(row[-1])
    
        return (date, total)
        
(d1, cases) = get_total('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
(d2, deaths) = get_total('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
(d3, recovered) = get_total('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')

assert(d1 == d2 == d3)
date = datetime.strptime(d1 + ' 23:59:59', '%m/%d/%y %H:%M:%S')

new_yaml = None

with open('../_data/covid.yml') as f:
    s = f.read()
    dict = yaml.safe_load(s)
    if dict['updated'] != date:
        dict = {
            'cases' : cases,
            'deaths' : deaths,
            'recovered' : recovered,
            'updated' : date
        }
        new_yaml = yaml.dump(dict)

if new_yaml is not None:
    with open('../_data/covid.yml', 'w') as f:
        f.write(new_yaml)