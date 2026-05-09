#include "tableInt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
  Analisador de colisões da Hash Table
  Uso: collision_analyzer.exe <arquivo> <tamanho> <multiplicador>

  multiplicador: mapSize = maiorPrimo(tamanho * multiplicador)
    1 = fator de carga ~100%
    2 = fator de carga ~50%
    3 = fator de carga ~33%
*/

int *lerArquivo (const char *caminho, int tam) {
  FILE *f = fopen(caminho, "r");
  if (!f) { printf("Erro ao abrir %s\n", caminho); return NULL; }

  int *vetor = (int *) malloc (tam * sizeof(int));
  for (int i = 0; i < tam; i++) {
    if (fscanf(f, "%d", &vetor[i]) != 1) break;
  }
  fclose(f);
  return vetor;
}

Item_int *criateTableComStats (int *vetor, int mapSize, int tamVet,
                                int *totalColisoes, int *maxTentativas,
                                int *histograma, int histoSize) {

  Item_int *table = (Item_int *) calloc (mapSize, sizeof(Item_int));
  *totalColisoes = 0;
  *maxTentativas = 0;

  for (int i = 0; i < tamVet; i++) {
    int key = hashInt1(vetor[i], mapSize);
    int tentativas = 0;

    while (table[key].occupied) {
      tentativas++;
      key = hashInt2(vetor[i], mapSize, tentativas);
    }

    table[key].valor = vetor[i];
    table[key].occupied = true;

    *totalColisoes += tentativas;
    if (tentativas > *maxTentativas)
      *maxTentativas = tentativas;

    if (tentativas < histoSize)
      histograma[tentativas]++;
    else
      histograma[histoSize - 1]++;
  }

  return table;
}

int main (int argc, char *argv[]) {
  if (argc != 4) {
    printf("Uso: collision_analyzer.exe <arquivo> <tamanho> <multiplicador>\n");
    printf("  multiplicador: 1=100%%, 2=50%%, 3=33%%\n");
    return 1;
  }

  const char *arquivo = argv[1];
  int tamanho = atoi(argv[2]);
  int multiplicador = atoi(argv[3]);

  int *vetor = lerArquivo(arquivo, tamanho);
  if (!vetor) return 1;

  int mapSize = maiorPrimo(tamanho * multiplicador);
  double fatorCarga = (double)tamanho / mapSize;

  int histoSize = 100;
  int *histograma = (int *) calloc (histoSize, sizeof(int));
  int totalColisoes = 0;
  int maxTentativas = 0;

  Item_int *table = criateTableComStats(vetor, mapSize, tamanho,
                                         &totalColisoes, &maxTentativas,
                                         histograma, histoSize);

  int slotsVazios = 0;
  for (int i = 0; i < mapSize; i++) {
    if (!table[i].occupied) slotsVazios++;
  }

  double media = (double)totalColisoes / tamanho;
  int semColisao = histograma[0];

  // Saída CSV para stdout (capturada pelo Python)
  // formato: tamanho,multiplicador,fator_carga,total_colisoes,max_tentativas,media_tentativas,sem_colisao_pct,com_colisao_pct
  printf("%d,%d,%.4f,%d,%d,%.4f,%.1f,%.1f\n",
    tamanho, multiplicador, fatorCarga,
    totalColisoes, maxTentativas, media,
    (double)semColisao / tamanho * 100,
    (double)(tamanho - semColisao) / tamanho * 100);

  free(histograma);
  free(table);
  free(vetor);
  return 0;
}
