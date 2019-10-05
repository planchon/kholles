import requests
from bs4 import BeautifulSoup
import re
import lxml
import json
import random
import string
import sqlite3

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

def scrap_exo_page(page):
	tmp_exo = []
	page = requests.get(page).content
	soup = BeautifulSoup(page, features="lxml")
	type_exo = soup.select("h1")[0].text.strip()
	raw_links = soup.find_all("div", {"class": "exo"})
	for link in raw_links:
		title_raw = str(link.find("div", {"class": "titreexo"}))
		stars = title_raw.count("www.bibmath.net/ressources/lib/Icone_etoile.png")
		title = re.search(" - (.*)<a href=\"http://www.bibmath.net/ressources/signalerreur.", title_raw).group(1)

		enonce_html = str(link.find("div", {"class": "enonce"}))
		indication_html = str(link.find("div", {"class": "indication"}))
		corrige_html = str(link.find("div", {"class": "corrige"}))
		enonce = html_to_latex(enonce_html)
		corrige = html_to_latex(corrige_html)
		indication = html_to_latex(indication_html)

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
		# 	"chapter": type_exo
		# }

		exo = (title, stars, enonce, indication, corrige, enonce_html, indication_html, corrige_html, type_exo)
		tmp_exo.append(exo)

	add_to_database(tmp_exo)

def add_to_database(data):
	for e in data:
		query = 'INSERT INTO exo VALUES (NULL,?, ?, ?, ?, ?, ?, ?, ?, ?);'
		cursor.execute(query, e)

if __name__ == "__main__":
	for annee in BASE_LINKS:
		links = scrap_menu_page(annee)
		for link in links:
			scrap_exo_page(link)