from common.funcoes.funcao import jwt_production
from flask_restful import Resource, reqparse, request
from common.funcoes import msg
from app import api
from common.SQL.sql_resource import find_base, put_base, delete_base, post_base
from api.usuario.usuario_model import UsuarioModel
from .cliente_model import ClienteModel



oModel = ClienteModel  #colocar aqui o Model utilizado.


tipo_id = "uuid"  #caso o tipo id seja Autoincrement, mude o tipo_id para outra string
atrib = reqparse.RequestParser()


if tipo_id == "uuid":
    atrib.add_argument("id", type=str, required=False)

# adicionar abaixo os argumentos da requisicao
atrib.add_argument("name", type=str, required=False, help=msg.campo_obrigatorio)
atrib.add_argument("created_at", required=False)
atrib.add_argument("updated_at", required=False)
atrib.add_argument("curadoria", type=str, required=False)
atrib.add_argument("curadoria_at", type=str, required=False)
atrib.add_argument("curadoria_id", type=str, required=False)
atrib.add_argument("cpf_cnpj", type=str, required=False)
atrib.add_argument("razao_social", type=str, required=False)
atrib.add_argument("inscricao_municipal", type=str, required=False)
atrib.add_argument("inscricao_estadual", type=str, required=False)
atrib.add_argument("tel_ddi", type=str, required=False)
atrib.add_argument("tel_ddd", type=str, required=False)
atrib.add_argument("tel_numero", type=str, required=False)
atrib.add_argument("end_cep", type=str, required=False)
atrib.add_argument("end_pais", type=str, required=False)
atrib.add_argument("end_estado", type=str, required=False)
atrib.add_argument("end_cidade", type=str, required=False)
atrib.add_argument("end_bairro", type=str, required=False)
atrib.add_argument("end_tipo_logradouro", type=str, required=False)
atrib.add_argument("end_logradouro", type=str, required=False)
atrib.add_argument("end_numero", type=str, required=False)
atrib.add_argument("end_complemento", type=str, required=False)


dados = []


class ClienteResource(Resource):
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
    
class ClienteShowAll(Resource):
    @jwt_production
    def get(self, parameter):
        print("osparameter", parameter)
        clientes = [administrador.json() for administrador in ClienteModel.find_cliente_all(parameter)]
        if clientes:
            return {"clientes": clientes}, 200
        else:
            return {"message": msg.reg_nao_encontrado}, 200

api.add_resource(
    ClienteResource, "/cliente/<string:id>", methods=["GET", "POST", "PATCH", "DELETE"]
)
api.add_resource(ClienteShowAll, "/cliente", methods=["GET"])
