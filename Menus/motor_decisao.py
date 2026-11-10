requisitos_minimos = {
    "energia": 20,
    "combustivel": 50,
    "temperatura_interna": (15, 35),
    "temperatura_externa": (5, 45),
}

def motor_decisao(modulos):
    energia = modulos.get("energia", {}).get("objeto")
    combustivel = modulos.get("combustivel", {}).get("objeto")
    temperatura = modulos.get("temperatura", {}).get("objeto")
    print("\n===== MOTOR DE DECISÃO ADAPTATIVA =====\n")

    if energia is None:
        print("Energia: módulo não cadastrado")
    else:
        if energia.percentual_carga >= requisitos_minimos["energia"]:
            print("Energia OK")
        else:
            print("Energia falhou")

        if energia.integridade:
            print("Integridade da energia OK")
        else:
            print("Integridade da energia falhou")

    if combustivel is None:
        print("Combustível: módulo não cadastrado")
    else:
        from modulos.modulos import Modulo
        if Modulo.COMBUSTIVEL_FRENAGEM_KG is None or Modulo.COMBUSTIVEL_CORRECAO_KG is None:
            print('Combustível: consumo por etapa ainda não configurado.')
        else:
            necessario = Modulo.COMBUSTIVEL_FRENAGEM_KG + 2 * Modulo.COMBUSTIVEL_CORRECAO_KG
            if combustivel.combustivel_kg >= necessario:
                print('Combustível suficiente para uma etapa (verificação global ocorre na missão).')
            else:
                print('Combustível insuficiente para uma etapa.')

        if combustivel.integridade:
            print("Integridade do combustível OK")
        else:
            print("Integridade do combustível falhou")

    if temperatura is None:
        print("Temperatura: módulo não cadastrado")
    else:
        minimo_interno, maximo_interno = requisitos_minimos["temperatura_interna"]

        if minimo_interno <= temperatura.temperatura_interna <= maximo_interno:
            print("Temperatura interna OK")
        else:
            print("Temperatura interna falhou")

        minimo_externo, maximo_externo = requisitos_minimos["temperatura_externa"]

        if minimo_externo <= temperatura.temperatura_externa <= maximo_externo:
            print("Temperatura externa OK")
        else:
            print("Temperatura externa falhou")

        if temperatura.integridade:
            print("Integridade do módulo de temperatura OK")
        else:
            print("Integridade do módulo de temperatura falhou")

    print("\n===== FIM DA ANÁLISE =====")
    input("\nPressione Enter para voltar ao menu...")

def avaliar_pouso(unidade, nave):
    """Encaminha a decisão para a regra consolidada da Nave."""
    combustivel = nave.modulos['combustivel']['objeto']
    # Obtém a base comum por import para evitar depender da hierarquia concreta.
    from modulos.modulos import Modulo
    if Modulo.COMBUSTIVEL_FRENAGEM_KG is None or Modulo.COMBUSTIVEL_CORRECAO_KG is None:
        raise ValueError('Consumos ainda não configurados.')
    quantidade = Modulo.COMBUSTIVEL_FRENAGEM_KG + 2 * Modulo.COMBUSTIVEL_CORRECAO_KG
    suficiente = combustivel is not None and combustivel.integridade and combustivel.combustivel_kg >= quantidade
    temperatura = nave.modulos['temperatura']['objeto']
    atmosfera = (temperatura is not None and temperatura.integridade
                 and 15 <= temperatura.temperatura_interna <= 35
                 and 5 <= temperatura.temperatura_externa <= 45)
    return nave._avaliar_autorizacao(unidade.objeto, suficiente, atmosfera)