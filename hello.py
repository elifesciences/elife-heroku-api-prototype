import sys
import os
from flask import Flask
import requests

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    print "in user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def hello():
    r = requests.get('http://httpbin.org/status/418')
    times = int(os.environ.get('TIMES',3))
    print r.text
    return r.text * times

@app.route('/putperson')
def putperson():
    print "hi"
    print "hi"
    user = User('John Doe', 'john.doe@example.com')
    print "user created"
    db.session.add(user)
    db.session.commit()
    return "user created"

@app.route('/showperson')
def showpeople():
    all_users = User.query.all()
    user_names = []
    for user in all_users:
        user_names.append(user.name)
    output = "\n".join(user_names)
    return output

if __name__ == '__main__':
    app.run()
