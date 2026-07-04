import logging
from dotenv import load_dotenv
import os

load_dotenv()

# Criando e configurando o handler do console
console = logging.StreamHandler()
console.setFormatter(logging.Formatter('[%(asctime)s] - %(levelname)s : %(name)s - %(message)s'))
console.setLevel(logging.DEBUG)

# Criando, configurando e adicionando o handler ao logger app_logger
app_logger = logging.getLogger('app_logger')
app_logger.setLevel(logging.DEBUG)
app_logger.addHandler(console)

# Se o programa não estiver rodando no Render, cria um handler para salvar logs em uma pasta logs
ambiente = os.getenv('RENDER')
if not ambiente:
    # Verifica a existência da pasta, e cria, se necessário
    dir_logs = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(dir_logs, exist_ok=True)

    # Cria, configura e adiciona o handler ao app_logger
    arquivo = logging.FileHandler(os.path.join(dir_logs, 'app_log.log'), 'a')
    arquivo.setFormatter(logging.Formatter('[%(asctime)s] - %(levelname)s : %(name)s - %(message)s'))
    arquivo.setLevel(logging.WARNING)
    app_logger.addHandler(arquivo)
