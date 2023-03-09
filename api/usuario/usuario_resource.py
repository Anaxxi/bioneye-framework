import traceback
import uuid
from flask import request, make_response, jsonify, render_template, flash, config
from flask_cors import cross_origin
from flask_restful import Resource, reqparse, url_for


from api.usuario.usuario_model import UsuarioModel
import flask_jwt_extended
from flask_jwt_extended import (
    create_access_token,
    get_raw_jwt,
    create_refresh_token,
    jwt_required,
)

from common.funcoes.funcao import jwt_production
from common.security.blacklist import BLACKLIST
from common.funcoes import msg, funcao

from app import api, jwt
from datetime import timedelta

from config import PASSWORD_TOKEN_EXPIRE, MAILGUN_EMAIL_SENDER, APP_NAME, DEBUG
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, InputRequired

atrib = reqparse.RequestParser()
atrib.add_argument("_od", type=str, required=False)
atrib.add_argument("email", type=str, required=True, help=msg.email_obrigatorio)
atrib.add_argument("password", type=str, required=True, help=msg.senha_falta)
atrib.add_argument("cpf", type=str, required=False)
atrib.add_argument("ativo", type=str, required=False, default="S")
atrib.add_argument("email_confirmado", type=str, required=False, default="N")
atrib.add_argument("chave_email_confirmado", type=str, required=False)
atrib.add_argument("created_at", required=False)
atrib.add_argument("updated_at", required=False)
atrib.add_argument("name", type=str, required=False)
atrib.add_argument("sobrenome", type=str, required=False)
atrib.add_argument("tel_ddi", type=str, required=False)
atrib.add_argument("tel_ddd", type=str, required=False)
atrib.add_argument("tel_numero", type=str, required=False)
atrib.add_argument("cliente_id", type=str, required=False)
#


class UserResource(Resource):
    @jwt_production
    def get(self, _od):
        user = UsuarioModel.find_user(_od)
        if user and user.ativo:
            return user.json(),200
        
        else:
            return {"message": msg.reg_nao_encontrado}, 200

    @jwt_production
    def delete(self, _od):
        user = UsuarioModel.find_user(_od)
        if user and user.ativo=="S":
            user.ativo = "N"
            user.save_user()
            return user.json(), 200
        else:
            return {"message": msg.reg_nao_encontrado}, 200

#    def patch(self, _od):
#        user = UsuarioModel.find_user(_od)
#        dados = atrib.parse_args()
#        if not user:
#            return {"message": msg.reg_nao_encontrado}, 200
#        user.update_user(**dados)
#        try:
#            result = user.save_user()
#            return result.json(), 200
#        except Exception as e:
#            return {msg.msg: f"{e}"}, 207


class UserAll(Resource):
    @jwt_production
    def get(self, parameter):
        print("osparameter", parameter)
        users = [user.json() for user in UsuarioModel.find_user_all(parameter)]
        if users:
            return {"users": users}, 200
        else:
            return {"message": msg.reg_nao_encontrado}, 200


class UserRegister(Resource):



    def post(self):
        dados = atrib.parse_args()
        if not dados.get("email") or dados.get("email") is None:
            return {"message": msg.campo_obrigatorio + ": email."}, 200
        user = UsuarioModel.find_user_email(dados["email"])
        if user:
            return {"message": msg.email_cadastrado}, 200
        user = UsuarioModel(**dados)
        user._od = str(uuid.uuid4())
        user.gera_senha(None)
        user.email_confirmado = "N"
        user.ativo = "S"
        user.gera_senha(dados["email"])
        # try: não está enviando email de confirmação
        #   user.save_user()
        #   try:
        #     user.send_confirmation_email()
        #   except Exception as e:
        #     user.delete_user()
        #     traceback.print_exc()
        #     return {'message email': e.args}, 207
        try:
            user.save_user()
            if DEBUG == "Ubuntu":
                return {"message": msg.sucesso_salvar}, 201
            else:
                return {"message": msg.sucesso_salvar, "user_od": user._od}, 201
        except Exception as e:
            return {"message user salvar": e.args}, 207


