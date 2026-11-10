from _modulos import ler_numero, validar_objeto
from menus.ordenar import ordenar_fila
from modulos.habitacao import Habitacao
from modulos.combustivel import Combustivel
from modulos.energia import Energia
from modulos.temperatura import Temperatura
from modulos.laboratorio import Laboratorio
from modulos.logistica import Logistica
from modulos.suporte_medico import SuporteMedico
from modulos.modulos import Modulo
from visuais.exibir_card import exibir_card

class Nave:
    def __init__(self):
        self.modulos = {
            "habitacao": {
                "classe": Habitacao,
                "nome": "Tripulação e suporte à vida",
                "prioridade" : 5 ,
                "objeto": None
            },

            "combustivel": {
                "classe": Combustivel,
                "nome": "Combustível",
                "prioridade" : -1,
                "objeto": None
            },

            "energia": {
                "classe": Energia,
                "nome": "Energia",
                "prioridade" : 4,
                "objeto": None
            },

            "temperatura": {
                "classe": Temperatura,
                "nome": "Temperatura Interna e Externa",
                "prioridade" : 3,
                "objeto": None
            },

            "laboratorio": {
                "classe": Laboratorio,
                "nome": "Laboratório",
                "prioridade" : 2,
                "objeto": None
            },

            "logistica": {
                "classe": Logistica,
                "nome": "Logística",
                "prioridade" : 2 ,
                "objeto": None
            },

            "suporte_medico": {
                "classe": SuporteMedico,
                "nome": "Suporte Médico",
                "prioridade" : 4,
                "objeto": None
            }
        }

        self.lista_modulos = []
        self.fila = []
        self.pousados = []
        self.em_espera = []
        self.alerta = []
        self.pilha_historico = []
        self.atmosfera_ok = True
        self.area_livre = True
        self.tempo_minutos = 0

    def configurar_modulo(self, tipo):
        modulo = self.modulos[tipo]

        try:
            objeto = modulo["classe"].cadastrar()
            validar_objeto(objeto)
            unidade = UnidadePouso.coletar(tipo, objeto, modulo['prioridade'])
        except ValueError as erro:
            print('Cadastro cancelado:', erro)
            return
        modulo['objeto'] = objeto
        modulo['prioridade'] = unidade.prioridade
        objeto.prioridade = unidade.prioridade
        self.lista_modulos.append(unidade)
        self.fila.append(unidade)

    def exibir_modulo(self, tipo):
        modulo = self.modulos[tipo]

        if modulo["objeto"] is not None:
            modulo["objeto"].exibir()

    def editar_modulo(self, tipo):
        modulo = self.modulos[tipo]

        if modulo["objeto"] is not None:
            objeto = modulo['objeto']
            unidade = self.buscar_tipo(tipo)
            if unidade in self.pousados:
                print('Módulo já pousado: edição operacional indisponível.')
                return
            anteriores = vars(objeto).copy()
            try:
                objeto.editar()
                validar_objeto(objeto)
                dados = UnidadePouso.coletar(tipo, objeto, objeto.prioridade)
            except ValueError as erro:
                objeto.__dict__.clear()
                objeto.__dict__.update(anteriores)
                print('Edição cancelada; dados anteriores preservados:', erro)
                return
            unidade.__dict__.update(vars(dados))
            modulo['prioridade'] = unidade.prioridade
            objeto.prioridade = unidade.prioridade
            if unidade in self.alerta:
                self.alerta.remove(unidade)
            if unidade in self.em_espera:
                self.em_espera.remove(unidade)
            if unidade not in self.fila:
                self.fila.append(unidade)

    @staticmethod
    def _classificar_condicoes(
        combustivel_suficiente,
        modulo_integro,
        atmosfera_favoravel,
    ):
        condicoes = (
            combustivel_suficiente,
            modulo_integro,
            atmosfera_favoravel,
        )
        if any(not isinstance(condicao, bool) for condicao in condicoes):
            raise ValueError("Condições devem ser booleanas.")

        condicoes_criticas_atendidas = (
            combustivel_suficiente and modulo_integro
        )
        alerta = not condicoes_criticas_atendidas
        em_espera = condicoes_criticas_atendidas and not atmosfera_favoravel

        decisao = (
            "alerta" if alerta
            else "em_espera" if em_espera
            else "autorizado"
        )
        return decisao

    def _avaliar_autorizacao(
        self,
        objeto,
        combustivel_suficiente,
        atmosfera_favoravel,
    ):
        unidade = self.buscar_tipo(objeto.tipo) if objeto is not None else None
        energia = self.modulos['energia']['objeto']
        energia_ok = energia is not None and energia.integridade and energia.percentual_carga >= 20
        sensores_ok = unidade is not None and unidade.sensores_ok
        combustivel_veiculo_ok = unidade is not None and unidade.combustivel_percentual >= 50
        chegou = unidade is not None and unidade.chegada_minutos <= self.tempo_minutos
        return self._classificar_condicoes(
            bool(combustivel_suficiente and energia_ok and combustivel_veiculo_ok),
            bool(objeto is not None and objeto.integridade and sensores_ok),
            bool(atmosfera_favoravel and self.atmosfera_ok and self.area_livre and chegou),
        )

    def _verificar_modulos(self):
        combustivel = self.modulos["combustivel"]["objeto"]
        temperatura = self.modulos["temperatura"]["objeto"]

        combustivel_por_modulo = (
            Modulo.COMBUSTIVEL_FRENAGEM_KG
            + 2 * Modulo.COMBUSTIVEL_CORRECAO_KG
        )
        pendentes = sum(1 for info in self.modulos.values()
                        if info['objeto'] is None or not info['objeto'].pouso_concluido)
        combustivel_necessario = pendentes * combustivel_por_modulo
        combustivel_suficiente = (
            combustivel is not None
            and (combustivel.integridade or pendentes == 0)
            and combustivel.combustivel_kg >= combustivel_necessario
        )
        temperatura_interna_ok = (
            temperatura is not None
            and temperatura.integridade
            and 15 <= temperatura.temperatura_interna <= 35
        )
        temperatura_externa_ok = (
            temperatura is not None
            and temperatura.integridade
            and 5 <= temperatura.temperatura_externa <= 45
        )
        atmosfera_favoravel = temperatura_interna_ok and temperatura_externa_ok

        linhas = []
        algum_autorizado = False
        for tipo, info in self.modulos.items():
            objeto = info["objeto"]
            resultado = self._avaliar_autorizacao(
                objeto,
                combustivel_suficiente,
                atmosfera_favoravel,
            )
            unidade = self.buscar_tipo(tipo)
            if objeto is not None and objeto.pouso_concluido:
                resultado = 'autorizado'
            elif unidade is not None:
                self.registrar_estado(unidade, 'aguardando' if resultado == 'autorizado' else resultado)
            autorizado = resultado == "autorizado"
            algum_autorizado = algum_autorizado or (autorizado and objeto is not None and not objeto.pouso_concluido)
            status_modulo = (
                "não cadastrado" if objeto is None
                else "íntegro" if objeto.integridade
                else "inoperante"
            )
            linhas.append(
                f"{'✅' if autorizado else '❌'} {tipo}: "
                f"{status_modulo}, {resultado}"
            )

        linhas.extend((
            f"Temperatura interna: {'Ok' if temperatura_interna_ok else 'Falha'}",
            f"Temperatura externa: {'Ok' if temperatura_externa_ok else 'Falha'}",
            f"Combustível necessário: {combustivel_necessario:.2f} kg",
            f"Combustível disponível: {combustivel.combustivel_kg:.2f} kg"
            if combustivel is not None
            else "Combustível disponível: não cadastrado",
        ))
        exibir_card(
            "Autorização de pouso",
            "Verificação de cadastro e condições por módulo:",
            linhas,
        )
        input("Pressione Enter para continuar...")
        return algum_autorizado

    def pousar_modulo(self, tipo):
        modulo = self.modulos[tipo]

        if modulo["objeto"] is not None:
            modulo["objeto"].pousar()

    def simular_missao(self):
        Modulo.configurar_consumos()
        self.tempo_minutos = ler_numero('Instante da missão (min): ', minimo=0)
        self.atmosfera_ok = ler_numero('Atmosfera favorável (1 sim, 0 não): ', True, 0, 1) == 1
        self.area_livre = ler_numero('Área livre (1 sim, 0 não): ', True, 0, 1) == 1
        if not self._verificar_modulos():
            exibir_card(
                "Missão não iniciada",
                "As verificações iniciais não foram aprovadas.",
                ["Corrija os módulos e tente novamente."],
            )
            input("Pressione Enter para continuar...")
            return False

        combustivel = self.modulos["combustivel"]["objeto"]
        quantidade_por_modulo = (
            Modulo.COMBUSTIVEL_FRENAGEM_KG
            + 2 * Modulo.COMBUSTIVEL_CORRECAO_KG
        )
        ordenar_fila(self.fila)
        # Preserva a decisão explícita do time: combustível sempre por último.
        fila_pouso = [(u.tipo, self.modulos[u.tipo]) for u in self.fila if u.tipo != 'combustivel' and u.estado == 'aguardando']
        fila_pouso.extend((u.tipo, self.modulos[u.tipo]) for u in self.fila if u.tipo == 'combustivel' and u.estado == 'aguardando')

        resultados = {}
        for tipo, info in fila_pouso.copy():
            objeto = info["objeto"]
            etapa_sucesso = False
            mensagem = ""

            if objeto.pouso_concluido:
                etapa_sucesso = True
                mensagem = "Este módulo já havia pousado."
            elif combustivel.combustivel_kg < quantidade_por_modulo:
                mensagem = "Pouso não realizado: combustível insuficiente."
            else:
                combustivel.consumir(quantidade_por_modulo)
                objeto.abastecer(quantidade_por_modulo)
                self.area_livre = False
                try:
                    etapa_sucesso = objeto.pousar()
                finally:
                    self.area_livre = True
                mensagem = (
                    "Pouso realizado com sucesso."
                    if etapa_sucesso
                    else "Falha durante o pouso."
                )

            unidade = self.buscar_tipo(tipo)
            self.registrar_estado(unidade, 'pousados' if etapa_sucesso else 'alerta')
            resultados[tipo] = etapa_sucesso
            fila_pouso.remove((tipo, info))
            proximos = [
                tipo_pendente.capitalize()
                for tipo_pendente, _ in fila_pouso
            ]
            linhas_etapa = [
                mensagem,
                f"Combustível restante: {combustivel.combustivel_kg:.2f} kg",
                "Módulos aguardando:",
                *(proximos or ["Nenhum"]),
            ]

            exibir_card(
                f"Etapa de pouso: {tipo}",
                info["nome"],
                linhas_etapa,
            )

            input("Pressione Enter para continuar...")

        resumo = []
        for tipo, info in self.modulos.items():
            objeto = info["objeto"]
            situacao = (
                "não cadastrado" if objeto is None
                else "operacional" if objeto.integridade
                else "inoperante"
            )
            status_pouso = (
                "pouso realizado" if objeto is not None and objeto.pouso_concluido
                else "pouso não realizado"
            )
            resumo.append(f"{tipo}: {situacao}; {status_pouso}")
        missao_concluida = all(info['objeto'] is not None and info['objeto'].pouso_concluido
                               for info in self.modulos.values())
        resumo.insert(
            0,
            "Resultado da missão: "
            f"{'sucesso' if missao_concluida else 'falha'}",
        )
        exibir_card("Resumo da missão", "Status final dos módulos:", resumo)
        input("Pressione Enter para continuar...")
        return missao_concluida

    def buscar_tipo(self, tipo):
            # Busca linear, adequada ao pequeno conjunto de módulos.
            for unidade in self.lista_modulos:
                if unidade.tipo == tipo:
                    return unidade
            return None

    def buscar_menor_combustivel(self):
            menor = None
            for unidade in self.lista_modulos:
                if menor is None or unidade.combustivel_percentual < menor.combustivel_percentual:
                    menor = unidade
            return menor

    def buscar_maior_prioridade(self):
            maior = None
            for unidade in self.lista_modulos:
                if maior is None or unidade.prioridade > maior.prioridade:
                    maior = unidade
            return maior

    def retirar_ultimo_registro(self):
            # Consulta LIFO; remover registro NÃO desfaz um pouso.
            if self.pilha_historico:
                return self.pilha_historico.pop()
            return None

    def registrar_estado(self, unidade, estado):
        if unidade is None:
            return
        for lista in (self.pousados, self.em_espera, self.alerta):
            if unidade in lista:
                lista.remove(unidade)
        if estado == 'pousados':
            self.pousados.append(unidade)
            if unidade in self.fila:
                self.fila.remove(unidade)
        elif estado == 'em_espera':
            self.em_espera.append(unidade)
        elif estado == 'alerta':
            self.alerta.append(unidade)
        unidade.estado = estado
        self.pilha_historico.append(dict(tipo=unidade.tipo, estado=estado,
                                        tempo_minutos=self.tempo_minutos))

