## Demo
To view the live demo of the project, you can visit [https://dda.rabindhamala.com.np](https://dda.rabindhamala.com.np)

superuser credentials:
- username: `admin`, password: `admin123`

student credentials: (currently readonly)
- username: `rabin`, password: `test123`
- username: `simran`, password: `test123`
- username: `rakesh`, password: `test123`
- username: `priyanka`, password: `test123`

## Design decisions

- Each student and instructor is also a user. So, there is one to one relationship between user and student/instructor.

- While creating a student or instructor, the user is created first and then the student/instructor is created with a foreign key to the user.

- For this, I have added an extra email field on the student and instructor form field. This creates their user instance.

- Also, I have decided to stick to function based views over class based views for simplicity. I just feel you don't need a whole class just to find the template name
  and render it. Also, I find the function based views much easier to read and everything is right there.

- I am also using just plain forms instead of ModelForms. Again, there is no magic underneath, obviously when we write the update view, the code is a bit verbose, but it's very readable.

- Currently both user and admin are using the same page including login. Ideally, user and admin having completely different pages is much better. 

## Todos
- [ ] Add more tests
- [ ] Make permissions more granular
- [ ] Extract the repeated UI style and javascript into a separate file
- [ ] For customer support forum, host a discourse server
- [ ] Generate documentation with mkdocs
- [ ] Custom error pages(404, 401, 403, 500) served by nginx


## To run the project locally
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/dev.txt
cp sample.env .env
```
**Run the migrations**

```bash
python manage.py migrate
```

**Create a superuser** 
```bash
DJANGO_SUPERUSER_USERNAME=superuser\
DJANGO_SUPERUSER_EMAIL=superuser@email.com \
DJANGO_SUPERUSER_PASSWORD=test123 \
python manage.py createsuperuser --noinput
```
** seed data **
To seed the database with some initial data, you can run the following command. 
This will create a few students and instructors with random data.

```bash
python seed_data.py
```
**Run the development server**

```bash
python manage.py runserver
```

## Docker

for docker, there are two profiles. One is `dev` and the other is `prod`. 
Specify the profile in the `.env` file with `COMPOSE_PROFILES=dev` or `COMPOSE_PROFILES=prod`.

To run the docker container, run the following command (just make sure, you set the env variables):

```bash
cp sample.env .env
docker compose up --build --detach
```

## Test
```
python manage.py test 
```
## Github hooks
- [X] Currently automated tests are run on every push to the `main`  and `dev` branch.
- [ ] Automated deployment to production on every push to the `main` branch.

## Deployment
Current setup is to push to remote repo and run docker container with nginx acting as reverse proxy
- [ ] Use github actions to automate deployment to production server
- [ ] Have dedicated documenation for server config, currently hosting on ec2 instance
