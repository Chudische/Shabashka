# Shabashka 

Shabashka is the service for people to find some extra job on the one hand, and on the other hand it’s a service for a people who have some work to be done. Basicly  Shabaashka is an online extra job marketplace that provides a means for worker and employer. In additional, let’s take a look at example:
- Someone(employer) need to remodel his bathroom
- He creates a new offer, provides title, description, expected price, photo, ect.
- Workers are responding  for this offer, providing their price, time amount, and comment
- Employer chose from workers which he’s like and clicks “Take offer”
- Now worker and employer can discuss all details of the deal in chat 
- Worker done his job
- Employer is closes his offer and leave a review for worker
- Everybody is happy

## Installation

- Install project dependencies by running `pip install -r requirements.txt`. Requirements contains:
    - django
    - django-bootstrap4
    - pillow
    - easy-thumbnails
    - django-cleanup
    - djangorestframework
    - django-cors-headers
    - django-crispy-forms
    - python-dotenv
- Make and apply migrations by running `python manage.py makemigrations` and `python manage.py migrate`.
- Create file `.env` near the `manage.py`. This file should contains enviroment variables, such as:
    - SECRET - Django secret key 
    - GMAIL_HOST_USER - mail username for smtp messages 
    - GMAIL_HOST_PASSWORD - mail password 
    - DJANGO_DATABASE - in settings.py there are 3 option of this variable (network, remote, local) network is default
    - DB_NAME - name of database for PostgreSQL backend 
    - DB_USER - user of database for PostgreSQL backend 
    - DB_PASSWORD - password of database for PostgreSQL backend
    - DB_IP - ip address of database for PostgreSQL backend

## Email settings 

Shabashka uses smtp.gmail.com for sending emails. Make shure you allow django to send email through gmail by turn on "Access for less secure apps" on your google account. Shabashka is sending such notifications:
- `send_activation_notification()` - after regitration user receive an activation letter;
- `send_comment_notification()` - after worker posts comment to offer, offer author gets an email;
- `send_chat_message_notification()` - after user posts message in chat, receiver gets an email;
- `send_review_notification()` - after the offer closed, offer author makes a review to worker and worker gets an email.


## API

Get first 30 offers:
    `/api/offers`

Get offer details:
    `/api/offers/pk` 
    (where __pk__ is offer id)

Get or post offer comments:
    `/api/offers/pk/comments`
    (where __pk__ is offer id; User can post comment only if authenticated)


##  Project structure 

- shabashka
    - api
        - migrations
        - \__init__.py
        - admin.py
        - apps.py
        - models.py
        - serializers.py
        - tests.py
        - urls.py
        - views.py
    - main
        - migrations 
        - static
            - main
                - css
                    - lightbox.css
                    - style.css 
                - images
                - js
                    - html5shiv.js
                    - jquery.pinto.js
                    - jquery.pinto.min.js
                    - lightbox.js
                    - main.js
                    - respond.min.js
        - templates
            - email
                - activation_letter_body.txt
                - activation_letter_subject.txt
                - new_chat_message_body.txt
                - new_chat_message_subject.txt
                - new_comment_body.txt
                - new_comment_subject.txt
                - new_review_body.txt
                - new_review_subject.txt                
            - main
                - about.html
                - activation_done.html
                - add_new_offer.html
                - bad_signature.html
                - by_category.html
                - change_offer.html
                - change_profile.html
                - chat_list.html
                - chat_messages.html
                - contact.html
                - delete_offer.html
                - delete_user.html
                - detail.html
                - favorite.html
                - index.html
                - layout.html
                - login.html
                - logout.html
                - password_change.html
                - password_regenerate.html
                - password_reset_confirm.html
                - password_reset_done.html
                - password_reset_email_subject.html
                - password_reset_email.html
                - password_reset_sent.html
                - password_reset.html
                - profile.html
                - register_done.html
                - register_user.html
                - reviews.html
                - user_is_activated.html
                - user_review.html
        - templatetags
            - \__init__.py
            - custom_tags.py
        - \__init__.py
        - admin.py
        - apps.py
        - forms.py
        - middlewares.py
        - models.py
        - tests.py
        - utilities.py
        - views.py
    - media 
        - thumbnails 
    - shabashka
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
    - db.sqlite3
    - manage.py
    - README.md
    - requirements.txt


