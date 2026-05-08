"""
gerar_dados.py
==============
Gera dados aleatórios (inteiros e strings) em arquivos .txt
para uso nos testes de benchmark do projeto AEDII 2026.

Uso:
    python gerar_dados.py

Saída:
    dados/inteiros_100.txt
    dados/inteiros_1000.txt
    dados/inteiros_10000.txt
    dados/inteiros_100000.txt
    dados/inteiros_1000000.txt
    dados/strings_100.txt
    ...
"""

import random
import string
import os

# ──────────────────────────────────────────────
# CONFIGURAÇÕES
# ──────────────────────────────────────────────

TAMANHOS = [100, 1_000, 10_000, 100_000, 1_000_000]

INT_MIN = 0
INT_MAX = 1_000_000

STR_MIN_LEN = 4    # tamanho mínimo de cada string
STR_MAX_LEN = 10   # tamanho máximo de cada string

PASTA_SAIDA = "dados"

# ──────────────────────────────────────────────


def gerar_inteiros(quantidade: int) -> list:
    """Gera uma lista de inteiros aleatórios."""
    return [random.randint(INT_MIN, INT_MAX) for _ in range(quantidade)]


def gerar_strings(quantidade: int) -> list:
    """Gera uma lista de strings aleatórias (letras minúsculas)."""
    strings = []
    for _ in range(quantidade):
        tamanho = random.randint(STR_MIN_LEN, STR_MAX_LEN)
        palavra = ''.join(random.choices(string.ascii_lowercase, k=tamanho))
        strings.append(palavra)
    return strings


def salvar_txt(dados: list, nome_arquivo: str) -> None:
    """Salva uma lista de valores em um arquivo .txt (um valor por linha)."""
    with open(nome_arquivo, 'w', encoding='utf-8') as f:
        for item in dados:
            f.write(f"{item}\n")
    print(f"  [OK] {nome_arquivo}  ({len(dados)} itens)")


def main():
    os.makedirs(PASTA_SAIDA, exist_ok=True)

    print("=" * 50)
    print("  Gerador de Dados — AEDII 2026")
    print("=" * 50)

    for tamanho in TAMANHOS:
        print(f"\nGerando {tamanho:,} itens...")

        # Inteiros
        inteiros = gerar_inteiros(tamanho)
        salvar_txt(inteiros, os.path.join(PASTA_SAIDA, f"inteiros_{tamanho}.txt"))

        # Strings
        strings = gerar_strings(tamanho)
        salvar_txt(strings, os.path.join(PASTA_SAIDA, f"strings_{tamanho}.txt"))

    print("\n" + "=" * 50)
    print(f"  Concluído! Arquivos salvos em: ./{PASTA_SAIDA}/")
    print("=" * 50)


if __name__ == "__main__":
    main()
