from flask import Flask, render_template, send_file
import json
import sqlite3
import base64
from tex_gen import *
import random
import string

app = Flask(__name__)

exo_to_render = []

def decode(data):
	return base64.b64decode(data[2:len(data)-1].encode("utf-8")).decode("utf-8")

@app.route('/exos')
def all_exos():
	conn = sqlite3.connect("../data")
	cursor = conn.cursor()

	rows = cursor.execute("SELECT * FROM exo LIMIT 50")

	exo = []
	for row in rows:
		tmp = [row[0], row[1], row[2], decode(row[3]), row[4], decode(row[5]), decode(row[6]), decode(row[7]), decode(row[8]), row[9], row[10], row[11]]
		exo.append(tmp)

	return render_template('exos.html', exos=exo)


@app.route('/chapter')
def all_chapter():
	conn = sqlite3.connect("../data")
	cursor = conn.cursor()

	rows = cursor.execute("SELECT * FROM chapter")

	chapter = []
	for row in rows:
		chapter.append(row)

	return render_template('all_chapters.html', chapter=chapter)

@app.route('/chapter/<id>')
def get_chapter(id):
	conn = sqlite3.connect("../data")
	cursor = conn.cursor()

	rows = cursor.execute("SELECT * FROM exo WHERE chapter_id={}".format(id))

	exo = []
	for row in rows:
		tmp = [row[0], row[1], row[2], decode(row[3]), row[4], decode(row[5]), decode(row[6]), decode(row[7]), decode(row[8]), row[9], row[10], row[11]]
		exo.append(tmp)

	rows = cursor.execute("SELECT title FROM chapter WHERE id = {}".format(id))
	for row in rows:
		name = row[0]

	return render_template('chapter.html', chapitre=name, exos=exo)

@app.route('/send_exo/<id>', methods=['POST'])
def send_exo(id):
	if id not in exo_to_render:
		exo_to_render.append(id)

	print(exo_to_render)

@app.route('/delete_exo/<id>', methods=['POST'])
def delete_exo(id):
	exo_to_render.remove(id)

@app.route('/liste')
def ma_liste():
	conn = sqlite3.connect("../data")
	cursor = conn.cursor()

	liste = "("
	for i in range(len(exo_to_render)):
		if i == len(exo_to_render) - 1:
			liste += exo_to_render[i]
		else:
			liste += exo_to_render[i] + ","
	liste += ")"	

	q = "SELECT * FROM exo WHERE id IN {}".format(liste)
	print(q)
	rows = cursor.execute(q)

	exo = []
	for row in rows:
		tmp = [row[0], row[1], row[2], decode(row[3]), row[4], decode(row[5]), decode(row[6]), decode(row[7]), decode(row[8]), row[9], row[10], row[11]]
		exo.append(tmp)

	return render_template('liste.html', exos=exo, rand=random_word())

def random_word(size=10):
	return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(size))


@app.route('/generate/<id>')
def gen_latex(id):
	print("HERERERERERERERER")
	conn = sqlite3.connect("../data")
	cursor = conn.cursor()

	liste = "("
	for i in range(len(exo_to_render)):
		if i == len(exo_to_render) - 1:
			liste += exo_to_render[i]
		else:
			liste += exo_to_render[i] + ","
	liste += ")"	

	q = "SELECT * FROM exo WHERE id IN {}".format(liste)
	print(q)
	rows = cursor.execute(q)

	exo = []
	for row in rows:
		if row[4] != "b''":
			tmp = [row[0], row[1], row[2], decode(row[3]), decode(row[4]), decode(row[5]), decode(row[6]), decode(row[7]), decode(row[8]), row[9], row[10], row[11]]
		else:
			tmp = [row[0], row[1], row[2], decode(row[3]), "pas d'indication :(", decode(row[5]), decode(row[6]), decode(row[7]), decode(row[8]), row[9], row[10], row[11]]
		exo.append(tmp)

	link = latex(exo)
	print(link)
	return send_file(link, attachment_filename=link)

def latex(exos):
	# enonces
	exos_data = "\\section{Exercices}"
	for e in exos:
		exos_data += "\\subsection{" + e[1] + "}"
		exos_data += e[3] 

	exos_data += "\\newpage"
	exos_data += "\\section{Indicators}"
	for e in exos:
		exos_data += "\\section{" + e[1] + "}"
		exos_data += e[4] 

	exos_data += "\\newpage"
	exos_data += "\\section{Corriges}"
	for e in exos:
		exos_data += "\\section{" + e[1] + "}"
		exos_data += e[5]

	obj = TexGenerator(exos_data)

	return obj.generatePath(".pdf") 

if __name__ == '__main__':
	app.run()
