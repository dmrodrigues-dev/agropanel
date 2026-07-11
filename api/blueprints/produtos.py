import database
import utils
from flask import Blueprint, jsonify, request
from sqlalchemy import text

produtos_bp = Blueprint('produtos', __name__)


# Rota para adicionar produto e listar produtos (não precisa de id)
@produtos_bp.route('/api/produtos', methods=['POST', 'GET'])
def produtos():
    # Com uma conexão da engine feita, execute o bloco
    with database.engine.connect() as conn:

        # Se o método for POST
        if request.method == 'POST':
            # Recebe os dados
            produto = request.json

            # Valida se o campo nome foi preenchido
            utils.is_request_ok(produto, ['nome',])

            # Adiciona novo produto
            conn.execute(text("insert into produtos(nome) values (:nome)"),
                         {'nome':produto.get('nome')})
            conn.commit()
            return jsonify({'message': 'Produto cadastrado com sucesso!'})

        # Se o método for GET
        else:
            # Seleciona todos os produtos
            produtos = utils.get_all_or_abort(conn, 'produtos')

            # Retorna uma lsta de dicionários para cada item retornado
            return jsonify([dict(row._mapping) for row in produtos])


# Rota para alterar, deletar ou buscar por ID (precisa de ID)
@produtos_bp.route('/api/produtos/<int:product_id>', methods=['PUT', 'DELETE', 'GET'])
def produto(product_id):
    # Com uma conexão da engine feita, execute o bloco
    with database.engine.connect() as conn:

        # Se o método fot PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca o produto pelo ID
            utils.get_line_or_abort(conn, 'produtos', product_id)

            # Valida se a alteração é no nome
            utils.is_request_ok(data, ['nome',])

            # Atualiza 'nome' pelo id
            conn.execute(text('update produtos set nome = :nome where id = :id'),
                         {'nome': data['nome'], 'id': product_id})
            conn.commit()
            return jsonify({'message': 'Produto atualizado com sucesso!'})

        # Se o método for DELETE
        elif request.method == 'DELETE':
            # Busca o produto pelo ID no banco
            utils.get_line_or_abort(conn, 'produtos', product_id)

            # Deleta o produto
            conn.execute(text("delete from produtos where id = :id"),
                         {'id': product_id})
            conn.commit()
            return jsonify({'message': 'Produto deletado com sucesso!'})

        # Se o método for GET
        else:
            # Busca o produto pelo id no banco
            produto = utils.get_line_or_abort(conn, 'produtos', product_id)
            return jsonify(dict(produto._mapping))
