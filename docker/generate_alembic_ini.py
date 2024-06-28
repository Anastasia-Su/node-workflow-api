import os
from dotenv import load_dotenv
from configparser import ConfigParser


load_dotenv()

config = ConfigParser()
config.read("alembic.ini")


database_url = os.getenv("MARIADB_DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL environment variable is not set")

config.set("alembic", "sqlalchemy.url", database_url)


with open("../alembic.ini", "w") as configfile:
    config.write(configfile)

print("alembic.ini file has been updated with the DATABASE_URL")
