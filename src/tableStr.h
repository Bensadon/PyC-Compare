#ifndef TABLESTR_H
#define TABLESTR_H

#include <stdbool.h>

// Struct do item da hash table de strings
typedef struct Item_str {
  char *str;
  bool occupied;
} Item_str;

// Leitura de entrada
char **entradaStr (int tam);

// Hash table
Item_str *criateTableStr (char **vetor, int mapSize, int tamVet);
int hashStr1 (const char *str, int mapSize);
int hashStr2 (const char *str, int mapSize, int tentativa);

// Busca
bool buscaStr (Item_str *table, const char *str, int mapSize);

// Remoção + resize
Item_str *resizeStr (Item_str *table, int oldSize, int count, int *newSize);
Item_str *removeStr (Item_str *table, const char *str, int mapSize, int *count, int *currentSize);

#endif
