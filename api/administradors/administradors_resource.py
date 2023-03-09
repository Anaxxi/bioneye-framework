import traceback
import uuid
from flask import request, make_response, jsonify, render_template, flash, config
from flask_cors import cross_origin
from flask_restful import Resource, reqparse, url_for

from api.administradors.administradors_model import AdministradorsModel
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
#
atrib.add_argument("hash", type=str, required=False)

class AdministradorResource(Resource):
    @jwt_production
    def get(self, _od):
        administrador = AdministradorsModel.find_administrador(_od)
        if administrador and administrador.ativo=="S":
            return administrador.json(), 200
        else:
            return {"message": msg.reg_nao_encontrado}, 200

    @jwt_production
    def delete(self, _od):
        administrador = AdministradorsModel.find_administrador(_od)
        if administrador and administrador.ativo=="S":
            administrador.ativo = "N"
            administrador.save_administrador()
            return administrador.json(), 200
        else:
            return {"message": msg.reg_nao_encontrado}, 200


class AdministradorAll(Resource):
    @jwt_production
    def get(self, parameter):
        print("osparameter", parameter)
        administradors = [administrador.json() for administrador in AdministradorsModel.find_administrador_all(parameter)]
        if administradors:
            return {"administradors": administradors}, 200
        else:
            return {"message": msg.reg_nao_encontrado}, 200


class AdministradorRegister(Resource):
    def post(self):
        dados = atrib.parse_args()
        if not dados.get("email") or dados.get("email") is None:
            return {"message": msg.campo_obrigatorio + ": email."}, 200
        administrador = AdministradorsModel.find_administrador_email(dados["email"])
        if administrador:
            return {"message": msg.email_cadastrado}, 200
        administrador = AdministradorsModel(**dados)
        administrador._od = str(uuid.uuid4())
        administrador.api_key = str(uuid.uuid4())
        administrador.gera_senha(None)
        administrador.email_confirmado = False
        administrador.gera_senha(dados["email"])
        # try: não está enviando email de confirmação
        #   user.save_user()
        #   try:
        #     user.send_confirmation_email()
        #   except Exception as e:
        #     user.delete_user()
        #     traceback.print_exc()
        #     return {'message email': e.args}, 207
        try:
            administrador.save_administrador()
            if DEBUG == "Ubuntu":
                return {"message": msg.sucesso_salvar}, 201
            else:
                return {"message": msg.sucesso_salvar, "administrador_od": administrador._od}, 201
        except Exception as e:
            return {"message administrador salvar": e.args}, 207


class AdministradorLogin(Resource):
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
        administrador = AdministradorsModel.find_administrador_email(dados["email"])
        if administrador:
            theIdentify = administrador._od
            if administrador.ver_senha(dados["password"], administrador.password):
                access_token = create_access_token(
                    identity=theIdentify, expires_delta=timedelta(seconds=60000)
                )
                refresh_token = create_refresh_token(identity=theIdentify)
                return make_response(
                    jsonify(
                        {
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "message": msg.sucesso_login,
                            "admin": administrador._od,
                        }
                    ),
                    200,
                )
            else:
                return {msg.msg: msg.erro_login}, 200
        else:
            return {msg.msg: msg.erro_login}, 200


class AdministradorLogout(Resource):
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


class AdministradorConfirm(Resource):
    @classmethod
    def get(cls, _od):
        ip_administrador = request.remote_addr
        administrador = AdministradorsModel.find_administrador_chave_email_confirmado(_od)
        if not administrador:
            return {msg.msg: msg.reg_nao_encontrado}, 200
        administrador.email_confirmado = "S"
        try:
            administrador.save_administrador()
            subject = msg.email_confirmado_subject
            texto_email = render_template(
                "email_confirmado.txt", app_name=APP_NAME, ip_administrador=ip_administrador
            )
            html_email = render_template(
                "email_confirmado.html", app_name=APP_NAME, ip_administrador=ip_administrador
            )
            funcao.send_email_mailgun(
                subject, administrador.email, None, texto_email, html_email
            )
            return {msg.msg: msg.email_enviado_sucesso}, 200
        except:
            return {"message": msg.email_erro_confirmacao_salvar}, 207


