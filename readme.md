## Design decisions

- Each student and instructor is also a user. So, there is one to one relationship between user and student/instructor.

- While creating a student or instructor, the user is created first and then the student/instructor is created with a foreign key to the user.

- For this, I have added an extra email field on the student and instructor form field. This creates their user instance.

- Also, I have decided to stick to function based views over class based views for simplicity. I just feel you don't need a whole class just to find the template name
  and render it. Also, I find the function based views much easier to read and everything is right there.

- I am also using just plain forms instead of ModelForms. Again, there is no magic underneath, obviously when we write the update view, the code is a bit verbose, but it's very readable.

- Currently both user and admin are using the same page including login. Ideally, user and admin having completely different pages is much better. 

## superuser
```python
DJANGO_SUPERUSER_USERNAME=admin \
DJANGO_SUPERUSER_EMAIL=admin@email.com \
DJANGO_SUPERUSER_PASSWORD=test123 \
python manage.py createsuperuser --noinput
```

## seed permissions

## Docker

for docker, there are two profiles. One is `dev` and the other is `prod`. Specify the profile in the `.env` file with `COMPOSE_PROFILES=dev` or `COMPOSE_PROFILES=prod`.

To run the docker container, run the following command:

```bash
docker compose up --build --detach
```

## test
```
python manage.py test 
```
