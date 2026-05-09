# PyC-Compare

Comparação de desempenho entre uma implementação de hash table em **C** e o `dict` nativo do **Python**.

Projeto da disciplina AEDII — 2026.

## Estrutura do Projeto

```
PyC-Compare/
├── src/                           # Código-fonte
│   ├── main.c                     # Benchmark C (tempo + memória)
│   ├── collision_analyzer.c       # Analisador de colisões da hash table
│   ├── tableInt.c / .h            # Hash table para inteiros
│   ├── tableStr.c / .h            # Hash table para strings
│   ├── ordAlg.c / .h              # Algoritmos de ordenação
│   ├── benchmark_python.py        # Benchmark Python (tempo + memória)
│   ├── gerar_dados.py             # Gerador de dados de teste
│   ├── gerar_graficos.py          # Geração de gráficos e relatório
│   └── run_benchmarks.py          # Automação completa
├── dados/                         # Arquivos de teste (.txt)
├── results/                       # CSVs, gráficos e relatórios
├── programa.exe                   # Benchmark compilado
└── collision_analyzer.exe         # Analisador compilado
```

## Pré-requisitos

- **GCC** (MinGW no Windows)
- **Python 3.10+**
- **matplotlib**: `pip install matplotlib`

## Como usar

### Modo rápido (automação completa)

```bash
python src/run_benchmarks.py
```

Este script executa tudo em sequência:
1. Compila `programa.exe` e `collision_analyzer.exe`
2. Roda o benchmark C para todos os tamanhos (100, 1.000, 10.000)
3. Roda o analisador de colisões com fator de carga ~100% e ~50%
4. Roda o benchmark Python
5. Gera todos os gráficos e o relatório em Markdown

### Modo manual

**Gerar dados de teste:**
```bash
python src/gerar_dados.py
```

**Compilar:**
```bash
gcc src/main.c src/tableInt.c src/tableStr.c src/ordAlg.c -o programa.exe -Wall -O2 -lpsapi
gcc src/collision_analyzer.c src/tableInt.c -o collision_analyzer.exe -Wall -O2
```

**Rodar benchmark C:**
```bash
# Uso: programa.exe <arquivo> <tipo> <tamanho> <multiplicador>
# multiplicador: 1 = fator ~100%, 2 = fator ~50%, 3 = fator ~33%

.\programa.exe dados\inteiros_10000.txt inteiro 10000 2
.\programa.exe dados\strings_1000.txt string 1000 2
```

**Rodar analisador de colisões:**
```bash
# Uso: collision_analyzer.exe <arquivo> <tamanho> <multiplicador>

.\collision_analyzer.exe dados\inteiros_10000.txt 10000 1    # fator ~100%
.\collision_analyzer.exe dados\inteiros_10000.txt 10000 2    # fator ~50%
```

**Rodar benchmark Python:**
```bash
python src/benchmark_python.py
```

**Gerar gráficos (requer CSVs já existentes):**
```bash
python src/gerar_graficos.py
```

## Implementação em C

### Hash Table (Endereçamento Aberto + Double Hashing)

- `h1(k) = k % mapSize` — hash primário
- `h2(k) = primo_aux - (k % primo_aux)` — tamanho do pulo
- Nova posição: `(h1 + tentativa * h2) % mapSize`
- Tamanho da tabela é sempre um **número primo** (garante coprimalidade com h2)
- Para strings: usa **DJB2** (h1) e **SDBM** (h2)

### Fator de Carga

O `multiplicador` controla o fator de carga da tabela:

| Multiplicador | mapSize | Fator de carga |
|:---:|:---:|:---:|
| 1 | `maiorPrimo(n)` | ~100% |
| 2 | `maiorPrimo(n * 2)` | ~50% |
| 3 | `maiorPrimo(n * 3)` | ~33% |

### Remoção

- Usa **sentinela** (`INT_MIN` para inteiros, `NULL` para strings)
- O slot continua marcado como `occupied = true` para não quebrar a cadeia de probing
- Quando a ocupação cai abaixo de **25%**, a tabela faz **resize + rehash** para ~66% de ocupação

### Algoritmos de Ordenação

| Algoritmo | Complexidade |
|---|---|
| Insertion Sort | O(n²) |
| Merge Sort | O(n log n) |
| Quick Sort | O(n log n) médio |

## Métricas medidas

| Métrica | C | Python |
|---|---|---|
| Tempo de execução | `clock()` | `time.perf_counter()` |
| Pico de memória | `GetProcessMemoryInfo()` (Windows API) | `tracemalloc` |

## Resultados gerados

Todos os resultados ficam na pasta `results/`:

| Arquivo | Conteúdo |
|---|---|
| `resultados_c.csv` | Tempos e memória do benchmark C |
| `resultados_python_v2.csv` | Tempos e memória do benchmark Python |
| `colisoes.csv` | Análise de colisões por fator de carga |
| `tempo_inteiro.png` | Gráfico: C vs Python (inteiros) |
| `tempo_string.png` | Gráfico: C vs Python (strings) |
| `ordenacao_inteiro.png` | Gráfico: algoritmos de ordenação (inteiros) |
| `ordenacao_string.png` | Gráfico: algoritmos de ordenação (strings) |
| `colisoes_comparacao.png` | Gráfico: impacto do fator de carga nas colisões |
| `relatorio.md` | Relatório completo em Markdown |

## Operações testadas

- Inserção na hash table / dict
- Busca de todos os elementos
- Remoção de todos os elementos
- Ordenação (3 algoritmos em C vs `sorted()` em Python)
- Análise de colisões com diferentes fatores de carga
