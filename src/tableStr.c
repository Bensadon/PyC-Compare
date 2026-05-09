#include "tableStr.h"
#include "tableInt.h"  // para usar isPrimo, menorPrimo, maiorPrimo
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
Monta as hash tables com as entradas (strings)
*/

// recebe entrada de strings
char **entradaStr (int tam) {

  char **vetor = (char **) malloc (tam * sizeof(char *));

  if (vetor == NULL)
    return NULL;

  char buffer[256];

  for (int i = 0; i < tam; i++) {
    if (scanf("%255s", buffer) != 1)
      break;
    vetor[i] = (char *) malloc ((strlen(buffer) + 1) * sizeof(char));
    strcpy(vetor[i], buffer);
  }

  return vetor;
}

// hash primário para strings (djb2)
int hashStr1 (const char *str, int mapSize) {

  unsigned long hash = 5381;
  int c;

  while ((c = *str++)) {
    hash = ((hash << 5) + hash) + c;  // hash * 33 + c
  }

  return (int)(hash % mapSize);
}

// hash secundário para strings (double hashing)
int hashStr2 (const char *str, int mapSize, int tentativa) {

  int h1 = hashStr1(str, mapSize);

  int primo_aux = menorPrimo(mapSize);

  // hash auxiliar diferente do h1 (sdbm)
  unsigned long hash2 = 0;
  const char *p = str;
  int c;
  while ((c = *p++)) {
    hash2 = c + (hash2 << 6) + (hash2 << 16) - hash2;
  }

  int h2 = primo_aux - (int)(hash2 % primo_aux);

  return (h1 + tentativa * h2) % mapSize;
}

// cria a hash table de strings
Item_str *criateTableStr (char **vetor, int mapSize, int tamVet) {

  int i = 0;

  Item_str *table = (Item_str *) calloc (mapSize, sizeof(Item_str));

  while (i < tamVet) {

    int key;
    int j = 1;

    key = hashStr1(vetor[i], mapSize);

    while (table[key].occupied) {

      key = hashStr2(vetor[i], mapSize, j);
      j++;
    }

    table[key].str = vetor[i];  // aponta para a mesma string
    table[key].occupied = true;
    i++;
  }

  return table;
}

// Busca uma string na hash table
bool buscaStr (Item_str *table, const char *str, int mapSize) {

  int key = hashStr1(str, mapSize);
  int j = 1;

  while (table[key].occupied) {
    if (table[key].str != NULL && strcmp(table[key].str, str) == 0)
      return true;
    key = hashStr2(str, mapSize, j);
    j++;
    if (j > mapSize) break;
  }

  return false;
}

// Resize + rehash para strings
Item_str *resizeStr (Item_str *table, int oldSize, int count, int *newSize) {

  *newSize = maiorPrimo(count * 3 / 2);
  Item_str *newTable = (Item_str *) calloc (*newSize, sizeof(Item_str));

  for (int i = 0; i < oldSize; i++) {
    if (table[i].occupied && table[i].str != NULL) {
      int key = hashStr1(table[i].str, *newSize);
      int j = 1;

      while (newTable[key].occupied) {
        key = hashStr2(table[i].str, *newSize, j);
        j++;
      }

      newTable[key].str = table[i].str;
      newTable[key].occupied = true;
    }
  }

  free(table);
  return newTable;
}

// Remove uma string da hash table (marca str como NULL, slot continua occupied)
Item_str *removeStr (Item_str *table, const char *str, int mapSize, int *count, int *currentSize) {

  int key = hashStr1(str, mapSize);
  int j = 1;

  while (table[key].occupied) {
    if (table[key].str != NULL && strcmp(table[key].str, str) == 0) {
      free(table[key].str);   // libera a memória da string
      table[key].str = NULL;  // sentinela: slot occupied mas vazio
      (*count)--;

      if (*count > 0 && *count < mapSize / 4) {
        table = resizeStr(table, mapSize, *count, currentSize);
      }

      return table;
    }
    key = hashStr2(str, mapSize, j);
    j++;
    if (j > mapSize) break;
  }

  return table;
}
