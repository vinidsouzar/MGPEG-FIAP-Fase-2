from _modulos import ler_numero, validar_objeto
from visuais.exibir_card import exibir_card

from modulos.modulos import Modulo

class SuporteMedico(Modulo):
    def __init__(
        self,
        leitos,
        kits_emergencia
    ):
        # Informações gerais do módulo
        # Inicializa também altitude, velocidade e registro de pouso.
        super().__init__('Suporte Médico', 'suporte_medico', 4, 3)

        # Dados informados pelo usuário
        self.leitos = leitos
        self.kits_emergencia = kits_emergencia
        validar_objeto(self)

    def exibir(self):
        exibir_card(
            self.rotulo.upper(),
            "Informações do módulo",
            [
                "",
                f"Quantidade de leitos: {self.leitos}",
                "",
                f"Kits de emergência: {self.kits_emergencia}",
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

        self.leitos = ler_numero(f"Quantidade de leitos "
                f"[{self.leitos}]: ", inteiro=True)

        self.kits_emergencia = ler_numero(f"Quantidade de kits de emergência "
                f"[{self.kits_emergencia}]: ", inteiro=True)

    @classmethod
    def cadastrar(cls):
        exibir_card(
            "SUPORTE MÉDICO",
            "Cadastro do módulo",
            [
                "",
                "Informe os dados necessários:",
                "",
            ]
        )

        leitos = ler_numero("Quantidade de leitos: ", inteiro=True)

        kits_emergencia = ler_numero("Quantidade de kits de emergência: ", inteiro=True)

        suporte_medico = cls(
            leitos,
            kits_emergencia
        )

        suporte_medico.exibir()

        return suporte_medico