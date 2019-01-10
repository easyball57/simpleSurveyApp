import sqlite3 as lite
from datetime import datetime

from flask import Flask

dbFile = '/db/simplesurveyapp.db'

app = Flask(__name__)

@app.route('/')
def hello_world():
	return 'Simple Survey App!'

@app.route('/yes/<int:survey_id>')
def yes_survey(survey_id):
	# add the answer YES to the survey id survey_id
	con = lite.connect(dbFile)
	con.execute("INSERT INTO SSA (survey_id, answer, ts) VALUES (?,?,?)", (survey_id, True, datetime.now()))
	con.commit()
	con.close()
	return 'Thanks for participating'

@app.route('/no/<int:survey_id>')
def no_survey(survey_id):
	# add the answer NO to the survey id survey_id
	con = lite.connect(dbFile)
	con.execute("INSERT INTO SSA (survey_id, answer, ts) VALUES (?,?,?)", (survey_id, False, datetime.now()))
	con.commit()
	con.close()
	return 'Thanks for participating'

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
		result = result + str(row[0]) + ";" + str(row[1]) + ";" + row[2] + "<br>"
	return result

@app.route('/results/<int:survey_id>')
def results_survey(survey_id):
	# show the list of answers for a given survey id survey_id
	con = lite.connect(dbFile)
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
	con = lite.connect(dbFile)
	cur = con.cursor()
	cur.execute("SELECT DISTINCT survey_id FROM SSA")
	rows = cur.fetchall()
	con.close()
	result = "survey_id<br>"
	for row in rows:
		result = result + str(row[0]) + "<br>"
	return result

@app.route('/reset/<int:survey_id>')
def reset_survey():
	# add the answer NO to the survey id survey_id
	con = lite.connect(dbFile)
	con.execute("DELETE * FROM SSA WHERE survey_id=?", (survey_id,))
	con.commit()
	con.close()
	result = 'Survey #' + str(survey_id) + ' has been deleted.'
	return result

@app.route('/pie/<int:survey_id>')
def pie_survey():
	# show the list of answers for a given survey id survey_id
	con = lite.connect(dbFile)
	cur = con.cursor()
	cur.execute("SELECT survey_id, answer, count(*) FROM SSA WHERE survey_id=? GROUP BY answer", (survey_id,))
	rows = cur.fetchall()
	con.close()
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
	result = result + 'var yes_no=' + str(rows[0][0]) + ';'
	result = result + 'var yes_nb=' + str(rows[1][0]) + ';'
	result = '''
  var data = google.visualization.arrayToDataTable([
  ["Answers", "Numbers"],
  ["Yes", yes_nb],
  ["No", no_nb]
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
	
	

	
