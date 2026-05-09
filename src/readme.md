# PyC-Compare

Comparação de desempenho entre uma implementação de hash table em **C** e o `dict` nativo do **Python**.

Projeto da disciplina AEDII — 2026.

## Estrutura do Projeto

```
PyC-Compare/
├── src/                        # Código-fonte
│   ├── main.c                  # Benchmark C (tempo + memória)
│   ├── tableInt.c / .h         # Hash table para inteiros
│   ├── tableStr.c / .h         # Hash table para strings
│   ├── ordAlg.c / .h           # Algoritmos de ordenação
│   ├── benchmark_python.py     # Benchmark Python (tempo + memória)
│   ├── gerar_dados.py          # Gerador de dados de teste
│   ├── gerar_graficos.py       # Geração de gráficos comparativos
│   └── run_benchmarks.py       # Automação completa
├── dados/                      # Arquivos de teste (.txt)
├── results/                    # CSVs e gráficos gerados
└── programa.exe                # Executável compilado
```

## Pré-requisitos

- **GCC** (MinGW no Windows)
- **Python 3.10+**
- **matplotlib**: `pip install matplotlib`

## Como usar

### 1. Gerar dados de teste

```bash
python src/gerar_dados.py
```

Cria arquivos em `dados/` com 100, 1.000, 10.000, 100.000 e 1.000.000 itens (inteiros e strings).

### 2. Rodar tudo automaticamente

```bash
python src/run_benchmarks.py
```

Este script:
1. Compila o programa C
2. Roda o benchmark C para todos os arquivos de teste
3. Roda o benchmark Python
4. Gera os gráficos comparativos

Os resultados ficam em `results/`.

### 3. Rodar manualmente (opcional)

**Compilar o programa C:**
```bash
gcc src/main.c src/tableInt.c src/tableStr.c src/ordAlg.c -o programa.exe -Wall -O2 -lpsapi
```

**Rodar o benchmark C para um arquivo específico:**
```bash
./programa.exe dados/inteiros_100000.txt inteiro 100000
./programa.exe dados/strings_10000.txt string 10000
```

**Rodar apenas o benchmark Python:**
```bash
python src/benchmark_python.py
```

**Gerar apenas os gráficos (requer CSVs já existentes):**
```bash
python src/gerar_graficos.py
```

## Implementação em C

### Hash Table
- **Endereçamento aberto** com resolução de colisões por **double hashing**
- `h1(k) = k % mapSize` (hash primário)
- `h2(k) = primo_aux - (k % primo_aux)` (tamanho do pulo)
- Nova posição: `(h1 + tentativa * h2) % mapSize`
- Tamanho da tabela é sempre um **número primo** (garante coprimalidade)

### Remoção
- Usa **sentinela** (`INT_MIN` para inteiros, `NULL` para strings) — o slot continua marcado como ocupado
- Quando a ocupação cai abaixo de **25%**, a tabela é **redimensionada** para ~2/3 de ocupação e todos os elementos são **re-hashados**

### Algoritmos de Ordenação
- **Insertion Sort** — O(n²)
- **Merge Sort** — O(n log n)
- **Quick Sort** — O(n log n) médio

## Métricas medidas

| Métrica | C | Python |
|---|---|---|
| Tempo de execução | `clock()` | `time.perf_counter()` |
| Pico de memória | `GetProcessMemoryInfo()` (Windows API) | `tracemalloc` |

## Operações testadas

- Inserção na hash table / dict
- Busca de todos os elementos
- Remoção de todos os elementos
- Ordenação (3 algoritmos em C vs `sorted()` em Python)
