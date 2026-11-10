MGPEB — Missão Marte

Projeto em Python para gerenciar módulos de uma nave e simular uma sequência de pousos em Marte, utilizando um menu no terminal. Os dados e consumos da simulação são hipotéticos.

Funcionalidades
•Configurar, visualizar e editar módulos da nave.
•Gerenciar habitação, combustível, energia, temperatura, laboratório, logística e suporte médico.
•Calcular disponibilidade e autonomia de recursos.
•Organizar a fila de prioridade dos módulos.
•Verificar condições e simular a missão de pouso.

Tecnologias
•Python.
•Programação orientada a objetos.
•Interface textual pelo terminal.

Estrutura do projeto
menus/
    configurar_modulo.py
    editar_modulo.py
    menu_modulos.py
    menu_principal.py
    motor_decisao.py
    ordenar.py
    visualizar_modulo.py
modulos/
    combustivel.py
    energia.py
    habitacao.py
    laboratorio.py
    logistica.py
    modulos.py
    suporte_medico.py
    temperatura.py
visuais/
    exibir_card.py
.gitignore
README.md
REQUISITOS.MD
_modulos.py
main.py
nave.py

•menus/: telas e funções de interação com o usuário.
•modulos/: classes dos módulos da nave.
•visuais/: apresentação dos cards no terminal.
•main.py: ponto de entrada do programa.
•nave.py: gerenciamento da nave e integração dos módulos.
•REQUISITOS.MD: documentação dos requisitos e regras do sistema.

Como executar
1.	Instale o Python. Para a versão que utiliza match/case, use Python 3.10 ou superior.
2.	Baixe ou clone o repositório.
3.	Abra o terminal na pasta principal do projeto, onde está o arquivo main.py.
4.	Execute:
python main.py

Se o comando do seu ambiente for python3, utilize:
python3 main.py

Mantenha as pastas e os arquivos na estrutura do repositório.
Como utilizar
1.	Configure os módulos pelo menu principal.
2.	Visualize os dados e faça as edições necessárias.
3.	Consulte a fila de prioridade.
4.	Inicie a simulação da missão e acompanhe os resultados apresentados no terminal.
Objetivo acadêmico
Aplicar conceitos de programação orientada a objetos, organização de código em módulos, gerenciamento de recursos e tomada de decisão em uma simulação simplificada.
