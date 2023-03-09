from common.user.user_model import UserModel
from app import db_sql
import uuid
from passlib.hash import pbkdf2_sha256
from flask_validator import ValidateInteger, ValidateString, ValidateEmail, ValidateLength

class AdministradorsModel(UserModel):
    __tablename__ = "administradors"

    hash = db_sql.Column(db_sql.String(255))

    administrador_plano = db_sql.relationship("PlanoModel", primaryjoin="AdministradorsModel._od==PlanoModel.administrador_id")
    administrador_teste = db_sql.relationship("TesteModel", primaryjoin="AdministradorsModel._od==TesteModel.administrador_id")

    def __init__(
    self,
    _od,
    email,
    password,
    ativo,
    cpf,
    email_confirmado,
    chave_email_confirmado,
    name,
    sobrenome,
    tel_ddi,
    tel_ddd,
    tel_numero,
    created_at,
    updated_at,
    hash
    ):
        self._od = _od
        self.email = email
        self.password = password
        self.ativo = ativo
        self.cpf = cpf
        self.email_confirmado = email_confirmado
        self.chave_email_confirmado = chave_email_confirmado
        self.name = name
        self.sobrenome = sobrenome
        self.tel_ddi = tel_ddi
        self.tel_ddd = tel_ddd
        self.tel_numero = tel_numero
        self.created_at = created_at
        self.updated_at = updated_at
        self.hash = hash

    def json(self):
        return{
        "_od": self._od,
        "email": self.email,
        "ativo": self.ativo,
        "cpf": self.cpf,
        "email_confirmado": self.email_confirmado,
        "chave_email_confirmado": self.chave_email_confirmado,
        "name": self.name,
        "sobrenome": self.sobrenome,
        "tel_ddi": self.tel_ddi,
        "tel_ddd": self.tel_ddd,
        "tel_numero": self.tel_numero,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
        "hash": self.hash
        }

    @classmethod
    def __declare_last__(cls):
        ValidateLength(AdministradorsModel.password, max_length=255, min_length=8, throw_exception=True, message="A senha tem que ter 8 ou mais caracteres")
        ValidateLength(AdministradorsModel.cpf, max_length=11, min_length=11, throw_exception=True, message="CPF invalido")
        ValidateString(AdministradorsModel.name)
        ValidateString(AdministradorsModel.sobrenome)
        ValidateString(AdministradorsModel.tel_ddd)
        ValidateString(AdministradorsModel.tel_ddi)
        ValidateLength(AdministradorsModel.tel_numero, max_length=10, min_length=8, throw_exception=True, message="Telefone Invalido")
        ValidateEmail(AdministradorsModel.email, throw_exception=True, message="E-mail invalido")

    def gera_senha(self, email):
        if email:
            self.chave_email_confirmado = str(uuid.uuid4())
        else:
            self.password = pbkdf2_sha256.hash(self.password)

    def ver_senha(self, password, password_data):
        return pbkdf2_sha256.verify(password, password_data)

    @classmethod
    def find_administrador_chave_email_confirmado(cls, chave):
        administrador = cls.query.filter_by(chave_email_confirmado=chave).first()
        if administrador:
            return administrador
        else:
            return None

    @classmethod
    def administrador_email_confirmado(cls, _od):
        administrador = cls.query.filter_by(_od=_od).first()
        if administrador:
            if administrador.email_confirmado:
                return administrador.email_confirmado
            else:
                return None
        else:
            return None

    @classmethod
    def find_administrador(cls, _od):
        administrador = cls.query.filter_by(_od=_od).first()
        if administrador:
            return administrador
        else:
            return None

    @classmethod
    def find_administrador_all(cls, parameter):
        if parameter == "all":
            administrador = cls.query.all()
        else:
            administrador = cls.query.limit(parameter)
        if administrador:
            return administrador
        else:
            return None

    @classmethod
    def find_administrador_email(cls, email):
        administrador = cls.query.filter_by(email=email).first()
        if administrador:
            return administrador
        else:
            return None

#    @classmethod
#    def find_administrador_api_key(cls, api_key):
#        administrador = cls.query.filter_by(api_key=api_key).first()
#        if administrador:
#            return administrador
#        else:
#            return None

    def save_administrador(self):
        db_sql.session.add(self)
        db_sql.session.commit()

    def update_administrador(self, password, ativo, email_confirmado):
        if password:
            self.password = password
        if ativo:
            self.ativo = ativo
        if email_confirmado:
            self.email_confirmado = email_confirmado

    def delete_administrador(self):
        self.ativo = False
        AdministradorsModel.save_administrador(self)

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
