from api import database
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

            # Se não houver chave 'nome' nos dados, retorna 400
            if not 'nome' in produto:
                return jsonify({'message': 'Insira um nome válido para o produto'}), 400

            # Adiciona novo produto
            cursor.execute("insert into produtos values (null, %s)", (produto.get('nome'),))
            db.commit()
            return jsonify({'message': 'Produto cadastrado com sucesso!'})

        # Se o método for GET
        else:
            # Seleciona todos os produtos
            cursor.execute('select * from produtos')
            produtos = cursor.fetchall()
            lista_produtos = []

            # Adiciona dicionário para cada produto na lista
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
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método fot PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca o produto pelo ID
            cursor.execute("select * from produtos where id = %s", (product_id,))
            produto = cursor.fetchone()

            # Se não houver produto com esse id no banco, ou nçao houver a chave 'nome' nos dados, retorna erro 404 ou 400
            if not produto:
                return jsonify({'message': 'Produto não encontrado'}), 404
            if not 'nome' in data:
                return jsonify({'message': 'Insira um novo nome válido'}), 400

            # Atualiza 'nome' pelo id
            cursor.execute('update produtos set nome = %s where id = %s', (data['nome'], product_id))
            db.commit()
            return jsonify({'message': 'Produto atualizado com sucesso!'})

        # Se o método for DELETE
        elif request.method == 'DELETE':
            # Busca o produto pelo ID no banco
            cursor.execute("select * from produtos where id = %s", (product_id,))
            produto = cursor.fetchone()

            # Se não achar o produto, retorna 404
            if not produto:
                return jsonify({'message': 'Produto não encontrado'}), 404

            # Deleta o produto
            cursor.execute("delete from produtos where id = %s", (product_id,))
            db.commit()
            return jsonify({'message': 'Produto deletado com sucesso!'})

        # Se o método for GET
        else:
            # Busca o produto pelo id no banco
            cursor.execute("select * from produtos where id = %s", (product_id,))
            produto = cursor.fetchone()

            # Se não há produto com o id fornecido, retorna 404
            if not produto:
                return jsonify({'message': 'Produto não encontrado'}), 404

            return jsonify({'id': produto[0], 'nome': produto[1]})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()