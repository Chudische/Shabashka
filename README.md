# Shabashka

## Idea

We often need to do certain work in which we may not be very competent. For example:
home repair, electronics or car repair, computer setup, landscape design.

Perhaps we need to do something not difficult, but time-consuming, and we don't have a time.
For example: cleaning, walking pets, caring for the elderly, etc.

Or we don't have the necessary equipment. For example: tow truck services, delivery of large cargo, dry cleaning, well drilling, welding ...

Of course, there are various large and small companies that are ready to provide all the necessary services. But they are not in every city and their services can cost much more than the services of a private person. On the other hand, there are many people competent in different spheres of life who would like to earn a little extra money and are ready to help us with our problems.
But where to find them? And how do you know how authoritative they are? This project aims to address these tasks.

Shabashka is the service for people to find some extra job on the one hand, and it’s a service for a people who have some work to be done on the other hand. Basically  Shabashka is an online extra job marketplace that provides a means for worker and employer. Additionaly, let’s take a look at an example:
- Someone (an employer) needs to remodel his or her bathroom
- He/she creates a new offer, provides title, description, expected price, photo, etc.
- Workers are responding  for this offer, providing their price, time needed to perform this job and comments
- The employer chooses the worker he/she likes more
- Now worker and employer can discuss the deal in detail in the chat 
- Worker does his or her job
- The employer closes his or her offer and leaves a review for worker
- Everyone is happy



## Installation

- Install project dependencies by running `pip install -r requirements.txt`. Requirements contain:
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
-  For the project to be more secure I had used Python-dotenv module. So all data that I do not want to share I put into enrivoment variable. Create file `.env` near the `manage.py`. This file should contain enviroment variables, such as:
    - SECRET - Django secret key 
    - GMAIL_HOST_USER - mail username for smtp messages 
    - GMAIL_HOST_PASSWORD - mail password 
    - DJANGO_DATABASE - in settings.py there are 3 options of this variable (network, remote, local)
        - network is default. It's  an actual database settings on the server
        - remote is development settings from my PC to remote database
        - local is sqlite settings for local testing 
    - DB_NAME - name of the database for PostgreSQL backend 
    - DB_USER - user of the database for PostgreSQL backend 
    - DB_PASSWORD - password of the database for PostgreSQL backend
    - DB_IP - ip address of the database for PostgreSQL backend

## Email settings 

Shabashka uses smtp.gmail.com for sending emails. Make sure you allow django to send emails through gmail by turning on "Access for less secure apps" in your google account. Shabashka sends such notifications:
- `send_activation_notification()` - after registration a user receives an activation letter;
- `send_comment_notification()` - after worker posts a comment to an offer, offer author gets an email;
- `send_chat_message_notification()` - after a user posts a message in a chat, receiver gets an email;
- `send_review_notification()` - after the offer is closed, an employer makes a review to the worker, the worker gets an email.

## Project description

### Authentication and authorization

ShaUser model is inherited from AbstractUser class with some additional fields:
- is_activated - for a user to confirm his or her email address
- send_message - if a user want to receive emails from Shabashka
- location - the place where user is live (optional, in the future I want to populate my project for all cities in my country)
- average_rating - calculating when user is gets a review 
- favorite - m2m field for following to employers

Authentication system has the following functionality:
- Register user
- Login user
- Logout user


It is also possible to recover the user password with an email address. It is done with inheritance of such classes:
- PasswordResetView;
- PasswordResetDoneView;
- PasswordResetConfirmView;
- PasswordResetCompleteView

### Profile

After registration user goes to his or her profile page. Profile has the following functionality:
- Change user profile data (first name, last name, location, etc.);
- Change user password;
- Change avatar (by default a user sees only avatar placeholder);
- Delete profile (when a user delete his or her profile, their offers and all pictures will be deleted to using django-cleanup module);
- See user rating;
- See user reviews

On user profile page there are all of his offers with different statuses.

If user goes to the other user profile page, he or she will see only his or her active offers in status "New". Also they can follow this user by clicking "follow" link. 

Additionally an authenticated user in account dropdown(in navbar) can click on to the message list page, where he can see all of his conversations grouped by offers. After clicking on a message he or she is taken to the offer chat. 

### Categories

Categories are devided into two parts:
- Super Category
- Sub Category

They are all in one table of database. But you can create an offer only in the sub category. Super category is made only for a good looking(just for now) 


### Main page 

On the main page there are all offers in active status . A user can:
- click on every offer to get to the offer detail page;
- click on the category to get to the "by_category" page which shows every offer in this particular category
- click on the user name in every offer to go to the user profile page

Each offer on the main page, the category page or the profile page has the following:
- category
- data and time (when an offer was created)
- title (no more than 64 characters)
- description (short version of decription which is limited by `limit_text()` function from `custom_tags.py`)
- number of views
- number of comments
- number of followers (and if user follows offer author it marks by red color)
- number of shares
- price 
- offer author

On every page that has an offers there is a bootstrap pagination for speed up page loading and more appealing look of the page

Search and pagination functionalities are provided by `shabashka_context_processor()` from `main.middlewares` module
The keyword search done through titles and descriptions of the offers.

### Offer detail page 

On the offer detail page in addition to offer look in main page or category page a user sees the following:
- main photo 
- additional photos (if exist)
- comments 
- comment form (for authenticated users)

### Offer life cycle

- at first user creates a new offer in `Create` tab in the Navbar;
- an offer is created with status `new` and `is_active`;
- other users respond to the offer by leaving their comments, offering their price and time needed to complete the job;
- when an offer author accepts one of responds:
    - all the other responds `is_active` change to `False`(they aren't shown on the offer page)
    - offer status change to `accepted`
- the offer author sees the following buttons: `cancel`, `chat`, `done`:
    - `cancel`:
        - all the other responds `is_active` are changed to `True`
        - the offer status is changed to `new`
    - `chat` - opens chat between the offer author and a responder
    - `done`:
        - the offer author is redirected to the review form
        - the employer writes a review to the worker
        - offer status changed to `done` 
        - `is_active` changed to `False`        
- for a responder there is only a `chat` button
- after an offer is closed an employer can delete it in his or her profile page


## Admin interface

Admin interface makes possible to manage any Shabashka data within the main application interface. The admin interface has the following elements:
- Users and groups
- Users avatars
- Super Categories
- Sub Categories
- Offers
- Comments
- Chat messages
- Users reviews

Additionaly Users admin interface provides filters:
- user activated 
- user didn't activate account for more than 3 days
- user didn't activate account for more than a week

Using these filters and action `send activation notification` admin can send an activation letter to users.

## API

Get first 30 offers:
    `/api/offers`

Get offer details:
    `/api/offers/pk` 
    (where __pk__ is offer id)

Get or post offer comments:
    `/api/offers/pk/comments`
    (where __pk__ is offer id; User can post comment only if authenticated)


##  TODO list
- Migrate to Django 4
- Authentication via social media
- Location via google maps
- Search by locations
- Adding photos via Drag and drop
