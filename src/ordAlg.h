#ifndef ORDALG_H
#define ORDALG_H

// Ordenação de inteiros
void insertionSortInt (int *vetor, int n);
void mergeSortInt (int *vetor, int esq, int dir);
void quickSortInt (int *vetor, int low, int high);

// Ordenação de strings
void insertionSortStr (char **vetor, int n);
void mergeSortStr (char **vetor, int esq, int dir);
void quickSortStr (char **vetor, int low, int high);

#endif
