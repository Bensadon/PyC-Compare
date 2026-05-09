#include "tableInt.h"
#include "tableStr.h"
#include "ordAlg.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <windows.h>
#include <psapi.h>

// Retorna o pico de memória do processo em bytes
size_t getPeakMemory () {
  PROCESS_MEMORY_COUNTERS pmc;
  if (GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc)))
    return pmc.PeakWorkingSetSize;
  return 0;
}

// Lê inteiros de um arquivo
int *lerArquivoInt (const char *caminho, int tam) {
  FILE *f = fopen(caminho, "r");
  if (!f) { printf("Erro ao abrir %s\n", caminho); return NULL; }

  int *vetor = (int *) malloc (tam * sizeof(int));
  for (int i = 0; i < tam; i++) {
    if (fscanf(f, "%d", &vetor[i]) != 1) break;
  }
  fclose(f);
  return vetor;
}

// Lê strings de um arquivo
char **lerArquivoStr (const char *caminho, int tam) {
  FILE *f = fopen(caminho, "r");
  if (!f) { printf("Erro ao abrir %s\n", caminho); return NULL; }

  char **vetor = (char **) malloc (tam * sizeof(char *));
  char buffer[256];
  for (int i = 0; i < tam; i++) {
    if (fscanf(f, "%255s", buffer) != 1) break;
    vetor[i] = (char *) malloc ((strlen(buffer) + 1) * sizeof(char));
    strcpy(vetor[i], buffer);
  }
  fclose(f);
  return vetor;
}

// Copia um vetor de inteiros (para ordenação sem destruir o original)
int *copiarVetorInt (int *vetor, int tam) {
  int *copia = (int *) malloc (tam * sizeof(int));
  memcpy(copia, vetor, tam * sizeof(int));
  return copia;
}

// Copia um vetor de ponteiros de strings
char **copiarVetorStr (char **vetor, int tam) {
  char **copia = (char **) malloc (tam * sizeof(char *));
  memcpy(copia, vetor, tam * sizeof(char *));
  return copia;
}

// Imprime uma linha CSV
void printCSV (const char *tipo, int tamanho, const char *operacao, double tempo, size_t memoria) {
  printf("c,%s,%d,%s,%.6f,%lu\n", tipo, tamanho, operacao, tempo, (unsigned long)memoria);
}

void benchmarkInt (const char *caminho, int tamanho) {
  int *vetor = lerArquivoInt(caminho, tamanho);
  if (!vetor) return;

  clock_t inicio, fim;
  double tempo;
  size_t mem_antes, mem_depois;

  // --- Inserção na hash table ---
  int mapSize = maiorPrimo(tamanho);
  mem_antes = getPeakMemory();
  inicio = clock();
  Item_int *table = criateTable(vetor, mapSize, tamanho);
  fim = clock();
  mem_depois = getPeakMemory();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("inteiro", tamanho, "hash_insercao", tempo, mem_depois - mem_antes);

  // --- Busca de todos os elementos ---
  inicio = clock();
  for (int i = 0; i < tamanho; i++)
    buscaInt(table, vetor[i], mapSize);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("inteiro", tamanho, "hash_busca", tempo, 0);

  // --- Remoção de todos os elementos ---
  int count = tamanho;
  int currentSize = mapSize;
  inicio = clock();
  for (int i = 0; i < tamanho; i++)
    table = removeInt(table, vetor[i], currentSize, &count, &currentSize);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("inteiro", tamanho, "hash_remocao", tempo, 0);
  free(table);

  // --- Insertion Sort ---
  int *copia = copiarVetorInt(vetor, tamanho);
  inicio = clock();
  insertionSortInt(copia, tamanho);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("inteiro", tamanho, "insertion_sort", tempo, 0);
  free(copia);

  // --- Merge Sort ---
  copia = copiarVetorInt(vetor, tamanho);
  inicio = clock();
  mergeSortInt(copia, 0, tamanho - 1);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("inteiro", tamanho, "merge_sort", tempo, 0);
  free(copia);

  // --- Quick Sort ---
  copia = copiarVetorInt(vetor, tamanho);
  inicio = clock();
  quickSortInt(copia, 0, tamanho - 1);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("inteiro", tamanho, "quick_sort", tempo, 0);
  free(copia);

  free(vetor);
}

void benchmarkStr (const char *caminho, int tamanho) {
  char **vetor = lerArquivoStr(caminho, tamanho);
  if (!vetor) return;

  clock_t inicio, fim;
  double tempo;
  size_t mem_antes, mem_depois;

  // --- Inserção na hash table ---
  int mapSize = maiorPrimo(tamanho);
  mem_antes = getPeakMemory();
  inicio = clock();
  Item_str *table = criateTableStr(vetor, mapSize, tamanho);
  fim = clock();
  mem_depois = getPeakMemory();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("string", tamanho, "hash_insercao", tempo, mem_depois - mem_antes);

  // --- Busca de todos os elementos ---
  inicio = clock();
  for (int i = 0; i < tamanho; i++)
    buscaStr(table, vetor[i], mapSize);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("string", tamanho, "hash_busca", tempo, 0);

  // --- Remoção de todos os elementos ---
  int count = tamanho;
  int currentSize = mapSize;
  inicio = clock();
  for (int i = 0; i < tamanho; i++)
    table = removeStr(table, vetor[i], currentSize, &count, &currentSize);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("string", tamanho, "hash_remocao", tempo, 0);
  free(table);

  // --- Insertion Sort ---
  char **copia = copiarVetorStr(vetor, tamanho);
  inicio = clock();
  insertionSortStr(copia, tamanho);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("string", tamanho, "insertion_sort", tempo, 0);
  free(copia);

  // --- Merge Sort ---
  copia = copiarVetorStr(vetor, tamanho);
  inicio = clock();
  mergeSortStr(copia, 0, tamanho - 1);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("string", tamanho, "merge_sort", tempo, 0);
  free(copia);

  // --- Quick Sort ---
  copia = copiarVetorStr(vetor, tamanho);
  inicio = clock();
  quickSortStr(copia, 0, tamanho - 1);
  fim = clock();
  tempo = (double)(fim - inicio) / CLOCKS_PER_SEC;
  printCSV("string", tamanho, "quick_sort", tempo, 0);
  free(copia);

  // Libera strings
  for (int i = 0; i < tamanho; i++)
    if (vetor[i]) free(vetor[i]);
  free(vetor);
}

int main (int argc, char *argv[]) {
  if (argc != 4) {
    printf("Uso: programa.exe <arquivo> <tipo> <tamanho>\n");
    printf("  tipo: inteiro | string\n");
    return 1;
  }

  const char *arquivo = argv[1];
  const char *tipo = argv[2];
  int tamanho = atoi(argv[3]);

  if (strcmp(tipo, "inteiro") == 0)
    benchmarkInt(arquivo, tamanho);
  else if (strcmp(tipo, "string") == 0)
    benchmarkStr(arquivo, tamanho);
  else
    printf("Tipo invalido: %s (use 'inteiro' ou 'string')\n", tipo);

  return 0;
}
