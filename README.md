[![Build Status](https://travis-ci.org/henryyang42/NTHU_Course.svg?branch=master)](https://travis-ci.org/henryyang42/NTHU_Course)
# NTHU Course

A system that fetch the course data and provide service that is instinctive, easy to use.


# Getting Started


## Install dependency

- python
    - version: >= 3.5

- tesseract
    - version: >= 3.03
    - mac: `brew install tesseract --devel # Without --devel, it will install tesseract 3.02`
    - ubuntu: `sudo apt install tesseract-ocr`
    - arch linux: `sudo pacman -S tesseract tesseract-data-eng`

- mariadb
    - version: >= 10.0.27
    - mac: `brew install mariadb`
    - ubuntu: `sudo apt install mariadb-server`
    - arch linux: `sudo pacman -S mariadb`


## Install and Setup Virtualenv (optional)

We highly recommend developers to setup environment with **virtualenv**.

You can install this package by typing `pip install virtualenv` in your console.


## Basic Settings for Database

By default, the system will find a configuration file in `NTHU_Course/mysql.ini`.

So you need to create it and put your settings in this file. The following
 script is the example for `mysql.ini`.

```ini
[client]
database = <database name>
user = <mysql username>
password = <mysql password>
host = <mysql server ip>
port = <mysql server port>
default-character-set = utf8
```


## Build the System.

Typing the commands below may help you build this system.

```bash
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py crawl_course
$ python manage.py update_index
```

To clear all contents in db, use ``python manage.py crawl_course clear``

To update all syllabus, use ``python manage.py update_syllabus``


## Launch

```bash
$ python manager.py collectstatic
$ python manager.py runserver --insecure
```



# Heroku settings
To use it in heroku, you have to set the following environment variables

```bash
TESSDATA_PREFIX=/app/.apt/usr/share/tesseract-ocr/tessdata
BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git
DJANGO_SETTINGS_MODULE=NTHU_Course.settings.heroku
SECRET_KEY=hard-to-guess-string
```

this can be achieved by ``heroku config:set`` or the web panel
