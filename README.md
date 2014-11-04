# About

This is a demo flask app, with a postgres db, to create a lightwight JSON api for eLife content. It can run locally, or be pushed to heroku. 

## Quickstart - local

This assumes that you have a local postgres db running.

	$ git clone git@github.com:elifesciences/elife-heroku-api-prototype.git
	$ cd elife-heroku-api-prototype
	$ pip install virtualenvwrapper
	$ mkvirtualenv env1
	$ pip install -r requirements.txt
	$ python redo_db.py
	$ set -x DATABASE_URL postgresql://localhost/ian
	$ set -x XML_PATH /Users/ian/Dropbox/code/public-code/elife-articles/
	$ set -x LOCAL_BASE_URL http://127.0.0.1:5000/
	$ python load_db.py -l l
	$ python run.py
	$ open http://127.0.0.1:5000/articles

## Quickstart - heroku

This assumes that you have added a postgres db to your heroku
account using the free tier availalbe in the addons area
of heroku.

	$ git clone git@github.com:elifesciences/elife-heroku-api-prototype.git
	$ cd elife-heroku-api-prototype
	$ pip install virtualenvwrapper
	$ mkvirtualenv env1
	$ pip install -r requirements.txt
	$ heroku login
	$ heroku create
	$ git push heroku master
	$ heroku run python redo_db.py
	$ set -x XML_PATH /Users/ian/Dropbox/code/public-code/elife-articles/
	$ set -x HEROKU_BASE_URL $WEB_URL
	$ python load_db.py -l h
	$ heroku ps:scale web=1
	$ heroku open

## Quickstart - update your heroku app

Assuming you enviornemnt is already setup

	$ git push heroku master

## Quickstart - nuke your heroku db, and repopulate

	$ heroku run python redo_db.py
	$ python load_db.py -l h

# Setup and run locally

### get the code
	$ git clone git@github.com:elifesciences/elife-heroku-api-prototype.git
	$ cd elife-heroku-api-prototype

### create a new virtual enviornment
###### using virutalenvwrapper
	$ pip install virtualenvwrapper
	$ mkvirtualenv env1

###### using virtualfish
get `virtualfish` from https://github.com/adambrenecki/virtualfish  

	$ vf new env1


##### install postgres
On a mac I used http://postgresapp.com

#### making your path aware of the Postgres binaries

For flask to talk to Postgres you need to install a postgres-python adaptor,
and we will use [psycopg](http://initd.org/psycopg/), but to install correctly using
pip you need to let you system know about the location of the postgres binary files.
When using Postgres.app on a mac with fish shell you do this with something like

	$ set -gx PATH /Applications/Postgres.app/Contents/Versions/9.3/bin/ $PATH

You can then go ahead and

### install the dependencies
	$ pip install -r requirements.txt


## Setup and populate the db

### setup the DB locallay

#### export the path to the postgres DB

Postgressapp will create a default db for you with you username.
You need to set the path to the DB as an environemnt variable for
the flask setup to work, for example the command I run is:

	$ set -x DATABASE_URL postgresql://localhost/ian

#### create the databases locally

We have to create the tables and models in postgres before
we can do anything else, I've provided a small utility script
that can do this for you

	$ python redo_db.py

#### fill the local db with test data

`load_db.py` uses `parseNLM.py` to extract nodes from our article XML, and pushes them against the PUT method of the API to populate the postgres DB.

It needs to know the location of a directory that contains a set of article XML files that it will scrape. This directory will be on local disk and the script will look for the location of the direcotry in the environemt variable `XML_PATH`, I use the following command to set this

	$ set -x XML_PATH /Users/ian/Dropbox/code/public-code/elife-articles/

You also need to set an enviornemnt variable that indicates the location of the local API base endpoint. I use the following

	$ set -x LOCAL_BASE_URL http://127.0.0.1:5000/

With these set, you can use `load_db.py` to insert a set of data into the DB via

	$ python load_db.py -l l

# Setup and run on heroku

There is a good [tutorial](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) on using
heroku and flask, the deployment of the app broadly follows that tutorial.

## Deploy the app, and setup the remote DB

Assuming that you have created a heroku account, and installed the heroku toolbelt, the steps to deploying this app are:

	$ heroku login
	$ heroku create
	$ git push heroku master

You can configure a postgres database through the heroku addons, and this will set a DB url avaialbe at `$DATABASE_URL` on the heroku system.

You now need to setup the db, and you can do this with

	$ heroku run python redo_db.py


#### fill the heroku db with test data

As above you will have set the path to the location of the local
XML files. You now need to set the location of the heroku
API endpoint. You can find your app URL using the following command

	$ heroku apps:info

Use this to set the location of the web url for the api.

	$ set -x HEROKU_BASE_URL $WEB_URL

With these set, you can use `load_db.py` to insert a set of data into the DB via

	$ python load_db.py -l h

#### Running the app

Run the app

	$ heroku ps:scale web=1

This will use the information in the `Procfile` to run the app on heroku with one dynamo. You can now open you app with

	$ heroku open
