from test_app import app
from test_app import db
import requests
from test_app import models
import random

def gen_random_term():
	terms = ["gene", "hox", "peterson", "alpha"]
	this_term = random.choice(terms)
	term_types = ["organisim", "author keyword", "keyword"]
	this_term_type = random.choice(term_types)
	term = models.Term(term=this_term, term_type=this_term_type)
	return term

def select_random_term():
	all_terms = models.Term.query.all()
	print all_terms
	if all_terms:
		random_term = random.choice(all_terms)
		return random_term
	else:
		return None

def prep_terms():
	t = gen_random_term()
	u = gen_random_term()
	s = select_random_term()
	inject_terms = [t,u]
	if s and s not in inject_terms:
		inject_terms.append(s)
	return inject_terms

def gen_random_author():
	names = ["bob", "joe", "sue", "ann"]
	this_name = random.choice(names)
	author = models.Author(name=this_name)
	return author

def select_random_author():
	authors = models.Author.query.all()
	if authors:
		random_author = random.choice(authors)
		return random_author
	else:
		return None

def prep_authors():
	a = gen_random_author()
	b = gen_random_author()
	s = select_random_author()
	inject_authors = [a,b]
	if s and s not in inject_authors:
		inject_authors.append(s)
	return inject_authors

@app.route('/putarticle')
def putarticle():

	inject_terms = prep_terms()
	inject_authors = prep_authors()
	print inject_terms
	print inject_authors

	art = models.Article(title='This is the title', doi='this is the DOI',
				pub_date="2014-08-10", terms=inject_terms, authors=inject_authors)
	db.session.add(art)
	db.session.commit()
	return "article created"

@app.route('/showarticles')
def showarticles():
	all_articles = models.Article.query.all()
	article_details = []
	for article in all_articles:
		out_string = article.title

		terms = article.terms
		term_string = ""
		for t in terms:
			term_string += " " + t.term
		out_string = out_string + " " + term_string

		authors = article.authors
		author_string = ""
		for a in authors:
			author_string += " " + a.name
		out_string = out_string + " " + author_string

		article_details.append(out_string)

	output = "<br/>".join(article_details)
	return output
