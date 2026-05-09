"""
gerar_graficos.py
=================
Lê os CSVs de resultados (C e Python) e gera gráficos comparativos.

Uso:
    python gerar_graficos.py
"""

import csv
import os
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # backend sem GUI

PASTA_RESULTADOS = "results"
CSV_C = os.path.join(PASTA_RESULTADOS, "resultados_c.csv")
CSV_PY = os.path.join(PASTA_RESULTADOS, "resultados_python_v2.csv")

def ler_csv(caminho):
    dados = []
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["tamanho"] = int(row["tamanho"])
            row["tempo_segundos"] = float(row["tempo_segundos"])
            row["memoria_bytes"] = int(row.get("memoria_bytes", 0))
            dados.append(row)
    return dados

def filtrar(dados, **kwargs):
    resultado = dados
    for chave, valor in kwargs.items():
        resultado = [d for d in resultado if d.get(chave) == valor]
    return resultado

def extrair(dados, campo="tempo_segundos"):
    tamanhos = sorted(set(d["tamanho"] for d in dados))
    valores = []
    for t in tamanhos:
        matches = [d for d in dados if d["tamanho"] == t]
        valores.append(matches[0][campo] if matches else 0)
    return tamanhos, valores

def plot_comparacao(titulo, dados_c, dados_py, operacao_c, operacao_py, tipo_dado, nome_arquivo, campo="tempo_segundos", ylabel="Tempo (s)"):
    fig, ax = plt.subplots(figsize=(10, 6))

    c_filtrado = filtrar(dados_c, tipo_dado=tipo_dado, operacao=operacao_c)
    py_filtrado = filtrar(dados_py, tipo_dado=tipo_dado, operacao=operacao_py)

    if c_filtrado:
        tam_c, val_c = extrair(c_filtrado, campo)
        ax.plot(tam_c, val_c, "o-", label=f"C ({operacao_c})", linewidth=2, markersize=6)

    if py_filtrado:
        tam_py, val_py = extrair(py_filtrado, campo)
        ax.plot(tam_py, val_py, "s--", label=f"Python ({operacao_py})", linewidth=2, markersize=6)

    ax.set_xscale("log")
    ax.set_xlabel("Tamanho da entrada", fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)

    caminho = os.path.join(PASTA_RESULTADOS, nome_arquivo)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"  Salvo: {caminho}")

def plot_ordenacao(titulo, dados_c, dados_py, tipo_dado, nome_arquivo):
    fig, ax = plt.subplots(figsize=(10, 6))

    for op in ["insertion_sort", "merge_sort", "quick_sort"]:
        c_filt = filtrar(dados_c, tipo_dado=tipo_dado, operacao=op)
        if c_filt:
            tam, val = extrair(c_filt)
            ax.plot(tam, val, "o-", label=f"C {op}", linewidth=2, markersize=5)

    py_filt = filtrar(dados_py, tipo_dado=tipo_dado, operacao="sorted")
    if py_filt:
        tam, val = extrair(py_filt)
        ax.plot(tam, val, "s--", label="Python sorted()", linewidth=2, markersize=6)

    ax.set_xscale("log")
    ax.set_xlabel("Tamanho da entrada", fontsize=12)
    ax.set_ylabel("Tempo (s)", fontsize=12)
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    caminho = os.path.join(PASTA_RESULTADOS, nome_arquivo)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"  Salvo: {caminho}")

def main():
    if not os.path.exists(CSV_C):
        print(f"Arquivo não encontrado: {CSV_C}")
        print("Rode primeiro: python src/run_benchmarks.py")
        return
    if not os.path.exists(CSV_PY):
        print(f"Arquivo não encontrado: {CSV_PY}")
        print("Rode primeiro: python src/benchmark_python.py")
        return

    dados_c = ler_csv(CSV_C)
    dados_py = ler_csv(CSV_PY)

    print("Gerando gráficos...\n")

    # Inserção: C hash vs Python dict
    for tipo in ["inteiro", "string"]:
        plot_comparacao(
            f"Inserção — {tipo}s (C hash table vs Python dict)",
            dados_c, dados_py, "hash_insercao", "dict_insercao", tipo,
            f"insercao_{tipo}.png"
        )

    # Busca: C hash vs Python dict
    for tipo in ["inteiro", "string"]:
        plot_comparacao(
            f"Busca — {tipo}s (C hash table vs Python dict)",
            dados_c, dados_py, "hash_busca", "dict_busca", tipo,
            f"busca_{tipo}.png"
        )

    # Remoção: C hash vs Python dict
    for tipo in ["inteiro", "string"]:
        plot_comparacao(
            f"Remoção — {tipo}s (C hash table vs Python dict)",
            dados_c, dados_py, "hash_remocao", "dict_remocao", tipo,
            f"remocao_{tipo}.png"
        )

    # Ordenação: C (3 algos) vs Python sorted()
    for tipo in ["inteiro", "string"]:
        plot_ordenacao(
            f"Ordenação — {tipo}s (C vs Python sorted)",
            dados_c, dados_py, tipo,
            f"ordenacao_{tipo}.png"
        )

    # Memória: inserção
    for tipo in ["inteiro", "string"]:
        plot_comparacao(
            f"Memória na inserção — {tipo}s",
            dados_c, dados_py, "hash_insercao", "dict_insercao", tipo,
            f"memoria_{tipo}.png",
            campo="memoria_bytes", ylabel="Memória (bytes)"
        )

    print(f"\nTodos os gráficos salvos em: {PASTA_RESULTADOS}/")

if __name__ == "__main__":
    main()
