# NTHU Course
A system that fetch the course data and provide service that is insinctive, easy to use.

Typing the commands below may help you build this system.
```
pip install -r requirement.txt
python manage.py syncdb
python manage.py makemigrations
python manage.py migrate
python manage.py crawl_course
python manage.py rebuild_index
```
To clear all contents in db, use ``python manage.py crawl_course clear``
