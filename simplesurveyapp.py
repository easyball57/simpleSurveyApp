import sqlite3 as lite
from datetime import datetime

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Simple Survey App!'

@app.route('/yes/<int:survey_id>')
def yes_survey(survey_id):
	# add the answer YES to the survey id survey_id
	con = lite.connect('db/simpleSurveyApp.db')
	con.execute("INSERT INTO SSA (survey_id, answer, ts) VALUES (?,?,?)", (survey_id, True, datetime.now()))
	con.commit()
	con.close()
	return 'Thanks for participating'

@app.route('/no/<int:survey_id>')
def no_survey(survey_id):
	# add the answer NO to the survey id survey_id
	con = lite.connect('db/simpleSurveyApp.db')
	con.execute("INSERT INTO SSA (survey_id, answer, ts) VALUES (?,?,?)", (survey_id, False, datetime.now()))
	con.commit()
	con.close()
	return 'Thanks for participating'

@app.route('/answers/<int:survey_id>')
def answers_survey(survey_id):
	# show the list of answers for a given survey id survey_id
	con = lite.connect('db/simpleSurveyApp.db')
	cur = con.cursor()
	cur.execute("SELECT * FROM SSA WHERE survey_id=?", (survey_id,))
	rows = cur.fetchall()
	con.close()
	result = "survey_id;answer;ts<br>"
	for row in rows:
		result = result + str(row[0]) + ";" + str(row[1]) + ";" + row[2] + "<br>"
	return result

@app.route('/results/<int:survey_id>')
def results_survey(survey_id):
	# show the list of answers for a given survey id survey_id
	con = lite.connect('db/simpleSurveyApp.db')
	cur = con.cursor()
	cur.execute("SELECT survey_id, answer, count(*) FROM SSA WHERE survey_id=? GROUP BY answer", (survey_id,))
	rows = cur.fetchall()
	con.close()
	result = "survey_id;answer;number<br>"
	for row in rows:
		result = result + str(row[0]) + ";" + str(row[1]) + ";" + str(row[2]) + "<br>"
	return result

@app.route('/list')
def list_survey():
	# show the list of survey id's
	con = lite.connect('db/simpleSurveyApp.db')
	cur = con.cursor()
	cur.execute("SELECT DISTINCT survey_id FROM SSA")
	rows = cur.fetchall()
	con.close()
	result = "survey_id<br>"
	for row in rows:
		result = result + str(row[0]) + "<br>"
	return result
