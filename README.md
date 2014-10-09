# Setup

This is a flask app, with a postgres db, to create a lightwight JSON api
for eLife content.

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

###### install dependencies
	$ pip install -r requirements.txt

### Setup and populate the db locally

##### install postgres
On a mac I used http://postgresapp.com

#### export the path to the postgres DB using fish shell
Postgressapp will create a default db for you with you username.
You need to set the path to the DB as an environemnt variable for
the flask setup to work

	$ set -x DATABASE_URL postgresql://localhost/ian

##### create the databases locally
We have to create the tables and models in postgres before
we can do anything else, I've provided a small utility script
that can do this for you

	$ python redo_db.py

##### fill the local db with test data
At the moment the `load_db.py` script only loads the heroku api endpoint, but I'll modify this to load against a named endpoint.

# Setup and run on heroku

There is a good [tutorial](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) on using
heroku and flask, the deployment of the app broadly follows that tutorial.
