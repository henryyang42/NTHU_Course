# NTHU Course
A system that fetch the course data and provide service that is insinctive, easy to use.

Typing the commands below may help you build this system.
```
pip install -r requirement.txt
python manage.py syncdb
python manage.py makemigrations
python manage.py migrate
python manage.py crawl_course tnpa7e61l4a3c5vrf2kvacaof6 956
```
Note that ``tnpa7e61l4a3c5vrf2kvacaof6 956`` will vary each day.
Please get a new pair of the token from [this site](https://www.ccxp.nthu.edu.tw/ccxp/INQUIRE/JH/6/6.2/6.2.9/JH629001.php).
