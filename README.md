# Shabashka 

Shabashka is the service for people to find some extra job on the one hand, and on the other hand it’s a service for a people who have some work to be done. Basicly  Shabaashka is an online extra job marketplace that provides a means for worker and employer. In additional, let’s take a look at example:
- Someone(employer) need to remodel his bathroom
- He creates an new offer, provides title, description, expected price, photo, ect.
- Workers are responding  for this offer, providing their price, time amount, and comment
- Employer chose from workers which he’s like and clicks “Take offer”
- Now worker and employer can discuss all details of the deal in chat 
- Worker done his job
- Employer is closes his offer and leave a review for worker
- Everybody is happy

## Installation

- Install project dependencies by running pip install -r requirements.txt. Requirements contains:
    - django
    - django-bootstrap4
    - pillow
    - easy-thumbnails
    - django-cleanup
    - djangorestframework
    - django-cors-headers
    - django-crispy-forms
    - python-dotenv
- Make and apply migrations by running python manage.py makemigrations and python manage.py migrate.
- Create near the manage.py file ".env". This file contains enviroment variables, such as:
    - SECRET - secret key 
    - GMAIL_HOST_USER - mail username for smtp messages 
    - GMAIL_HOST_PASSWORD - mail password 
    - DJANGO_DATABASE
    - DB_NAME
    - DB_USER
    - DB_PASSWORD
    - DB_IP

##  Project structure 

