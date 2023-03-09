import uuid
import os
import base64

from config import UPLOAD_FOLDER_IMAGE, UPLOAD_SERVER_IMAGE
from common.funcoes.funcao import jwt_production
from flask_restful import Resource, reqparse, request
from common.funcoes import msg
from app import api
from common.base.SQL.sql_resource import find_base

from common.base.SQL.sql_image_file_model import SqlImageFileModel

oModel = SqlImageFileModel  # colocar aqui o Model utilizado.

tipo_id = "uuid"  # caso o tipo id seja Autoincrement, mude o tipo_id para outra string
atrib = reqparse.RequestParser()
atrib_64 = reqparse.RequestParser()

if tipo_id == "uuid":
    atrib.add_argument("id", type=str, required=False)

# adicionar abaixo os argumentos da requisicao
atrib.add_argument("name", type=str, required=False)
atrib.add_argument("created_at", required=False)
atrib.add_argument("updated_at", required=False)

# atrib.add_argument('user_id', required=False)
atrib.add_argument("prefixo", required=True)
atrib.add_argument("extensao", type=str, required=False)
atrib.add_argument("folder", type=str, required=False)
atrib.add_argument("server", type=str, required=False)
atrib.add_argument("file_tipo", type=str, required=False)
atrib_64.add_argument("imagem_base64", type=str, required=False)


class SqlImageFileResource(Resource):
    @jwt_production
    def post(self, id):
        dados = atrib.parse_args()
        file = request.files.get("imagem_file")
        if file is not None:
            file_tipo = "file"
        elif file is None:
            file64 = atrib_64.parse_args()
            file = file64["imagem_base64"]
            file_tipo = "base64"
            oStart = file.find("data:image/") + len("data:image/")
            oEnd = file.find(";base64,")
            oEnd_2 = file.find(";base64,") + len(";base64,")
            base64_extensao = file[oStart:oEnd]
            base64_file = file[oEnd_2:]
        else:
            return {msg.msg: msg.arquivo_nao_enviado}, 207

        if dados["server"] is None:
            dados["server"] = UPLOAD_SERVER_IMAGE.strip()
        if dados["folder"] is None:
            dados["folder"] = UPLOAD_FOLDER_IMAGE.strip()
        dados["id"] = str(uuid.uuid4())
        if file_tipo == "file":
            dados["extensao"] = file.filename.split(".", 1)[1].lower()
        else:
            dados["extensao"] = base64_extensao
        dados["name"] = (
            dados["prefixo"] + "_" + dados["id"] + "_SQL" + "." + dados["extensao"]
        )
        dados["file_tipo"] = file_tipo
        save_path = dados["folder"]
        base = SqlImageFileModel(**dados)
        if file_tipo == "file":
            try:
                file.save(save_path + dados["name"])
            except Exception as e:
                return {"message2": e.args}, 207
        else:
            file_convertido = base64.b64decode(base64_file)
            handler = open(save_path + dados["name"], "wb+")
            try:
                handler.write(file_convertido)
                handler.close()
            except Exception as e:
                return {"message2": e.args}, 207
        try:
            result = base.save_image()
            return result.json(), 201
        except Exception as e:
            return {"message1": e.args}, 207

    @jwt_production
    def delete(self, id):
        if request.args:
            erase_file = request.args["erase_file"]
        else:
            erase_file = None
        msg_del = None
        result = SqlImageFileModel.find_id(id)
        if not result:
            return {msg.msg: msg.reg_nao_encontrado}, 200
        else:
            try:
                if erase_file == "sim":
                    diretorio = result.server + result.folder
                    diretorio_arquivos = os.listdir(diretorio)
                    if result.name in diretorio_arquivos:
                        caminho = os.path.join(diretorio, result.name)
                        try:
                            os.remove(caminho)
                            print(
                                f"Arquivo {result.name} apagado no banco de dados e no diretório"
                            )
                        except:
                            msg_del = msg.arquivo_del(
                                result.name, diretorio, "nao_apagado"
                            )
                    else:
                        msg_del = msg.arquivo_del(
                            result.name, diretorio, "nao_encontrado"
                        )
                result.delete_base()
                print("sql_image_file_resource 113", msg.reg_deletado)
                if msg_del == None:
                    msg_del = msg.reg_deletado
                return {msg.msg: msg_del}, 200
            except Exception as e:
                return {msg.msg: f"{e}"}, 207

    @jwt_production
    def get(self, id):
        return find_base(self, id, oModel, request)


api.add_resource(
    SqlImageFileResource, "/sqlimagefile/<string:id>", methods=["GET", "POST", "DELETE"]
)
