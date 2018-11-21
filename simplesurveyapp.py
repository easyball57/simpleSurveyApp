from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Simple Survey App!'

@app.route('/yes/<int:survey_id>')
def yes_survey(survey_id):
    # add the answer YES to the survey id survey_id
    return 'Sondage %d : YES' % survey_id

@app.route('/no/<int:survey_id>')
def no_survey(post_id):
    # add the answer NO to the survey id survey_id
    return 'Sondage %d : NO' % survey_id

@app.route('/answers/<int:survey_id>')
def answers_survey(survey_id):
    # show the list of answers for a given survey id survey_id
    return 'Sondage %d : ANSWERS' % survey_id

@app.route('/list')
def list_survey():
    # show the list of survey id's
    return 'Sondage : LIST'