class AdministradorPasswordForget(Resource):
    def post(self):
        ip_administrador = request.remote_addr
        atrib1 = reqparse.RequestParser()
        atrib1.add_argument(
            "email", type=str, required=True, help=msg.email_obrigatorio
        )
        dados = atrib1.parse_args()
        administrador = AdministradorsModel.find_administrador_email(dados["email"])
        theIdentify = administrador._od
        if not administrador:
            return {msg.msg: msg.email_erro_invalido}, 200
        expires = timedelta(hours=PASSWORD_TOKEN_EXPIRE)
        reset_token = create_access_token(theIdentify, expires_delta=expires)
        link = request.url_root[:-1] + url_for("administradorpasswordreset", token=reset_token)
        texto_email = render_template(
            "password_reset.txt", app_name=APP_NAME, ip_administrador=ip_administrador, url=link
        )
        html_email = render_template(
            "password_reset.html", app_name=APP_NAME, ip_administrador=ip_administrador, url=link
        )
        subject = msg.senha_redefina_subject
        try:
            funcao.send_email_mailgun(
                subject, dados["email"], MAILGUN_EMAIL_SENDER, texto_email, html_email
            )
            return {msg.msg: msg.email_enviado_sucesso}, 200
        except:
            return {msg.msg: msg.email_erro_enviar}, 200


class AdministradorEmail(Resource):
    # @cross_origin()
    def post(self):
        atrib1 = reqparse.RequestParser()
        atrib1.add_argument(
            "email", type=str, required=True, help=msg.email_obrigatorio
        )
        dados = atrib1.parse_args()
        administrador = AdministradorsModel.find_administrador_email(dados["email"])
        if not administrador:
            return {msg.msg: msg.email_erro_invalido}, 200
        return administrador.json(), 200

    # @cross_origin()
    def get(self):
        atrib1 = reqparse.RequestParser()
        atrib1.add_argument(
            "email", type=str, required=False, help=msg.email_obrigatorio
        )
        dados = atrib1.parse_args()
        print(dados)
        administrador = AdministradorsModel.find_administrador_email(dados["email"])
        if not administrador:
            return {msg.msg: msg.email_erro_invalido}, 200
        return administrador.json(), 200


class AdministradorPasswordReset(Resource):
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


class AdministradorPasswordChange(Resource):
    def post(self):
        ip_administrador = request.remote_addr
        atrib = reqparse.RequestParser()
        atrib.add_argument("password", type=str, required=True)
        atrib.add_argument("token", type=str, required=True)
        dados = atrib.parse_args()
        print("olhasosdados", dados)
        aPassword = dados["password"]
        token = dados["token"]
        id = flask_jwt_extended.decode_token(encoded_token=token)["identity"]
        administrador = AdministradorsModel.find_administrador(id)
        if not administrador:
            flash(msg.link_invalido, "error")
            return {msg.msg: msg.reg_nao_encontrado}, 200
        administrador.password = aPassword
        administrador.gera_senha(None)
        administrador.update_administrador(administrador.password, None, None, None, None)
        try:
            print("entrou no try")
            administrador.save_administrador()
            flash(msg.senha_atualizada, "success")
            texto_email = render_template(
                "password_changed_ok.txt", app_name=APP_NAME, ip_administrador=ip_administrador
            )
            html_email = render_template(
                "password_changed_ok.html", app_name=APP_NAME, ip_administrador=ip_administrador
            )
            subject = msg.senha_atualizada_subject
            funcao.send_email_mailgun(
                subject, administrador.email, MAILGUN_EMAIL_SENDER, texto_email, html_email
            )
            return {msg.msg: msg.sucesso_salvar}, 200
        except:
            print("entrou no except")
            flash(msg.erro_interno, "error")
            return {msg.msg: msg.erro_interno}, 207



api.add_resource(AdministradorResource, "/administrador/<string:_od>", methods=["GET", "DELETE"])
api.add_resource(AdministradorRegister, "/administrador/register", methods=["POST"])
api.add_resource(AdministradorLogin, "/administrador/login", methods=["POST"])
api.add_resource(AdministradorLogout, "/administrador/logout", methods=["POST"])
api.add_resource(AdministradorConfirm, "/administrador/confirm/<string:_od>", methods=["GET"])
api.add_resource(AdministradorEmail, "/administrador/email", methods=["POST", "GET"])
api.add_resource(AdministradorPasswordForget, "/administrador/forget", methods=["POST"])
api.add_resource(AdministradorPasswordReset, "/administrador/reset", methods=["GET"])
api.add_resource(AdministradorPasswordChange, "/administrador/change", methods=["POST"])
api.add_resource(AdministradorAll, "/administradors/<string:parameter>", methods=["GET"])
