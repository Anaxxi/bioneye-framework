from app import db_sql
from sqlalchemy import text


class SqlModel(db_sql.Model):
    __abstract__ = True

    id = db_sql.Column(db_sql.String(36), primary_key=True, nullable=False)
    name = db_sql.Column(db_sql.String(100), nullable=True)
    created_at = db_sql.Column(db_sql.DateTime, default=db_sql.func.now())
    updated_at = db_sql.Column(
        db_sql.DateTime, default=db_sql.func.now(), onupdate=db_sql.func.now()
    )

    def __init__(self, name, created_at, updated_at):
        self.name = name
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self):
        return f"{type(self).__class__.__name__}: Nome: {self.name}"

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def find_id(cls, id):
        base = cls.query.filter_by(id=id).first()
        return base

    @classmethod
    def find_like(cls, chave, valor_chave, page, per_page, order_by):
        pass
        # implementado na classe model final

    @classmethod
    def find_multiple(
        cls, chaves, condicionais, valores, dataFinal, page, per_page, order_by
    ):
        pass

    # implementado na classe model final

    @classmethod
    def find_all(cls, parameter, page, per_page, order_by):
        if parameter == "all":
            bases = cls.query.order_by(text(order_by))
            if per_page:
                bases = bases.paginate(page, per_page, False)
            else:
                bases = bases.all()
        else:  # limit não tem como utilizar paginação pois ela tem que entrar depois da paginaçao,
            # se for o caso use all e pagine até onde precisar
            bases = cls.query.order_by(text(order_by)).limit(parameter)
        return bases

    def save_base(self):
        db_sql.session.add(self)
        db_sql.session.commit()
        return self

    def aupdate_base(self, name):
        self.name = name
        return self

    def delete_base(self):
        db_sql.session.delete(self)
        db_sql.session.commit()
