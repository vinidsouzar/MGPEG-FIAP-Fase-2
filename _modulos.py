modulo = [
#     {
#         "rotulo": "Tripulação e suporte à vida",
#         "tipo": "habitacao",
#         "prioridade": 4,
#         "criticidade": 4,
#         "integridade": True,
#         "detalhes": {
#             "capacidade_pessoas": 8,
#             "oxigenio": x,
#             }
#     }
#     {
#         "rotulo": "Combustivel",
#         "tipo": "combustivel",
#         "prioridade": 5,
#         "criticidade": 5,
#         "combustivel": x,
#         "integridade": True,
#         "detalhes": {
#             "carga": 70,
#             "capacidade_kwh": 100,
#         }
#     }
#     {
#         "rotulo": "Energia",
#         "tipo": "energia",
#         "prioridade": x,
#         "criticidade": 5,
#         "combustivel": x,
#         "energia": 80, #coloquei uma energia base porem ela pode ser alterada e deixei fora do detalhes para que o usuario possa acessar ela sem dificuldades (turatti)
#         "integridade": True,
#         "detalhes": {
#             "capacidade_kwh": 100
#         }
#         }
#         { #criei um modulo de temperatura (turatti)
#         "rotulo": "Temperatura Interna e Externa",
#         "tipo": "temperatura",
#         "prioridade": 3,
#         "criticidade": 1,
#         "temperatura_interna": x,
#         "temeperatura_externa": x,
#         "integridade": True,
#         "detalhes": { 
#             "controle de temperatura interna e externa do modulo",
#             } 
#         }
#         {
#         "rotulo": "Laboratório",
#         "tipo": "laboratorio",
#         "prioridade": 3,
#         "criticidade": 1,
#         "integridade": True,
#         "detalhes": { x,
#         }
#         }
#         {
#         "rotulo": "Logística",
#         "tipo": "logistica",
#         "prioridade": 2,
#         "criticidade": 2,
#         "integridade": True,
#         "detalhes": {
#             "capacidade_carga_kg": x,
#             "alimentos_kg": x,
#         }
#         }
#         {
#         "rotulo": "Suporte Médico",
#         "tipo": "suporte_medico",
#         "prioridade":2 ,
#         "criticidade": 3,
#         "integridade": True,
#         "detalhes": {
#             "leitos": x ,
#             "kits_emergencia": x,
#         }
#         }
# ]
]

# Complementos básicos compartilhados: não substituem as classes dos módulos.
def ler_numero(mensagem, inteiro=False, minimo=None, maximo=None):
    while True:
        try:
            texto = input(mensagem).replace(',', '.')
            valor = int(texto) if inteiro else float(texto)
            if valor != valor or valor in (float('inf'), -float('inf')):
                raise ValueError('Informe um número finito.')
            if minimo is not None and valor < minimo:
                raise ValueError('Valor abaixo do mínimo.')
            if maximo is not None and valor > maximo:
                raise ValueError('Valor acima do máximo.')
            return valor
        except ValueError as erro:
            print('Entrada inválida:', erro)

def validar_objeto(objeto):
    # Temperaturas podem ser negativas; quantidades físicas, não.
    for nome, valor in vars(objeto).items():
        if isinstance(valor, (int, float)) and not isinstance(valor, bool) and not nome.startswith('autonomia_') and nome != 'prioridade':
            if valor != valor or valor in (float('inf'), -float('inf')):
                raise ValueError('Dados devem ser finitos.')
            if not nome.startswith('temperatura_') and valor < 0:
                raise ValueError(nome + ' não pode ser negativo.')
    for capacidade, atual in [('capacidade_tanque_kg', 'combustivel_kg'),
                              ('capacidade_bateria_kwh', 'carga_kwh'),
                              ('capacidade_pessoas', 'pessoas_atuais'),
                              ('capacidade_carga_kg', 'alimentos_kg')]:
        if hasattr(objeto, capacidade):
            if getattr(objeto, capacidade) <= 0:
                raise ValueError(capacidade + ' deve ser positivo.')
            if getattr(objeto, atual) > getattr(objeto, capacidade):
                raise ValueError(atual + ' excede a capacidade.')
    for nome in ['consumo_kg_segundo', 'consumo_medio_kw']:
        if hasattr(objeto, nome) and getattr(objeto, nome) <= 0:
            raise ValueError(nome + ' deve ser positivo.')
    if not (1 <= objeto.prioridade <= 5 or (objeto.tipo == 'combustivel' and objeto.prioridade == -1)) or not 1 <= objeto.criticidade <= 5:
        raise ValueError('Prioridade e criticidade devem estar entre 1 e 5.')