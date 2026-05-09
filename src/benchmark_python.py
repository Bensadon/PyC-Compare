"""
benchmark_python.py
===================
Benchmark do dict e sorted() do Python.
Mede tempo (perf_counter) e memória (tracemalloc).

Uso:
    python src/benchmark_python.py
"""

import time
import os
import csv
import random
import tracemalloc

# ── CONFIGURAÇÕES ──

TAMANHOS = [10, 100, 1_000, 10_000, 100_000]
PASTA_DADOS = "dados"
PASTA_RESULTADOS = "results"
ARQUIVO_RESULTADO = os.path.join(PASTA_RESULTADOS, "resultados_python_v2.csv")


def ler_inteiros(tamanho):
    caminho = os.path.join(PASTA_DADOS, f"inteiros_{tamanho}.txt")
    with open(caminho, "r") as f:
        return [int(linha.strip()) for linha in f.readlines()]


def ler_strings(tamanho):
    caminho = os.path.join(PASTA_DADOS, f"strings_{tamanho}.txt")
    with open(caminho, "r") as f:
        return [linha.strip() for linha in f.readlines()]


def medir(func, *args):
    """Executa func(*args) medindo tempo e pico de memória."""
    tracemalloc.start()
    inicio = time.perf_counter()
    resultado = func(*args)
    fim = time.perf_counter()
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return fim - inicio, peak, resultado


# ── OPERAÇÕES ──

def teste_insercao_dict(dados):
    d = {}
    for i, valor in enumerate(dados):
        d[i] = valor
    return d


def teste_busca_dict(d, idx):
    _ = d[idx]


def teste_remocao_dict(d, idx):
    del d[idx]


def teste_sorted(dados):
    return sorted(dados)


# ── MAIN ──

def main():
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    print("=" * 60)
    print("  Benchmark Python — PyC-Compare")
    print(f"  Tamanhos: {[f'{t:,}' for t in TAMANHOS]}")
    print("=" * 60)

    with open(ARQUIVO_RESULTADO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["linguagem", "tipo_dado", "tamanho", "operacao", "tempo_segundos", "memoria_bytes"])

        for tamanho in TAMANHOS:
            print(f"\n  Tamanho: {tamanho:,}")

            for tipo, ler_dados in [("inteiro", ler_inteiros), ("string", ler_strings)]:
                caminho = os.path.join(PASTA_DADOS, f"{'inteiros' if tipo == 'inteiro' else 'strings'}_{tamanho}.txt")
                if not os.path.exists(caminho):
                    print(f"    [{tipo}] PULADO (arquivo não existe)")
                    continue

                print(f"    Tipo: {tipo}")
                dados = ler_dados(tamanho)

                # Dict — inserção
                t, mem, d = medir(teste_insercao_dict, dados)
                print(f"      [dict] insercao:  {t:.6f}s  | mem: {mem:>12,} bytes")
                writer.writerow(["python", tipo, tamanho, "dict_insercao", f"{t:.6f}", mem])

                # Dict — busca de 10 elementos aleatórios (média)
                n_amostras = 10 if tamanho >= 100 else 1
                random.seed(42)
                indices = [random.randint(0, len(dados) - 1) for _ in range(n_amostras)]
                soma_t = 0
                for idx in indices:
                    t, mem, _ = medir(teste_busca_dict, d, idx)
                    soma_t += t
                t_media = soma_t / n_amostras
                print(f"      [dict] busca:     {t_media:.6f}s  | (média de {n_amostras})")
                writer.writerow(["python", tipo, tamanho, "dict_busca", f"{t_media:.6f}", 0])

                # Dict — remoção de 10 elementos aleatórios (média)
                random.seed(123)
                indices_rem = [random.randint(0, len(dados) - 1) for _ in range(n_amostras)]
                soma_t = 0
                for idx in indices_rem:
                    d2 = dict(d)  # copia para cada remoção
                    t, mem, _ = medir(teste_remocao_dict, d2, idx)
                    soma_t += t
                t_media = soma_t / n_amostras
                print(f"      [dict] remocao:   {t_media:.6f}s  | (média de {n_amostras})")
                writer.writerow(["python", tipo, tamanho, "dict_remocao", f"{t_media:.6f}", 0])

                # Sorted
                t, mem, _ = medir(teste_sorted, dados)
                print(f"      [sorted]:         {t:.6f}s  | mem: {mem:>12,} bytes")
                writer.writerow(["python", tipo, tamanho, "sorted", f"{t:.6f}", mem])

    print("\n" + "=" * 60)
    print(f"  Resultados salvos em: {ARQUIVO_RESULTADO}")
    print("=" * 60)


if __name__ == "__main__":
    main()
