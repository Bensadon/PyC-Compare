#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>









int NextPrimo (int n_entrada){
}






int main(){



    int n_entrada;
    int tableSize;
    clock_t inicio, fim;
    double tempo_total;

    inicio = clock();

    scanf ("%d", &n_entrada);

    tableSize = NextPrimo(n_entrada);

    Item_int** hashtable = (Item_int **) calloc (tableSize, sizeof(Item_int *));

    hashtable = HashFunction_int (hashtable, tableSize);

    fim = clock();

    tempo_total = (double)(fim - inicio) / CLOCKS_PER_SEC;
    
}


