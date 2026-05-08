#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>


/*
Monta as hash tables com as entradas
*/




typedef struct Item_int{
    int valor;
    bool occupied;
} Item_int;




//recebe entrada

int* entradaInt (int tam) {

    int* vetor = (int*) malloc (tam * sizeof(int));

    if (vetor == NULL) return NULL;

    for (int i = 0; i < tam; i++){
        if (scanf("%d" , &vetor[i]) != 1) break;
    }

    return vetor;
}



Item_int* criateTable (int *vetor, int mapSize, int tamVet) { 

    int i = 0;

    Item_int *table = (Item_int *) calloc (mapSize, sizeof(Item_int));

    while (i < tamVet - 1) {
        
        int key;
        int j = 1;

        key = hashInt1 (vetor[i], mapSize);
        
        while (table[key].occupied == true) {

            key = hashInt2 (vetor[i], mapSize, j);
            j++;
        }

        table[key].valor = vetor[i];
        table[key].occupied = true;
        i++;
    }

    return table;
}


int hashInt1 (int valor, int mapSize) {

    int key;

    return key = valor % mapSize;
}


int hashInt2 (int valor,int mapSize, int try){}









