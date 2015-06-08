[![Build Status](https://travis-ci.org/henryyang42/NTHU_Course.svg?branch=master)](https://travis-ci.org/henryyang42/NTHU_Course)
# NTHU Course

[![Join the chat at https://gitter.im/henryyang42/NTHU_Course](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/henryyang42/NTHU_Course?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
A system that fetch the course data and provide service that is insinctive, easy to use.

Typing the commands below may help you build this system.
```
pip install -r requirements.txt
python manage.py syncdb
python manage.py makemigrations
python manage.py migrate
python manage.py crawl_course
python manage.py update_index
```

For auto decaptcha feature, it requires ``tesseract 3.03``

To clear all contents in db, use ``python manage.py crawl_course clear``

To update all syllabus, use ``python manage.py update_syllabus``

