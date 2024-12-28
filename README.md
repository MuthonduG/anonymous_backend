# anonymous_backend

#### Get app ####
1. Clone https://github.com/MuthonduG/anonymous_backend.git
2. create .env and add smtp credentials
3. Start app using either:
    - docker decompose up
    - docker decompose up --build

# Apps 

#### User App ####
Defines user logic including:
1. User registration
2. User login
3. Email confirmation feature
4. User anonymous id creation
5. 

#### Reports ####


# docker commands

#### To start app ####

Run either of the commands:
    *** docker decompose up ***
    *** docker decompose up --build ***

#### Incase of issues with migrations ####
1. First decompose down. This can be either done for volumes or containers
    - docker decompose down
    - docker decompose down --volumes

2. Directly make migrations and yhe migrate
    - docker exec -it djangoapp python manage.py makemigrations
    - docker exec -it djangoapp python manage.py migrate

3. Finally, decompose up with either of the below:
    - docker decompose up
    - docker decompose up --build


#### Incase of errors with database ####

1. First decompose down. This can be either done for volumes or containers
    - docker decompose down
    - docker decompose down --volumes

2. Activate your container without actually having to use actively:
    - docker compose up -d db

3. Access psql shell:
    - docker exec -it db psql -U postgres

4. Drop and recreate the database:
    - \c template1
    - DROP DATABASE postgres WITH (FORCE);
    CREATE DATABASE postgres;

5. Finally decompose up to activate containers with either of the commands below:
    - docker decompose up
    - docker decompose up --build



