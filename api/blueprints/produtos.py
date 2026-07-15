import database
import utils
from flask import Blueprint, jsonify, request, abort
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

            # Se receber uma string vazia no preco_de_venda, aborta com erro 400
            if str(produto.get('preco_de_venda')).strip() == '':
                abort(400, 'O preço não pode estar vazio.')

            # Valida se o campo nome foi preenchido
            utils.is_request_ok(produto, ['nome', 'preco_de_venda'], ['nome', 'preco_de_venda'])

            # Valida se o preco_de_venda é positivo
            utils.is_request_non_negative(produto)

            # Adiciona novo produto
            conn.execute(text("insert into produtos(nome, preco_de_venda) values (:nome, :preco_de_venda)"),
                         {'nome':produto.get('nome'),
                          'preco_de_venda':produto.get('preco_de_venda')})
            conn.commit()
            return jsonify({'message': 'Produto cadastrado com sucesso!'})

        # Se o método for GET
        else:
            # Seleciona todos os produtos
            produtos = utils.get_all_or_abort(conn, 'produtos')

            # Retorna uma lsta de dicionários para cada item retornado
            return jsonify([utils.type_casted_dict(dict(row._mapping)) for row in produtos])


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

            # Se receber uma string vazia no preco_de_venda, aborta com erro 400
            if str(data.get('preco_de_venda')).strip() == '':
                abort(400, 'O preço não pode estar vazio.')

            # Valida se a alteração é no nome
            utils.is_request_ok(data, ['nome','preco_de_venda'])

            # Valida se tem preco_de_venda positivo
            utils.is_request_non_negative(data)

            # Criar string com todos os campos, seguidos por "= :campo" separados por ","
            campos_update = ', '.join([f"{campo} = :{campo}" for campo in data.keys()])
            # Adicionar o item 'id' ao dicionário 'data'
            data['id'] = product_id

            conn.execute(text(f'update produtos set {campos_update} where id = :id'),
                         data)

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
            return jsonify(utils.type_casted_dict(dict(produto._mapping)))