class UnidadePouso:
    # Complemento novo: atributos de pouso sem alterar construtores originais.
    def __init__(self, tipo, objeto, prioridade, combustivel_percentual,
                 massa_kg, chegada_minutos, sensores_ok=True):
        if not (1 <= prioridade <= 5 or (tipo == 'combustivel' and prioridade == -1)) or not 0 <= combustivel_percentual <= 100:
            raise ValueError('Prioridade ou combustível fora dos limites.')
        if massa_kg <= 0 or chegada_minutos < 0:
            raise ValueError('Massa deve ser positiva e chegada não negativa.')
        for valor in (massa_kg, chegada_minutos, combustivel_percentual):
            if valor != valor or valor in (float('inf'), -float('inf')):
                raise ValueError('Dados de pouso devem ser finitos.')
        self.tipo = tipo
        self.objeto = objeto
        self.prioridade = prioridade
        self.criticidade = objeto.criticidade
        self.combustivel_percentual = combustivel_percentual
        self.massa_kg = massa_kg
        self.chegada_minutos = chegada_minutos
        self.sensores_ok = sensores_ok
        self.estado = 'aguardando'

    @classmethod
    def coletar(cls, tipo, objeto, prioridade):
        print('Dados operacionais de pouso para:', tipo)
        if tipo == 'combustivel':
            prioridade = -1
            print('Combustível mantém prioridade -1 e pousa por último.')
        else:
            prioridade = ler_numero('Prioridade (1 a 5; 5 primeiro): ', True, 1, 5)
        combustivel = ler_numero('Combustível do veículo de pouso (%): ', minimo=0, maximo=100)
        massa = ler_numero('Massa total (kg): ', minimo=0.001)
        chegada = ler_numero('Chegada à órbita (min desde início): ', minimo=0)
        sensores = ler_numero('Sensores íntegros? 1=sim, 0=não: ', True, 0, 1) == 1
        return cls(tipo, objeto, prioridade, combustivel, massa, chegada, sensores)