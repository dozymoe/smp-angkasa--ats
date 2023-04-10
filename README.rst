-----------------------------
Middle School Website Project
-----------------------------

Quickstart
----------

1. Create symlink etc/runner.json from etc/runner-development.json
   See https://github.com/dozymoe/fireh_runner

2. Create PostgreSQL database according to etc/development/web/database.json

3. Create entries in /etc/hosts according to etc/development/web/server.json

4. Run ./run setup

5. Run ./run django-manage migrate

6. Run ./run django-manage collectstatic --no-input


They are not comprehensive instructions, just enough to get started if you had
background knowledge in Django (Python Web Framework).

There are two routing configurations, the first entry in ALLOWED_HOSTS will
receive **web.urls_admin**, the staff management website.
