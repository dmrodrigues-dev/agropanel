from api import database
from flask import Blueprint, jsonify, request

vendas_bp = Blueprint('vendas', __name__)

chaves_vendas = ('dia', 'produto_id', 'preco', 'qtd') # Ultimo campo, "comprador" é opcional

# Rota para adicionar venda ou listar vendas
@vendas_bp.route('/api/vendas', methods=['GET', 'POST'])
def vendas():
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        if request.method == 'GET':
            dias = request.args.get('dias')

            if not dias:
                cursor.execute("select * from vendas")
            else:
                cursor.execute("select * from vendas where dia >= curdate() - interval %s day", (int(dias),))

            vendas = cursor.fetchall()
            lista_vendas = []

            for venda in vendas:
                lista_vendas.append({
                    'id': venda[0],
                    'dia': venda[1],
                    'produto_id': venda[2],
                    'preco': venda[3],
                    'qtd': venda[4],
                    'comprador': venda[5]
                })

            return jsonify(lista_vendas)


        else:
            registro = request.json

            for chave in chaves_vendas:
                if chave not in registro:
                    return jsonify({'message': 'Todos os campos obrigatórios devem ser preenchidos'}), 400

            cursor.execute("insert into vendas values (null, %s, %s, %s, %s, %s)",
                                    (registro.get('dia'),
                                     registro.get('produto_id'),
                                     registro.get('preco'),
                                     registro.get('qtd'),
                                     registro.get('comprador', '')))
            db.commit()
            return jsonify({'message': 'Venda cadastrado com sucesso!'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()


# Rota para alterar venda ou deletar vendas
@vendas_bp.route('/api/vendas/<int:venda_id>', methods=['PUT', 'DELETE'])
def venda(venda_id):
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        if request.method == 'PUT':
            data = request.json
            cursor.execute("select * from vendas where id = %s", (venda_id,))
            venda = cursor.fetchone()

            if not data:
                return jsonify({'message': 'Nenhum dado enviado'}), 400
            if not venda:
                return jsonify({'message': 'Venda não encontrada'}), 404
            for campo in data:
                if campo not in chaves_vendas and campo != 'comprador':
                    return jsonify({'message': 'Campo inválido inserido'}), 400

            campos_update = ', '.join([f"{campo} = %s" for campo in data.keys()])
            valores = list(data.values())
            valores.append(venda_id)

            cursor.execute(f'update vendas set {campos_update} where id = %s', tuple(valores))
            db.commit()
            return jsonify({'message': 'Venda atualizada com sucesso!'})


        else:
            cursor.execute("select * from vendas where id = %s", (venda_id,))
            venda = cursor.fetchone()

            if not venda:
                return jsonify({'message': 'Venda não encontrado'}), 404

            cursor.execute("delete from vendas where id = %s", (venda_id,))
            db.commit()
            return jsonify({'message': 'Venda deletada com sucesso!'})

    except Exception as e:
        return jsonify({'message': str(e)}), 500

    finally:
        cursor.close()
        db.close()