#include "tableInt.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// acha os primos 
bool isPrimo (int n) {
  if (n <= 1) return false;
  if (n == 2 || n == 3) return true;
  if (n % 2 == 0 || n % 3 == 0) return false;
  for (int i = 5; i * i <= n; i += 6) {
    if (n % i == 0 || n % (i + 2) == 0)
      return false;
  }
  return true;
}

int menorPrimo (int x) {
  if (x <= 3) return 2;
  int i = (x - 1) % 2 == 0 ? x - 2 : x - 1;  // começa no ímpar mais próximo abaixo de x
  while (i >= 3) {
    if (isPrimo(i)) return i;
    i -= 2;  // pula pares
  }
  return 2;
}

int maiorPrimo (int x) {
  if (x < 2) return 2;
  int i = (x + 1) % 2 == 0 ? x + 2 : x + 1;  // começa no ímpar mais próximo acima de x
  while (true) {
    if (isPrimo(i)) return i;
    i += 2;  // pula pares
  }
}

// recebe entrada

int *entradaInt(int tam) {

  int *vetor = (int *) malloc (tam * sizeof(int));

  if (vetor == NULL)
    return NULL;

  for (int i = 0; i < tam; i++) {
    if (scanf("%d", &vetor[i]) != 1)
      break;
  }

  return vetor;
}

Item_int* criateTable (int *vetor, int mapSize, int tamVet) {

  int i = 0;

  Item_int *table = (Item_int *) calloc (mapSize, sizeof(Item_int));

  while (i < tamVet - 1) {

    int key;
    int j = 1;

    key = hashInt1(vetor[i], mapSize);

    while (table[key].occupied == true) {

      key = hashInt2(vetor[i], mapSize, j);
      j++;
    }

    table[key].valor = vetor[i];
    table[key].occupied = true;
    i++;
  }

  return table;
}

int hashInt1(int valor, int mapSize) {

  int key;

  return key = valor % mapSize;
}

int hashInt2(int valor, int mapSize, int try) {

  int h1 = hashInt1(valor, mapSize);

  // Usa o menor primo em relação ao mapSize
  int primo_aux = menorPrimo(mapSize);
  
  int h2 = primo_aux - (valor % primo_aux);

  return (h1 + try * h2) % mapSize;
}

// Sentinela para marcar slots deletados
#include <limits.h>
#define DELETED_INT INT_MIN

// Busca um valor na hash table
bool buscaInt (Item_int *table, int valor, int mapSize) {

  int key = hashInt1(valor, mapSize);
  int j = 1;

  while (table[key].occupied) {
    if (table[key].valor != DELETED_INT && table[key].valor == valor)
      return true;
    key = hashInt2(valor, mapSize, j);
    j++;
    if (j > mapSize) break;  // percorreu a tabela inteira
  }

  return false;
}

// Resize + rehash: cria nova tabela com ~2/3 de ocupação
Item_int *resizeInt (Item_int *table, int oldSize, int count, int *newSize) {

  *newSize = maiorPrimo(count * 3 / 2);  // novo tamanho ≈ count / (2/3)
  Item_int *newTable = (Item_int *) calloc (*newSize, sizeof(Item_int));

  for (int i = 0; i < oldSize; i++) {
    if (table[i].occupied && table[i].valor != DELETED_INT) {
      int key = hashInt1(table[i].valor, *newSize);
      int j = 1;

      while (newTable[key].occupied) {
        key = hashInt2(table[i].valor, *newSize, j);
        j++;
      }

      newTable[key].valor = table[i].valor;
      newTable[key].occupied = true;
    }
  }

  free(table);
  return newTable;
}

// Remove um valor da hash table (marca com sentinela)
// Retorna a tabela (pode mudar de endereço se houve resize)
Item_int *removeInt (Item_int *table, int valor, int mapSize, int *count, int *currentSize) {

  int key = hashInt1(valor, mapSize);
  int j = 1;

  while (table[key].occupied) {
    if (table[key].valor != DELETED_INT && table[key].valor == valor) {
      table[key].valor = DELETED_INT;  // marca como deletado (slot continua occupied)
      (*count)--;

      // Se ocupação caiu abaixo de 25%, faz resize
      if (*count > 0 && *count < mapSize / 4) {
        table = resizeInt(table, mapSize, *count, currentSize);
      }

      return table;
    }
    key = hashInt2(valor, mapSize, j);
    j++;
    if (j > mapSize) break;
  }

  return table;  // valor não encontrado
}
