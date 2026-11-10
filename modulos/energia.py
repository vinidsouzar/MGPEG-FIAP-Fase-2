from _modulos import ler_numero, validar_objeto
from visuais.exibir_card import exibir_card

from modulos.modulos import Modulo

class Energia(Modulo):
    def __init__(
        self,
        capacidade_bateria_kwh,
        carga_kwh,
        consumo_medio_kw
    ):
        # Informações gerais do módulo
        # Inicializa também altitude, velocidade e registro de pouso.
        super().__init__('Energia', 'energia', 4, 5)

        # Dados informados pelo usuário
        self.capacidade_bateria_kwh = capacidade_bateria_kwh
        self.carga_kwh = carga_kwh
        self.consumo_medio_kw = consumo_medio_kw

        # Valores calculados
        self.percentual_carga = 0
        self.autonomia_horas = 0
        self.autonomia_dias = 0

        self.atualizar_calculos()

    def atualizar_calculos(self):
        validar_objeto(self)
        """Atualiza os valores derivados do módulo."""

        self.percentual_carga = (
            self.carga_kwh /
            self.capacidade_bateria_kwh
        ) * 100

        self.autonomia_horas = (
            self.carga_kwh /
            self.consumo_medio_kw
        )

        self.autonomia_dias = (
            self.autonomia_horas / 24
        )

    def consumir(self, quantidade_kwh):
        if quantidade_kwh < 0:
            raise ValueError("Consumo não pode ser negativo.")
        self.carga_kwh -= quantidade_kwh

        if self.carga_kwh <= 0:
            self.integridade = False
            self.carga_kwh = 0

        self.atualizar_calculos()

    def exibir(self):
        exibir_card(
            self.rotulo.upper(),
            "Informações do módulo",
            [
                "",
                f"Carga da bateria: "
                f"{self.carga_kwh:.2f}/"
                f"{self.capacidade_bateria_kwh:.2f} kWh",
                "",
                f"Carga disponível: "
                f"{self.percentual_carga:.1f}%",
                "",
                f"Consumo médio: "
                f"{self.consumo_medio_kw:.2f} kW",
                "",
                f"Autonomia: "
                f"{self.autonomia_horas:.2f} horas",
                f"           "
                f"{self.autonomia_dias:.2f} dias",
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

        self.capacidade_bateria_kwh = ler_numero(f"Capacidade da bateria (kWh) "
                f"[{self.capacidade_bateria_kwh}]: ", inteiro=False)

        self.carga_kwh = ler_numero(f"Carga atual (kWh) "
                f"[{self.carga_kwh}]: ", inteiro=False)

        self.consumo_medio_kw = ler_numero(f"Consumo médio (kW) "
                f"[{self.consumo_medio_kw}]: ", inteiro=False)

        self.atualizar_calculos()

    @classmethod
    def cadastrar(cls):
        exibir_card(
            "ENERGIA",
            "Cadastro do módulo",
            [
                "",
                "Informe os dados necessários:",
                "",
            ]
        )

        capacidade_bateria_kwh = ler_numero("Capacidade da bateria (kWh): ", inteiro=False)

        carga_kwh = ler_numero("Carga atual da bateria (kWh): ", inteiro=False)

        consumo_medio_kw = ler_numero("Consumo médio (kW): ", inteiro=False)

        energia = cls(
            capacidade_bateria_kwh,
            carga_kwh,
            consumo_medio_kw
        )

        energia.exibir()

        return energia