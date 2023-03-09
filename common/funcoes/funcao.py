import datetime
from datetime import date

import requests
import math

from functools import wraps
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from config import (
    DEBUG,
    MAILGUN_API_KEY,
    MAILGUN_DOMAIN,
    MAILGUN_EMAIL_SENDER,
    UPLOAD_FOLDER_IMAGE,
)


def idade_anos(data: date):
    today = date.today()
    idade = (
        today.year
        - int(data.year)
        - ((today.month, today.day) < (data.month, data.day))
    )
    return idade


def custom_validator(view_function):
    pass


# calcula distancias baseadas em latitude e longitude a partir do ponto informado
def distance_lat_long(lat1, lng1, lat2, lng2, math=math):
    ang = math.acos(
        math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.cos(math.radians(lng2) - math.radians(lng1))
        + math.sin(math.radians(lat1)) * math.sin(math.radians(lat2))
    )
    # para milhas usar o parametro 3959
    return 6371 * ang


def grava_erro_arquivo(nome_arquivo, oErro):
    adata = datetime.datetime.now()
    adata = adata.isoformat()
    arquivo = open(f"{UPLOAD_FOLDER_IMAGE}{nome_arquivo}", "a")
    arquivo.seek(0, 2)
    arquivo.write(f"Data: {adata}: Erro___: {oErro}")
    arquivo.close()
    print(f"Erro request notificacao na funcao: {oErro}")


def jwt_production(f):
    @wraps(f)
    def decorada(*args, **kwargs):
        if DEBUG == False:
            print("entrou aqui e nao devia")
        verify_jwt_in_request()
        return f(*args, **kwargs)

    return decorada


def send_email_mailgun(subject, emailTo, emailSender, oText, oHtml):
    if emailSender is None:
        emailSender = MAILGUN_EMAIL_SENDER
    link_post = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    print("olink_post", link_post)
    orequest = requests.post(
        link_post,
        auth=("api", MAILGUN_API_KEY),
        data={
            "from": emailSender,
            "to": emailTo,
            "subject": subject,
            "text": oText,
            "html": oHtml,
        },
    )
    print("statusrequest", orequest.status_code)
    print("thebari", orequest.text)
    return orequest


def trata_order_by(order_by):
    if order_by.endswith(" asc"):
        order_by = order_by[:-4]
        order_by = order_by.strip()
    elif order_by.endswith(" desc"):
        order_by = order_by[:-4]
        order_by = order_by.strip()
        order_by = f"-{order_by}"
    else:
        order_by = order_by.strip()
    return order_by