class UserLogin(Resource):

    @classmethod
    def __declare_last__(cls):
        ValidateEmail(UsuarioModel.email)

    @classmethod
    def post(cls):
        atrib1 = reqparse.RequestParser()
        atrib1.add_argument(
            "email", type=str, required=True, help=msg.email_obrigatorio
        )
        atrib1.add_argument("password", type=str, required=True, help=msg.senha_falta)
        atrib1.add_argument("cpf", type=str, required=False)
        atrib1.add_argument("name", type=str, required=False)
        atrib1.add_argument("sobrenome", type=str, required=False)
        atrib1.add_argument("tel_ddi", type=str, required=False)
        atrib1.add_argument("tel_ddd", type=str, required=False)
        atrib1.add_argument("tel_numero", type=str, required=False)
        dados = atrib1.parse_args()
        user = UsuarioModel.find_user_email(dados["email"])
        if user:
            theIdentify = user._od
            if user.ver_senha(dados["password"], user.password):
                access_token = create_access_token(
                    identity=theIdentify, expires_delta=timedelta(seconds=60000)
                )
                refresh_token = create_refresh_token(identity=theIdentify)
                return make_response(
                    jsonify(
                        {
                            "access_token": access_token,
                            "user_id": user._od,
                            "refresh_token": refresh_token,
                            "message": msg.sucesso_login,
                        }
                    ),
                    200,
                )
            else:
                return {msg.msg: msg.erro_login}, 200
        else:
            return {msg.msg: msg.erro_login}, 200


class UserLogout(Resource):
    @jwt_production
    def post(self):
        jwt_id = get_raw_jwt()["jti"]
        print(jwt_id)
        BLACKLIST.add(jwt_id)
        return {"message": msg.sucesso_logout}, 200

    # try:
    #   jwt_id = get_raw_jwt()['jti']
    #   print(jwt_id)
    #   BLACKLIST.add(jwt_id)
    #   return {'message': msg.sucesso_logout}, 200
    # except Exception as e:
    #   return {msg.msg: f'{e}'}, 207


class UserConfirm(Resource):
    @classmethod
    def get(cls, _od):
        ip_user = request.remote_addr
        user = UsuarioModel.find_user_chave_email_confirmado(_od)
        if not user:
            return {msg.msg: msg.reg_nao_encontrado}, 200
        user.email_confirmado = "S"
        try:
            user.save_user()
            subject = msg.email_confirmado_subject
            texto_email = render_template(
                "email_confirmado.txt", app_name=APP_NAME, ip_user=ip_user
            )
            html_email = render_template(
                "email_confirmado.html", app_name=APP_NAME, ip_user=ip_user
            )
            funcao.send_email_mailgun(
                subject, user.email, None, texto_email, html_email
            )
            return {msg.msg: msg.email_enviado_sucesso}, 200
        except:
            return {"message": msg.email_erro_confirmacao_salvar}, 207


class UserPasswordForget(Resource):
    def post(self):
        ip_user = request.remote_addr
        atrib1 = reqparse.RequestParser()
        atrib1.add_argument(
            "email", type=str, required=True, help=msg.email_obrigatorio
        )
        dados = atrib1.parse_args()
        user = UsuarioModel.find_user_email(dados["email"])
        theIdentify = user._od
        if not user:
            return {msg.msg: msg.email_erro_invalido}, 200
        expires = timedelta(hours=PASSWORD_TOKEN_EXPIRE)
        reset_token = create_access_token(theIdentify, expires_delta=expires)
        link = request.url_root[:-1] + url_for("userpasswordreset", token=reset_token)
        texto_email = render_template(
            "password_reset.txt", app_name=APP_NAME, ip_user=ip_user, url=link
        )
        html_email = render_template(
            "password_reset.html", app_name=APP_NAME, ip_user=ip_user, url=link
        )
        subject = msg.senha_redefina_subject
        try:
            funcao.send_email_mailgun(
                subject, dados["email"], MAILGUN_EMAIL_SENDER, texto_email, html_email
            )
            return {msg.msg: msg.email_enviado_sucesso}, 200
        except:
            return {msg.msg: msg.email_erro_enviar}, 200


