from app import db_sql
from sqlalchemy_utils import ChoiceType
from common.SQL.sql_model import SqlModel
from common.SQL import sql_resource
from common.funcoes.enums import SIM_NAO

from flask_validator import ValidateLength

class ClienteModel(SqlModel):
    __tablename__ = "clientes"

    curadoria = db_sql.Column(db_sql.String(1), ChoiceType(SIM_NAO), nullable=False, default="N")
    curadoria_at = db_sql.Column(db_sql.DateTime)
    curadoria_id = db_sql.Column(db_sql.String(36))
    razao_social = db_sql.Column(db_sql.String(100), nullable=False)
    cpf_cnpj = db_sql.Column(db_sql.String(13), nullable=False, unique=True)
    inscricao_municipal = db_sql.Column(db_sql.String(45))
    inscricao_estadual = db_sql.Column(db_sql.String(45))
    tel_ddi = db_sql.Column(db_sql.String(3))
    tel_ddd = db_sql.Column(db_sql.String(3))
    tel_numero = db_sql.Column(db_sql.String(11), nullable=True)
    end_cep = db_sql.Column(db_sql.String(8))
    end_pais = db_sql.Column(db_sql.String(20), nullable=False)
    end_estado = db_sql.Column(db_sql.String(2))
    end_cidade = db_sql.Column(db_sql.String(30))
    end_bairro = db_sql.Column(db_sql.String(20))
    end_tipo_logradouro = db_sql.Column(db_sql.String(10))
    end_logradouro = db_sql.Column(db_sql.String(30))
    end_numero = db_sql.Column(db_sql.String(10))
    end_complemento = db_sql.Column(db_sql.String(30))


    usuario = db_sql.relationship("UsuarioModel", backref="clientes")


    def __init__(
        self,
        id,
        name,
        created_at,
        updated_at,
        curadoria,
        curadoria_at,
        curadoria_id,
        razao_social,
        cpf_cnpj,
        inscricao_municipal,
        inscricao_estadual,
        tel_ddi,
        tel_ddd,
        tel_numero,
        end_cep,
        end_pais,
        end_estado,
        end_cidade,
        end_bairro,
        end_tipo_logradouro,
        end_logradouro,
        end_numero,
        end_complemento
    ):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.curadoria = curadoria
        self.curadoria_at = curadoria_at
        self.curadoria_id = curadoria_id
        self.razao_social = razao_social
        self.cpf_cnpj = cpf_cnpj
        self.inscricao_municipal = inscricao_municipal
        self.inscricao_estadual = inscricao_estadual
        self.tel_ddi = tel_ddi
        self.tel_ddd = tel_ddd
        self.tel_numero = tel_numero
        self.end_cep = end_cep
        self.end_pais = end_pais
        self.end_estado = end_estado
        self.end_cidade = end_cidade
        self.end_bairro = end_bairro
        self.end_tipo_logradouro = end_tipo_logradouro
        self.end_logradouro = end_logradouro
        self.end_numero = end_numero
        self.end_complemento = end_complemento


    @classmethod
    def __declare_last__(cls):
        ValidateLength(UsuarioModel.cpf, max_length=11, min_length=11, throw_exception=True, message="CPF invalido")
        ValidateLength(UsuarioModel.tel_numero, max_length=10, min_length=8, throw_exception=True, message="Telefone Invalido")

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "curadoria": self.curadoria,
            "cpf_cnpj": self.cpf_cnpj,
            "razao_social": self.razao_social,
            "inscricao_municipal": self.inscricao_municipal,
            "inscricao_estadual": self.inscricao_estadual,
            "tel_ddi": self.tel_ddi,
            "tel_ddd": self.tel_ddd,
            "tel_numero": self.tel_numero,
            "end_cep": self.end_cep,
            "end_pais": self.end_pais,
            "end_estado": self.end_estado,
            "end_cidade": self.end_cidade,
            "end_bairro": self.end_bairro,
            "end_tipo_logradouro": self.end_tipo_logradouro,
            "end_logradouro": self.end_logradouro,
            "end_numero": self.end_numero,
            "end_complemento": self.end_complemento,
            }

    @classmethod
    def find_cliente_all(cls, parameter):
        if parameter == "all":
            cliente = cls.query.all()

        if cliente:
            return cliente
        else:
            return None
    @classmethod
    def __declare_last__(cls):
        ValidateLength(ClienteModel.tel_numero, max_length=10, min_length=8, throw_exception=True, message="Telefone Invalido")


    @classmethod
    def find_like(cls, chave, valor_chave, page, per_page, order_by):
        return sql_resource.base_find_like(
            cls, chave, valor_chave, page, per_page, order_by, sendModel()
        )

    @classmethod
    def find_intervalo(
        cls, chave, valor_inicial, valor_final, page, per_page, order_by
    ):
        return sql_resource.base_find_intervalo(
            cls,
            chave,
            valor_inicial,
            valor_final,
            page,
            per_page,
            order_by,
            sendModel(),
        )

    @classmethod
    def find_multiple(
        cls, chaves, condicionais, valores, dataFinal, page, per_page, order_by
    ):
        return sql_resource.base_find_multiple(
            cls,
            chaves,
            condicionais,
            valores,
            dataFinal,
            page,
            per_page,
            order_by,
            sendModel(),
        )

    def update_base(self, **dados):
        sql_resource.base_update_dados(self, **dados)


def sendModel():
    return ClienteModel
