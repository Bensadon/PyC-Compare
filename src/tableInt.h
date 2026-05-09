#ifndef TABLEINT_H
#define TABLEINT_H

#include <stdbool.h>
#include <limits.h>

#define DELETED_INT INT_MIN

// Struct do item da hash table de inteiros
typedef struct Item_int {
  int valor;
  bool occupied;
} Item_int;

// Funções de primos
bool isPrimo (int n);
int menorPrimo (int x);
int maiorPrimo (int x);

// Leitura de entrada
int *entradaInt (int tam);

// Hash table
Item_int *criateTable (int *vetor, int mapSize, int tamVet);
int hashInt1 (int valor, int mapSize);
int hashInt2 (int valor, int mapSize, int tentativa);

// Busca
bool buscaInt (Item_int *table, int valor, int mapSize);

// Remoção + resize
Item_int *resizeInt (Item_int *table, int oldSize, int count, int *newSize);
Item_int *removeInt (Item_int *table, int valor, int mapSize, int *count, int *currentSize);

#endif
