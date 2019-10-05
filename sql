DROP TABLE IF EXISTS chapter;
DROP TABLE IF EXISTS exo;

CREATE TABLE chapter (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT 
);

CREATE TABLE exo (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	title TEXT,
	stars INTEGER,
	enonce TEXT,
	indication TEXT,
	corrige TEXT,
	enonce_html TEXT,
	indication_html TEXT,
	corrige_html TEXT,
	enonce_hash VARCHAR(30),
	indication_hash VARCHAR(30),
	corrige_hash VARCHAR(30),
	chapter_id INTEGER
);