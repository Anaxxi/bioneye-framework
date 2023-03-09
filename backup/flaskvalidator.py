@classmethod
def __declare_last__(cls):
    ValidateLength(AdministradorsModel.password, max_length=255, min_length=8, throw_exception=True, message="A senha tem que ter 8 ou mais caracteres")
    ValidateLength(AdministradorsModel.cpf, max_length=11, min_length=11, throw_exception=True, message="CPF invalido")
    ValidateString(AdministradorsModel.name)
    ValidateString(AdministradorsModel.sobrenome)
    ValidateString(AdministradorsModel.tel_ddd)
    ValidateString(AdministradorsModel.tel_ddi)
    ValidateEmail(AdministradorsModel.email, throw_exception=True, message="E-mail invalido")



    @classmethod
    def __declare_last__(cls):
        ValidateLength(UsuarioModel.password, max_length=255, min_length=8, throw_exception=True, message="A senha tem que ter 8 ou mais caracteres")
        ValidateLength(UsuarioModel.cpf, max_length=11, min_length=11, throw_exception=True, message="CPF invalido")
        ValidateString(UsuarioModel.name)
        ValidateString(UsuarioModel.sobrenome)
        ValidateString(UsuarioModel.tel_ddd)
        ValidateString(UsuarioModel.tel_ddi)
        ValidateEmail(UsuarioModel.email, throw_exception=True, message="E-mail invalido")
