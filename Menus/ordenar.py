
def fila_ordenada(fila):
    """Exibe somente os módulos da fila operacional, na mesma ordem."""
    print('\n--- FILA OPERACIONAL DE POUSO ---')
    if not fila:
        print('Nenhum módulo aguardando.')
    for unidade in fila:
        print(f'- {unidade.tipo}: prioridade={unidade.prioridade}, '
              f'criticidade={unidade.criticidade}, '
              f'combustível={unidade.combustivel_percentual:.1f}%, '
              f'chegada={unidade.chegada_minutos} min')
    input('\nPressione Enter para voltar ao menu...')

def ordenar_fila(fila):
    # Bubble sort estável: prioridade maior, criticidade menor,
    # combustível menor e chegada anterior. Empates preservam cadastro.
    itens = list(fila)
    for i in range(len(itens) - 1):
        for j in range(len(itens) - 1 - i):
            a, b = itens[j], itens[j + 1]
            chave_a = (a.tipo == 'combustivel', -a.prioridade, a.criticidade, a.combustivel_percentual, a.chegada_minutos)
            chave_b = (b.tipo == 'combustivel', -b.prioridade, b.criticidade, b.combustivel_percentual, b.chegada_minutos)
            if chave_a > chave_b:
                itens[j], itens[j + 1] = b, a
    fila.clear()
    fila.extend(itens)
    return itens