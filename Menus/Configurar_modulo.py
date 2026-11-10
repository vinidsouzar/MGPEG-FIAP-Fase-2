from visuais.exibir_card import exibir_card
from Menus.menu_modulos import selecionar_modulo


def configurar_modulo(nave):
    tipo = selecionar_modulo(nave)

    if tipo is None:
        return

    modulo = nave.modulos[tipo]

    if modulo["objeto"] is not None:
        exibir_card(
            "MÓDULO JÁ CONFIGURADO",
            "Configuração",
            [
                "",
                "Este módulo já possui",
                "informações cadastradas.",
                ""
            ]
        )

        input("\nPressione ENTER para continuar...")
        return

    nave.configurar_modulo(tipo)