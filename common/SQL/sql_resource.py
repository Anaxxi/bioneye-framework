import uuid

from common.funcoes import msg
from flask_restful import request, url_for
from sqlalchemy import text, and_


def base_update_dados(self, **dados):
    for key, value in dados.items():
        if value != None:
            setattr(self, key, value)
    return self


def base_find_like(cls, chave, valor_chave, page, per_page, order_by, oModel):
    bases = cls.query.filter(getattr(oModel, chave).ilike(f"%{valor_chave}%")).order_by(
        text(order_by)
    )
    if per_page:
        bases = bases.paginate(page, per_page, False)
    return bases


def base_find_intervalo(
    cls, chave, valor_inicial, valor_final, page, per_page, order_by, oModel
):
    valor_inicial = valor_inicial.strip()
    valor_final = valor_final.strip()
    if valor_final is None:
        valor_final = valor_inicial
    if (
        valor_inicial.count("-") == 2
        and "-" not in valor_inicial[:4]
        and len(valor_inicial) == 10
    ):
        valor_final = valor_final + "T23:59:59"
    bases = (
        cls.query.filter(getattr(oModel, chave) >= valor_inicial)
        .filter(getattr(oModel, chave) <= valor_final)
        .order_by(text(order_by))
    )
    if per_page:
        bases = bases.paginate(page, per_page, False)
    return bases


def base_find_multiple(
    cls, chaveList, condList, valorList, dataFinalList, page, per_page, order_by, oModel
):
    filters = []
    tamChaves = len(chaveList)
    # print('aschavelist',chaveList)
    # print('astamchaves', tamChaves)
    for i in range(tamChaves):
        # print('sql_resouce A CHAVELIST',chaveList[i])
        if dataFinalList[i] == "sim":
            if (
                valorList[i].count("-") == 2
                and "-" not in valorList[i][:4]
                and len(valorList[i]) == 10
            ):
                valorList[i] = valorList[i] + "T23:59:59"
        if condList[i] == ">=":
            filters.append(getattr(oModel, chaveList[i]) >= valorList[i])
        elif condList[i] == "<=":
            filters.append(getattr(oModel, chaveList[i]) <= valorList[i])
        elif condList[i] == "!=":
            filters.append(getattr(oModel, chaveList[i]) != valorList[i])
        elif condList[i] == "==":
            filters.append(getattr(oModel, chaveList[i]) == valorList[i])
        elif condList[i] == "like":
            filters.append(getattr(oModel, chaveList[i]).ilike(f"%{valorList[i]}%"))
    bases = cls.query.filter(and_(*filters)).order_by(text(order_by))
    if per_page:
        bases = bases.paginate(page, per_page, False)
    return bases


def post_base(self, oModel, dados, tipo_id):
    # print('nopostbase',tipo_id)
    if tipo_id == "uuid":
        dados["id"] = str(uuid.uuid4())
    # print('omodel do resource', dados)
    base = oModel(**dados)
    try:
        result = base.save_base()
        return result.json(), 201
    except Exception as e:
        return {msg.msg: f"{e}"}, 207


def delete_base(self, id, OModel):
    result = OModel.find_id(id)
    if not result:
        return {msg.msg: msg.reg_nao_encontrado}, 200
    else:
        try:
            result.delete_base()
            # print('passou aqui', msg.reg_deletado)
            return {msg.msg: msg.reg_deletado}, 200
        except Exception as e:
            return {msg.msg: f"{e}"}, 207


def put_base(self, id, OModel, dados):
    base = OModel.find_id(id)
    if not base:
        return {msg.msg: msg.reg_nao_encontrado}, 200
    base.update_base(**dados)
    try:
        result = base.save_base()
        return result.json(), 200
    except Exception as e:
        return {msg.msg: f"{e}"}, 207


