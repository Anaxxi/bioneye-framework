APROVACAO_STATUS = [
    (u"A", u"Aprovado"),
    (u"E", u"Esperando Aprovação"),
    (u"R", u"Recusado"),
]

COLECAO_TIPO = [(u"A", u"Pública"), (u"P", u"Privada")]

ESPECIE = [
    (
        u"CA",
        u"CÃO",
    ),
    (u"GA", u"GATO"),
    (u"RO", u"ROEDOR"),
    (u"MA", u"MACACO"),
    (u"BO", u"BOVINO"),
    (u"SU", u"SUINO"),
    (u"CP", u"CAPRINO"),
    (u"OT", u"OUTRO"),
    (u"HU", u"HUMANO"),
]

MEIOPAGAMENTO = [
    (u"DI", u"Dinheiro"),
    (u"CC", u"Cartão de Crédito"),
    (u"CD", u"Cartão de Débito"),
    (u"DC", u"DOC"),
    (u"TD", u"TED"),
    (u"PX", u"PIX"),
    (u"OU", u"Outros"),
]

PARTES_ENUM = [
    (u"cabeca", u"CABEÇA"),
    (u"pescoco", u"PESCOÇO"),
    (u"torax", u"TORAX"),
    (u"membros", u"MEMBROS"),
    (u"costas", u"COSTAS"),
    (u"abdome", u"ABDOME E PELVE"),
    (u"coluna", u"COLUNA"),
]

PORTE = [
    (u"MI", u"Micro"),
    (u"PE", u"Pequeno"),
    (u"ME", u"Médio"),
    (u"GR", u"Grande"),
    (u"GI", u"Gigante"),
]

SEXO_ENUM = [(u"M", u"Masculino"), (u"F", u"Feminino")]

SIM_NAO = [(u"S", u"Sim"), (u"N", u"Não")]

TIPO_CARRO = [
    (
        u"C",
        u"CARRO",
    ),
    (u"M", u"MOTO"),
    (u"B", u"BICICLETA"),
    (u"N", u"NAVIO"),
    (u"A", u"AVIÃO"),
    (u"T", u"CAMINHÃO"),
]

TIPO_DENUNCIA_ENUM = [
    (u"D", u"Fake"),
    (u"R", u"Não possui Registro"),
    (u"O", u"Incita o ódio"),
    (u"A", u"Assunto não relacionado"),
    (u"D", u"Demonstra desconhecimento"),
    (u"O", u"Esse conteúdo é meu"),
    (u"T", u"Esse conteúdo é de terceiros"),
]

TIPO_TIMELINE_ENUM = [
    (u"C", u"Caso"),
    (u"E", u"Exame"),
    (u"Q", u"Pergunta"),
    (u"P", u"Publicação"),
]

TIPO_USER_GRUPO_ENUM = [
    (u"A", u"Administrador"),
    (u"E", u"Empresa"),
    (u"C", u"Cliente")]

UTIL_ELEMENTO = [  # qual elemento foi bom nesse caso
    (u"I", u"Imagens"),
    (u"C", u"Discussão"),
    (u"A", u"Atualização"),
    (u"R", u"Resposta Aceita"),
    (u"D", u"Descrição"),
]

UTIL_FALTOU = [
    (u"I", u"Mais informações do paciente"),
    (u"D", u"Descrição detalhada"),
    (u"A", u"Atualização"),
    (u"F", u"Diagnóstico Final"),
    (u"Q", u"Imagens de melhor qualidade"),
    (u"E", u"Diagnóstico baseado em evidência"),
]

UTIL_PROVEITO = [  # qual proveito voce tirou ?
    (u"R", u"Boa revisão de caso clínico"),
    (u"V", u"Nova visão para um caso"),
    (u"A", u"Ampliou meu conhecimento"),
    (u"N", u"Situação Nova"),
    (u"M", u"Mudou um conceito meu"),
]

UTIL_TIPO_CASO = [  # como descreveria o caso?
    (u"I", u"Raro"),
    (u"F", u"Fonte para Livro"),
    (u"C", u"Comum"),
    (u"A", u"Comum, mas a Apresentação é atípica"),
    (u"X", u"Complexo"),
    (u"P", u"Motivo para Pesquisa"),
]
