import sqlite3 as lite
from datetime import datetime
import os

from flask import Flask, request, make_response, render_template

#dbFile = './db/simplesurveyapp.db'
dbFile = os.environ["SSA_DB"]

NO_YES=('No', 'Yes')

app = Flask(__name__, template_folder='./')

def yes_no(survey_id, answer):
	all = request.cookies.get('ssa')
	if(all is None):
		all=""
	if(all.find("D"+str(survey_id)+"F") == -1):
		# add the answer YES to the survey id survey_id
		all = all + "D" + str(survey_id) + "F"
		con = lite.connect(dbFile)
		con.execute("INSERT INTO SSA (survey_id, answer, ts) VALUES (?,?,?)", (survey_id, answer, datetime.now()))
		con.commit()
		con.close()
		resp = make_response(render_template('thanks.html'))
		resp.set_cookie('ssa', all)
	else:
		resp = make_response(render_template('already.html'))
	return resp

@app.route('/')
def home_page():
	return "Welcome to Simple Survey App v1.0" 

@app.route('/cook')
def cook():
	return request.cookies.get('ssa')

@app.route('/kooc')
def kooc():
	resp = make_response(render_template('cook.html'))
	resp.set_cookie('ssa', '')
	return resp 

@app.route('/help')
def help():
	result = "Simple Survey App DB : " + dbFile + " <br>"
	result = result + "Cookies : ssa : " + request.cookies.get('ssa') + " <br>"
	f = open("README.md", "r")
	for line in f:
		result = result + line + "<br>"
	return result

@app.route('/yes/<int:survey_id>')
def yes_survey(survey_id):
	return yes_no(survey_id, 1)

@app.route('/no/<int:survey_id>')
def no_survey(survey_id):
	return yes_no(survey_id, 0)

@app.route('/answers/<int:survey_id>')
def answers_survey(survey_id):
	# show the list of answers for a given survey id survey_id
	con = lite.connect(dbFile)
	cur = con.cursor()
	cur.execute("SELECT * FROM SSA WHERE survey_id=?", (survey_id,))
	rows = cur.fetchall()
	con.close()
	result = "survey_id;answer;ts<br>"
	for row in rows:
		result = result + str(row[0]) + ";" + NO_YES[row[1]] + ";" + row[2] + "<br>"
	return result

@app.route('/results/<int:survey_id>')
def results_survey(survey_id):
	# show the count of YES and NO for a given survey id survey_id
	con = lite.connect(dbFile)
	cur = con.cursor()
	cur.execute("SELECT survey_id, answer, count(*) FROM SSA WHERE survey_id=? GROUP BY answer ORDER BY answer", (survey_id,))
	rows = cur.fetchall()
	con.close()
	result = "survey_id;answer;number<br>"
	for row in rows:
		result = result + str(row[0]) + ";" + NO_YES[row[1]] + ";" + str(row[2]) + "<br>"
	return result

@app.route('/list')
def list_survey():
	# show the list of survey id's
	con = lite.connect(dbFile)
	cur = con.cursor()
	cur.execute("SELECT DISTINCT survey_id FROM SSA")
	rows = cur.fetchall()
	con.close()
	result = "survey_id<br>"
	for row in rows:
		result = result + str(row[0]) + "<br>"
	return result

@app.route('/reset/<int:survey_id>/<int:yes_nb>')
def reset_survey(survey_id, yes_nb):
	# delete all data from a survey 
	# but before check the number of yes as a confirmation
	con = lite.connect(dbFile)
	cur = con.cursor()
	cur.execute("SELECT count(*) FROM SSA WHERE survey_id=? AND answer=1", (survey_id,))
	rows = cur.fetchall()
	con.close()
	if(rows[0][0] == yes_nb):
		con = lite.connect(dbFile)
		con.execute("DELETE FROM SSA WHERE survey_id=?", (survey_id,))
		con.commit()
		con.close()
		result = 'Survey #' + str(survey_id) + ' has been deleted.'
	else:
		result = 'Survey #' + str(survey_id) + ' has NOT been deleted.'
	return result

@app.route('/pie/<int:survey_id>')
def pie_survey(survey_id):
	# graph a pie chart for a given survey id survey_id
	con = lite.connect(dbFile)
	cur = con.cursor()
	cur.execute("SELECT survey_id, answer, count(*) FROM SSA WHERE survey_id=? GROUP BY answer ORDER BY answer", (survey_id,))
	rows = cur.fetchall()
	con.close()
	no_nb = 0
	yes_nb = 0
	for row in rows:
		if(row[1] == 0):
			no_nb = row[2]
		else:
			yes_nb = row[2]

	result = '''
<!DOCTYPE html>
<html lang="en-US">
<body>

<div id="piechart"></div>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>

<script type="text/javascript">
// Load google charts
google.charts.load("current", {"packages":["corechart"]});
google.charts.setOnLoadCallback(drawChart);

// Draw the chart and set the chart values
function drawChart() {
	'''
	result = result + 'var survey_nb=' + str(survey_id) + ';'
	result = result + 'var no_nb=' + str(no_nb) + ';'
	result = result + 'var yes_nb=' + str(yes_nb) + ';'
	result = result + '''
  var data = google.visualization.arrayToDataTable([
  ["Answers", "Numbers"],
  ["Yes("+yes_nb+")", yes_nb],
  ["No("+no_nb+")", no_nb]
]);
  // Optional; add a title and set the width and height of the chart
  var options = {"title":"Survey #"+survey_nb, "width":550, "height":400};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById("piechart"));
  chart.draw(data, options);
}
</script>

</body>
</html>
  	'''
	return result

