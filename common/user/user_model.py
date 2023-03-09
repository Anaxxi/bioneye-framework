import uuid
from app import db_sql
from passlib.hash import pbkdf2_sha256
from ..funcoes.enums import TIPO_USER_GRUPO_ENUM
from sqlalchemy_utils import ChoiceType
from flask_restful import request, url_for
from ..funcoes import msg, funcao
from sqlalchemy_utils import ChoiceType
from common.funcoes.enums import SIM_NAO


class UserModel(db_sql.Model):
    __abstract__ = True

    _od = db_sql.Column(db_sql.String(36), primary_key=True, nullable=False)
    created_at = db_sql.Column(db_sql.DateTime, default=db_sql.func.now())
    updated_at = db_sql.Column(
        db_sql.DateTime, default=db_sql.func.now(), onupdate=db_sql.func.now()
    )


    email = db_sql.Column(db_sql.String(100), nullable=False, unique=True)
    password = db_sql.Column(db_sql.String(255), nullable=False)
    cpf = db_sql.Column(db_sql.String(11), nullable=False, unique=False)
    api_key = db_sql.Column(db_sql.String(36), nullable=True, unique=True)
    ativo = db_sql.Column(db_sql.String(1), ChoiceType(SIM_NAO), default="S")
    email_confirmado = db_sql.Column(db_sql.String(1), ChoiceType(SIM_NAO), default="N")
    chave_email_confirmado = db_sql.Column(db_sql.String(255), nullable=False)
    name = db_sql.Column(db_sql.String(30), nullable=False)
    sobrenome = db_sql.Column(db_sql.String(50), nullable=False)
    tel_ddi = db_sql.Column(db_sql.String(3), nullable=False, default="55")
    tel_ddd = db_sql.Column(db_sql.String(3), nullable=False)
    tel_numero = db_sql.Column(db_sql.String(10), nullable=False)

    def __init__(
        self,
        _od,
        email,
        password,
        cpf,
        ativo,
        email_confirmado,
        chave_email_confirmado,
        created_at,
        updated_at,
        name,
        sobrenome,
        tel_ddi,
        tel_ddd,
        tel_numero,
    ):
        self._od = _od
        self.email = email
        self.password = password
        self.cpf = cpf
        self.ativo = ativo
        self.email_confirmado = email_confirmado
        self.chave_email_confirmado = chave_email_confirmado
        self.created_at = created_at
        self.updated_at = updated_at
        self.name = name
        self.sobrenome = sobrenome
        self.tel_ddi = tel_ddi
        self.tel_ddd = tel_ddd
        self.tel_numero = tel_numero


    def json(self):
        return {
            "_od": self._od,
            "email": self.email,
            "cpf": self.cpf,
            "ativo": self.ativo,
            "email_confirmado": self.email_confirmado,
            "chave_email_confirmado": self.chave_email_confirmado,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "name": self.name,
            "sobrenome": self.sobrenome,
            "tel_ddi": self.tel_ddi,
            "tel_ddd": self.tel_ddd,
            "tel_numero": self.tel_numero
        }

    def gera_senha(self, email):
        if email:
            self.chave_email_confirmado = str(uuid.uuid4())
        else:
            self.password = pbkdf2_sha256.hash(self.password)

    def ver_senha(self, password, password_data):
        return pbkdf2_sha256.verify(password, password_data)

    @classmethod
    def find_user_chave_email_confirmado(cls, chave):
        user = cls.query.filter_by(chave_email_confirmado=chave).first()
        if user:
            return user
        else:
            return None

    @classmethod
    def user_email_confirmado(cls, _od):
        user = cls.query.filter_by(_od=_od).first()
        if user:
            if user.email_confirmado:
                return user.email_confirmado
            else:
                return None
        else:
            return None

    @classmethod
    def find_user(cls, _od):
        user = cls.query.filter_by(_od=_od).first()
        if user:
            return user
        else:
            return None

    @classmethod
    def find_user_all(cls, parameter):
        if parameter == "all":
            users = cls.query.all()
        else:
            users = cls.query.limit(parameter)
        if users:
            return users
        else:
            return None

    @classmethod
    def find_user_email(UserModel, email):
        user = UserModel.query.filter_by(email=email).first()
        if user:
            return user
        else:
            return None

#    @classmethod
#    def find_user_api_key(cls, api_key):
#        user = cls.query.filter_by(api_key=api_key).first()
#        if user:
#            return user
#        else:
#            return None

    def save_user(self):
        db_sql.session.add(self)
        db_sql.session.commit()

    def update_user(self, password, is_admin, ativo, tipo_user, email_confirmado):
        if password:
            self.password = password
        if email_confirmado:
            self.email_confirmado = email_confirmado

    def delete_user(self):
        self.ativo = False
        UserModel.save_user(self)

    def send_confirmation_email(self):
        resource_url = "userconfirm"
        subject = msg.email_confirmado_subject
        email_sender = None
        link = request.url_root[:-1] + url_for(
            resource_url, _od=self.chave_email_confirmado
        )
        texto_email = msg.confirme_seu_cadastro + f"{link}"
        html_email = f'<html><p>{msg.confirme_seu_cadastro} <a href="{link}">CONFIRMAR EMAIL</a></p></html>'
        return funcao.send_email_mailgun(
            subject, self.email, email_sender, texto_email, html_email
        )
