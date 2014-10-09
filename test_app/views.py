from test_app import app
from test_app import db
import requests
from test_app import models
import random
from flask.ext.restful import reqparse, abort, Api, Resource
from flask import jsonify, Response
import json

api = Api(app)

INDEX_SCHEMA = {
    "_id": "/type/article",
    "name": "Projects",
    "properties": {
      "name": {
        "name": "Article Name",
        "type": "string",
        "unique": True
      },
      "journal": {
        "name": "Journal",
        "type": "string",
        "unique": True
      },
      "authors": {
        "name": "Author",
        "type": "string",
        "unique": False,
        "meta": {
          "details": True
        }
      },
      "published_at": {
        "name": "Published Date",
        "type": "date",
        "unique": True
      },
      "image": {
        "name": "Image",
        "type": "string",
        "unique": True
      },
      "abstract": {
        "name": "Abstract",
        "type": "string",
        "unique": True
      },
      "article-type": {
        "name": "Article Type",
        "type": "string",
        "unique": True,
        "meta": {
          "facet": True,
          "details": True
        }
      },
      "organisms": {
        "name": "Organisms",
        "type": "string",
        "unique": False,
        "meta": {
          "facet": True,
          "details": True
        }
      },
      "subjects": {
        "name": "Subjects",
        "type": "string",
        "unique": False,
        "meta": {
          "facet": True,
          "details": True
        }
      },
      "keywords": {
        "name": "Keywords",
        "type": "string",
        "unique": False,
        "meta": {
          "facet": False,
          "details": True
        }
      }
    }
  }

def jsonp_wrapper(result):
	return "if (!window.handleDocList) { console.error('Could not find JSONP callback.'); } else { window.handleDocList(" + result +"); }"

def unpack_authors_from_article(article):
	authors = article.authors
	author_names = []
	for author in authors:
		author_names.append(author.name)
	return author_names

def unpack_terms_from_article(article, this_term_type):
	terms = article.terms
	print terms
	return_terms = []
	for term in terms:
		if term.term_type == this_term_type:
			return_terms.append(term.term)
	return return_terms

def get_article_representation(uid):
	this_article = models.Article.query.filter_by(doi=uid).first()
	author_names = unpack_authors_from_article(this_article)
	keywords = unpack_terms_from_article(this_article, "keywords")
	subjects = unpack_terms_from_article(this_article, "subjects")
	organisms = unpack_terms_from_article(this_article, "organisms")
	rep = {"_id": this_article.doi,
			"published_at": this_article.pub_date,
			"name": this_article.title,
			"journal": "eLife",
			"article-type": "Research-Article",
			"authors": author_names,
			"keywords": keywords,
			"subjects": subjects,
			"organisms": organisms,
			"url": "documents/" + uid
			}
	return rep

def generate_lens_index(uids):
	all_reps = []
	for uid in uids:
		try:
			article_rep = get_article_representation(uid)
			all_reps.append(article_rep)
		except:
			continue
	return all_reps

def get_article_uids():
	articles = models.Article.query.all()
	dois = []
	for article in articles: dois.append(article.doi)
	return dois

def get_existing_or_create_new_article(uid):
	this_article = models.Article.query.filter_by(doi=uid).first()
	if this_article == None:
		this_article = models.Article(doi=uid)
	return this_article

def get_existing_or_create_new_author(author_name):
	this_author = models.Author.query.filter_by(name=author_name).first()
	if this_author == None:
		this_author = models.Author(name=author_name)
	return this_author

def get_existing_or_create_new_authors(author_names):
	authors = []
	for author_name in author_names:
		this_author = get_existing_or_create_new_author(author_name)
		authors.append(this_author)
	return authors

def get_existing_or_create_new_term(term_description):
	print term_description
	term_name, term_type = term_description.split(":")
	print term_name, term_type
	this_term = models.Term.query.filter_by(term=term_name).first()  # watch out, this means we can't have differt types with different names
	if this_term == None:
		this_term = models.Term()
		this_term.term = term_name
		this_term.term_type = term_type
	return this_term

def get_existing_or_create_new_terms(term_descriptions):
	terms = []
	for term_description in term_descriptions:
		this_term = get_existing_or_create_new_term(term_description)
		terms.append(this_term)
	return terms

def create_update_research_article_on_uid(uid, update_info):
	this_article = get_existing_or_create_new_article(uid)
	print update_info
	keys = update_info.keys()
	# if we were updating simple attributes then the following might work
	# could try something like a.__dict__.update(d)
	# however we need to create new objects for terms and authors, based off of our DB classes
	# so this approach won't work
	for key in keys:
		print key, update_info[key]
		if key == "title" : this_article.title = update_info[key]
		if key == "pub_date" : this_article.pub_date = update_info[key]
		if key == "authors":
			author_names = update_info[key]
			author_objects = get_existing_or_create_new_authors(author_names)
			this_article.authors = author_objects
		if key == "terms":
			term_descriptions = update_info[key]
			term_objects = get_existing_or_create_new_terms(term_descriptions)
			this_article.terms = term_objects
	db.session.add(this_article)
	db.session.commit()
	return True

class About(Resource):
	def get(self):
		return "this is a test api for eLife prototyping"

class LensIndex(Resource):
	def get(self):
		uids = get_article_uids()
		result = {};
		result['type'] = INDEX_SCHEMA
		result['objects'] = generate_lens_index(uids)
		data = jsonp_wrapper(json.dumps(result, indent=2))
		resp = Response(response=data,
			status=200,
			mimetype="application/javascript")
		return resp

class ArticleList(Resource):
	def get(self):
		uids = get_article_uids()
		return jsonify(dois=uids)

class Article(Resource):
	def get(self, uid):
		article_info = get_article_representation(uid)
		return jsonify(article=article_info)  # jsonify moved to decorator to allow decorator to inspect return value of function

	def put(self, uid):
		attributes = optional_parser.parse_args()
		update_info = {}
		if attributes["title"]: update_info["title"] = attributes["title"]
		if attributes["pub_date"]: update_info["pub_date"] = attributes["pub_date"]
		if attributes["terms"]: update_info["terms"] = attributes["terms"]
		if attributes["authors"]: update_info["authors"] = attributes["authors"]
		create_update_research_article_on_uid(uid, update_info)  # create the article in the DB
		return uid, 201

optional_parser = reqparse.RequestParser() #  arguments that are optional
optional_parser.add_argument('title', type=str, help="a title for the article")
optional_parser.add_argument('pub_date', type=str, help="a date for the article")
optional_parser.add_argument('terms', type=str, action='append', help="types of terms for the article")
optional_parser.add_argument('authors', type=str, action='append', help="authors of the article")

api.add_resource(About, '/')
api.add_resource(ArticleList, '/articles')
api.add_resource(Article, '/articles/uid/<string:uid>')
api.add_resource(LensIndex, '/lens/documents.js')
