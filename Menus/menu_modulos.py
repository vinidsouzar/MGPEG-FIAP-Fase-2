from visuais.exibir_card import exibir_card


def exibir_menu_modulos(nave):
    conteudo = [
        "",
        "Selecione um módulo:",
        ""
    ]

    tipos = list(nave.modulos.keys())

    for indice, tipo in enumerate(tipos, start=1):
        modulo = nave.modulos[tipo]

        status = (
            "Configurado"
            if modulo["objeto"] is not None
            else "Pendente"
        )

        conteudo.append(
            f"{indice}. {modulo['nome']} - {status}"
        )

    conteudo.extend([
        "",
        "0. Voltar",
        ""
    ])

    exibir_card(
        "MÓDULOS",
        "Gerenciamento da nave",
        conteudo
    )

    return tipos


def selecionar_modulo(nave):
    tipos = exibir_menu_modulos(nave)

    try:
        opcao = int(input("\nSelecione um módulo: "))
    except ValueError:
        return None

    if opcao == 0:
        return None

    if opcao < 1 or opcao > len(tipos):
        return None

    return tipos[opcao - 1]