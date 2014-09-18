from test_app import app
from test_app import db
import requests
from test_app import models

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
	user = models.User('John Doe', 'john.doe@example.com')
	print "user created"
	db.session.add(user)
	db.session.commit()
	return "user created"

@app.route('/putarticle')
def putarticle():
	art = models.Article('This is the title', 'this is the DOI', "2014-08-10")
	print "user created"
	db.session.add(art)
	db.session.commit()
	a = models.Article.query.get(1)
	t = models.Term(term="name", term_type="type", article=a)
	db.session.add(t)
	db.session.commit()
	return "article created"

@app.route('/putterm')
def putterm():
	terms = ["gene", "hox", "peterson", "alpha"]
	this_term = random.choice(terms)
	term_types = ["organisim", "author keyword", "keyword"]
	this_term_type = random.choice(term_types)
	term = models.Term(this_term, this_term_type)
	db.session.add(term)
	db.session.commit()
	return "created term"

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
		article_details.append(out_string)
	output = "<br/>".join(article_details)
	return output


@app.route('/showperson')
def showpeople():
	all_users = models.User.query.all()
	user_names = []
	for user in all_users:
		user_names.append(user.name)
	output = "<br/>".join(user_names)
	return output
