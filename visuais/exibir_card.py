def exibir_card(titulo, subtitulo, conteudo):
    
    largura = 50
    print("\033[H\033[J", end="")
    print()
    print("╔" + "═" * largura + "╗")
    print("║" + " MISSÃO MARTE".center(largura) + "║")
    print("╠" + "═" * largura + "╣")
    print("║" + titulo.center(largura) + "║")
    print("║" + subtitulo.center(largura) + "║")
    print("╠" + "═" * largura + "╣")

    for linha in conteudo:
        print("║" + linha.ljust(largura)[:largura] + "║")

    print("╚" + "═" * largura + "╝")