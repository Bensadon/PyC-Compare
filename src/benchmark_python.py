"""
benchmark_python.py
===================
Testa o desempenho do dict (Python) e do sorted() nativo
com inteiros e strings.

Mede tempo de execução e pico de memória (tracemalloc).

Lê os .txt gerados pelo gerar_dados.py e salva os resultados em:
    results/resultados_python_v2.csv

Uso:
    python benchmark_python.py
"""

import time
import os
import csv
import tracemalloc

# ──────────────────────────────────────────────
# CONFIGURAÇÕES
# ──────────────────────────────────────────────

TAMANHOS = [100, 1_000, 10_000, 100_000, 1_000_000]
PASTA_RESULTADOS = "results"
ARQUIVO_RESULTADO = os.path.join(PASTA_RESULTADOS, "resultados_python_v2.csv")

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
# MEDIÇÃO COM TEMPO + MEMÓRIA
# ──────────────────────────────────────────────

def medir(func, *args):
    """Executa func(*args) medindo tempo e pico de memória."""
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = func(*args)
    fim = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return fim - inicio, peak, resultado

# ──────────────────────────────────────────────
# TESTES DO DICT
# ──────────────────────────────────────────────

def teste_insercao_dict(dados):
    d = {}
    for i, valor in enumerate(dados):
        d[i] = valor
    return d

def teste_busca_dict(d, dados):
    for i in range(len(dados)):
        _ = d[i]

def teste_remocao_dict(d, dados):
    for i in range(len(dados)):
        del d[i]

# ──────────────────────────────────────────────
# TESTE DO SORTED
# ──────────────────────────────────────────────

def teste_sorted(dados):
    return sorted(dados)

# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────

def main():
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    print("=" * 50)
    print("  Benchmark Python — AEDII 2026 (v2)")
    print("=" * 50)

    with open(ARQUIVO_RESULTADO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["linguagem", "tipo_dado", "tamanho", "operacao", "tempo_segundos", "memoria_bytes"])

        for tamanho in TAMANHOS:
            print(f"\nTamanho: {tamanho:,}")

            for tipo, ler_dados in [("inteiro", ler_inteiros), ("string", ler_strings)]:
                print(f"  Tipo: {tipo}")
                dados = ler_dados(tamanho)

                # Dict — inserção
                t, mem, d = medir(teste_insercao_dict, dados)
                print(f"    [dict] insercao:  {t:.6f}s  | mem: {mem:,} bytes")
                writer.writerow(["python", tipo, tamanho, "dict_insercao", f"{t:.6f}", mem])

                # Dict — busca
                t, mem, _ = medir(teste_busca_dict, d, dados)
                print(f"    [dict] busca:     {t:.6f}s  | mem: {mem:,} bytes")
                writer.writerow(["python", tipo, tamanho, "dict_busca", f"{t:.6f}", mem])

                # Dict — remoção
                d2 = dict(d)  # copia para não perder o dict
                t, mem, _ = medir(teste_remocao_dict, d2, dados)
                print(f"    [dict] remocao:   {t:.6f}s  | mem: {mem:,} bytes")
                writer.writerow(["python", tipo, tamanho, "dict_remocao", f"{t:.6f}", mem])

                # Sorted
                t, mem, _ = medir(teste_sorted, dados)
                print(f"    [sorted]:         {t:.6f}s  | mem: {mem:,} bytes")
                writer.writerow(["python", tipo, tamanho, "sorted", f"{t:.6f}", mem])

    print("\n" + "=" * 50)
    print(f"  Resultados salvos em: {ARQUIVO_RESULTADO}")
    print("=" * 50)


if __name__ == "__main__":
    main()