class UserEmail(Resource):
    # @cross_origin()
    def post(self):
        atrib1 = reqparse.RequestParser()
        atrib1.add_argument(
            "email", type=str, required=True, help=msg.email_obrigatorio
        )
        dados = atrib1.parse_args()
        user = UsuarioModel.find_user_email(dados["email"])
        if not user:
            return {msg.msg: msg.email_erro_invalido}, 200
        return user.json(), 200

    # @cross_origin()
    def get(self):
        atrib1 = reqparse.RequestParser()
        atrib1.add_argument(
            "email", type=str, required=False, help=msg.email_obrigatorio
        )
        dados = atrib1.parse_args()
        print(dados)
        user = UsuarioModel.find_user_email(dados["email"])
        if not user:
            return {msg.msg: msg.email_erro_invalido}, 200
        return user.json(), 200


class UserPasswordReset(Resource):
    def get(self):
        atrib = reqparse.RequestParser()
        atrib.add_argument("token", type=str, required=True)
        dados = atrib.parse_args()
        token = dados["token"]
        aForm = PasswordResetForm()
        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("password_reset_with_token.html", form=aForm, token=token),
            200,
            headers,
        )


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "Senha",
        validators=[
            InputRequired(),
            EqualTo("confirmPassword", message=msg.senha_confirme_invalida),
        ],
    )
    confirmPassword = PasswordField("Confirme a Senha", validators=[DataRequired()])
    submit = SubmitField("Enviar")


class UserPasswordChange(Resource):
    def post(self):
        ip_user = request.remote_addr
        atrib = reqparse.RequestParser()
        atrib.add_argument("password", type=str, required=True)
        atrib.add_argument("token", type=str, required=True)
        dados = atrib.parse_args()
        print("olhasosdados", dados)
        aPassword = dados["password"]
        token = dados["token"]
        id = flask_jwt_extended.decode_token(encoded_token=token)["identity"]
        user = UsuarioModel.find_user(id)
        if not user:
            flash(msg.link_invalido, "error")
            return {msg.msg: msg.reg_nao_encontrado}, 200
        user.password = aPassword
        user.gera_senha(None)
        user.update_user(user.password, None, None, None, None)
        try:
            print("entrou no try")
            user.save_user()
            flash(msg.senha_atualizada, "success")
            texto_email = render_template(
                "password_changed_ok.txt", app_name=APP_NAME, ip_user=ip_user
            )
            html_email = render_template(
                "password_changed_ok.html", app_name=APP_NAME, ip_user=ip_user
            )
            subject = msg.senha_atualizada_subject
            funcao.send_email_mailgun(
                subject, user.email, MAILGUN_EMAIL_SENDER, texto_email, html_email
            )
            return {msg.msg: msg.sucesso_salvar}, 200
        except:
            print("entrou no except")
            flash(msg.erro_interno, "error")
            return {msg.msg: msg.erro_interno}, 207




api.add_resource(UserResource, "/user/<string:_od>", methods=["GET", "DELETE", "PATCH"])
api.add_resource(UserRegister, "/user/register", methods=["POST"])
api.add_resource(UserLogin, "/user/login", methods=["POST"])
api.add_resource(UserLogout, "/user/logout", methods=["POST"])
api.add_resource(UserConfirm, "/user/confirm/<string:_od>", methods=["GET"])
api.add_resource(UserEmail, "/user/email", methods=["POST", "GET"])

api.add_resource(UserPasswordForget, "/user/forget", methods=["POST"])
api.add_resource(UserPasswordReset, "/user/reset", methods=["GET"])
api.add_resource(UserPasswordChange, "/user/change", methods=["POST"])

api.add_resource(UserAll, "/users/<string:parameter>", methods=["GET"])
