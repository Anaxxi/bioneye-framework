from app import db_sql
from common.base.SQL.sql_model import SqlModel
from common.base.SQL import sql_resource


class SqlImageFileModelAbstract(SqlModel):
    __abstract__ = True

    # criar abaixo os campos da tabela
    prefixo = db_sql.Column(db_sql.String(10), nullable=False)
    extensao = db_sql.Column(db_sql.String(10), nullable=False)
    folder = db_sql.Column(db_sql.String(100), nullable=False)
    server = db_sql.Column(db_sql.String(100), nullable=False)
    file_tipo = db_sql.Column(db_sql.String(6), nullable=True)
    # user_id = db_sql.Column(db_sql.String(36), nullable=False)

    def __init__(
        self,
        id,
        name,
        created_at,
        updated_at,
        prefixo,
        extensao,
        folder,
        server,
        file_tipo,
    ):
        self.id = id
        self.name = name.strip()
        self.created_at = created_at
        self.updated_at = updated_at
        # self.user_id = user_id
        self.prefixo = prefixo.strip()
        self.extensao = extensao
        self.folder = folder
        self.server = server
        self.file_tipo = file_tipo

    def json(self):
        return {
            "id": self.id,
            "name": self.name.strip(),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            # colocar abaixo os campos desse modelo
            # "user_id": self.user_id,
            "prefixo": self.prefixo.strip(),
            "extensao": self.extensao.strip(),
            "folder": self.folder.strip(),
            "server": self.server.strip(),
            "file_tipo": self.file_tipo,
            "url": self.server + self.folder + self.name,
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

    def save_image(self):
        db_sql.session.add(self)
        db_sql.session.commit()
        return self

    def update_base(self, **dados):
        sql_resource.base_update_dados(self, **dados)


def sendModel():
    return SqlImageFileModelAbstract
