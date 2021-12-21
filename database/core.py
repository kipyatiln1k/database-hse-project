import sqlalchemy
from sqlalchemy_utils import database_exists, create_database, drop_database
from settings import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST
from database.functions import FUNCTIONS_AND_PROCEDURES

engine = sqlalchemy.create_engine(
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')


def _create_database():
    if not database_exists(engine.url):
        create_database(engine.url)
        send_query(FUNCTIONS_AND_PROCEDURES['create_database'])
        send_query(FUNCTIONS_AND_PROCEDURES['create_functions'])
        send_query(FUNCTIONS_AND_PROCEDURES['create_tables'])
    

def _drop_database():
    if database_exists(engine.url):
        drop_database(engine.url)


# def send_queries(*queries):
#     result = []
#     with engine.connect() as cursor:
#         for query in queries:
#             result.append(cursor.execute(query))
#         cursor.begin().commit()
    
#     return result


def send_query(query):
    with engine.connect() as cursor:
        result = cursor.execute(sqlalchemy.text(query))
        cursor.begin().commit()
    
    return result