from api import database
from flask import Blueprint, jsonify, request

produtos_bp = Blueprint('produtos', __name__)


# Rota para adicionar produto e listar produtos (não precisa de id)
@produtos_bp.route('/api/produtos', methods=['POST', 'GET'])
def produtos():
    if request.method == 'POST':
        produto = request.json

        if not 'nome' in produto:
            return jsonify({'message': 'Insira um nome válido para o produto'}), 400

        database.cursor.execute("insert into produtos values (null, %s)", (produto.get('nome'),))
        database.db.commit()
        return jsonify({'message': 'Produto cadastrado com sucesso!'})


    else:
        database.cursor.execute('select * from produtos')
        produtos = database.cursor.fetchall()
        lista_produtos = []

        for produto in produtos:
            lista_produtos.append({
                'id': produto[0],
                'nome': produto[1]
            })

        return jsonify(lista_produtos)


# Rota para alterar, deletar ou buscar por ID (precisa de ID)
@produtos_bp.route('/api/produtos/<int:product_id>', methods=['PUT', 'DELETE', 'GET'])
def produto(product_id):
    if request.method == 'PUT':
        data = request.json
        database.cursor.execute("select * from produtos where id = %s", (product_id,))
        produto = database.cursor.fetchone()

        if not produto:
            return jsonify({'message': 'Produto não encontrado'}), 404
        if not 'nome' in data:
            return jsonify({'message': 'Insira um novo nome válido'}), 400

        database.cursor.execute('update produtos set nome = %s where id = %s', (data['nome'], product_id))
        database.db.commit()
        return jsonify({'message': 'Produto atualizado com sucesso!'})


    elif request.method == 'DELETE':
        database.cursor.execute("select * from produtos where id = %s", (product_id,))
        produto = database.cursor.fetchone()

        if not produto:
            return jsonify({'message': 'Produto não encontrado'}), 404

        database.cursor.execute("delete from produtos where id = %s", (product_id,))
        database.db.commit()
        return jsonify({'message': 'Produto deletado com sucesso!'})


    else:
        database.cursor.execute("select * from produtos where id = %s", (product_id,))
        produto = database.cursor.fetchone()

        if not produto:
            return jsonify({'message': 'Produto não encontrado'}), 404

        return jsonify({'id': produto[0], 'nome': produto[1]})
