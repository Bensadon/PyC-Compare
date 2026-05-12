"""
run_benchmarks.py
=================
Automação completa:
1. Gera dados de teste (se não existirem)
2. Compila os programas C
3. Roda benchmark C (hash + ordenação)
4. Roda collision analyzer (100% e 50%)
5. Roda benchmark Python
6. Gera gráficos e relatório

Uso:
    python src/run_benchmarks.py
"""

import subprocess
import os
import sys

# ═══════════════════════════════════════
#  CONFIGURAÇÕES
# ═══════════════════════════════════════

TAMANHOS = [10, 1_000, 100_000, 1_000_000]

# Insertion sort é O(n²) — fica impraticável a partir de certo tamanho.
# Definimos um limite para pular automaticamente.
LIMITE_INSERTION_SORT = 100_000

MULTIPLICADORES_COLISAO = [1, 2]  # 1=100%, 2=50%
MULTIPLICADOR_BENCHMARK = 2       # fator de carga padrão para o benchmark

PASTA_DADOS = "dados"
PASTA_RESULTADOS = "results"
CSV_C = os.path.join(PASTA_RESULTADOS, "resultados_c.csv")
CSV_PY = os.path.join(PASTA_RESULTADOS, "resultados_python_v2.csv")
CSV_COLISOES = os.path.join(PASTA_RESULTADOS, "colisoes.csv")

EXE_PROGRAMA = os.path.abspath("programa.exe")
EXE_COLISOES = os.path.abspath("collision_analyzer.exe")


def etapa(n, total, titulo):
    print(f"\n{'=' * 60}")
    print(f"  [{n}/{total}] {titulo}")
    print(f"{'=' * 60}\n")


# ── ETAPA 1: GERAR DADOS ──

def gerar_dados():
    etapa(1, 6, "Gerando dados de teste...")
    r = subprocess.run(
        [sys.executable, "src/gerar_dados.py"],
        capture_output=True, text=True
    )
    print(r.stdout)
    if r.returncode != 0:
        print(f"ERRO: {r.stderr}")
        sys.exit(1)


# ── ETAPA 2: COMPILAR ──

def compilar():
    etapa(2, 6, "Compilando programas C...")

    cmds = [
        (["gcc", "src/main.c", "src/tableInt.c", "src/tableStr.c", "src/ordAlg.c",
          "-o", "programa.exe", "-Wall", "-O2", "-lpsapi"], "programa.exe"),
        (["gcc", "src/collision_analyzer.c", "src/tableInt.c",
          "-o", "collision_analyzer.exe", "-Wall", "-O2"], "collision_analyzer.exe"),
    ]

    for cmd, nome in cmds:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ERRO compilando {nome}:\n{r.stderr}")
            sys.exit(1)
        print(f"  OK: {nome}")


# ── ETAPA 3: BENCHMARK C ──

def rodar_benchmark_c():
    etapa(3, 6, "Rodando Benchmark C...")
    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    with open(CSV_C, "w", encoding="utf-8") as f:
        f.write("linguagem,tipo_dado,tamanho,operacao,tempo_segundos,memoria_bytes\n")

        for tamanho in TAMANHOS:
            for tipo, prefixo in [("inteiro", "inteiros"), ("string", "strings")]:
                arquivo = os.path.normpath(os.path.join(PASTA_DADOS, f"{prefixo}_{tamanho}.txt"))

                if not os.path.exists(arquivo):
                    print(f"  {tipo:>7} | {tamanho:>12,} | PULADO (arquivo não existe)")
                    continue

                print(f"  {tipo:>7} | {tamanho:>12,} itens... ", end="", flush=True)

                # Timeout maior para tamanhos grandes
                timeout = 60 if tamanho <= 100_000 else 600

                try:
                    r = subprocess.run(
                        [EXE_PROGRAMA, arquivo, tipo, str(tamanho), str(MULTIPLICADOR_BENCHMARK)],
                        capture_output=True, text=True, timeout=timeout
                    )

                    if r.returncode != 0:
                        print(f"ERRO (exit {r.returncode})")
                        continue

                    f.write(r.stdout)
                    print("OK")

                except subprocess.TimeoutExpired:
                    print(f"TIMEOUT ({timeout}s)")

    print(f"\n  Salvo: {CSV_C}")


# ── ETAPA 4: COLLISION ANALYZER ──

def rodar_colisoes():
    etapa(4, 6, "Rodando Collision Analyzer...")

    with open(CSV_COLISOES, "w", encoding="utf-8") as f:
        f.write("tamanho,multiplicador,fator_carga,total_colisoes,max_tentativas,media_tentativas,sem_colisao_pct,com_colisao_pct\n")

        for tamanho in TAMANHOS:
            arquivo = os.path.normpath(os.path.join(PASTA_DADOS, f"inteiros_{tamanho}.txt"))

            if not os.path.exists(arquivo):
                print(f"  {tamanho:>12,} | PULADO (arquivo não existe)")
                continue

            for mult in MULTIPLICADORES_COLISAO:
                label = f"~{100 // mult}%"
                print(f"  {tamanho:>12,} itens | fator {label}... ", end="", flush=True)

                timeout = 60 if tamanho <= 100_000 else 600

                try:
                    r = subprocess.run(
                        [EXE_COLISOES, arquivo, str(tamanho), str(mult)],
                        capture_output=True, text=True, timeout=timeout
                    )

                    if r.returncode != 0:
                        print(f"ERRO (exit {r.returncode})")
                        continue

                    f.write(r.stdout)
                    print("OK")

                except subprocess.TimeoutExpired:
                    print(f"TIMEOUT ({timeout}s)")

    print(f"\n  Salvo: {CSV_COLISOES}")


# ── ETAPA 5: BENCHMARK PYTHON ──

def rodar_benchmark_python():
    etapa(5, 6, "Rodando Benchmark Python...")

    r = subprocess.run(
        [sys.executable, "src/benchmark_python.py"],
        capture_output=True, text=True, timeout=1800
    )
    print(r.stdout)
    if r.returncode != 0:
        print(f"ERRO: {r.stderr}")


# ── ETAPA 6: GRÁFICOS ──

def gerar_graficos():
    etapa(6, 6, "Gerando gráficos e relatório...")

    r = subprocess.run(
        [sys.executable, "src/gerar_graficos.py"],
        capture_output=True, text=True
    )
    print(r.stdout)
    if r.returncode != 0:
        print(f"ERRO: {r.stderr}")


# ── MAIN ──

def main():
    print("\n" + "=" * 60)
    print("  PyC-Compare — Automação Completa")
    print(f"  Tamanhos: {[f'{t:,}' for t in TAMANHOS]}")
    print("=" * 60)

    gerar_dados()
    compilar()
    rodar_benchmark_c()
    rodar_colisoes()
    rodar_benchmark_python()
    gerar_graficos()

    print("\n" + "=" * 60)
    print("  Tudo concluído! Verifique a pasta results/")
    print("=" * 60)


if __name__ == "__main__":
    main()
