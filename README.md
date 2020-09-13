# Candidate Matcher

## About 
* Web server which provides candidate recommendations for given jobs
* Implements various APIs for expressing opinions / adding notes / querying data for candidates and jobs

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
    

* Make migrations / migrate tables:
       
       python manage.py makemigrations
       python manage.py migrate

* Reading initial data into the database:
        
       python manage.py loaddata skills.json jobs.json candidates.json

* Running server:
       
       python manage.py runserver
        
* Overview of all REST API calls: 
    
    https://documenter.getpostman.com/view/3026991/TVK5d29a

* Running tests:
        
       python manage.py test matcher_app
       
## Running on Heroku
* Main url for making REST API calls: 
    
   https://candidate-matching.herokuapp.com/
        
   - Heroku database has same initial data as local database


## Candidate Matching 

The naive approach taken in this application checks for a match based on title matching (or some substring
of the title matching) as well as a skills match.

A more advanced approach for this use case would be to use fuzzy matching. Since the goal is to link some text
(candidate job title / skills) with the target job title / skill, we can try to identify non-exact matches
between the two.

We can do this by calculating the Levenshtein Distance representing the number of transformations required to get
from the source string to the target string, with a lower distance representing a higher match probability.

The downside to this approach is that it does not account for relevance, and misspellings / typos could completely
transform the meaning of the word. This would be problematic when comparing "Developer" to "Engineer".
Even though the two words are very similar job wise, the Levenshtein distance would be large between the two.

Another way to solve this is to extract features from the text using something like word2vec, where
the text data is converted into numeric format.

# Ranking the Candidates
We can assign probabilities to each job skill - for example, we assume 70% of 
candidates know python, while only 1% know cobalt. 
    
We can convert each skill into points based on this percentage (ex: 70% --> 30 points, 1% --> 99 points) and 
sum the total points for each candidate to create a ranking. This rewards candidates who 
have a skill that is less common and presumably also more difficult to learn. 

There are a few problems with this approach:
1. It is linear - the maximum points that can be given for a given skill with this method
is 99 points. It would be better for the point system to be exponential, where a skill 
that a smaller percentage of candidates have is represented by a greater number of points

2. It does not take into account conditional probabilities: for example, a candidate 
who has skills of django and python, where django is conditional on knowing python