# Sistema Inteligente de Gerenciamento de Recursos da Colônia

Projeto acadêmico desenvolvido em Python para representar, de forma integrada, o monitoramento e a gestão de recursos de uma colônia. A aplicação organiza dados em estruturas hierárquicas, aplica regras de decisão e usa regressão linear simples para estimar a geração de energia eólica.

## Objetivo

Transformar informações sobre energia, consumo, clima e sistemas da colônia em análises e recomendações simples. O projeto demonstra a organização de dados, a navegação entre subsistemas, a aplicação de lógica condicional e o uso de dados históricos para fazer uma estimativa.

## O que o sistema faz

- Organiza os dados da colônia em dicionários hierárquicos.
- Exibe a hierarquia e permite consultar um valor por um caminho, como `colonia/energia/solar`.
- Verifica níveis de energia solar e eólica, combustível, temperaturas e estado dos sistemas.
- Compara geração e consumo e informa déficit, excedente ou equilíbrio; também identifica o sistema ativo de maior consumo.
- Aplica regras de decisão para recomendar redução de consumo, modo econômico ou armazenamento de excedentes.
- Ajusta uma reta por mínimos quadrados com os dados históricos de vento e geração eólica, e estima a geração para uma velocidade informada.
- Simula recomendações para eventos climáticos predefinidos.
- Permite registrar novas leituras diárias no histórico durante a execução.
- Ativa e desativa um modo econômico que mantém o suporte à vida ligado e desliga os sistemas não essenciais (laboratório e iluminação), reduzindo o consumo. Ao desativar, os sistemas voltam ao estado anterior.

## Como os dados e as regras estão organizados

Os dados correntes ficam em `dados/dados.py`, em um dicionário com as chaves `energia`, `combustivel`, `clima` e `sistema`. Os dados históricos ficam em `dados/historico.py`, separados em listas de geração solar, geração eólica, velocidade do vento, temperatura externa e consumo.

A lógica de decisão está em `sistema/decisao.py`. Por exemplo, com energia abaixo de 50 e consumo de pelo menos 80, o sistema recomenda ativar o modo econômico; com energia abaixo de 50, mas consumo menor, recomenda reduzir o consumo. A análise de balanço em `sistema/energia.py` compara geração e consumo: consumo maior indica alerta, geração maior sugere armazenar excedente e valores iguais indicam equilíbrio.

A previsão eólica usa a velocidade do vento como variável de entrada e a geração eólica como variável estimada. A regressão é calculada a partir do histórico existente e o programa avisa quando a velocidade informada está fora do intervalo observado. É uma estimativa simples, não uma garantia de geração futura.

## Exemplo de entrada e saída

**Decisão (opção 4 → 2, simular valores).** Com energia 40 e consumo 70, o sistema aplica a regra de menor energia e responde:

```
Energia (0 a 100): 40
Consumo: 70
Geração: 0
Decisão: ALERTA: reduzir consumo
```

Com energia 40 e consumo 90 (consumo alto), a regra de maior prioridade é acionada:

```
Decisão: MODO ECONOMIA: desligar sistemas não essenciais
```

**Análise de geração e consumo (opção 4 → 2).** Com energia 80, consumo 70 e geração 40:

```
Decisão: ALERTA: consumo maior que geração
```

Com energia 80, consumo 30 e geração 80:

```
Decisão: SUGESTÃO: armazenar energia excedente
```

**Previsão (opção 6).** Com vento de `11 m/s`, o histórico atual produz uma estimativa próxima de `27.5`:

```
Velocidade do vento prevista (m/s): 11
Energia eólica prevista: 27.5
```

**Análise geração x consumo (opção 7).** Usa os dados atuais da colônia (geração solar + eólica e sistemas ligados):

```
Geração: 100 | Consumo: 85 | Saldo: 15
SUGESTÃO: armazenar energia excedente
Maior consumidor: suporte_vida (35)
```

## Executar o projeto

### Pré-requisitos

- Python 3.10 ou superior (o menu usa `match/case`, disponível a partir do Python 3.10).
- Git, caso queira clonar o repositório.

Não são necessárias bibliotecas externas.

### Clonar e iniciar

```
git clone https://github.com/Guthias/fiap-fase-3.git
cd fiap-fase-3
python main.py
```

Em alguns ambientes, use `python3 main.py`.

## Menu da aplicação

Ao iniciar `main.py`, o programa apresenta as seguintes opções:

1. Ver a hierarquia da colônia.
2. Consultar um valor por caminho.
3. Verificar os dados da colônia.
4. Executar o sistema de decisão com dados atuais ou valores simulados.
5. Ativar ou desativar o modo econômico.
6. Prever energia eólica por regressão linear.
7. Analisar geração, consumo, saldo e maior consumidor.
8. Simular um evento climático.
9. Registrar um novo dia no histórico.
0. Sair.

## Estrutura do projeto

```
├── main.py                 # Ponto de entrada e fluxo do programa
├── menu_principal.py       # Menu principal em formato de card
├── README.md
├── dados/
│   ├── consumo.py          # Consumo dos sistemas ativos e geração atual
│   ├── dados.py            # Estado inicial da colônia
│   ├── historico.py        # Séries históricas e registro de novas leituras
│   ├── limite.py           # Limites de segurança usados na verificação
│   └── navegacao.py        # Exibição e consulta da hierarquia
├── previsao/
│   ├── eventos.py          # Eventos climáticos e recomendações
│   ├── gastos.py           # Balanço energético e maior consumidor
│   └── regressao.py        # Ajuste da reta e previsão eólica
├── sistema/
│   ├── decisao.py          # Regras de decisão com prioridade
│   ├── energia.py          # Comparação entre geração e consumo
│   ├── modo_economico.py   # Verificação de dados e modo econômico
│   └── utilidades.py       # Leitura de valores numéricos
└── visuais/
    └── exibir_card.py      # Exibição do menu em formato de card
```

O fluxo principal atualmente é iniciado por `main.py`, que apresenta o menu no terminal. O registro de novos dias é mantido em memória e não persiste depois que a aplicação é encerrada.

## Escopo e observações

- O modo econômico desliga laboratório e iluminação e mantém o suporte à vida ligado, o que reduz o consumo calculado. Ao desativá-lo, restaura o estado anterior dos sistemas.
- A reserva energética é usada em algumas regras e simulações, mas a análise de geração e consumo compara a geração solar e eólica com o consumo dos sistemas ligados.
- A opção 4 com os dados atuais usa a reserva (50) como energia; para ver os alertas e o modo economia, use a simulação com valores digitados.
- Os eventos climáticos retornam recomendações simuladas; eles não alteram automaticamente os dados da colônia.
- O sistema é uma simulação acadêmica, não um controlador de recursos de uma instalação real.

## Contexto acadêmico

O projeto atende à proposta de integrar organização de dados, lógica de decisão, análise do uso de energia e previsão simples com regressão, priorizando clareza, funções e conceitos introdutórios de programação. Neste projeto, não utilizamos banco de dados nem recursos de desenvolvimento mais avançados. Os dados ficam em estruturas mantidas na memória enquanto o programa está aberto; por isso, os registros feitos durante a execução não são preservados depois que ele é encerrado.
