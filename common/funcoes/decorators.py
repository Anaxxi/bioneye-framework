from functools import wraps
from flask_jwt_extended import verify_fresh_jwt_in_request, get_jwt_claims, jwt_required
from flask import make_response, jsonify, request
from ..user import user_model


# def prod_jwt_required(f):
#   @wraps(f)
#   def wrapper(*arg,**kwargs):
#     if not app.debug:
#       decorators = [jwt_required]
#   return wrapper()


def admin_required(fn):
    @wraps(fn)
    def wrapper(*arg, **kwargs):
        verify_fresh_jwt_in_request()
        claims = get_jwt_claims()
        if claims["roles"] != "admin":
            return make_response(jsonify(mensagem="Usuário não permitido"), 403)
        else:
            return fn(*arg, **kwargs)
        return wrapper


def api_key_required(fn):
    @wraps(fn)
    def wraper(*args, **kwargs):
        api_key = request.args.get("api_key")
        if api_key:
            user = user_model.UserModel.find_user_api_key(api_key)
            if user:
                return user.json()
            else:
                return make_response(jsonify(mensagem="Usuário não Autorizado"), 200)
        else:
            print("nossa apikey", api_key)
            return make_response(jsonify(mensagem="Usuário não Autorizado111"), 200)
        return wraper
