
import requests
from bs4 import BeautifulSoup
import re
import lxml
import json
import random
import string
import sqlite3
import base64

BASE_LINKS = ["http://www.bibmath.net/ressources/index.php?action=affiche&quoi=mathsup/index", 
			  "http://www.bibmath.net/ressources/index.php?action=affiche&quoi=mathspe/index"]

BIBMATH_BASE_URL = "http://www.bibmath.net/ressources/"

conn = sqlite3.connect("data")
cursor = conn.cursor()

def scrap_menu_page(page):
	page = requests.get(page).content
	soup = BeautifulSoup(page, features="lxml")
	raw_links = soup.find_all("a")
	filtered_links = list(filter(lambda x: ("fexo" in str(x)) and ("colle" not in str(x)), raw_links))
	return [BIBMATH_BASE_URL + x.get("href") for x in filtered_links]

# raw html data in text
def html_to_latex(text):
	text = re.sub("<ol.*?>", "\\\\begin{itemize}", text)
	text = re.sub("</ol>", "\\end{itemize}", text)
	text = re.sub("<li>", "\\item", text)
	text = re.sub("<div.*?>", "", text)
	text = re.sub("<a.*?>", "", text)
	text = re.sub("Enoncé.*</a>", "", text)
	text = re.sub("Indication.*</a>", "", text)
	text = re.sub("Corrigé.*</a>", "", text)
	text = re.sub("</div>", "", text)

	text = re.sub("</li>", "", text)

	return text

def sanitize_html(text):
	text = re.sub("<div.*?>", "", text)
	text = re.sub("<a.*?>", "", text)
	text = re.sub("Enoncé.*</a>", "", text)
	text = re.sub("Indication.*</a>", "", text)
	text = re.sub("Corrigé.*</a>", "", text)
	text = re.sub("</div>", "", text)

	return text

def random_word(size=10):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))

def create_chapter(chapter):
	query = "INSERT INTO chapter VALUES (NULL, \"{}\")".format(chapter)
	cursor.execute(query)
	conn.commit()
	return cursor.lastrowid

def scrap_exo_page(page):
	page = requests.get(page).content
	soup = BeautifulSoup(page, features="lxml")
	type_exo = soup.select("h1")[0].text.strip()
	raw_links = soup.find_all("div", {"class": "exo"})

	chapter = create_chapter(type_exo)

	for link in raw_links:
		title_raw = str(link.find("div", {"class": "titreexo"}))
		stars = title_raw.count("www.bibmath.net/ressources/lib/Icone_etoile.png")
		title = re.search(" - (.*)<a href=\"http://www.bibmath.net/ressources/signalerreur.", title_raw).group(1)

		enonce_html = sanitize_html(str(link.find("div", {"class": "enonce"})))
		indication_html = sanitize_html(str(link.find("div", {"class": "indication"})))
		corrige_html = sanitize_html(str(link.find("div", {"class": "corrige"})))
		enonce = html_to_latex(enonce_html)
		corrige = html_to_latex(corrige_html)
		indication = html_to_latex(indication_html)

		enonce_html = base64.b64encode(enonce_html.encode("utf-8"))
		indication_html = base64.b64encode(indication_html.encode("utf-8"))
		corrige_html = base64.b64encode(corrige_html.encode("utf-8"))
		enonce = base64.b64encode(enonce.encode("utf-8"))
		corrige = base64.b64encode(corrige.encode("utf-8"))
		indication = base64.b64encode(indication.encode("utf-8"))
		
		# exercice = {
		# 	"title": title,
		# 	"stars": stars,
		# 	"enonce": enonce,
		# 	"indication": indication,
		# 	"corrige": corrige,
		# 	"enonce_html": sanitize_html(enonce_html),
		# 	"indication_html": sanitize_html(indication_html),
		# 	"corrige_html": sanitize_html(corrige_html),
		# 	"enonce_hash": random_word(),
		# 	"indication_hash": random_word(),
		# 	"corrige_hash": random_word(),
		# }

		exo = (title, stars, enonce, indication, corrige, enonce_html, indication_html, corrige_html, random_word(), random_word(), random_word(), chapter)
		add_to_database(exo)
		


def add_to_database(exo):
	query = 'INSERT INTO exo VALUES (NULL, \"{}\", {}, \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", \"{}\", {})'.format(exo[0], exo[1], exo[2], exo[3], exo[4], exo[5], exo[6], exo[7], exo[8], exo[9], exo[10], exo[11])
	cursor.execute(query)
	conn.commit()

if __name__ == "__main__":
	for annee in BASE_LINKS:
		links = scrap_menu_page(annee)
		for link in links:
			scrap_exo_page(link)

	with open("data.json", "w") as data:
		json.dump(database, data)

	print("scrapped")
	
