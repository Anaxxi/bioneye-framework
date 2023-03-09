from common.funcoes.funcao import jwt_production
from flask_restful import Resource, reqparse, request
from common.funcoes import msg
from app import api
from common.SQL.sql_resource import find_base, put_base, delete_base, post_base

from .teste_model import TesteModel


oModel = TesteModel

tipo_id = "uuid"
atrib = reqparse.RequestParser()


if tipo_id == "uuid":
    atrib.add_argument("id", type=str, required=False)

# adicionar abaixo os argumentos da requisicao
atrib.add_argument("name", type=str, required=False, help=msg.campo_obrigatorio)
atrib.add_argument("created_at", required=False)
atrib.add_argument("updated_at", required=False)
#
atrib.add_argument("especie", required=False)
atrib.add_argument("material_amostra", type=str, required=False)
atrib.add_argument("peso_link", required=False)
atrib.add_argument("responsavel_tecnico", required=False)
atrib.add_argument("observacao_interna", required=False)
atrib.add_argument("observacao_exame", required=False)
atrib.add_argument("preco", required=False)
atrib.add_argument("administrador_id", required=False)
atrib.add_argument("peso_administrador_id", required=False)


class TesteResource(Resource):
    @jwt_production
    def post(self, id):
        dados = atrib.parse_args()
        return post_base(self, oModel, dados, tipo_id)

    @jwt_production
    def delete(self, id):
        return delete_base(self, id, oModel)

    @jwt_production
    def get(self, id):
        return find_base(self, id, oModel, request)

    @jwt_production
    def patch(self, id):
        dados = atrib.parse_args()
        return put_base(self, id, oModel, dados)


api.add_resource(
    TesteResource, "/teste/<string:id>", methods=["GET", "POST", "PATCH", "DELETE"]
)
