# The Big Coronavirus Board

This is a Jekyll-powered website aimed at displaying Coronavirus deaths in context, as compared to other causes of death worldwide.

## Architecture and Methodology

A cron job runs [the update.py script](https://github.com/joeycastillo/thebigboard.cc/blob/master/scripts/update.py) every half hour, which pulls [data](https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv) from the Johns Hopkins real-time dashboard and places it in [a YAML file](https://github.com/joeycastillo/thebigboard.cc/blob/master/_data/covid.yml). It then pushes the update to GitHub, which triggers a CircleCI build that generates the static files and deploys them via rsync.

The site uses the JHU data to generate its COVID stats. Data about other causes of death comes from the [Global Burden of Disease Study](http://ghdx.healthdata.org/gbd-2017); it's the data from 2017, the most recent year the study covered, and it prorates those annual deaths to the date of the last data update (naïvely assuming that all other causes of death grow linearly over the course of the year). 

## Other Feeds

In addition to the landing page, I realized that downloading and processing these statistics puts me in a position to offer useful, structured data about the pandemic. As such, I have also added a series of JSON feeds with [global summary data](http://www.thebigboard.cc/feeds/v1/global.json), [country-level data](http://www.thebigboard.cc/feeds/v1/countries.json), and state/province level data for [Australia](http://www.thebigboard.cc/feeds/v1/australia.json), [Canada](http://www.thebigboard.cc/feeds/v1/canada.json), [China](http://www.thebigboard.cc/feeds/v1/china.json) and the [United States](http://www.thebigboard.cc/feeds/v1/us.json) (the countries with detailed state and province level reporting). These static files are generated at the same time that the cron job triggers a broader site update. 

## License

Feel free to use any of the designs, code or data as you see fit; [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) seems appropriate.