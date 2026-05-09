#include "ordAlg.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


// =============================================
//   ORDENAÇÃO DE INTEIROS
// =============================================

// Insertion Sort - Inteiros
void insertionSortInt (int *vetor, int n) {

  for (int i = 1; i < n; i++) {
    int chave = vetor[i];
    int j = i - 1;

    while (j >= 0 && vetor[j] > chave) {
      vetor[j + 1] = vetor[j];
      j--;
    }

    vetor[j + 1] = chave;
  }
}

// Merge Sort - funções auxiliares para inteiros
static void mergeInt (int *vetor, int esq, int meio, int dir) {

  int n1 = meio - esq + 1;
  int n2 = dir - meio;

  int *L = (int *) malloc (n1 * sizeof(int));
  int *R = (int *) malloc (n2 * sizeof(int));

  for (int i = 0; i < n1; i++)
    L[i] = vetor[esq + i];
  for (int j = 0; j < n2; j++)
    R[j] = vetor[meio + 1 + j];

  int i = 0, j = 0, k = esq;

  while (i < n1 && j < n2) {
    if (L[i] <= R[j]) {
      vetor[k] = L[i];
      i++;
    } else {
      vetor[k] = R[j];
      j++;
    }
    k++;
  }

  while (i < n1) {
    vetor[k] = L[i];
    i++;
    k++;
  }

  while (j < n2) {
    vetor[k] = R[j];
    j++;
    k++;
  }

  free(L);
  free(R);
}

// Merge Sort - Inteiros
void mergeSortInt (int *vetor, int esq, int dir) {

  if (esq < dir) {
    int meio = esq + (dir - esq) / 2;

    mergeSortInt(vetor, esq, meio);
    mergeSortInt(vetor, meio + 1, dir);
    mergeInt(vetor, esq, meio, dir);
  }
}

// Quick Sort - partição para inteiros
static int partitionInt (int *vetor, int low, int high) {

  int pivot = vetor[high];
  int i = low - 1;

  for (int j = low; j < high; j++) {
    if (vetor[j] <= pivot) {
      i++;
      int temp = vetor[i];
      vetor[i] = vetor[j];
      vetor[j] = temp;
    }
  }

  int temp = vetor[i + 1];
  vetor[i + 1] = vetor[high];
  vetor[high] = temp;

  return i + 1;
}

// Quick Sort - Inteiros
void quickSortInt (int *vetor, int low, int high) {

  if (low < high) {
    int pi = partitionInt(vetor, low, high);

    quickSortInt(vetor, low, pi - 1);
    quickSortInt(vetor, pi + 1, high);
  }
}


// =============================================
//   ORDENAÇÃO DE STRINGS
// =============================================

// Insertion Sort - Strings
void insertionSortStr (char **vetor, int n) {

  for (int i = 1; i < n; i++) {
    char *chave = vetor[i];
    int j = i - 1;

    while (j >= 0 && strcmp(vetor[j], chave) > 0) {
      vetor[j + 1] = vetor[j];
      j--;
    }

    vetor[j + 1] = chave;
  }
}

// Merge Sort - funções auxiliares para strings
static void mergeStr (char **vetor, int esq, int meio, int dir) {

  int n1 = meio - esq + 1;
  int n2 = dir - meio;

  char **L = (char **) malloc (n1 * sizeof(char *));
  char **R = (char **) malloc (n2 * sizeof(char *));

  for (int i = 0; i < n1; i++)
    L[i] = vetor[esq + i];
  for (int j = 0; j < n2; j++)
    R[j] = vetor[meio + 1 + j];

  int i = 0, j = 0, k = esq;

  while (i < n1 && j < n2) {
    if (strcmp(L[i], R[j]) <= 0) {
      vetor[k] = L[i];
      i++;
    } else {
      vetor[k] = R[j];
      j++;
    }
    k++;
  }

  while (i < n1) {
    vetor[k] = L[i];
    i++;
    k++;
  }

  while (j < n2) {
    vetor[k] = R[j];
    j++;
    k++;
  }

  free(L);
  free(R);
}

// Merge Sort - Strings
void mergeSortStr (char **vetor, int esq, int dir) {

  if (esq < dir) {
    int meio = esq + (dir - esq) / 2;

    mergeSortStr(vetor, esq, meio);
    mergeSortStr(vetor, meio + 1, dir);
    mergeStr(vetor, esq, meio, dir);
  }
}

// Quick Sort - partição para strings
static int partitionStr (char **vetor, int low, int high) {

  char *pivot = vetor[high];
  int i = low - 1;

  for (int j = low; j < high; j++) {
    if (strcmp(vetor[j], pivot) <= 0) {
      i++;
      char *temp = vetor[i];
      vetor[i] = vetor[j];
      vetor[j] = temp;
    }
  }

  char *temp = vetor[i + 1];
  vetor[i + 1] = vetor[high];
  vetor[high] = temp;

  return i + 1;
}

// Quick Sort - Strings
void quickSortStr (char **vetor, int low, int high) {

  if (low < high) {
    int pi = partitionStr(vetor, low, high);

    quickSortStr(vetor, low, pi - 1);
    quickSortStr(vetor, pi + 1, high);
  }
}
