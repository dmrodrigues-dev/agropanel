from api import database
from flask import Blueprint, jsonify, request

produtos_bp = Blueprint('produtos', __name__)


# Rota para adicionar produto e listar produtos (não precisa de id)
@produtos_bp.route('/api/produtos', methods=['POST', 'GET'])
def produtos():
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        if request.method == 'POST':
            produto = request.json

            if not 'nome' in produto:
                return jsonify({'message': 'Insira um nome válido para o produto'}), 400

            cursor.execute("insert into produtos values (null, %s)", (produto.get('nome'),))
            db.commit()
            return jsonify({'message': 'Produto cadastrado com sucesso!'})


        else:
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
            lista_produtos = []

            for produto in produtos:
                lista_produtos.append({
                    'id': produto[0],
                    'nome': produto[1]
                })

            return jsonify(lista_produtos)

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()


# Rota para alterar, deletar ou buscar por ID (precisa de ID)
@produtos_bp.route('/api/produtos/<int:product_id>', methods=['PUT', 'DELETE', 'GET'])
def produto(product_id):
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        if request.method == 'PUT':
            data = request.json
            cursor.execute("select * from produtos where id = %s", (product_id,))
            produto = cursor.fetchone()

            if not produto:
                return jsonify({'message': 'Produto não encontrado'}), 404
            if not 'nome' in data:
                return jsonify({'message': 'Insira um novo nome válido'}), 400

            cursor.execute('update produtos set nome = %s where id = %s', (data['nome'], product_id))
            db.commit()
            return jsonify({'message': 'Produto atualizado com sucesso!'})


        elif request.method == 'DELETE':
            cursor.execute("select * from produtos where id = %s", (product_id,))
            produto = cursor.fetchone()

            if not produto:
                return jsonify({'message': 'Produto não encontrado'}), 404

            cursor.execute("delete from produtos where id = %s", (product_id,))
            db.commit()
            return jsonify({'message': 'Produto deletado com sucesso!'})


        else:
            cursor.execute("select * from produtos where id = %s", (product_id,))
            produto = cursor.fetchone()

            if not produto:
                return jsonify({'message': 'Produto não encontrado'}), 404

            return jsonify({'id': produto[0], 'nome': produto[1]})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()