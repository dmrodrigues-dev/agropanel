import database
from datetime import date
import os
import secrets
from flask import Blueprint, jsonify, request

reset_bp = Blueprint('reset_bp', __name__)

@reset_bp.route('/api/seed/reset', methods=['POST'])
def resetar():
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Recuperar o registro mais recente do DB, na tabela vendas, e verificar se a data é a mesma de hj, se não for, executa o script reset_table.sql

        # Validar a chave secreta
        chave_fornecida = request.headers.get('Secret-token')
        if not chave_fornecida or not secrets.compare_digest(os.getenv('SEED_SECRET_TOKEN'), chave_fornecida):
            return jsonify({'message': 'Sem permissão para acessar a rota.'}), 401

        # Recupera a data do registro mais recente do Banco de dados
        cursor.execute("select dia from vendas order by dia desc limit 1")
        last_date = cursor.fetchone()
        today = date.today()

        # Verifica se a data recuperada é a mesma de hoje
        if ( not last_date or last_date[0] < today):
            # Abra o arquivo reset_table.sql e guarde o seu conteúdo
            path_seed = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'reset_table.sql')
            with open(path_seed, 'r') as seed:
                reset_seed = seed.read()

            # Execute os comandos do script e faça o commit do banco de dados
            reset_seed = reset_seed.split(';')
            for comando in reset_seed:
                if not comando:
                    continue
                cursor.execute(comando.strip())

            db.commit()

            return jsonify({'message': 'O Banco de dados foi atualizado.'})

        return jsonify({'message': 'O Banco de Dados está atualizado.'})

    finally:
        cursor.close()
        db.close()