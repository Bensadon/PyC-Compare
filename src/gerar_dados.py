"""
gerar_dados.py
==============
Gera arquivos de teste organizados para o benchmark.

Estrutura:
    dados/
    ├── inteiros_10.txt
    ├── inteiros_100.txt
    ├── ...
    ├── strings_10.txt
    ├── strings_100.txt
    └── ...

Uso:
    python src/gerar_dados.py
"""

import os
import random
import string

PASTA_DADOS = "dados"
TAMANHOS = [10, 1_000, 100_000, 1_000_000]
# Descomente para incluir tamanhos maiores (cuidado: arquivos de vários GB!)
# TAMANHOS += [10_000_000, 100_000_000]


def gerar_string_aleatoria(tamanho_min=3, tamanho_max=15):
    """Gera uma string aleatória com letras minúsculas."""
    tam = random.randint(tamanho_min, tamanho_max)
    return ''.join(random.choices(string.ascii_lowercase, k=tam))


def gerar_inteiros(tamanho):
    caminho = os.path.join(PASTA_DADOS, f"inteiros_{tamanho}.txt")
    if os.path.exists(caminho):
        print(f"  Já existe: {caminho}")
        return

    print(f"  Gerando {tamanho:>12,} inteiros... ", end="", flush=True)
    with open(caminho, "w") as f:
        for _ in range(tamanho):
            f.write(f"{random.randint(-1_000_000_000, 1_000_000_000)}\n")
    tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
    print(f"OK ({tamanho_mb:.1f} MB)")


def gerar_strings(tamanho):
    caminho = os.path.join(PASTA_DADOS, f"strings_{tamanho}.txt")
    if os.path.exists(caminho):
        print(f"  Já existe: {caminho}")
        return

    print(f"  Gerando {tamanho:>12,} strings... ", end="", flush=True)
    with open(caminho, "w") as f:
        for _ in range(tamanho):
            f.write(gerar_string_aleatoria() + "\n")
    tamanho_mb = os.path.getsize(caminho) / (1024 * 1024)
    print(f"OK ({tamanho_mb:.1f} MB)")


def main():
    os.makedirs(PASTA_DADOS, exist_ok=True)

    print("=" * 50)
    print("  Gerador de Dados de Teste — PyC-Compare")
    print("=" * 50)
    print(f"\n  Tamanhos: {[f'{t:,}' for t in TAMANHOS]}\n")

    print("  --- Inteiros ---")
    for tam in TAMANHOS:
        gerar_inteiros(tam)

    print("\n  --- Strings ---")
    for tam in TAMANHOS:
        gerar_strings(tam)

    print(f"\n  Todos os arquivos em: {PASTA_DADOS}/")
    print("=" * 50)


if __name__ == "__main__":
    main()
