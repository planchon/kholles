from flask import Flask, render_template
import json
from tinydb import TinyDB, Query

app = Flask(__name__)

db = TinyDB('../bdd.json')

@app.route('/exos')
def all_exos():
	with open('../bdd.json') as bdd_raw_file:
		exos_bdd = json.load(bdd_raw_file)

	return render_template('exos.html', exos=exos_bdd)

if __name__ == '__main__':
	app.run()
