from blueprints import produtos, compras, vendas
from flask import Flask

app = Flask(__name__)

app.register_blueprint(produtos.produtos_bp)
app.register_blueprint(compras.compras_bp)
app.register_blueprint(vendas.vendas_bp)

if __name__ == "__main__":
    app.run(debug=True)