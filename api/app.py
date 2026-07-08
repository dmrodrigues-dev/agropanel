from blueprints import produtos, estatisticas, compras, vendas, reset_route
import loggers
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# errorhandlers para centralizar respostas e chamar app_logger para erros 400, 404 e 500
@app.errorhandler(400)
def bad_request(e):
    loggers.app_logger.warning(f'{e.description}')
    return jsonify({'erro': f'{e.description}'}), 400

@app.errorhandler(404)
def not_found(e):
    loggers.app_logger.info(f'{e.description}')
    return jsonify({'erro': f'{e.description}'}), 404

@app.errorhandler(500)
def internal_error(e):
    # Log duplicado intencionalmente, o Flask loga qualquer exceção não tratada
    # Escolhi manter ambos os logs, o nativo do Flask como rede de segurança, e este com formatação própria, nivel customizado e persistencia em arquivo local
    loggers.app_logger.error(f'{e.original_exception}', exc_info=e.original_exception)
    return jsonify({'erro': f'{e.description}'}), 500

app.register_blueprint(produtos.produtos_bp)
app.register_blueprint(estatisticas.estatisticas_bp)
app.register_blueprint(compras.compras_bp)
app.register_blueprint(vendas.vendas_bp)
app.register_blueprint(reset_route.reset_bp)

if __name__ == "__main__":
    app.run(debug=(loggers.ambiente is None))