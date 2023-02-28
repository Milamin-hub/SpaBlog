# Spablog

## Installation

- git clone https://github.com/Milamin-hub/SpaBlog.git

## Getting started 
- cd SpaBlog
- docker build
- docker-compose up
### OR 
- cd SpaBlog
- pip3 install -r requirements.txt
- python3 manage.py migrate
- python3 manage.py makemigrations
- python3 manage.py runserver


## Description
- The user can leave comments on posts and reply to comments
- User can post
- The user can register and log into his account
- All comments entered by the user are stored in a relational database (DB), including user data (data that will help identify the client).
- For each entry, you can write as many entries as you like (without cascading display).
- Comments can be sorted by the following fields: User Name,
E-mail, and date added (both in descending order and in reverse)
- Messages are divided into pages of 25 messages per page.
- The default sort is LIFO.
- The design is written with css
- The user can add a picture or a text file to the message.

## Used technologies
- Django
- Django ORM
- PostgreSQL
- JS, CSS, HTML
- Docker, docker-compose
- Git
