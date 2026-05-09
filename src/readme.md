# PyC-Compare

**Comparação de desempenho entre uma Hash Table implementada em C e o `dict` nativo do Python.**

Projeto da disciplina Algoritmos e Estrutura de Dados II — 2026.

---

## Índice

1. [Objetivo](#objetivo)
2. [Pré-requisitos](#pré-requisitos)
3. [Estrutura do Projeto](#estrutura-do-projeto)
4. [Como Usar](#como-usar)
5. [Como o Programa Funciona](#como-o-programa-funciona)
6. [Operações Testadas](#operações-testadas)
7. [Resultados Gerados](#resultados-gerados)
8. [Detalhes Técnicos](#detalhes-técnicos)

---

## Objetivo

Este projeto implementa uma **Hash Table com endereçamento aberto e Double Hashing** em C e compara seu desempenho contra o `dict` nativo do Python nas seguintes dimensões:

- **Tempo de inserção** — inserir N elementos
- **Tempo de busca** — buscar 10 elementos aleatórios (média)
- **Tempo de remoção** — remover 10 elementos aleatórios (média)
- **Tempo de ordenação** — 3 algoritmos em C vs `sorted()` do Python
- **Consumo de memória** — pico de memória durante inserção
- **Colisões** — como o fator de carga afeta a distribuição de colisões

---

## Pré-requisitos

| Ferramenta | Versão mínima | Para que serve |
|---|---|---|
| **GCC** | MinGW 8+ | Compilar os programas C |
| **Python** | 3.10+ | Benchmark Python e gráficos |
| **matplotlib** | — | Geração de gráficos |

### Instalação do matplotlib

```powershell
pip install matplotlib
```

---

## Estrutura do Projeto

```
PyC-Compare/
│
├── src/                              Código-fonte
│   ├── main.c                        Programa principal (benchmark C)
│   ├── collision_analyzer.c          Analisador de colisões
│   ├── tableInt.c / tableInt.h       Hash table para inteiros
│   ├── tableStr.c / tableStr.h       Hash table para strings
│   ├── ordAlg.c / ordAlg.h           Algoritmos de ordenação
│   ├── benchmark_python.py           Benchmark Python
│   ├── gerar_dados.py                Gerador de dados de teste
│   ├── gerar_graficos.py             Gerador de gráficos e relatório
│   ├── run_benchmarks.py             Script de automação completa
│   └── readme.md                     Este arquivo
│
├── dados/                            Arquivos de teste
│   ├── inteiros_10.txt               10 inteiros aleatórios
│   ├── inteiros_100.txt              100 inteiros aleatórios
│   ├── inteiros_1000.txt             ...
│   ├── inteiros_10000.txt
│   ├── inteiros_100000.txt
│   ├── strings_10.txt                10 strings aleatórias
│   ├── strings_100.txt               ...
│   └── ...
│
├── results/                          Saída dos testes
│   ├── resultados_c.csv              Benchmark C
│   ├── resultados_python_v2.csv      Benchmark Python
│   ├── colisoes.csv                  Dados de colisões
│   ├── tempo_inteiro.png             Gráfico: C vs Python (inteiros)
│   ├── tempo_string.png              Gráfico: C vs Python (strings)
│   ├── ordenacao_inteiro.png         Gráfico: ordenação (inteiros)
│   ├── ordenacao_string.png          Gráfico: ordenação (strings)
│   ├── memoria_inteiro.png           Gráfico: memória (inteiros)
│   ├── memoria_string.png            Gráfico: memória (strings)
│   ├── colisoes_comparacao.png       Gráfico: colisões 100% vs 50%
│   └── relatorio.md                  Relatório completo
│
├── programa.exe                      Benchmark C compilado
└── collision_analyzer.exe            Analisador compilado
```

---

## Como Usar

### Opção 1: Automação completa (recomendado)

Um único comando faz tudo:

```powershell
python src/run_benchmarks.py
```

**O que esse comando faz:**

1. **Gera dados** — cria arquivos de teste em `dados/` (se não existirem)
2. **Compila** — `programa.exe` e `collision_analyzer.exe`
3. **Benchmark C** — roda o programa C para cada tamanho (10, 100, 1K, 10K, 100K)
4. **Colisões** — analisa colisões com fator de carga ~100% e ~50%
5. **Benchmark Python** — roda o benchmark Python com os mesmos dados
6. **Gráficos** — gera todos os gráficos e o relatório em `results/`

### Opção 2: Passo a passo manual

**Etapa 1 — Gerar dados de teste:**
```powershell
python src/gerar_dados.py
```

**Etapa 2 — Compilar:**
```powershell
gcc src/main.c src/tableInt.c src/tableStr.c src/ordAlg.c -o programa.exe -Wall -O2 -lpsapi
gcc src/collision_analyzer.c src/tableInt.c -o collision_analyzer.exe -Wall -O2
```

**Etapa 3 — Rodar benchmark C:**
```powershell
.\programa.exe dados\inteiros_10000.txt inteiro 10000 2
```

Onde:
- `dados\inteiros_10000.txt` = arquivo de entrada
- `inteiro` = tipo dos dados (`inteiro` ou `string`)
- `10000` = quantidade de elementos
- `2` = multiplicador (fator de carga ~50%)

**Etapa 4 — Rodar analisador de colisões:**
```powershell
.\collision_analyzer.exe dados\inteiros_10000.txt 10000 2
```

**Etapa 5 — Rodar benchmark Python:**
```powershell
python src/benchmark_python.py
```

**Etapa 6 — Gerar gráficos:**
```powershell
python src/gerar_graficos.py
```

---

## Como o Programa Funciona

### Hash Table em C

A hash table usa **endereçamento aberto** (todos os elementos ficam no próprio array) com **double hashing** para resolver colisões.

**Inserção:**
1. Calcula `h1(chave)` = posição primária
2. Se a posição está ocupada (colisão), calcula o pulo `h2(chave)`
3. Avança `h2` posições até encontrar um slot vazio
4. Insere o elemento

**Busca:**
1. Calcula `h1(chave)` e verifica
2. Se não é o elemento, avança usando `h2`
3. Para quando encontra o elemento ou um slot vazio

**Remoção:**
1. Encontra o elemento (mesma lógica da busca)
2. Marca o valor como **sentinela** (`INT_MIN` para inteiros, `NULL` para strings)
3. Mantém `occupied = true` para não quebrar a cadeia de probing
4. Se a tabela ficar com menos de **25% de ocupação**, faz **resize + rehash**

### Fator de carga

O multiplicador controla o tamanho da tabela em relação aos dados:

```
mapSize = maiorPrimo(N × multiplicador)
```

| Multiplicador | Fator de carga | Efeito |
|:---:|:---:|---|
| 1 | ~100% | Muitas colisões, mais lento, menos memória |
| 2 | ~50% | Poucas colisões, mais rápido, mais memória |
| 3 | ~33% | Quase sem colisões, mais rápido ainda |

### Benchmark

Para **busca e remoção**, o programa seleciona **10 elementos aleatórios** (com seed fixa para reprodutibilidade) e reporta o **tempo médio** por operação.

Para **inserção e ordenação**, mede o tempo total da operação completa.

### Formato de saída CSV

Tanto o programa C quanto o Python geram linhas CSV no formato:

```
linguagem,tipo_dado,tamanho,operacao,tempo_segundos,memoria_bytes
```

---

## Operações Testadas

| Operação | O que faz | Complexidade |
|---|---|---|
| `hash_insercao` | Insere **todos** os N elementos | O(N) amortizado |
| `hash_busca` | Busca **10 aleatórios**, reporta média | O(1) amortizado |
| `hash_remocao` | Remove **10 aleatórios**, reporta média | O(1) amortizado |
| `insertion_sort` | Ordena todos os elementos | O(N²) |
| `merge_sort` | Ordena todos os elementos | O(N log N) |
| `quick_sort` | Ordena todos os elementos | O(N log N) médio |

---

## Resultados Gerados

Todos os resultados ficam na pasta `results/` após rodar `python src/run_benchmarks.py`:

### CSVs

| Arquivo | Conteúdo |
|---|---|
| `resultados_c.csv` | Tempos e memória de todas as operações em C |
| `resultados_python_v2.csv` | Tempos e memória de todas as operações em Python |
| `colisoes.csv` | Total de colisões, max tentativas, média, etc. |

### Gráficos

| Gráfico | O que mostra |
|---|---|
| `tempo_inteiro.png` | Inserção, busca e remoção: C vs Python (inteiros) |
| `tempo_string.png` | Inserção, busca e remoção: C vs Python (strings) |
| `ordenacao_inteiro.png` | insertion_sort vs merge_sort vs quick_sort vs Python sorted |
| `ordenacao_string.png` | Idem para strings |
| `memoria_inteiro.png` | Pico de memória: hash table C vs dict Python |
| `memoria_string.png` | Idem para strings |
| `colisoes_comparacao.png` | Impacto do fator de carga (100% vs 50%) |

### Relatório

O arquivo `relatorio.md` contém tabelas comparativas com todos os tempos, indicando qual linguagem foi mais rápida em cada operação.

---

## Detalhes Técnicos

### Funções de Hash

**Para inteiros:**
- `h1(k) = k % mapSize`
- `h2(k) = primo_aux - (k % primo_aux)`
- Posição: `(h1 + tentativa × h2) % mapSize`

**Para strings:**
- `h1` = DJB2 (`hash = hash × 33 + c`)
- `h2` = SDBM (`hash = c + hash × 65599`)

### Medição de tempo

| Linguagem | Método |
|---|---|
| C | `clock()` da `<time.h>` |
| Python | `time.perf_counter()` |

### Medição de memória

| Linguagem | Método |
|---|---|
| C | `GetProcessMemoryInfo()` — API Windows (`PeakWorkingSetSize`) |
| Python | `tracemalloc` — mede pico de memória alocada |

### Tamanhos testados

O benchmark roda para os seguintes tamanhos de entrada:

| N | Arquivo inteiros | Arquivo strings |
|---|---|---|
| 10 | `inteiros_10.txt` | `strings_10.txt` |
| 100 | `inteiros_100.txt` | `strings_100.txt` |
| 1.000 | `inteiros_1000.txt` | `strings_1000.txt` |
| 10.000 | `inteiros_10000.txt` | `strings_10000.txt` |
| 100.000 | `inteiros_100000.txt` | `strings_100000.txt` |

Para adicionar tamanhos maiores, edite a variável `TAMANHOS` nos arquivos `gerar_dados.py`, `run_benchmarks.py` e `benchmark_python.py`.
