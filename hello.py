import os
from flask import Flask
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    r = requests.get('http://httpbin.org/status/418')
    print r.text
    return r.text
