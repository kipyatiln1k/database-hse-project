import sqlalchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from settings import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST
from database.functions import FUNCTIONS_AND_PROCEDURES

engine = sqlalchemy.create_engine(
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')


def _create_database():
    if not database_exists(engine.url):
        create_database(engine.url)
    
    print(send_queries(
        FUNCTIONS_AND_PROCEDURES['create_database'],
        'CALL create_tables();'
    ))
    print(send_query("INSERT INTO city(city_name) VALUES ('New York');"))
    print(send_query('SELECT * FROM city;').fetchall())
    print(send_query('SELECT all_cities();').fetchone()[0])
    

def _drop_database():
    if database_exists(engine.url):
        drop_database(engine.url)


def send_queries(*queries):
    result = []
    with engine.connect() as cursor:
        for query in queries:
            result.append(cursor.execute(query))
        cursor.begin().commit()
    
    return result


def send_query(query):
    with engine.connect() as cursor:
        result = cursor.execute(query)
        cursor.begin().commit()
    
    return result