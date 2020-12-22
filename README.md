# Shabashka 

Shabashka is the service for people to find some extra job on the one hand, and on the other hand it’s a service for a people who have some work to be done. Basically  Shabashka is an online extra job marketplace that provides a means for worker and employer. In additional, let’s take a look at example:
- Someone(employer) need to remodel his bathroom
- He creates a new offer, provides title, description, expected price, photo, ect.
- Workers are responding  for this offer, providing their price, time amount, and comment
- Employer chose from workers which he likes
- Worker and employer can discuss all details of the deal in chat 
- Worker done his job
- Employer is closes his offer and leave a review for worker
- Everybody is happy

Try it on [Shabashka.pp.ua](http://shabashka.pp.ua)

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
- For more secure of project I had used Python-dotenv module. So all data that i do not want to share i put into enrivoment variable. Create file `.env` near the `manage.py`. This file should contains enviroment variables, such as:
    - SECRET - Django secret key 
    - GMAIL_HOST_USER - mail username for smtp messages 
    - GMAIL_HOST_PASSWORD - mail password 
    - DJANGO_DATABASE - in settings.py there are 3 option of this variable (network, remote, local)
        - network is default. It's actual database settings on server
        - remote is development settings from my PC to remote database
        - local is sqlite settings for local testing 
    - DB_NAME - name of database for PostgreSQL backend 
    - DB_USER - user of database for PostgreSQL backend 
    - DB_PASSWORD - password of database for PostgreSQL backend
    - DB_IP - ip address of database for PostgreSQL backend

## Email settings 

Shabashka uses smtp.gmail.com for sending emails. Make sure you allow django to send email through gmail by turn on "Access for less secure apps" on your google account. Shabashka is sending such notifications:
- `send_activation_notification()` - after registration user receive an activation letter;
- `send_comment_notification()` - after worker posts comment to offer, offer author gets an email;
- `send_chat_message_notification()` - after user posts message in chat, receiver gets an email;
- `send_review_notification()` - after the offer closed, offer author makes a review to worker and worker gets an email.

## Project description

### Authentication and authorization

ShaUser model is inherited from AbstractUser class with some additional fields:
- is_activated - for user to confirm his email address
- send_message - does user want to receive emails from Shabashka
- location - where user is live (optional, in the future I want to populate my project for all cities in my country)
- average_rating - calculating when user is get a review 
- favorite - m2m field for following to employers

Authentication system has such functionality:
- Register user
- Login user
- Logout user


It is also possible to recover the user password with email address. It is done with inheritance of such classes:
- PasswordResetView;
- PasswordResetDoneView;
- PasswordResetConfirmView;
- PasswordResetCompleteView

### Profile

After registration user gets on his profile page. Profile has such functionality:
- Change user profile data(first name, last name, location, ect.);
- Change user password;
- Change avatar(by default user sees only avatar placeholder)
- Delete profile(when user delete his profile, his offers and all pictures will delete also using   django-cleanup module)

On users profile page there are all his offers with a different statuses

If user gets the other user profile page, he will see only his active offers in status "New". Also he can follow this user by clicking "follow" link. 

Also authenticated user in account dropdown can gets to the message list page, where he can see all his conversations grouped by offers. When he clicked on message he gest to offers chat. 

### Main page 

On the main page there are all offers in status active. User can:
- click on every offer to get to the offer detail page;
- click on category to get to the "by_category" page which shows every offer in this particular category
- click on user name in every offer to get to the user profile page

Each offer on main page, category page or profile page has:
- category
- data and time (when offer was created)
- title (no more than 64 letters)
- description (short version of decryption which limited by `limit_text()` function from `custom_tags.py`)
- number of views
- number of comments
- number of followers (and if user follows offer author it marks by red color)
- number of shares
- price 
- offer author

On every page that has a offers there is a bootstrap pagination for speed up page loading and more pleasant look of the page

Search and pagination are provided by `shabashka_context_processor()` from `main.middlewares` module
The keyword search is occur in titles and descriptions of the offers.

### Offer detail page 

In offer detail page in addition to offer look in main page or category page user sees:
- main photo 
- additional photos(if exist)
- comments 
- comment form (for authenticated users)

### Offer life cycle

- at first user create new offer in `create` tab in navbar;
- offer creates with status `new` and `is_active`;
- other users respond to the offer by leaving their comments, offering their price and lead time;
- offer author accepts one of responds:
    - all other responds `is_active` change to `False`(they dosen't shows in offer page)
    - offer status change to `accepted`
- for offer author appear buttons `cancel`, `chat`, `done`:
    - `cancel`:
        - all other responds `is_active` change to `True`
        - offer status change to `new`
    - `chat` - opens chat between offer author and responder
    - `done`:
        - offer author redirects to review form
        - author makes a review to responder
        - offer status change to `done` 
        - `is_active` changed to `False`        
- for responder there is only a `chat` button
- after offer is done offer author can delete it in profile page


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

- shabashka/ 
    - api/
        - migrations/
        - `__init__.py` 
        - admin.py
        - apps.py
        - models.py
        - serializers.py 
        - tests.py
        - urls.py 
        - views.py 
    - main/ 
        - migrations/
        - static/ 
            - main/ 
                - css/ 
                    - lightbox.css 
                    - style.css 
                - images/ 
                - js/ 
                    - html5shiv.js 
                    - jquery.pinto.js 
                    - jquery.pinto.min.js 
                    - lightbox.js 
                    - main.js 
                    - respond.min.js 
        - templates/
            - email/
                - activation_letter_body.txt
                - activation_letter_subject.txt
                - new_chat_message_body.txt
                - new_chat_message_subject.txt
                - new_comment_body.txt
                - new_comment_subject.txt
                - new_review_body.txt
                - new_review_subject.txt                
            - main/
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
        - templatetags/
            - `__init__.py`
            - custom_tags.py
        - `__init__.py`
        - admin.py
        - apps.py
        - forms.py
        - middlewares.py
        - models.py
        - tests.py
        - utilities.py
        - views.py
    - media/
        - thumbnails/ 
    - shabashka/
        - asgi.py
        - settings.py
        - urls.py
        - wsgi.py
    - db.sqlite3
    - manage.py
    - README.md
    - requirements.txt


