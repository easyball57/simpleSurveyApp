# simpleSurveyApp

Simple application based on Flask and SQLite3 to gather the response Yes or No for a question.

How to use it :

To add a 'Yes' to the survey number 'survey_nb'

/yes/'survey_nb'

To add a 'No' to the survey number 'survey_nb'

/no/'survey_nb'

To have the list of off actual surveys

/list

To have the list of all answers of survey number 'survey_nb'

/answers/'survey_id'

To have the results of a survey number 'survey_nb'

/results/'survey_id'

To have a pie chart with the results of survey number 'survey_nb'

/pie/'survey_id'

To reset a specific survey number 'survey_nb'

/reset/'survey_nb'/'nb_of_yes'

You have also to provide the nb of YES for this survey as a control.
Be carreful no confirmation will be asked! Once fired, all is gone!! 
