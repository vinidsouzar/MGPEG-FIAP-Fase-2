from _modulos import ler_numero, validar_objeto
from visuais.exibir_card import exibir_card

from modulos.modulos import Modulo

class Temperatura(Modulo):
    def __init__(
        self,
        temperatura_interna,
        temperatura_externa
    ):
        # Informações gerais do módulo
        # Inicializa também altitude, velocidade e registro de pouso.
        super().__init__('Temperatura Interna e Externa', 'temperatura', 3, 1)

        # Dados informados pelo usuário
        self.temperatura_interna = temperatura_interna
        self.temperatura_externa = temperatura_externa
        validar_objeto(self)

    def exibir(self):
        exibir_card(
            self.rotulo.upper(),
            "Informações do módulo",
            [
                "",
                f"Temperatura interna: "
                f"{self.temperatura_interna:.2f} °C",
                "",
                f"Temperatura externa: "
                f"{self.temperatura_externa:.2f} °C",
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

        self.temperatura_interna = ler_numero(f"Temperatura interna (°C) "
                f"[{self.temperatura_interna}]: ", inteiro=False)

        self.temperatura_externa = ler_numero(f"Temperatura externa (°C) "
                f"[{self.temperatura_externa}]: ", inteiro=False)

    @classmethod
    def cadastrar(cls):
        exibir_card(
            "TEMPERATURA INTERNA E EXTERNA",
            "Cadastro do módulo",
            [
                "",
                "Informe os dados necessários:",
                "",
            ]
        )

        temperatura_interna = ler_numero("Temperatura interna (°C): ", inteiro=False)

        temperatura_externa = ler_numero("Temperatura externa (°C): ", inteiro=False)

        temperatura = cls(
            temperatura_interna,
            temperatura_externa
        )

        temperatura.exibir()

        return temperatura