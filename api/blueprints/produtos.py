import database
import utils
from flask import Blueprint, jsonify, request

produtos_bp = Blueprint('produtos', __name__)


# Rota para adicionar produto e listar produtos (não precisa de id)
@produtos_bp.route('/api/produtos', methods=['POST', 'GET'])
def produtos():
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método for POST
        if request.method == 'POST':
            # Recebe os dados
            produto = request.json

            # Valida se o campo nome foi preenchido
            utils.is_request_ok(produto, ['nome',])

            # Adiciona novo produto
            cursor.execute("insert into produtos values (null, %s)", (produto.get('nome'),))
            db.commit()
            return jsonify({'message': 'Produto cadastrado com sucesso!'})

        # Se o método for GET
        else:
            # Seleciona todos os produtos
            produtos = utils.get_all_or_abort(cursor, 'produtos')
            lista_produtos = []

            # Adiciona dicionário para cada produto na lista
            for produto in produtos:
                lista_produtos.append({
                    'id': produto[0],
                    'nome': produto[1]
                })

            return jsonify(lista_produtos)

    finally:
        cursor.close()
        db.close()


# Rota para alterar, deletar ou buscar por ID (precisa de ID)
@produtos_bp.route('/api/produtos/<int:product_id>', methods=['PUT', 'DELETE', 'GET'])
def produto(product_id):
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método fot PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca o produto pelo ID
            utils.get_line_or_abort(cursor, 'produtos', product_id)

            # Valida se a alteração é no nome
            utils.is_request_ok(data, ['nome',])

            # Atualiza 'nome' pelo id
            cursor.execute('update produtos set nome = %s where id = %s', (data['nome'], product_id))
            db.commit()
            return jsonify({'message': 'Produto atualizado com sucesso!'})

        # Se o método for DELETE
        elif request.method == 'DELETE':
            # Busca o produto pelo ID no banco
            utils.get_line_or_abort(cursor, 'produtos', product_id)

            # Deleta o produto
            cursor.execute("delete from produtos where id = %s", (product_id,))
            db.commit()
            return jsonify({'message': 'Produto deletado com sucesso!'})

        # Se o método for GET
        else:
            # Busca o produto pelo id no banco
            produto = utils.get_line_or_abort(cursor, 'produtos', product_id)

            return jsonify({'id': produto[0], 'nome': produto[1]})

    finally:
        cursor.close()
        db.close()