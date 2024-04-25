from django.db import connection

def set_isolation_level(level):
    with connection.cursor() as cursor:
        cursor.execute(f'SET TRANSACTION ISOLATION LEVEL {level}')

