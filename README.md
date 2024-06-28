
# Node Workflow API

API service for nodes management and workflow run, 
written on FastApi + SQLAlchemy.  
Workflows can be visualized using nx graphs.

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
from db import Base
from nodes.models import *
target_metadata = Base.metadata
```
Then type in your terminal:
```shell
alembic upgrade head
python -m uvicorn main:app
```

## Docker

Install Docker and run these commands:

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
Here is an example algorithm for building a workflow:  

![Diagram](src/images/short_diagram.drawio.png)  

Workflow starts. We receive an incoming message with a status.  
Status is checked using conditions.  
Then we receive a response message depending on the incoming message status.  
For example, if the incoming message status is `pending`, we'll get the following graph:  

![Diagram](src/images/workflow_graph_pending.png)  

### Create workflow

1. Add named workflows using `/workflows/` POST endpoint.
2. Create necessary nodes.  
* Indicate a workflow id and parent node ids for each node.  
* Note that `parent_condition_edge_id` is for response messages only.  
For example, if a response message is for Condition Node with `id 8` and edge `YES`,  
you should indicate this Condition Edge id.  
3.  Condition Edges are created automatically upon Condition Node create.  
You can see them in `/condition_edges/` GET endpoint.
4. Each workflow should begin with Start Node and finish with End Node.
5. You are allowed to create nodes with `null` id values, if it is more convenient for you to add nodes relationships later.
6. You can see workflows with all nodes created in `/workflows/` GET endpoints.  
To edit workflow content, just modify `workflow_id` in its nodes.

### Execute workflow

1. Use `/workflows/execute` POST endpoint.  
Choose if you want to draw graph, using dropdown menu.  
2. In `utils/graph.py`, you can set up graph options by following the comments there:  
you can choose different layout or choose to save a graph to your files.
3. If you would like to test workflow execution without creating it, you can load mock data.  
Type in the terminal: `load_mock_data.py mock_db.json` to test the above algorithm.  
Or type: `load_mock_data.py mock_db_long.json` to test the algorithm, shown below.  
If you prefer using SQLite, change URL to SQLITE_DATABASE_URL in `load_mock_data.py`.
4. You may notice that each time workflow runs, you get different incoming messages.  
This behavior is the result of using `random.choice`. It is intended to simulate status change in a network.  
You can delete it or substitute with your logic, if you want. To do it, follow comments in these files:  
`utils/building_blocks/handle_start_node.py` and `utils/building_blocks/handle_message_node.py`.  


Here is an example algorithm for building a longer workflow: 

![Diagram](src/images/long_diagram.drawio.png)  
  
Workflow construction process is almost the same.  
When you add incoming message node for the second round, you may indicate id for any parent response message node.  
Respective id will be placed automatically depending on you current workflow result.  
The resulting graph, when the first incoming message is `open` and the second one is `sent`, will be the following:  
  
![Diagram](src/images/workflow_graph_long_open_sent.png)  

## Instructions for running tests

`Tests` python package includes file `setup_test_db.py`. By default, it creates MariaDB testing database and loads mock data for testing.  
But if you prefer using SQLite, change URL to SQLITE_DATABASE_URL.   
To run tests, just type `pytest -vv`.


## Links

- DockerHub: https://hub.docker.com/repository/docker/anasu888/node-workflow-api/general
