"""
run_benchmarks.py
=================
Automação completa:
1. Compila os programas C
2. Roda benchmark C (tempo + memória) para cada arquivo de teste
3. Roda collision analyzer com fator 100% e 50%
4. Roda benchmark Python
5. Gera todos os gráficos e relatórios

Uso:
    python src/run_benchmarks.py
"""

import subprocess
import os
import sys
import csv

# ── CONFIGURAÇÕES ──
TAMANHOS = [100, 1_000, 10_000]
MULTIPLICADORES = [1, 2]  # 1 = 100%, 2 = 50%
PASTA_DADOS = "dados"
PASTA_RESULTADOS = "results"
CSV_C = os.path.join(PASTA_RESULTADOS, "resultados_c.csv")
CSV_PY = os.path.join(PASTA_RESULTADOS, "resultados_python_v2.csv")
CSV_COLISOES = os.path.join(PASTA_RESULTADOS, "colisoes.csv")


def compilar():
    print("=" * 60)
    print("  [1/5] Compilando programas C...")
    print("=" * 60)

    for cmd, nome in [
        (["gcc", "src/main.c", "src/tableInt.c", "src/tableStr.c", "src/ordAlg.c",
          "-o", "programa.exe", "-Wall", "-O2", "-lpsapi"], "programa.exe"),
        (["gcc", "src/collision_analyzer.c", "src/tableInt.c",
          "-o", "collision_analyzer.exe", "-Wall", "-O2"], "collision_analyzer.exe"),
    ]:
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"  ERRO compilando {nome}:\n{r.stderr}")
            sys.exit(1)
        print(f"  OK: {nome}")
    print()


def rodar_benchmark_c():
    print("=" * 60)
    print("  [2/5] Rodando Benchmark C...")
    print("=" * 60)

    os.makedirs(PASTA_RESULTADOS, exist_ok=True)
    multiplicador = 2  # tabela com 2x o tamanho (fator ~50%)

    with open(CSV_C, "w", encoding="utf-8") as f:
        f.write("linguagem,tipo_dado,tamanho,operacao,tempo_segundos,memoria_bytes\n")

        for tamanho in TAMANHOS:
            for tipo, prefixo in [("inteiro", "inteiros"), ("string", "strings")]:
                arquivo = os.path.normpath(os.path.join(PASTA_DADOS, f"{prefixo}_{tamanho}.txt"))
                print(f"  {tipo:>7} | {tamanho:>10,} itens... ", end="", flush=True)

                r = subprocess.run(
                    [os.path.abspath("programa.exe"), arquivo, tipo, str(tamanho), str(multiplicador)],
                    capture_output=True, text=True, timeout=300
                )
                if r.returncode != 0:
                    print(f"ERRO: {r.stderr.strip()}")
                    continue
                f.write(r.stdout)
                print("OK")

    print(f"\n  Salvo: {CSV_C}\n")


def rodar_colisoes():
    print("=" * 60)
    print("  [3/5] Rodando Collision Analyzer...")
    print("=" * 60)

    with open(CSV_COLISOES, "w", encoding="utf-8") as f:
        f.write("tamanho,multiplicador,fator_carga,total_colisoes,max_tentativas,media_tentativas,sem_colisao_pct,com_colisao_pct\n")

        for tamanho in TAMANHOS:
            for mult in MULTIPLICADORES:
                arquivo = os.path.normpath(os.path.join(PASTA_DADOS, f"inteiros_{tamanho}.txt"))
                label = f"{100 // mult}%"
                print(f"  {tamanho:>10,} itens | fator ~{label}... ", end="", flush=True)

                r = subprocess.run(
                    [os.path.abspath("collision_analyzer.exe"), arquivo, str(tamanho), str(mult)],
                    capture_output=True, text=True, timeout=300
                )
                if r.returncode != 0:
                    print(f"ERRO: {r.stderr.strip()}")
                    continue
                f.write(r.stdout)
                print("OK")

    print(f"\n  Salvo: {CSV_COLISOES}\n")


def rodar_benchmark_python():
    print("=" * 60)
    print("  [4/5] Rodando Benchmark Python...")
    print("=" * 60)

    r = subprocess.run(
        [sys.executable, "src/benchmark_python.py"],
        capture_output=True, text=True, timeout=600
    )
    print(r.stdout)
    if r.returncode != 0:
        print(f"ERRO: {r.stderr}")


def gerar_graficos():
    print("=" * 60)
    print("  [5/5] Gerando gráficos...")
    print("=" * 60)

    r = subprocess.run(
        [sys.executable, "src/gerar_graficos.py"],
        capture_output=True, text=True
    )
    print(r.stdout)
    if r.returncode != 0:
        print(f"ERRO: {r.stderr}")


def main():
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
