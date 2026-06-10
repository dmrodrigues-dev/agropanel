from api import database
from flask import Blueprint, jsonify, request

compras_bp = Blueprint('compras_bp', __name__)

chaves_obrigatorias = ('dia', 'produto_id', 'preco', 'qtd', 'fornecedor')

# Rota para adicionar compra ou listar compras
@compras_bp.route('/api/compras', methods=['GET', 'POST'])
def compras():
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método for GET
        if request.method == 'GET':
            # Quantos dias verá, se for 0, retorna todos os registros
            dias = request.args.get('dias')

            if not dias:
                cursor.execute("select * from compras")
            else:
                cursor.execute("select * from compras where dia >= curdate() - interval %s day", (int(dias),))

            compras = cursor.fetchall()
            lista_compras = []

            # Adiciona dicionários na lista
            for compra in compras:
                lista_compras.append({
                    'id': compra[0],
                    'dia': compra[1],
                    'produto_id': compra[2],
                    'preco': compra[3],
                    'qtd': compra[4],
                    'fornecedor': compra[5]
                })

            return jsonify(lista_compras) # Lista de registros de compras

        # Se o método for POST
        else:
            # Recebe os dados enviados
            registro = request.json

            # Se alguma chave da lista de obrigatórias não estiver no request, retorna erro 400
            for chave in chaves_obrigatorias:
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
        # Se houver algum erro, retorna o erro e internal server error
        return jsonify({'message': str(e)}), 500

    finally:
        # Fecha o cursor e a conexão com o banco
        cursor.close()
        db.close()


# Rota para alterar compra ou deletar compra
@compras_bp.route('/api/compras/<int:compra_id>', methods=['PUT', 'GET', 'DELETE'])
def compra(compra_id):
    # Conecta no DB e cria um cursor
    db = database.pool.get_connection()
    cursor = db.cursor()

    try:
        # Se o método for PUT
        if request.method == 'PUT':
            # Recebe os dados
            data = request.json

            # Busca a linha na tabela pelo id
            cursor.execute("select * from compras where id = %s", (compra_id,))
            compra = cursor.fetchone()

            # Se não houver dados enviados, linha com o id recebido ou algum campo dos dados que não esteja na lista de chaves obrigatórias
            if not data:
                return jsonify({'message': 'Nenhum dado enviado'}), 400
            if not compra:
                return jsonify({'message': 'Compra não encontrada'}), 404
            for campo in data:
                if campo not in chaves_obrigatorias:
                    return jsonify({'message': 'Campo inválido inserido'}), 400

            # Criar string com todos os campos, seguidos por "= %s" separados por ","
            campos_update = ', '.join([f"{campo} = %s" for campo in data.keys()])
            # Cria lista com os valores enviados
            valores = list(data.values())
            # Adiciona o id no final da lista de valores, pois será usado para fazer a seleção da linha
            valores.append(compra_id)

            cursor.execute(f'update compras set {campos_update} where id = %s', tuple(valores))
            db.commit()
            return jsonify({'message': 'Compra atualizada com sucesso!'})

        # Se o método for GET
        elif request.method == 'GET':
            # Busca a linha pelo ID
            cursor.execute('select * from compras where id = %s', (compra_id,))
            compra = cursor.fetchone()

            # Se não achar a linha com esse id, retorna 404
            if not compra:
                return jsonify({'message': 'Compra não encontrada'}), 404
            
            return jsonify({
                'id': compra[0],
                'dia': compra[1],
                'produto_id': compra[2],
                'preco': compra[3],
                'qtd': compra[4],
                'fornecedor': compra[5]
            })

        # Se o método for DELETE
        else:
            # Busca a linha na tabela pelo ID
            cursor.execute("select * from compras where id = %s", (compra_id,))
            compra = cursor.fetchone()

            # Se não achar a linha, retorna erro 404
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