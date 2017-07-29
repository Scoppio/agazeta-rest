A Gazeta de Geringontzan
---
[![CircleCI](https://circleci.com/gh/Scoppio/agazeta-rest/tree/master.svg?style=svg)](https://circleci.com/gh/Scoppio/agazeta-rest/tree/master)

TODO: 
- Add django-rest-pandas to run time series with group-by-month/week/year
- Add invitation-like email and confirmation for users
- Add Apscheduler to run DoraR jobs or something else like it

## Define which environment will run using the settings

To run with a simple sqlite database simple run:  `python manage.py runserver --settings=settings.dev-simple`

For a more sturdy enviroment of development you could use:  `python manage.py runserver --settings=settings.dev-mysql`

## Using libraries
- http://www.django-rest-framework.org
- pandas-rest
