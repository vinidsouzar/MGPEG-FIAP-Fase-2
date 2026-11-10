from random import random

class Modulo:
    ALTITUDE_ORBITA_M = 250_000
    ALTITUDE_ENTRADA_M = 125_000
    COMBUSTIVEL_FRENAGEM_KG = 20
    COMBUSTIVEL_CORRECAO_KG = 5

    def __init__(self, rotulo, tipo, prioridade, criticidade, integridade=True):
        self.rotulo = rotulo
        self.tipo = tipo
        self.prioridade = prioridade
        self.criticidade = criticidade
        self.integridade = integridade

        # Estado final do pouso.
        self.pouso_concluido = False

        # Leituras físicas, usando unidades do SI.
        self.altitude_orbita_m = self.ALTITUDE_ORBITA_M
        self.altitude_m = self.altitude_orbita_m
        self.velocidade_m_s = 0.0
        self.combustivel_pouso_kg = 0.0
        self.registro_pouso = []

    @classmethod
    def configurar_consumos(cls):
        """Parâmetros hipotéticos positivos; mantidos na classe-base comum."""
        from _modulos import ler_numero
        Modulo.COMBUSTIVEL_FRENAGEM_KG = ler_numero(
            'Consumo de frenagem por módulo (kg): ', minimo=0.001)
        Modulo.COMBUSTIVEL_CORRECAO_KG = ler_numero(
            'Consumo de cada correção (kg; reserva de duas): ', minimo=0.001)

    def abastecer(self, quantidade_kg):
        if quantidade_kg <= 0:
            raise ValueError("A quantidade para abastecimento deve ser positiva.")

        self.combustivel_pouso_kg += quantidade_kg

    def consumir_combustivel(self, quantidade_kg):
        if quantidade_kg <= 0:
            raise ValueError("A quantidade consumida deve ser positiva.")

        if self.combustivel_pouso_kg < quantidade_kg:
            return False

        self.combustivel_pouso_kg -= quantidade_kg
        return True

    def detectar_objeto(self, probabilidade):
        if not 0 <= probabilidade <= 1:
            raise ValueError("A probabilidade deve estar entre 0 e 1.")

        return random() < probabilidade

    def _registrar_etapa_pouso(self, etapa):
        self.registro_pouso.append({
            "altura_m": self.altitude_m,
            "etapa": etapa,
            "velocidade_m_s": self.velocidade_m_s,
        })

    def pousar(self):
        if self.pouso_concluido:
            return True

        self.registro_pouso = []

        for altura in (
            self.altitude_orbita_m,
            self.ALTITUDE_ENTRADA_M,
            11_000,
            8_000,
            1_600,
            50,
            0,
        ):
            self.altitude_m = altura

            match altura:
                # Início da descida orbital.
                case altitude if altitude == self.altitude_orbita_m:
                    self.velocidade_m_s = 3_500.0
                    etapa = "Inicio da descida orbital"

                # Entrada na atmosfera.
                case 125_000:
                    self.velocidade_m_s = 3_400.0
                    etapa = "Entrada na atmosfera"

                # Frenagem atmosférica e abertura do paraquedas.
                case 11_000:
                    self.velocidade_m_s = 405.0
                    etapa = "Frenagem atmosférica e abertura do paraquedas"

                # Orientação para o ponto de pouso.
                case 8_000:
                    self.velocidade_m_s = 125.0
                    etapa = "Orientação para o ponto de pouso"

                # Detecção de obstáculos e correção da trajetória.
                case 1_600:
                    self.velocidade_m_s = 80.0

                    # Máximo de duas correções, como previsto na reserva.
                    correcoes = 0
                    while correcoes < 2 and self.detectar_objeto(0.1):
                        correcoes += 1
                        if not self.consumir_combustivel(
                            self.COMBUSTIVEL_CORRECAO_KG
                        ):
                            self._registrar_etapa_pouso(
                                "Falha: combustível insuficiente para corrigir a trajetória"
                            )
                            self.integridade = False
                            return False

                        self._registrar_etapa_pouso(
                            "Objeto detectado; correção de trajetória"
                        )

                    etapa = "Detecção de obstáculos: área livre"

                # Disparo dos retrofoguetes.
                case 50:
                    self.velocidade_m_s = 52.0

                    if not self.consumir_combustivel(
                        self.COMBUSTIVEL_FRENAGEM_KG
                    ):
                        etapa = "Falha: combustível insuficiente para a frenagem"
                        self._registrar_etapa_pouso(etapa)
                        self.integridade = False
                        return False

                    etapa = "Disparo dos retrofoguetes e desaceleração"

                # Contato com o solo.
                case 0:
                    self.velocidade_m_s = 0.75
                    self.pouso_concluido = True
                    etapa = "Contato com o solo"

            self._registrar_etapa_pouso(etapa)

        return self.pouso_concluido
