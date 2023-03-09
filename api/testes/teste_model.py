from sqlalchemy_utils import ChoiceType
from app import db_sql
from common.SQL.sql_model import SqlModel
from common.SQL import sql_resource
from common.funcoes.enums import ESPECIE
from flask_validator import ValidateCurrency


class TesteModel(SqlModel):
    __tablename__ = "testes"
    especie = db_sql.Column(db_sql.String(20), nullable=False)
    material_amostra = db_sql.Column(db_sql.String(45), nullable=False)
    peso_link = db_sql.Column(db_sql.String(255), nullable=False)
    responsavel_tecnico = db_sql.Column(db_sql.String(50), nullable=True)
    observacao_interna = db_sql.Column(db_sql.String(500), nullable=True)
    observacao_exame = db_sql.Column(db_sql.String(500), nullable=True)
    preco = db_sql.Column(db_sql.Numeric(8,2), nullable=False)

    administrador_id = db_sql.Column(db_sql.String(36), db_sql.ForeignKey("administradors._od"))
    administrador = db_sql.relationship("AdministradorsModel", foreign_keys=[administrador_id])

    peso_administrador_id = db_sql.Column(db_sql.String(36), db_sql.ForeignKey("administradors._od"))
    peso_admin = db_sql.relationship("AdministradorsModel", foreign_keys=[peso_administrador_id])

    def __init__(
        self,
        id,
        name,
        created_at,
        updated_at,
        especie,
        material_amostra,
        peso_link,
        responsavel_tecnico,
        observacao_interna,
        observacao_exame,
        preco,
        administrador_id,
        peso_administrador_id

    ):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at
        self.especie = especie
        self.material_amostra = material_amostra
        self.peso_link = peso_link
        self.responsavel_tecnico = responsavel_tecnico
        self.observacao_interna = observacao_interna
        self.observacao_exame = observacao_exame
        self.preco = preco
        self.administrador_id = administrador_id
        self.peso_administrador_id = peso_administrador_id

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "especie": self.especie,
            "material_amostra": self.material_amostra,
            "peso_link": self.peso_link,
            "responsavel_tecnico": self.responsavel_tecnico,
            "observacao_interna": self.observacao_interna,
            "observacao_exame": self.observacao_exame,
            "preco": str(self.preco),
            "administrador_id": self.administrador_id,
            "peso_administrador_id": self.peso_administrador_id
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


def sendModel():
    return TesteModel
