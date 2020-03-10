# jekyll-nil-theme

The simplest possible starting point for a Jekyll project.

WHAT IT HAS: Header and footer includes, navigation and copyright boilerplate, analytics, [HTML proofreading](https://github.com/gjtorikian/html-proofer), and configuration for automatic testing and deployment with [CircleCI](https://circleci.com).

WHAT IT DOESN'T HAVE: Even a slight opinion about what your site should look like. While it does apply some very minimal styling out of the box, the intent is for you to rip it all out and do your own thing. Ideally, you would not want to fork this project or even clone it. Download it as a ZIP, init a new repo and and start building your own theme. You won't need upstream changes, and they'd conflict with what you're doing anyway.

## Automatic deployment with CircleCI

To use the automatic deployment feature:

* Update line 41 of `.circleci/config.yml` with the connection details for your server.
* Set up the project in CircleCI. You will need to give it an SSH key for your server; this is covered succinctly [here](https://circleci.com/docs/2.0/add-ssh-key/).
* Any changes merged into `master` will be checked with HTMLProofer and then rsync'ed over to your production server.

Note that HTMLProofer will fail on images with missing or blank `alt` tags. I have left the test phase configured this way to encourage the development of accessible websites, but if you know what you are doing, you may choose to add the `--empty_alt_ignore` flag to the HTMLProofer test phase.
