from sqlalchemy import create_engine
from sistema import THE_SISTEMA

DEBUG = True
SISTEMA_DEV = THE_SISTEMA
APP_NAME = "Lifepix"  # APP_NAME = 'lifepixserver'

if SISTEMA_DEV == "Windows":
    URL_SISTEMA = "127.0.0.1:5000"
elif SISTEMA_DEV == "Ubuntu":
    URL_SISTEMA = "http://austin.bioneye.com"
else:
    URL_SISTEMA = "http://austin.bioneye.com"


#Conector de banco de dados.
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://samuel:ss2syi@localhost/lifepix"  #'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{SERVER}/{DB}' -
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQL_ENGINE = create_engine(SQLALCHEMY_DATABASE_URI)


SECRET_KEY = "lifepixvetpixçdfkja oiwcianadajflksdfjalçsd kfjasd lkfjmarcodklfjalkçdsjfaçlkdjfa çlkeduardodlakdsjfaldskjfadamoneladkjfalsdkfja "
JWT_SECRET_KEY = "syoerufyasdiufyalifepix o dkajfsldkfjasld kfjas çlkgfilhoeduardoakdajfalkjnaoseiselucianatemfilhoilaksdjfçalksdjfa"
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

# UPLOADS
if SISTEMA_DEV == "Windows":
    UPLOAD_SERVER_IMAGE = "C:"
    UPLOAD_FOLDER_IMAGE = "/_flask/lifepix/_IMAGES/"
    UPLOAD_MAX_CONTENT_LENGHT = 16 * 1024 * 1024
elif SISTEMA_DEV == "Ubuntu":
    UPLOAD_SERVER_IMAGE = ""  # URL_SISTEMA
    UPLOAD_FOLDER_IMAGE = "_IMAGES/"  #'/home/vetpix/_IMAGES/'
    UPLOAD_MAX_CONTENT_LENGHT = 16 * 1024 * 1024

if SISTEMA_DEV == "Windows":
    URL_LOGIN = (
        "http://157.245.253.101:5000"  # INFORMAR aqui a URL de login do FrontEnd
    )
    URL_DEVELOPMENT = "http://157.245.253.101:5000"
    URL_PRODUCTION = "I/DONT/NOW"
elif SISTEMA_DEV == "Ubuntu":
    URL_LOGIN = URL_SISTEMA + "/"  # INFORMAR aqui a URL de login do FrontEnd
    URL_DEVELOPMENT = "http://127.0.0.1:5000"
    URL_PRODUCTION = URL_SISTEMA

# MAILGUN PARAMETROS

MAILGUN_API_KEY = "4fe762969cd9dc2dc0fc460a2b174ae0-3e51f8d2-1771b0f2"
MAILGUN_API_BASE_URL = "https://api.mailgun.net/v3/naotemaoinda.mailgun.org"
MAILGUN_DOMAIN = ".mailgun.org"
MAILGUN_EMAIL_SENDER = "contact@vetpix.com.br"

PASSWORD_TOKEN_EXPIRE = 48  # HORAS

# MONGO PARAMETROS
if DEBUG != True:  # DESENVOLVIMENTO
    MONGODB_DB = "lifepixweb"
    MONGODB_USERNAME = ""  #'dbAdmin'
    MONGODB_PASSWORD = ""  #'password'
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017
else:
    MONGODB_DB = "lifepixweb"
    # MONGODB_USERNAME= 'dbAdmin'
    # MONGODB_PASSWORD  = 'password'
    MONGODB_HOST = "localhost"
    MONGODB_PORT = 27017

# parametros pagseguro
PAGSEGURO_URL_PRODUCAO = "https://ws.pagseguro.uol.com.br/pre-approvals/"
PAGSEGURO_URL_TESTE = "https://ws.sandbox.pagseguro.uol.com.br/pre-approvals/"

PAGSEGURO_EMAIL = "sememail@email.com"

PAGSEGURO_TOKEN = "1a3fa705-c408-41b6-dfgsfs851e-7779e6215c34bfd9f9f94a8e89b9373483f46fa6ca2e9cce-2739-42cb-9748-0fbc9124f559"
PAGSEGURO_PLANO_BASICO = "95B212dfsd57-3333-A792-24F8-5FB3ADFC13F5"
PAGSEGURO_PLANO_ANUAL = "AF4D9CFCsdfsdfs-8A8A-CE9F-F4B6-BF82E001B87F"
PAGSEGURO_BOTAO_REDE_SOCIAL = "http://naotemaindapag.ae/sdfsdfs7V-JW78zu"
PAGSEGURO_BOTAO_REDE_SOCIAL_ANUAL = "http://naotemaindapag.ae/dsfsdfs7W4Qk_6w9"

# PAGSEGURO_CODIGO_BOTAO_SITE = <!-- INICIO FORMULARIO BOTAO PAGSEGURO: NAO EDITE OS COMANDOS DAS LINHAS ABAIXO -->
# <form action="https://pagseguro.uol.com.br/pre-approvals/request.html" method="post">
# <input type="hidden" name="code" value="95B212573333A79224F85FB3ADFC13F5" />
# <input type="hidden" name="iot" value="button" />
# <input type="image" src="https://stc.pagseguro.uol.com.br/public/img/botoes/assinaturas/209x48-assinar-assina.gif" name="submit" alt="Pague com PagSeguro - É rápido, grátis e seguro!" width="209" height="48" />
# </form>'
# <!-- FINAL FORMULARIO BOTAO PAGSEGURO -->
