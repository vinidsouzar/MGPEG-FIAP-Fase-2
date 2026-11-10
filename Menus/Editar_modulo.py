from visuais.exibir_card import exibir_card
from Menus.menu_modulos import selecionar_modulo


def editar_modulo(nave):
    tipo = selecionar_modulo(nave)

    if tipo is None:
        return

    modulo = nave.modulos[tipo]

    if modulo["objeto"] is None:
        exibir_card(
            "MÓDULO NÃO CONFIGURADO",
            "Edição",
            [
                "",
                "Configure o módulo antes",
                "de tentar editá-lo.",
                ""
            ]
        )

        input("\nPressione ENTER para continuar...")
        return

    nave.editar_modulo(tipo)