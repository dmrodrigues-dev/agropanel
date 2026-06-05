from api import database
from flask import Blueprint, jsonify, request

produtos_bp = Blueprint('produtos', __name__)

# Rota para adicionar produtos
@produtos_bp.route('/api/produtos/add', methods=['POST'])
def add_produto():
    produto = request.json

    if not 'nome' in produto:
        return jsonify({'message': 'Insira um nome válido para o produto'}), 400

    database.cursor.execute("insert into produtos values (null, %s)", (produto.get('nome'),))
    database.db.commit()
    return jsonify({'message': 'Produto cadastrado com sucesso!'})


# Rota para alterar o nome de algum produto
@produtos_bp.route('/api/produtos/update/<int:product_id>', methods=['PUT'])
def update_produto(product_id):
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


# Rota para deletar produto
@produtos_bp.route('/api/produtos/delete/<int:product_id>', methods=['DELETE'])
def del_produto(product_id):
    database.cursor.execute("select * from produtos where id = %s", (product_id,))
    produto = database.cursor.fetchone()

    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404

    database.cursor.execute("delete from produtos where id = %s", (product_id,))
    database.db.commit()
    return jsonify({'message': 'Produto deletado com sucesso!'})


# Rota para listar produtos cadastrados
@produtos_bp.route('/api/produtos', methods=['GET'])
def ver_produtos():
    database.cursor.execute('select * from produtos')
    produtos = database.cursor.fetchall()
    lista_produtos = []

    for produto in produtos:
        lista_produtos.append({
            'id': produto[0],
            'nome': produto[1]
        })

    return jsonify(lista_produtos)


# Rota para buscar produto pelo id
@produtos_bp.route('/api/produtos/<int:product_id>', methods=['GET'])
def buscar_produto(product_id):
    database.cursor.execute("select * from produtos where id = %s", (product_id,))
    produto = database.cursor.fetchone()

    if not produto:
        return jsonify({'message': 'Produto não encontrado'}), 404

    return jsonify({'id': produto[0], 'nome': produto[1]})