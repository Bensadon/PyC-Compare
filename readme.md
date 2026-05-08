# PyC-Compare

Implementação de um dicionário similar ao `dict` do Python, escrito em C, com medição de desempenho comparativa.

## Estrutura em C

Hash Table com **endereçamento aberto** e resolução de colisões por **double hashing**.

- Entradas de até 100M de itens
- Chaves únicas (sem duplicatas)
- Itens suportados: inteiros (`int`) e strings (`char *`)
- Operações implementadas: inserção, remoção, busca e ordenação

## Arquivos

| Arquivo | Descrição |
|---|---|
| `main.c` | Entrada do programa, leitura de dados e medição de tempo |
| `tableInt.c` | Hash table para chaves inteiras |
| `tableStr.c` | Hash table para chaves string |
| `ordAlg.c` | Algoritmos de ordenação (counting sort, merge sort, quick sort) |

## Resolução de Colisões

Usa **double hashing**:
- `hashInt1(valor, mapSize)` → hash primário: `valor % mapSize`
- `hashInt2(valor, mapSize, tentativa)` → hash secundário: a implementar

O tamanho da tabela (`mapSize`) é sempre um número primo para minimizar colisões.