from app import db_sql
from common.SQL.sql_model import SqlModel
from common.SQL import sql_resource
from sqlalchemy_utils import ChoiceType
from common.funcoes.enums import SIM_NAO
from flask_validator import ValidateCurrency


class PlanoModel(SqlModel):
    __tablename__ = "planos"


    preco_plano = db_sql.Column(db_sql.Numeric(8, 2), nullable=False, default=0)
    pagseguro = db_sql.Column(db_sql.String(36), nullable=False, unique=True)
    ativo = db_sql.Column(db_sql.String(1), ChoiceType(SIM_NAO), default="S")
    inativo_at = db_sql.Column(db_sql.DateTime, default=None, nullable=True)
    observacao = db_sql.Column(db_sql.Text(500))



    inativo_administrador_id = db_sql.Column(db_sql.String(36),db_sql.ForeignKey("administradors._od"))
    inativo = db_sql.relationship("AdministradorsModel", foreign_keys=[inativo_administrador_id])

    administrador_id = db_sql.Column(db_sql.String(36), db_sql.ForeignKey("administradors._od"))
    administrador = db_sql.relationship("AdministradorsModel", foreign_keys=[administrador_id])

    def __init__(
        self,
        id,
        name,
        created_at,
        updated_at,
        preco_plano,
        pagseguro,
        observacao,
        inativo_at,
        inativo_administrador_id,
        administrador_id,
        ativo
    ):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.preco_plano = preco_plano
        self.pagseguro = pagseguro
        self.observacao = observacao
        self.inativo_at = inativo_at
        self.inativo_administrador_id = inativo_administrador_id
        self.administrador_id = administrador_id
        self.ativo = ativo

    def json(self):
        if self.inativo_at is None:
            inativo_at = ""
        else:
            inativo_at = self.inativo_at.isoformat()
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "preco_plano": str(self.preco_plano),
            "pagseguro": self.pagseguro,
            "observacao": self.observacao,
            "ativo": self.ativo,
            "inativo_at": inativo_at,
            "inativo_administrador_id": self.inativo_administrador_id,
            "administrador": self.administrador.json()
        }

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


    def save_plano(self):
        db_sql.session.add(self)
        db_sql.session.commit()



def sendModel():
    return PlanoModel
