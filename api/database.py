from dotenv import load_dotenv
import os
import loggers

from mysql.connector.pooling import MySQLConnectionPool

load_dotenv()

raiz = os.path.dirname(os.path.dirname(__file__))

try:
    pool = MySQLConnectionPool(pool_size=5,
                           pool_name= 'agropanel',
                           host=os.getenv('DB_HOST'),
                           port=os.getenv('DB_PORT'),
                           user=os.getenv('DB_USER'),
                           password=os.getenv('DB_PASSWORD'),
                           database=os.getenv('DB_DATABASE'),
                           ssl_ca=os.path.join(raiz, 'certs', os.getenv('CA_CERTIFICATE')),
                           ssl_verify_cert=True
    )

except Exception as e:
    loggers.app_logger.critical(f'{e}')
    raise
