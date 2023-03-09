from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS, cross_origin
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from common.security.blacklist import BLACKLIST
from common.funcoes import msg
from flask_mongoengine import MongoEngine
import config

app = Flask(__name__, static_folder="_IMAGES")
app.debug = config.DEBUG
app.config.from_object("config")
db_sql = SQLAlchemy(app)
db_sql_connection = config.SQL_ENGINE.connect()
db_mng = MongoEngine(app)
ma = Marshmallow(app)
migrate = Migrate(app, db_sql)
jwt = JWTManager(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}}, support_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"

api = Api(app)


@jwt.token_in_blacklist_loader
def verifica_blacklist(token):
    print("blacklist", BLACKLIST)
    return token["jti"] in BLACKLIST


@jwt.revoked_token_loader
def token_de_acesso_invalidado():
    return jsonify({"message": msg.usuario_deslogado}), 401


@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello, Lifepix is here!</h1>"


@app.route("/images/<path:path>")
def serve_image(path):
    return send_from_directory("_IMAGES", path)


if app.debug == False:
    if __name__ == "__main__":
        app.run(host="0.0.0.0")
else:
    if __name__ == "__main__":
        app.run(host="0.0.0.0")


#importar modelos e resources aqui


from api.usuario import usuario_model, usuario_resource
from api.administradors import administradors_resource, administradors_model

from api.cliente import cliente_model, cliente_resource
from api.planos import planos_model, planos_resource
from api.testes import teste_model, teste_resource