def find_base(self, id, OModel, requeste):
    order_by = requeste.args.get(
        "order_by"
    )  # parametro url que se existir determina a ordem dos registros para paginacao
    if order_by == None:
        order_by = ""
    chave = requeste.args.get(
        "chave"
    )  # parametro URL nome do campo a ser buscado para comparar valor_chave, inicial e final
    if chave:
        chave = (
            chave.strip()
        )  # parametro URL valor do campo a ser buscado para verificar se já existe
    valor_chave = requeste.args.get("valor_chave")
    if valor_chave:
        valor_chave = valor_chave.strip()
    # seta parametros de busca por valor e data
    valor_inicial = requeste.args.get("valorinicial")
    valor_final = requeste.args.get("valorfinal")
    # verificacao do parametro de busca
    id = id.strip()
    tam = 6 - len(id)
    parameter = id[tam:]
    # verifica parametros de paginacao
    page = int(requeste.args.get("page", 1))
    this_page = page
    per_page = requeste.args.get("per_page")
    if per_page:
        per_page = int(per_page)
    a_results = None
    result = None
    # inicio args para busca multiple:
    chaves = requeste.args.get("chaves")
    condicionais = requeste.args.get("condicionais")
    valores = requeste.args.get("valores")
    dataFinal = requeste.args.get("dataFinal")
    # fim arqgs para busca multiple
    if id == "all":  # busca todos os registros
        if per_page:
            a_results = OModel.find_all("all", page, per_page, order_by)
        else:
            result = [
                result.json() for result in OModel.find_all("all", None, None, order_by)
            ]
    elif (
        id[:6] == "limit="
    ):  # busca os primeiros limit registros definidos por limit=<int>
        result = [
            result.json() for result in OModel.find_all(parameter, None, None, order_by)
        ]
    elif (
        id[:4] == "like"
    ):  # busca todos os registros definidos no campo de nome=<string>chave com o valor_chave
        if not chave:  # verifica se a requisição tem o parametro chave
            return {msg.msg: msg.chave_erro_nao_encontrada}, 200
        if not valor_chave:  # verifica se a requisicao tem o parametro valor_chave
            return {msg.msg: msg.chave_erro_valor_nao_encontrada}, 200
        if per_page:
            a_results = OModel.find_like(chave, valor_chave, page, per_page, order_by)
        else:
            result = [
                result.json()
                for result in OModel.find_like(chave, valor_chave, None, None, order_by)
            ]
    elif (
        id[:9] == "intervalo"
    ):  # busca os registros para campo numero entre valor_inicial e valor_final
        if not chave:  # verifica se a requisição tem o parametro chave
            return {msg.msg: msg.chave_erro_nao_encontrada}, 200
        if not valor_inicial:  # verifica se a requisicao tem o parametro valor_inicial
            return {msg.msg: msg.chave_erro_valor_nao_encontrada}, 200
        if per_page:
            a_results = OModel.find_intervalo(
                chave, valor_inicial, valor_final, page, per_page, order_by
            )
        else:
            result = [
                result.json()
                for result in OModel.find_intervalo(
                    chave, valor_inicial, valor_final, None, None, order_by
                )
            ]
    elif id[:8] == "multiple":  # busca os registros para multiplos filters AND

        print("aschaves", chaves)

        chaveList = (
            chaves.split()
        )  # lista dos campos a serem adicionados a query:  "campo_1","campo_1","campo_2"
        condList = (
            condicionais.split()
        )  # lista das condicionais obedecendo a ordem dos campos: ">=,<=,=="
        valorList = (
            valores.split()
        )  # lista dos valores obedecendo a ordem dos campos: "2020-01-01, 2020-01-10,50"
        dataFinalList = (
            dataFinal.split()
        )  # lista dos parametros informando se é data final: "nao,sim,nao"
        if len(chaveList) <= 0:
            return {msg.msg: msg.erro_lista_vazia}, 207
        if len(chaveList) != len(condList):
            return {
                msg.msg: msg.erro_valor_diferente(
                    "chaves", len(chaveList), "condicionais", len(condList)
                )
            }, 207
        if len(chaveList) != len(valorList):
            return {
                msg.msg: msg.erro_valor_diferente(
                    "chaves", len(chaveList), "calores", len(valorList)
                )
            }, 207
        if len(chaveList) != len(dataFinalList):
            return {
                msg.msg: msg.erro_valor_diferente(
                    "chaves", len(chaveList), "dataFinal", len(dataFinalList)
                )
            }, 207
        if per_page:
            a_results = OModel.find_multiple(
                chaveList, condList, valorList, dataFinalList, page, per_page, order_by
            )
        else:
            result = [
                result.json()
                for result in OModel.find_multiple(
                    chaveList, condList, valorList, dataFinalList, None, None, order_by
                )
            ]
    else:  # busca pelo campo id Primary_key
        result = OModel.find_id(id)
        if result is None:
            return {msg.msg: msg.reg_nao_encontrado}, 200
        # print('olhasresult',result)
        result = result.json()
    if a_results:
        if order_by == "":
            order_by = None
        results = [results.json() for results in a_results.items]
        next = url_for(
            request.endpoint,
            chaves=chaves,
            condicionais=condicionais,
            valores=valores,
            dataFinal=dataFinal,
            chave=chave,
            valor_chave=valor_chave,
            valorinicial=valor_inicial,
            valorfinal=valor_final,
            page=a_results.next_num if a_results.has_next else a_results.page,
            per_page=per_page,
            order_by=order_by,
            **request.view_args,
        )
        prev = url_for(
            request.endpoint,
            chaves=chaves,
            condicionais=condicionais,
            valores=valores,
            dataFinal=dataFinal,
            chave=chave,
            valor_chave=valor_chave,
            valorinicial=valor_inicial,
            valorfinal=valor_final,
            page=a_results.prev_num if a_results.has_prev else a_results.page,
            per_page=per_page,
            order_by=order_by,
            **request.view_args,
        )
        if a_results.total == 0:
            return {msg.msg: msg.reg_nao_encontrado}, 200
        else:
            return {
                "total": a_results.total,
                "pages": a_results.pages,
                "this_page": this_page,
                "next": next,
                "prev": prev,
                "results": results,
            }, 200
    elif result:
        return result, 200
    else:
        return {msg.msg: msg.reg_nao_encontrado}, 200
