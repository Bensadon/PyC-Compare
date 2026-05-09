"""
run_benchmarks.py
=================
Script de automação que:
1. Compila o programa C
2. Roda o benchmark C para cada arquivo de teste
3. Roda o benchmark Python
4. Gera os gráficos comparativos

Uso:
    python run_benchmarks.py
"""

import subprocess
import os
import sys

TAMANHOS = [100, 1_000, 10_000, 100_000, 1_000_000]
PASTA_DADOS = "dados"
PASTA_RESULTADOS = "results"
CSV_C = os.path.join(PASTA_RESULTADOS, "resultados_c.csv")

def compilar():
    print("=" * 50)
    print("  Compilando programa C...")
    print("=" * 50)
    result = subprocess.run(
        ["gcc", "src/main.c", "src/tableInt.c", "src/tableStr.c", "src/ordAlg.c",
         "-o", "programa.exe", "-Wall", "-O2", "-lpsapi"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"ERRO de compilação:\n{result.stderr}")
        sys.exit(1)
    print("  Compilado com sucesso!\n")

def rodar_benchmark_c():
    print("=" * 50)
    print("  Rodando Benchmark C...")
    print("=" * 50)

    os.makedirs(PASTA_RESULTADOS, exist_ok=True)

    with open(CSV_C, "w", encoding="utf-8") as f:
        f.write("linguagem,tipo_dado,tamanho,operacao,tempo_segundos,memoria_bytes\n")

        for tamanho in TAMANHOS:
            for tipo, prefixo in [("inteiro", "inteiros"), ("string", "strings")]:
                arquivo = os.path.join(PASTA_DADOS, f"{prefixo}_{tamanho}.txt")
                print(f"  {tipo} | {tamanho:>10,} itens... ", end="", flush=True)

                result = subprocess.run(
                    ["./programa.exe", arquivo, tipo, str(tamanho)],
                    capture_output=True, text=True, timeout=600
                )

                if result.returncode != 0:
                    print(f"ERRO: {result.stderr.strip()}")
                    continue

                f.write(result.stdout)
                print("OK")

    print(f"\n  Resultados salvos em: {CSV_C}\n")

def rodar_benchmark_python():
    print("=" * 50)
    print("  Rodando Benchmark Python...")
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, "src/benchmark_python.py"],
        capture_output=True, text=True, timeout=600
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERRO: {result.stderr}")

def gerar_graficos():
    print("=" * 50)
    print("  Gerando gráficos...")
    print("=" * 50)

    result = subprocess.run(
        [sys.executable, "src/gerar_graficos.py"],
        capture_output=True, text=True
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"ERRO: {result.stderr}")

def main():
    compilar()
    rodar_benchmark_c()
    rodar_benchmark_python()
    gerar_graficos()

    print("\n" + "=" * 50)
    print("  Tudo concluído! Verifique a pasta results/")
    print("=" * 50)

if __name__ == "__main__":
    main()
