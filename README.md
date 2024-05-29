
# Node Workflow API

API service for nodes management and workflow run, 
written on FastApi + SQLAlchemy.

## Installing / Getting started

Install MariaDB and create db. You can use MySQL Client: `CREATE DATABASE db_name;`

```shell
git clone https://github.com/Anastasia-Su/node-workflow-api.git
cd node-workflow-api
python -m venv venv
venv\Scripts\activate (on Windows)
source venv/bin/activate (on macOS)
pip install -r requirements.txt
```
Create `.env` file and set it according to `.env.sample`:

```shell
set MARIADB_DATABASE=<db name you created>
set MARIADB_USER=<your username, usually it is "root">
set MARIADB_ROOT_PASSWORD=<your root password>
set MYSQL_HOST=<db host: "localhost" for your machine and "db" for Docker>

set MARIADB_DATABASE_URL=<i.e. mysql+pymysql://root:${MARIADB_ROOT_PASSWORD}@${MYSQL_HOST}/${MARIADB_DATABASE}>
set MARIADB_TESTING_URL=<db URL to run tests: i.e. mysql+pymysql://root:${MARIADB_ROOT_PASSWORD}@localhost/test>

set SQLITE_DATABASE_URL=<If you prefer SQLite: sqlite:///./your_db_name.db>


alembic init alembic
alembic revision --autogenerate -m "initial_migration"
```

Then open alembic.ini and set `sqlalchemy.url` to your db url.
Open env.py in `alembic` folder. Add there these lines, if not present:
```shell
from database import Base
from nodes.models import *
target_metadata = Base.metadata
```
Then type in your terminal:
```shell
alembic upgrade head
python -m uvicorn main:app
```

## Docker

Docker should be installed.

```shell
docker-compose build
docker-compose up
```

## Features

* Documentation: `/docs/`
* CRUD for nodes: Start, Message, Condition, End
* CRUD for workflows
* Filter options for nodes
* Create workflows using nodes
* Run selected workflow
* Display or save nx diagrams for workflows



## Instructions for API
![Diagram](images/short_diagram.drawio.png)  
![Diagram](images/long_diagram.drawio.png)

## Instructions for running tests

`Tests` python package includes file `setup_test_db.py`. By default, it creates MariaDB testing database and loads mock data for testing.  
But if you prefer using SQLite, change URL to SQLITE_DATABASE_URL.   
To run tests, just type `pytest -vv`


## Links

- DockerHub: 
