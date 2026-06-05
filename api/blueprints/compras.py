from api import database
from flask import Blueprint, jsonify, request

compras_bp = Blueprint('compras_bp', __name__)

chaves_compras = ('dia', 'produto_id', 'preco', 'qtd', 'fornecedor')

# Rota para adicionar compra ou listar compras
@compras_bp.route('/api/compras', methods=['GET', 'POST'])
def compras():
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        if request.method == 'GET':
            dias = request.args.get('dias')

            if not dias:
                cursor.execute("select * from compras")
            else:
                cursor.execute("select * from compras where dia >= curdate() - interval %s day", (int(dias),))

            compras = cursor.fetchall()
            lista_compras = []

            for compra in compras:
                lista_compras.append({
                    'id': compra[0],
                    'dia': compra[1],
                    'produto_id': compra[2],
                    'preco': compra[3],
                    'qtd': compra[4],
                    'fornecedor': compra[5]
                })

            return jsonify(lista_compras)


        else:
            registro = request.json

            for chave in chaves_compras:
                if chave not in registro:
                    return jsonify({'message': 'Todos os campos obrigatórios devem ser preenchidos'}), 400

            cursor.execute("insert into compras values (null, %s, %s, %s, %s, %s)",
                                    (registro.get('dia'),
                                     registro.get('produto_id'),
                                     registro.get('preco'),
                                     registro.get('qtd'),
                                     registro.get('fornecedor')))
            db.commit()
            return jsonify({'message': 'Registro cadastrado com sucesso!'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()


# Rota para alterar compra ou deletar compra
@compras_bp.route('/api/compras/<int:compra_id>', methods=['PUT', 'DELETE'])
def compra(compra_id):
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        if request.method == 'PUT':
            data = request.json
            cursor.execute("select * from compras where id = %s", (compra_id,))
            compra = cursor.fetchone()

            if not data:
                return jsonify({'message': 'Nenhum dado enviado'}), 400
            if not compra:
                return jsonify({'message': 'Compra não encontrado'}), 404
            for campo in data:
                if campo not in chaves_compras:
                    return jsonify({'message': 'Campo inválido inserido'}), 400

            campos_update = ', '.join([f"{campo} = %s" for campo in data.keys()])
            valores = list(data.values())
            valores.append(compra_id)

            cursor.execute(f'update compras set {campos_update} where id = %s', tuple(valores))
            db.commit()
            return jsonify({'message': 'Compra atualizada com sucesso!'})

        else:
            cursor.execute("select * from compras where id = %s", (compra_id,))
            compra = cursor.fetchone()

            if not compra:
                return jsonify({'message': 'Compra não encontrada'}), 404

            cursor.execute("delete from compras where id = %s", (compra_id,))
            db.commit()
            return jsonify({'message': 'Compra deletada com sucesso!'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()