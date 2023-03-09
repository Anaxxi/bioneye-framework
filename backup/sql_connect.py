# PARAMETROS MYSQL
if DEBUG != True:
    USERNAME = "developer"
    PASSWORD = "mysql1QAZ!@#$2wsxmysql"
    SERVER = "localhost"
    DB = "lifepix"  # colocar aqui o nome da base de dados
else:
    USERNAME = "developer"
    if SISTEMA_DEV == "Windows":
        USERNAME = "root"
        PASSWORD = "12345"  #'LT4QCm:TXV}2c4EM'
    else:
        PASSWORD = "mysql1QAZ!@#$2wsxmysql"
    SERVER = "localhost"
    DB = "lifepix"  # colocar aqui o nome da base de dados
