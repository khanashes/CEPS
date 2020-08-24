This CEPS system which is basically a website which can compare products from different sites by using real time webscraping. It has a feature of keeping track of the prices of the product which user chooses so when the change occurs it will notify the user.
<-----------[requires]-------------------->
python_version = "3.7"
<------------------------------------->
for running this project you must need to open project on visual studio or whatever text editor you are using
Then open the terminal and change the current directory to your local project directory which in our case is CEPS
Then run this command "pip install pipenv" then next you need to run "pipenv shell" command to create virtual environment. Then instead of pip use pipenv to install following packges
<------------------Packages you need to install---------------------->
[packages]
django = "==3.0"
bs4 = "*"
requests = "*"
lxml = "*"
django-simple-history = "*"
psycopg2 = "*"
django-widget-tweaks = "*"
celery = "*"
redis = "==3.5.3"
django-notifications-hq = "*"
django-celery-beat = "*"

<------------------------To run schduler in the background------------------------------------------->
For this you need to install redis server and then you need to run following commands in virtual environment
celery -A main worker --loglevel=info
celery -A main beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
<------------------------Migration-------------------------------------------->
Now run the migration command
python manage.py makemigrations
python manage.py migrate
<-----------------------------Run the system------------------------------------------------->
Now you can finally run this system by using following command
python manage.py runserver
<--------------------------------------------------------------------------------------------->
