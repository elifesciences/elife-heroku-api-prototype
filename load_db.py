import parseNLM as nlm
from glob import glob
from bs4 import BeautifulSoup
import requests
import json
import logging
import time
import os
import argparse
import pdb


def get_doi(soup):
	doi = nlm.doi(soup)
	return doi

def get_date_article(soup):
	pub_year = nlm.pub_date_year(soup)
	pub_month = nlm.pub_date_month(soup)
	pub_day = nlm.pub_date_day(soup)
	pub_tuple = [str(pub_year), str(pub_month).zfill(2), str(pub_day).zfill(2)]
	pub_date = str(pub_year) + "-" + str(pub_month).zfill(2) + "-" + str(pub_day).zfill(2)
	return pub_date

def get_title(soup):
	title = nlm.title(soup)
	return title

def get_authors(soup):
	authors = nlm.authors(soup)
	author_names = []
	for author in authors:
		author_names.append(author["author"])
	return author_names

def get_keywords(soup):
	keywords = nlm.keywords(soup)
	decorated_keywords = []
	for keyword in keywords:
		decorated_keywords.append(keyword + ":keywords")
	return decorated_keywords

def get_subject_area(soup):
	subject_areas = nlm.subject_area(soup)
	decorated_sub_areas = []
	for sub_area in subject_areas:
		decorated_sub_areas.append(sub_area + ":subjects")
	return decorated_sub_areas

def get_research_organism(soup):
	research_organisms = nlm.research_organism(soup)
	decorated_research_organisms = []
	if type(research_organisms) is list:
		for research_organism in research_organisms:
			decorated_research_organisms.append(research_organism + ":organisms")
	else:
		decorated_research_organisms = [research_organisms + ":organisms"]
	return decorated_research_organisms

def get_uid_from_doi(doi):
	uid = doi.split(".")[-1]
	return uid

def get_article_details(article, api_base_url):
	#TODO: separate detail extraction from api upload

	soup = nlm.parse_document(article)

	uid = get_uid_from_doi(get_doi(soup))
	title = get_title(soup)
	pub_date = get_date_article(soup)
	authors = get_authors(soup)
	keywords = get_keywords(soup)
	research_organisms = get_research_organism(soup)
	subject_areas = get_subject_area(soup)

	all_keywords = keywords + research_organisms + subject_areas

	params = {"title": title,
			  "authors": authors,
			  "pub_date": pub_date,
			  "terms" : all_keywords
			}

	api_endpoint = api_base_url + "articles/uid/"+str(uid)
	r = requests.put(api_endpoint, params=params)

def main():

	xml_dir = os.environ["XML_PATH"]
	heroku_api_base = os.environ["HEROKU_BASE_URL"]
	local_api_base = os.environ["LOCAL_BASE_URL"]

	parser = argparse.ArgumentParser()
	parser.add_argument("-l", "--location", help="`l` sets this script to populate a local app instance, `h` populates the heroku app ")
	args = parser.parse_args()


	if args.location == "l":
		api_base_url = local_api_base
	elif args.location == "h":
		api_base_url = heroku_api_base

	print api_base_url

	articles = glob(xml_dir+"*.xml")
	for article in articles[30:40]:
	 	try:
			get_article_details(article, api_base_url)
			print "laoded " + article
	 	except:
			print "screwed up on " + article

if __name__ == '__main__':
	print('Executed from the command line')
	main()
