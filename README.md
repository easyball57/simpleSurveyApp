# simpleSurveyApp

Installation :
	- Sur base de Python,
	- Installer Flask
	- Installer SQLite3
	- Avoir un stockage persistent pour stocker la DB SQLite3
	
Script de démarrage :
	- Création de la DB si elle n'existe pas
	- Puis démarrage Flask
	
	$ export FLASK_APP=simpleSurveyApp.py
	$ flask run
	
Structure DB : SSA
Table SSA
	int : Survey_id
	bool : Answer = Yes / No
	timestamp : Datetime = timestamp
	
