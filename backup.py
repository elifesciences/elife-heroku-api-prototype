import sys
import os
from flask import Flask
import requests
import random

from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    doi = db.Column(db.String(120))
    pub_date = db.Column(db.String(120))
    # terms = db.relationship('Term', backref = 'article', lazy = 'dynamic')
    # authors = db.relationship('Author', backref = 'article', lazy = 'dynamic')

    def __init__(self, title, doi, pub_date):
        self.title = title
        self.doi = doi
        self.pub_date = pub_date

    def __repr__(self):
        return '<Name %r>' % self.doi


class Term(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    term = db.Column(db.String(120))
    term_type = db.Column(db.String(60))
    # article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, term, term_type):
        self.term = term
        self.term_type = term_type

    def __repr__(self):
        return '<Name %r>' % self.term


class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # article_id = db.Column(db.Integer, db.ForeignKey('article.id'))

    def __init__(self, name, email):
        self.name = name

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def hello():
    r = requests.get('http://httpbin.org/status/418')
    times = int(os.environ.get('TIMES',3))
    print r.text
    return r.text * times

@app.route('/putauthor')
def putauthor():
    initial = ["a", "b", "c", "d"]
    this_inital = random.choice(inital)
    name = this_inital + " dodds"
    author = Article(name)
    db.session.add(author)
    db.session.add(commit)
    return "created author"

@app.route('/putterm')
def putterm():
    terms = ["gene", "hox", "peterson", "alpha"]
    this_term = random.choice(terms)
    term_types = ["organisim", "author keyword", "keyword"]
    this_term_type = random.choice(term_types)
    term = Term(this_term, this_term_type)
    db.session.add(term)
    db.session.add(commit)
    return "created term"

@app.route('/putarticle')
def putarticle():
    doi = "dx.doi.90898"
    article = Article('This is the title', doi, "2014-09-16")
    "print created article"
    db.session.add(article)
    db.session.add(commit)
    # "comitted article"
    # created_article = Article.query.filter_by(doi=doi).first()
    # term = Term("mouse", "organsism", article=created_article)
    # db.session.add(term)
    # db.session.commit()
    return "created article with associated term"

@app.route('/showarticle')
def showarticle():
    # created_article = Article.query.filter_by(doi=doi).first()
    return "oh, hai!"

if __name__ == '__main__':
    app.run()
