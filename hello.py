import sys
import os
from flask import Flask
import requests
import logging, sys
logging.basicConfig(stream=sys.stderr)
import random

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(120))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<Name %r>' % self.name

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180))
    doi = db.Column(db.String(120))
    pub_date = db.Column(db.String(120))
    terms = db.relationship('Term', backref = 'article', lazy = 'dynamic')

    def __init__(self, title, doi, pub_date):
        self.title = title
        self.doi = doi
        self.pub_date = pub_date

    def __repr__(self):
        return '<Doi %r>' % self.doi

class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(120))
    term_type = db.Column(db.String(60))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    # def __init__(self, term, term_type):
    #     self.term = term
    #     self.term_type = term_type

    def __repr__(self):
        return '<Name %r>' % self.term

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

@app.route('/putarticle')
def putarticle():
    art = Article('This is the title', 'this is the DOI', "2014-08-10")
    print "user created"
    db.session.add(art)
    db.session.commit()
    a = Article.query.get(1)
    t = Term(term="name", term_type="type", article=a)
    db.session.add(t)
    db.session.commit()
    return "article created"

@app.route('/putterm')
def putterm():
    terms = ["gene", "hox", "peterson", "alpha"]
    this_term = random.choice(terms)
    term_types = ["organisim", "author keyword", "keyword"]
    this_term_type = random.choice(term_types)
    term = Term(this_term, this_term_type)
    db.session.add(term)
    db.session.commit()
    return "created term"

@app.route('/showarticles')
def showarticles():
    all_articles = Article.query.all()
    article_details = []
    for article in all_articles:
        out_string = article.title
        terms = article.terms
        term_string = ""
        for t in terms:
            term_string += " " + t.term
        out_string = out_string + " " + term_string
        article_details.append(out_string)
    output = "<br/>".join(article_details)
    return output


@app.route('/showperson')
def showpeople():
    all_users = User.query.all()
    user_names = []
    for user in all_users:
        user_names.append(user.name)
    output = "<br/>".join(user_names)
    return output

if __name__ == '__main__':
    app.run()
