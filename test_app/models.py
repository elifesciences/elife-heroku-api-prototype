from test_app import app
from test_app import db

article_taggings = db.Table('article_taggings',
    db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
    db.Column('term_id', db.Integer, db.ForeignKey('term.id'))
)

authorships = db.Table('authorships',
	db.Column('article_id', db.Integer, db.ForeignKey('article.id')),
	db.Column('author_id', db.Integer, db.ForeignKey('author.id'))
)

class Article(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(180))
	doi = db.Column(db.String(120))
	pub_date = db.Column(db.String(120))
	terms = db.relationship('Term', secondary=article_taggings,
        backref=db.backref('articles', lazy='dynamic'))
	authors = db.relationship('Author', secondary=authorships,
		backref=db.backref('articles', lazy='dynamic'))

	def __repr__(self):
		return '<Doi %r>' % self.title

class Author(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	def __repr__(self):
		return '<Name %r>' % self.name

class Term(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	term = db.Column(db.String(120))
	term_type = db.Column(db.String(60))

	def __repr__(self):
		return '<Name %r>' % self.term
