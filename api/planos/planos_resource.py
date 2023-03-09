from common.funcoes.funcao import jwt_production
from flask_restful import Resource, reqparse, request
from common.funcoes import msg
from app import api
from common.SQL.sql_resource import find_base, put_base, delete_base, post_base
from common.funcoes import msg, funcao

from .planos_model import PlanoModel


oModel = PlanoModel  # colocar aqui o Model utilizado.


tipo_id = "uuid"  # caso o tipo id seja Autoincrement, mude o tipo_id para outra string
atrib = reqparse.RequestParser()


if tipo_id == "uuid":
    atrib.add_argument("id", type=str, required=False)

# adicionar abaixo os argumentos da requisicao
atrib.add_argument("name", type=str, required=False, help=msg.campo_obrigatorio)
atrib.add_argument("created_at", required=False)
atrib.add_argument("updated_at", required=False)
#
atrib.add_argument("preco_plano", required=False)
atrib.add_argument("pagseguro", type=str, required=False)
atrib.add_argument("observacao", type=str, required=False)
atrib.add_argument("inativo_at", required=False)
atrib.add_argument("ativo", type=str, required=False, default="S")
atrib.add_argument("administrador_id", type=str, required=False)
atrib.add_argument("inativo_administrador_id", type=str, required=False)


class PlanoResource(Resource):
    @jwt_production
    def post(self, id):
        dados = atrib.parse_args()
        dados.ativo = "S"
        return post_base(self, oModel, dados, tipo_id)

    @jwt_production
    def delete(self, id):
        plan = PlanoModel.query.filter_by(id=id).first()
        if plan and plan.ativo=="S":
            plan.ativo = "N"
            plan.save_plano()
            return plan.json(), 200
        else:
            return {"message": msg.reg_nao_encontrado}, 200

    @jwt_production
    def get(self, id):
        return find_base(self, id, oModel, request)

    @jwt_production
    def patch(self, id):
        dados = atrib.parse_args()
        return put_base(self, id, oModel, dados)


api.add_resource(
    PlanoResource, "/plano/<string:id>", methods=["GET", "POST", "PATCH", "DELETE"]
)
