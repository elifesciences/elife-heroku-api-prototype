from test_app import app
from test_app import db

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
