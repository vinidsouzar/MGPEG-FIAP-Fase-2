from visuais.exibir_card import exibir_card
from Menus.menu_modulos import selecionar_modulo

def visualizar_modulo(nave):
    tipo = selecionar_modulo(nave)

    if tipo is None:
        return

    modulo = nave.modulos[tipo]

    if modulo["objeto"] is None:
        exibir_card(
            "MÓDULO NÃO CONFIGURADO",
            "Visualização",
            [
                "",
                "Este módulo ainda não",
                "foi configurado.",
                ""
            ]
        )

        input("\nPressione ENTER para continuar...")
        return

    modulo["objeto"].exibir()
    unidade = nave.buscar_tipo(tipo)
    if unidade is not None:
        print("Dados de pouso:", vars(unidade))

    input("\nPressione ENTER para continuar...")