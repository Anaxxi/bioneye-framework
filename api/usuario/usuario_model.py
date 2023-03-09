from common.user.user_model import UserModel
from api.cliente.cliente_model import ClienteModel
from common.SQL import sql_model
from app import db_sql
from passlib.hash import pbkdf2_sha256
import uuid
from flask_validator import ValidateInteger, ValidateString, ValidateEmail, ValidateLength, ValidateRange

class UsuarioModel(UserModel):
    __tablename__ = 'usuarios'

    cliente_id = db_sql.Column(db_sql.String(36), db_sql.ForeignKey("clientes.id"), unique=False, nullable=True)
    cliente = db_sql.relationship("ClienteModel")

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
    cliente_id
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
        self.cliente_id = cliente_id


    def json(self):
        return{
        "_od": self._od,
        "email": self.email,
        "ativo": self.ativo,
        "cpf": self.cpf,
        "email_confirmado": self.email_confirmado,
        "ativo": self.ativo,
        "chave_email_confirmado": self.chave_email_confirmado,
        "name": self.name,
        "sobrenome": self.sobrenome,
        "tel_ddi": self.tel_ddi,
        "tel_ddd": self.tel_ddd,
        "tel_numero": self.tel_numero,
        "created_at": self.created_at.isoformat(),
        "updated_at": self.updated_at.isoformat(),
        "cliente": self.cliente.json()

        }
   

    @classmethod
    def __declare_last__(cls):
        ValidateLength(UsuarioModel.password, max_length=255, min_length=8, throw_exception=True, message="A senha tem que ter 8 ou mais caracteres")
        ValidateLength(UsuarioModel.cpf, max_length=11, min_length=11, throw_exception=True, message="CPF invalido")
        ValidateString(UsuarioModel.name)
        ValidateString(UsuarioModel.sobrenome)
        ValidateString(UsuarioModel.tel_ddd)
        ValidateString(UsuarioModel.tel_ddi)
        ValidateLength(UsuarioModel.tel_numero, max_length=10, min_length=8, throw_exception=True, message="Telefone Invalido")
        ValidateEmail(UsuarioModel.email, throw_exception=True, message="E-mail invalido")


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

    def update_user(self, password, ativo, email_confirmado):
        if password:
            self.password = password
        if email_confirmado:
            self.email_confirmado = email_confirmado
        if ativo:
            self.ativo = ativo


    def delete_user(self):
        self.ativo = "N"
        UsuarioModel.save_user(self)

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
