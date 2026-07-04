from dotenv import load_dotenv
import os
import loggers

from mysql.connector.pooling import MySQLConnectionPool

load_dotenv()

try:
    pool = MySQLConnectionPool(pool_size=5,
                           pool_name= 'agropanel',
                           host=os.getenv('DB_HOST'),
                           user=os.getenv('DB_USER'),
                           password=os.getenv('DB_PASSWORD'),
                           database=os.getenv('DB_DATABASE')
    )

except Exception as e:
    loggers.app_logger.critical(f'{e}')
    raise
