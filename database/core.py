import sqlalchemy
from sqlalchemy_utils import database_exists, create_database
from settings import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST

engine = sqlalchemy.create_engine(
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')


    

def create_database():
    if not database_exists(engine.url):
        create_database(engine.url)
    cursor = engine.connect()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username VARCHAR(255));")
    
    cursor.begin()
    cursor.close()


def drop_database():
    cursor = engine.connect()
    if database_exists(engine.url):
        cursor.execute(f"DROP DATABASE IF EXISTS {DB_NAME}")


def send_transaction(query):
    with engine.connect() as cursor:
        result = cursor.execute(query)
    cursor.close()
    return result