from config import APP_NAME

msg = "message"

app_nome = APP_NAME
app_email_nao_responda = "Não responda"


def arquivo_del(arquivo, diretorio, arquivo_apagado):
    if arquivo_apagado == "nao_encontrado":
        return f"arquivo {arquivo} deletado no banco de dados, mas não encontrado no diretorio {diretorio}"
    elif arquivo_apagado == "nao_apagado":
        return f"Arquivo {arquivo} deletado no banco de dados, mas não apagado no diretório {diretorio}"


arquivo_nao_enviado = "arquivo_obrigatorio_nao_enviado"
arquivo_erro_salvar = "erro_salvar_arquivo"


def campo_cadastrado(chave, valor_chave):
    return f"O campo {chave} com valor {valor_chave} já está cadastrado"


campo_obrigatorio = "campo_obrigatorio"

chave_erro_nao_encontrada = "Chave de busca não foi passada como parametro"
chave_erro_valor_nao_encontrada = (
    "Valor da Chave de busca não foi passada como parametro"
)

confirme_seu_cadastro = "Confirme seu cadastro clicando no link: "

email_cadastrado = "email_ja_cadastrado"
email_confirmado = "email_confirmado_sucesso"
email_confirmado_subject = "email_confirmado"
email_enviado_sucesso = "email_enviado_sucesso"
email_erro_confirmacao_salvar = "erro_confirmar_email"
email_erro_confirmado = "email_nao_confirmado"
email_erro_enviar = "erro_enviar_email"
email_erro_invalido = "email_invalido"
email_obrigatorio = "email_obrigatorio"


erro_interno = "erro_interno"
erro_login = "erro_login"
erro_lista_vazia = "A lista de chaves está vazia"
erro_nao_permitido = "operacao_nao_permitida"
erro_salvar = "erro_interno_salvar"
erro_deletar = "erro_interno_deletar"


def erro_valor_diferente(campo1, valor1, campo2, valor2):

    return f"O campo ({campo1}) com {valor1} elementos é diferente do campo ({campo2}) com {valor2} elementos"


link_invalido = "link_invalido"


profile_igual = "O profile não pode ser igual ao user"


reg_deletado = "registro_deletado_sucesso"
reg_encontrado = "registro_encontrado"
reg_nao_encontrado = "registro_nao_encontrado"


senha_atualizada = "Sua senha foi atualizada com sucesso"
senha_atualizada_subject = app_nome + ": Atualização de Senha"
senha_digite = "Digite sua senha"
senha_confirme = "Digite novamente para confirmar"
senha_confirme_invalida = "senha_diferente_confirmesenha"
senha_falta = "senha_obrigatoria"
senha_redefina = "Redefina sua senha"
senha_redefina_subject = app_nome + ": Redefinição de Senha"


sucesso_login = "login_sucesso"
sucesso_logout = "logout_sucesso"
sucesso_salvar = "sucesso_salvar"


usuario_nao_encontrado = "Não foi encontrad usuário para o user_id"
usuario_deslogado = "usuario_deslogado"
