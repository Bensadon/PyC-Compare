"""
gerar_graficos.py
=================
Lê os CSVs de resultados e gera gráficos comparativos.

Uso:
    python src/gerar_graficos.py
"""

import csv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PASTA_RESULTADOS = "results"
CSV_C = os.path.join(PASTA_RESULTADOS, "resultados_c.csv")
CSV_PY = os.path.join(PASTA_RESULTADOS, "resultados_python_v2.csv")
CSV_COLISOES = os.path.join(PASTA_RESULTADOS, "colisoes.csv")


def ler_csv(caminho):
    dados = []
    with open(caminho, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for k in row:
                try:
                    row[k] = int(row[k])
                except ValueError:
                    try:
                        row[k] = float(row[k])
                    except ValueError:
                        pass
            dados.append(row)
    return dados


def filtrar(dados, **kwargs):
    r = dados
    for k, v in kwargs.items():
        r = [d for d in r if d.get(k) == v]
    return r


def extrair_serie(dados, x_campo, y_campo):
    pontos = sorted(set((d[x_campo], d[y_campo]) for d in dados))
    xs = [p[0] for p in pontos]
    ys = [p[1] for p in pontos]
    return xs, ys


def salvar(fig, nome):
    caminho = os.path.join(PASTA_RESULTADOS, nome)
    fig.tight_layout()
    fig.savefig(caminho, dpi=150)
    plt.close(fig)
    print(f"  Salvo: {caminho}")


# ═══════════════════════════════════════
#  GRÁFICOS DE TEMPO (C vs Python)
# ═══════════════════════════════════════

def graficos_tempo(dados_c, dados_py):
    operacoes = [
        ("hash_insercao", "dict_insercao", "Inserção"),
        ("hash_busca", "dict_busca", "Busca"),
        ("hash_remocao", "dict_remocao", "Remoção"),
    ]

    for tipo in ["inteiro", "string"]:
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle(f"C vs Python — {tipo}s", fontsize=16, fontweight="bold")

        for ax, (op_c, op_py, titulo) in zip(axes, operacoes):
            c_filt = filtrar(dados_c, tipo_dado=tipo, operacao=op_c)
            py_filt = filtrar(dados_py, tipo_dado=tipo, operacao=op_py)

            if c_filt:
                xs, ys = extrair_serie(c_filt, "tamanho", "tempo_segundos")
                ax.plot(xs, ys, "o-", label="C", linewidth=2, color="#2196F3")
            if py_filt:
                xs, ys = extrair_serie(py_filt, "tamanho", "tempo_segundos")
                ax.plot(xs, ys, "s--", label="Python", linewidth=2, color="#FF9800")

            ax.set_title(titulo, fontsize=13)
            ax.set_xlabel("Tamanho")
            ax.set_ylabel("Tempo (s)")
            ax.set_xscale("log")
            ax.legend()
            ax.grid(True, alpha=0.3)

        salvar(fig, f"tempo_{tipo}.png")


# ═══════════════════════════════════════
#  GRÁFICOS DE ORDENAÇÃO
# ═══════════════════════════════════════

def graficos_ordenacao(dados_c, dados_py):
    cores = {"insertion_sort": "#F44336", "merge_sort": "#4CAF50", "quick_sort": "#2196F3", "sorted": "#FF9800"}

    for tipo in ["inteiro", "string"]:
        fig, ax = plt.subplots(figsize=(10, 6))

        for op in ["insertion_sort", "merge_sort", "quick_sort"]:
            c_filt = filtrar(dados_c, tipo_dado=tipo, operacao=op)
            if c_filt:
                xs, ys = extrair_serie(c_filt, "tamanho", "tempo_segundos")
                ax.plot(xs, ys, "o-", label=f"C {op}", linewidth=2, color=cores[op])

        py_filt = filtrar(dados_py, tipo_dado=tipo, operacao="sorted")
        if py_filt:
            xs, ys = extrair_serie(py_filt, "tamanho", "tempo_segundos")
            ax.plot(xs, ys, "s--", label="Python sorted()", linewidth=2, color=cores["sorted"])

        ax.set_title(f"Ordenação — {tipo}s", fontsize=14, fontweight="bold")
        ax.set_xlabel("Tamanho")
        ax.set_ylabel("Tempo (s)")
        ax.set_xscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

        salvar(fig, f"ordenacao_{tipo}.png")


# ═══════════════════════════════════════
#  GRÁFICOS DE COLISÕES
# ═══════════════════════════════════════

def graficos_colisoes(dados_col):
    metricas = [
        ("total_colisoes", "Total de colisões"),
        ("max_tentativas", "Máx tentativas (pior caso)"),
        ("media_tentativas", "Média de tentativas"),
        ("sem_colisao_pct", "% Sem colisão"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Análise de Colisões por Fator de Carga", fontsize=16, fontweight="bold")

    cores_mult = {1: "#F44336", 2: "#4CAF50"}
    labels_mult = {1: "~100% (1x)", 2: "~50% (2x)"}

    for ax, (campo, titulo) in zip(axes.flat, metricas):
        for mult in [1, 2]:
            filt = filtrar(dados_col, multiplicador=mult)
            if filt:
                xs, ys = extrair_serie(filt, "tamanho", campo)
                ax.plot(xs, ys, "o-", label=labels_mult[mult], linewidth=2,
                        color=cores_mult[mult], markersize=7)

        ax.set_title(titulo, fontsize=12)
        ax.set_xlabel("Tamanho da entrada")
        ax.set_xscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

    salvar(fig, "colisoes_comparacao.png")


# ═══════════════════════════════════════
#  RELATÓRIO TEXTO
# ═══════════════════════════════════════

def gerar_relatorio(dados_c, dados_py, dados_col):
    caminho = os.path.join(PASTA_RESULTADOS, "relatorio.md")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("# Relatório de Benchmark — PyC-Compare\n\n")

        # Tabela C vs Python
        f.write("## Tempos de Execução (C vs Python)\n\n")
        f.write("| Tipo | Tamanho | Operação | C (s) | Python (s) | Mais rápido |\n")
        f.write("|------|---------|----------|-------|------------|-------------|\n")

        mapa_ops = [
            ("hash_insercao", "dict_insercao", "Inserção"),
            ("hash_busca", "dict_busca", "Busca"),
            ("hash_remocao", "dict_remocao", "Remoção"),
        ]

        for tipo in ["inteiro", "string"]:
            for op_c, op_py, nome in mapa_ops:
                c_filt = filtrar(dados_c, tipo_dado=tipo, operacao=op_c)
                py_filt = filtrar(dados_py, tipo_dado=tipo, operacao=op_py)

                for c_row in c_filt:
                    tam = c_row["tamanho"]
                    py_row = [p for p in py_filt if p["tamanho"] == tam]
                    if py_row:
                        tc = c_row["tempo_segundos"]
                        tp = py_row[0]["tempo_segundos"]
                        vencedor = "**C**" if tc < tp else "**Python**"
                        f.write(f"| {tipo} | {tam:,} | {nome} | {tc:.6f} | {tp:.6f} | {vencedor} |\n")

        # Tabela de colisões
        f.write("\n## Análise de Colisões\n\n")
        f.write("| Tamanho | Fator | Total colisões | Max tentativas | Média | Sem colisão |\n")
        f.write("|---------|-------|----------------|----------------|-------|-------------|\n")

        for row in dados_col:
            fator = f"~{100 // row['multiplicador']}%"
            f.write(f"| {row['tamanho']:,} | {fator} | {row['total_colisoes']:,} | {row['max_tentativas']} | {row['media_tentativas']:.2f} | {row['sem_colisao_pct']:.1f}% |\n")

    print(f"  Salvo: {caminho}")


# ═══════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════

def main():
    ok = True
    for f in [CSV_C, CSV_PY, CSV_COLISOES]:
        if not os.path.exists(f):
            print(f"  Arquivo não encontrado: {f}")
            ok = False
    if not ok:
        print("  Rode primeiro: python src/run_benchmarks.py")
        return

    dados_c = ler_csv(CSV_C)
    dados_py = ler_csv(CSV_PY)
    dados_col = ler_csv(CSV_COLISOES)

    print("Gerando gráficos e relatório...\n")

    graficos_tempo(dados_c, dados_py)
    graficos_ordenacao(dados_c, dados_py)
    graficos_colisoes(dados_col)
    gerar_relatorio(dados_c, dados_py, dados_col)

    print(f"\nTudo salvo em: {PASTA_RESULTADOS}/")


if __name__ == "__main__":
    main()
