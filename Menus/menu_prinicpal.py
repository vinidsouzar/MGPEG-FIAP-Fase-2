from visuais.exibir_card import exibir_card
from Menus.Configurar_modulo import configurar_modulo
from Menus.visualizar_modulo import visualizar_modulo
from Menus.Editar_modulo import editar_modulo
from Menus.ordenar import fila_ordenada
from Menus.motor_decisao import motor_decisao
from nave import Nave

def exibir_menu():
    exibir_card(
        "CENTRAL DE CONTROLE",
        "Menu principal",
        [
            "",
            "1. Configurar módulo",
            "2. Visualizar módulo",
            "3. Editar módulo",
            "4. Simular missão",
            "5. Exibir fila de prioridade",
            "6. Verificar requisitos",
            "7. Buscar módulos",
            "8. Consultar pilha de histórico",
            "9. Carregar exemplo hipotético",
            "0. Encerrar missão",
            ""
        ]
    )

def executar_menu(nave):
    while True:
        exibir_menu()
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Digite apenas números.")
            continue
        match opcao:
            case 1:
                configurar_modulo(nave)
            case 2:
                visualizar_modulo(nave)
            case 3:
                editar_modulo(nave)
            case 4:
                nave.simular_missao()
            case 5:
                from Menus.ordenar import ordenar_fila
                ordenar_fila(nave.fila)
                print([(u.tipo, u.prioridade, u.criticidade) for u in nave.fila])
                fila_ordenada(nave.fila)
            case 6:
                motor_decisao(nave.modulos)
            case 7:
                tipo = input('Tipo para busca: ')
                for titulo, resultado in [('Tipo', nave.buscar_tipo(tipo)),
                                          ('Menor combustível', nave.buscar_menor_combustivel()),
                                          ('Maior prioridade', nave.buscar_maior_prioridade())]:
                    print(titulo, vars(resultado) if resultado else 'Não encontrado')
                input('ENTER para voltar...')
            case 8:
                print(nave.pilha_historico[-1].copy() if nave.pilha_historico else 'Sem registros')
                if input('Retirar o topo da pilha? (s/n): ').strip().lower() == 's':
                    print(nave.retirar_ultimo_registro())
                input('ENTER para voltar...')
            case 9:
                carregar_exemplo(nave)
                input('ENTER para voltar...')
            case 0:
                exibir_card(
                    "MISSÃO FINALIZADA",
                    "Obrigado pela jornada!",
                    []
                )
                break
            case _:
                print("Opção inválida. Tente novamente.")

def carregar_exemplo(nave):
    """Dados novos exclusivamente para demonstração, não parâmetros reais."""
    if nave.lista_modulos:
        print('Exemplo só pode ser carregado em nave vazia.')
        return
    from nave import UnidadePouso
    from modulos.habitacao import Habitacao
    from modulos.combustivel import Combustivel
    from modulos.energia import Energia
    from modulos.temperatura import Temperatura
    from modulos.laboratorio import Laboratorio
    from modulos.logistica import Logistica
    from modulos.suporte_medico import SuporteMedico
    objetos = [Habitacao(8, 4, 20, 100), Combustivel(300, 280, 1),
               Energia(100, 80, 2), Temperatura(20, 20), Laboratorio(),
               Logistica(100, 30), SuporteMedico(2, 4)]
    for objeto in objetos:
        prioridade = nave.modulos[objeto.tipo]['prioridade']
        unidade = UnidadePouso(objeto.tipo, objeto, prioridade, 80, 100, 0)
        objeto.prioridade = prioridade
        nave.modulos[objeto.tipo]['objeto'] = objeto
        nave.lista_modulos.append(unidade)
        nave.fila.append(unidade)
    print('Exemplo carregado: estoque hipotético de 280 kg. Informe os consumos ao simular.')