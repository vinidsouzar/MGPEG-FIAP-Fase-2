from _modulos import ler_numero, validar_objeto
from visuais.exibir_card import exibir_card

from modulos.modulos import Modulo

class Laboratorio(Modulo):
    def __init__(self):
        
# Informações gerais do módulo
        # Inicializa também altitude, velocidade e registro de pouso.
        super().__init__('Laboratório', 'laboratorio', 2, 1)
        validar_objeto(self)

    def exibir(self):
        exibir_card(
            self.rotulo.upper(),
            "Informações do módulo",
            [
                "",
                f"Prioridade: {self.prioridade}",
                "",
                f"Criticidade: {self.criticidade}",
                "",
                (
                    "Status: Operacional"
                    if self.integridade
                    else "Status: Inoperante"
                )
            ]
        )

    def editar(self):
        exibir_card(
            self.rotulo.upper(),
            "Edição do módulo",
            [
                "",
                "Informe os novos dados:",
                "",
            ]
        )

        self.prioridade = ler_numero(f"Prioridade "
                f"[{self.prioridade}]: ", inteiro=True)

        self.criticidade = ler_numero(f"Criticidade "
                f"[{self.criticidade}]: ", inteiro=True)

    @classmethod
    def cadastrar(cls):
        exibir_card(
            "LABORATÓRIO",
            "Cadastro do módulo",
            [
                "",
                "Cadastro com as informações gerais",
                "definidas para o módulo.",
                "",
            ]
        )

        laboratorio = cls()

        laboratorio.exibir()

        return laboratorio