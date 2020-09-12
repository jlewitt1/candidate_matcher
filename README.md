# Candidate Matcher

## About 
* Web server which provides candidate recommendations for given jobs
* Implements various APIs for expressing opinions / adding notes / querying data on the matcher

## Stack
* Django
* Postgres

## Installing / Running Locally
* Install requirements
 
       pip install -r requirements.txt
       
* Create local postgres database with the name "matcher"
   
* In the matcher.settings file the database settings should be defined as follows:
       
       DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': 'matcher',
                'USER': {Your postgres user},
                'PASSWORD': {Your postgres password},
                'HOST': 'localhost',
                'PORT': '5432',
            }
       }
    

* Make migrations / migrate tables
       
       python manage.py makemigrations
       python manage.py migrate

* Reading initial data into the database:
        
       python manage.py loaddata skills.json jobs.json candidates.json

* Overview of all REST API calls 
    https://documenter.getpostman.com/view/3026991/TVK5d29a

* Running tests:
        
       python manage.py test matcher_app
       
## Running on Heroku


