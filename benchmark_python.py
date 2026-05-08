"""
benchmark_python.py
===================
Testa o desempenho do dict (Python) e do sorted() nativo
com inteiros e strings.

Lê os .txt gerados pelo gerar_dados.py e salva os resultados em:
    resultados/resultados_python.csv

Uso:
    python benchmark_python.py
"""

import time
import os
import csv

# ──────────────────────────────────────────────
# CONFIGURAÇÕES
# ──────────────────────────────────────────────

TAMANHOS = [100, 1_000, 10_000, 100_000, 1_000_000]
PASTA_RESULTADOS = "resultados"
ARQUIVO_RESULTADO = os.path.join(PASTA_RESULTADOS, "resultados_python.csv")

# ──────────────────────────────────────────────
# LEITURA DOS ARQUIVOS
# ──────────────────────────────────────────────

def ler_inteiros(tamanho):
    with open(f"dados/inteiros_{tamanho}.txt", "r") as f:
        return [int(linha.strip()) for linha in f.readlines()]

def ler_strings(tamanho):
    with open(f"dados/strings_{tamanho}.txt", "r") as f:
        return [linha.strip() for linha in f.readlines()]

# ──────────────────────────────────────────────
# TESTES DO DICT
# ──────────────────────────────────────────────

def teste_insercao_dict(dados):
    d = {}
    inicio = time.perf_counter()
    for i, valor in enumerate(dados):
        d[i] = valor
    fim = time.perf_counter()
    return fim - inicio

def teste_busca_dict(dados):
    d = {i: valor for i, valor in enumerate(dados)}
    inicio = time.perf_counter()
    for i in range(len(dados)):
        _ = d[i]
    fim = time.perf_counter()
    return fim - inicio

def teste_remocao_dict(dados):
    d = {i: valor for i, valor in enumerate(dados)}
    inicio = time.perf_counter()
    for i in range(len(dados)):
        del d[i]
    fim = time.perf_counter()
    return fim - inicio

# ──────────────────────────────────────────────
# TESTE DO SORTED
# ──────────────────────────────────────────────

def teste_sorted(dados):
    copia = dados.copy()
    inicio = time.perf_counter()
    sorted(copia)
    fim = time.perf_counter()
    return fim - inicio

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    print("=" * 50)
    print("  Benchmark Python — AEDII 2026")
    print("=" * 50)

    with open(ARQUIVO_RESULTADO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["linguagem", "tipo_dado", "tamanho", "operacao", "tempo_segundos"])

        for tamanho in TAMANHOS:
            print(f"\nTamanho: {tamanho:,}")

            for tipo, ler_dados in [("inteiro", ler_inteiros), ("string", ler_strings)]:
                print(f"  Tipo: {tipo}")
                dados = ler_dados(tamanho)

                # Dict
                t = teste_insercao_dict(dados)
                print(f"    [dict] insercao:  {t:.6f}s")
                writer.writerow(["python", tipo, tamanho, "dict_insercao", f"{t:.6f}"])

                t = teste_busca_dict(dados)
                print(f"    [dict] busca:     {t:.6f}s")
                writer.writerow(["python", tipo, tamanho, "dict_busca", f"{t:.6f}"])

                t = teste_remocao_dict(dados)
                print(f"    [dict] remocao:   {t:.6f}s")
                writer.writerow(["python", tipo, tamanho, "dict_remocao", f"{t:.6f}"])

                # Sorted
                t = teste_sorted(dados)
                print(f"    [sorted]:         {t:.6f}s")
                writer.writerow(["python", tipo, tamanho, "sorted", f"{t:.6f}"])

    print("\n" + "=" * 50)
    print(f"  Resultados salvos em: {ARQUIVO_RESULTADO}")
    print("=" * 50)


if __name__ == "__main__":
    main()
