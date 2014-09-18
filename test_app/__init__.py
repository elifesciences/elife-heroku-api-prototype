import sys
import os
import sys
import os
from flask import Flask
import requests
import logging, sys
import random
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config') # gets config info from config.py
db = SQLAlchemy(app)

import test_app.models
import test_app.views

if __name__ == '__main__':
	app.run()
