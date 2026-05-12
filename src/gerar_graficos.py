"""
gerar_graficos.py
=================
Gera gráficos comparativos e relatório a partir dos CSVs.

Gráficos gerados:
  1. Tempo por operação (C vs Python) — inteiros e strings
  2. Ordenação (C insertion/merge/quick vs Python sorted)
  3. Memória na inserção (C vs Python)
  4. Colisões: impacto do fator de carga
  5. Relatório markdown

Uso:
    python src/gerar_graficos.py
"""

import csv
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

PASTA = "results"
CSV_C = os.path.join(PASTA, "resultados_c.csv")
CSV_PY = os.path.join(PASTA, "resultados_python_v2.csv")
CSV_COL = os.path.join(PASTA, "colisoes.csv")

CORES = {
    "C": "#2196F3",
    "Python": "#FF9800",
    "insertion": "#F44336",
    "merge": "#4CAF50",
    "quick": "#2196F3",
    "sorted": "#FF9800",
    "100%": "#F44336",
    "50%": "#4CAF50",
}


def ler_csv(caminho):
    dados = []
    if not os.path.exists(caminho):
        return dados
    with open(caminho, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
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


def filtrar(dados, **kw):
    r = dados
    for k, v in kw.items():
        r = [d for d in r if d.get(k) == v]
    return r


def serie(dados, x="tamanho", y="tempo_segundos"):
    pontos = sorted(set((d[x], d[y]) for d in dados))
    return [p[0] for p in pontos], [p[1] for p in pontos]


def salvar(fig, nome):
    c = os.path.join(PASTA, nome)
    fig.tight_layout()
    fig.savefig(c, dpi=150)
    plt.close(fig)
    print(f"  Salvo: {c}")


# ═══════════════════════════════════════
#  1. TEMPO POR OPERAÇÃO (C vs Python)
# ═══════════════════════════════════════

def graficos_tempo(dc, dp):
    ops = [
        ("hash_insercao", "dict_insercao", "Inserção"),
        ("hash_busca", "dict_busca", "Busca"),
        ("hash_remocao", "dict_remocao", "Remoção"),
    ]

    for tipo in ["inteiro", "string"]:
        fig, axes = plt.subplots(1, 3, figsize=(18, 5))
        fig.suptitle(f"C vs Python — {tipo}s", fontsize=16, fontweight="bold")

        for ax, (oc, op, titulo) in zip(axes, ops):
            cf = filtrar(dc, tipo_dado=tipo, operacao=oc)
            pf = filtrar(dp, tipo_dado=tipo, operacao=op)

            if cf:
                xs, ys = serie(cf)
                ax.plot(xs, ys, "o-", label="C", lw=2, color=CORES["C"])
            if pf:
                xs, ys = serie(pf)
                ax.plot(xs, ys, "s--", label="Python", lw=2, color=CORES["Python"])

            ax.set_title(titulo, fontsize=13)
            ax.set_xlabel("Tamanho")
            ax.set_ylabel("Tempo (s)")
            ax.set_xscale("log")
            ax.legend()
            ax.grid(True, alpha=0.3)

        salvar(fig, f"tempo_{tipo}.png")


# ═══════════════════════════════════════
#  2. ORDENAÇÃO
# ═══════════════════════════════════════

def graficos_ordenacao(dc, dp):
    for tipo in ["inteiro", "string"]:
        fig, ax = plt.subplots(figsize=(11, 6))

        for op, cor, nome in [
            ("insertion_sort", CORES["insertion"], "C Insertion Sort"),
            ("merge_sort", CORES["merge"], "C Merge Sort"),
            ("quick_sort", CORES["quick"], "C Quick Sort"),
        ]:
            f = filtrar(dc, tipo_dado=tipo, operacao=op)
            f = [d for d in f if d["tempo_segundos"] >= 0]
            if f:
                xs, ys = serie(f)
                ax.plot(xs, ys, "o-", label=nome, lw=2, color=cor)

        pf = filtrar(dp, tipo_dado=tipo, operacao="sorted")
        if pf:
            xs, ys = serie(pf)
            ax.plot(xs, ys, "s--", label="Python sorted()", lw=2, color=CORES["sorted"])

        ax.set_title(f"Ordenação — {tipo}s", fontsize=14, fontweight="bold")
        ax.set_xlabel("Tamanho")
        ax.set_ylabel("Tempo (s)")
        ax.set_xscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

        salvar(fig, f"ordenacao_{tipo}.png")


# ═══════════════════════════════════════
#  3. MEMÓRIA
# ═══════════════════════════════════════

def graficos_memoria(dc, dp):
    for tipo in ["inteiro", "string"]:
        fig, ax = plt.subplots(figsize=(10, 6))

        cf = filtrar(dc, tipo_dado=tipo, operacao="hash_insercao")
        pf = filtrar(dp, tipo_dado=tipo, operacao="dict_insercao")

        if cf:
            xs, ys = serie(cf, y="memoria_bytes")
            ys_kb = [y / 1024 for y in ys]
            ax.plot(xs, ys_kb, "o-", label="C (hash table)", lw=2, color=CORES["C"])
        if pf:
            xs, ys = serie(pf, y="memoria_bytes")
            ys_kb = [y / 1024 for y in ys]
            ax.plot(xs, ys_kb, "s--", label="Python (dict)", lw=2, color=CORES["Python"])

        ax.set_title(f"Memória na inserção — {tipo}s", fontsize=14, fontweight="bold")
        ax.set_xlabel("Tamanho")
        ax.set_ylabel("Memória (KB)")
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

        salvar(fig, f"memoria_{tipo}.png")


# ═══════════════════════════════════════
#  4. COLISÕES
# ═══════════════════════════════════════

def graficos_colisoes(dcol):
    if not dcol:
        return

    metricas = [
        ("total_colisoes", "Total de colisões"),
        ("max_tentativas", "Máx tentativas (pior caso)"),
        ("media_tentativas", "Média de tentativas"),
        ("sem_colisao_pct", "% Sem colisão"),
    ]

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle("Análise de Colisões por Fator de Carga", fontsize=16, fontweight="bold")

    labels_m = {1: "~100% (1x)", 2: "~50% (2x)"}

    for ax, (campo, titulo) in zip(axes.flat, metricas):
        for mult, cor in [(1, CORES["100%"]), (2, CORES["50%"])]:
            f = filtrar(dcol, multiplicador=mult)
            if f:
                xs, ys = serie(f, y=campo)
                ax.plot(xs, ys, "o-", label=labels_m[mult], lw=2, color=cor, markersize=7)

        ax.set_title(titulo, fontsize=12)
        ax.set_xlabel("Tamanho da entrada")
        ax.set_xscale("log")
        ax.legend()
        ax.grid(True, alpha=0.3)

    salvar(fig, "colisoes_comparacao.png")


# ═══════════════════════════════════════
#  5. RELATÓRIO
# ═══════════════════════════════════════

def gerar_relatorio(dc, dp, dcol):
    caminho = os.path.join(PASTA, "relatorio.md")

    with open(caminho, "w", encoding="utf-8") as f:
        f.write("# Relatório de Benchmark — PyC-Compare\n\n")

        # ── Tabela de tempos ──
        f.write("## Tempos de Execução (C vs Python)\n\n")
        f.write("| Tipo | Tamanho | Operação | C (s) | Python (s) | Mais rápido |\n")
        f.write("|------|---------|----------|-------|------------|-------------|\n")

        mapa = [
            ("hash_insercao", "dict_insercao", "Inserção"),
            ("hash_busca", "dict_busca", "Busca"),
            ("hash_remocao", "dict_remocao", "Remoção"),
        ]

        for tipo in ["inteiro", "string"]:
            for oc, op, nome in mapa:
                cf = filtrar(dc, tipo_dado=tipo, operacao=oc)
                pf = filtrar(dp, tipo_dado=tipo, operacao=op)
                for cr in sorted(cf, key=lambda x: x["tamanho"]):
                    t = cr["tamanho"]
                    pr = [p for p in pf if p["tamanho"] == t]
                    if pr:
                        tc = cr["tempo_segundos"]
                        tp = pr[0]["tempo_segundos"]
                        v = "**C**" if tc < tp else ("**Python**" if tp < tc else "Empate")
                        f.write(f"| {tipo} | {t:,} | {nome} | {tc:.6f} | {tp:.6f} | {v} |\n")

        # ── Tabela de ordenação ──
        f.write("\n## Ordenação\n\n")
        f.write("| Tipo | Tamanho | insertion_sort | merge_sort | quick_sort | Python sorted |\n")
        f.write("|------|---------|----------------|------------|------------|---------------|\n")

        for tipo in ["inteiro", "string"]:
            tamanhos = sorted(set(d["tamanho"] for d in dc if d["tipo_dado"] == tipo))
            for t in tamanhos:
                vals = {}
                for op in ["insertion_sort", "merge_sort", "quick_sort"]:
                    r = filtrar(dc, tipo_dado=tipo, operacao=op, tamanho=t)
                    vals[op] = f"{r[0]['tempo_segundos']:.6f}" if r else "—"
                pr = filtrar(dp, tipo_dado=tipo, operacao="sorted", tamanho=t)
                vals["sorted"] = f"{pr[0]['tempo_segundos']:.6f}" if pr else "—"
                f.write(f"| {tipo} | {t:,} | {vals['insertion_sort']} | {vals['merge_sort']} | {vals['quick_sort']} | {vals['sorted']} |\n")

        # ── Tabela de colisões ──
        if dcol:
            f.write("\n## Análise de Colisões\n\n")
            f.write("| Tamanho | Fator | Total colisões | Max tentativas | Média | Sem colisão |\n")
            f.write("|---------|-------|----------------|----------------|-------|-------------|\n")
            for row in sorted(dcol, key=lambda x: (x["tamanho"], x["multiplicador"])):
                fator = f"~{100 // row['multiplicador']}%"
                f.write(f"| {row['tamanho']:,} | {fator} | {row['total_colisoes']:,} | {row['max_tentativas']} | {row['media_tentativas']:.2f} | {row['sem_colisao_pct']:.1f}% |\n")

    print(f"  Salvo: {caminho}")


# ═══════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════

def main():
    dc = ler_csv(CSV_C)
    dp = ler_csv(CSV_PY)
    dcol = ler_csv(CSV_COL)

    if not dc and not dp:
        print("  Nenhum CSV encontrado. Rode: python src/run_benchmarks.py")
        return

    print("Gerando gráficos e relatório...\n")

    if dc and dp:
        graficos_tempo(dc, dp)
    if dc or dp:
        graficos_ordenacao(dc, dp)
    if dc or dp:
        graficos_memoria(dc, dp)
    if dcol:
        graficos_colisoes(dcol)
    gerar_relatorio(dc, dp, dcol)

    print(f"\nTudo salvo em: {PASTA}/")


if __name__ == "__main__":
    main()
