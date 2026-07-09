from dotenv import load_dotenv
import os
import loggers

from mysql.connector.pooling import MySQLConnectionPool

load_dotenv()

raiz = os.path.dirname(os.path.dirname(__file__))
caminho_ca = os.path.join(raiz, 'certs', os.getenv('CA_CERTIFICATE'))

# Configuração da conexão com DB
dbconfig = {
    'pool_name': 'commerce_manager',
    'pool_size': 5,
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_DATABASE'),
    'ssl_ca': caminho_ca,
    'ssl_verify_cert': True
}

# Verificar se está no render
if os.getenv('RENDER') and os.getenv('RENDER') == 'true':
    # Se não existir o arquivo, cria e preenche
    if not (os.path.isfile(caminho_ca)):
        os.makedirs(os.path.dirname(caminho_ca), exist_ok=True)
        with open(caminho_ca, 'w') as ca:
            ca.write(os.getenv('CA_CERTIFICATE_CONTENT'))

try:
    pool = MySQLConnectionPool(**dbconfig)

except Exception as e:
    loggers.app_logger.critical(f'{e}')
    raise
