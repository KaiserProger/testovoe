HOW TO RUN IT:
    1. cd to /docker folder from here(cd docker)
    2. docker-compose up
CONFIG:
    Yeah, there's config at ./domain/config/config.json
    It contains several options(tbh, only one, two others are secret key
    and temp account UUID).
    Main option is verify_on_register, which enables verification when
    you're creating new user by email.
    NOTE: IF YOU WANNA RUN TESTS, DISABLE THIS OPTION!!!
Architecture notes:
    So, main part of my work came for getting with async SQLAlchemy and
    thinking about internal architecture,
    and it was hard at first, so I had really little time for FastAPI-endpoints.
    There's not so much validators, and sometimes you can pass wrong
    values in endpoints, and you're sending token in querys instead
    of headers(I know this is bad), and something else...
    CrudBase initially was my idea, cause I wanted to share same logic
    between different CRUD types, but later I'll create interface
    instead of CrudBase logic with different implementations.
Another one note:
    If you wish to run app local(at your PC),
    change all db name entries(at ./main.py, ./alembic.ini and
    domain/internal_tests/conftest.py) from "db" to "localhost".
    Also create user "postgres" with password "postgres" and db "maindb".
    Good luck!