# The Big Coronavirus Board

This is a Jekyll-powered website aimed at sharing data about the 2019–2020 coronavirus pandemic. When I started it, it compared the number of coronavirus deaths to other causes of death worldwide, in the hopes of getting people to take the virus seriously (because it seemed like a lot of people weren't). A week later, it seems like everyone is taking it seriously. Moreover, as I've watched the death toll climb and read stories about the human toll of the pandemic, I could not in good conscience continue with the original concept.

So now it merely shows the number of cases, the number of recovered patients and the number of deaths. These numbers alone show that the novel coronavirus is a very dangerous pathogen, and that we all have to do our part to keep it at bay.

The more useful portion of the site is the set of data feeds that it exposes. In addition to the landing page, there are a series of JSON feeds with:

* [Global summary data](http://www.thebigboard.cc/feeds/v1/global.json)
* [Country-level data](http://www.thebigboard.cc/feeds/v1/countries.json)
* State and territory level data for [Australia](http://www.thebigboard.cc/feeds/v1/australia.json)
* Province-level data for [Canada](http://www.thebigboard.cc/feeds/v1/canada.json)
* Province-level data for [China](http://www.thebigboard.cc/feeds/v1/china.json)
* State-level data for [The United States](http://www.thebigboard.cc/feeds/v1/us.json)

These static files are generated at the same time that the cron job triggers a broader site update. If you would like state or province level breakdowns for other countries, check to see if that data is available in [the source data](https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv) and [open an issue](https://github.com/joeycastillo/thebigboard.cc/issues).

## Architecture and Methodology

A cron job runs [the update.py script](https://github.com/joeycastillo/thebigboard.cc/blob/master/scripts/update.py) every half hour, which pulls [data](https://opendata.arcgis.com/datasets/bbb2e4f589ba40d692fab712ae37b9ac_1.csv) from the Johns Hopkins real-time dashboard and places it in [a YAML file](https://github.com/joeycastillo/thebigboard.cc/blob/master/_data/covid.yml). It then pushes the update to GitHub, which triggers a CircleCI build that generates the static files and deploys them via rsync.

## License

Feel free to use any of the designs, code or data as you see fit; [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) seems appropriate.
