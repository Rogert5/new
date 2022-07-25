// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
// Able to use node throughout program
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
//Left at 26 to cover 26 letters of the alphabet
const unsigned int N = 26;

// Hash table
node *table[N];

//Declare variables
//added for keeping count of words aswell ad value of hash in line 37
unsigned int word_count;
unsigned int hash_value;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    hash_value = hash(word);
    // setting cursor to be the start of the linked list
    node *cursor = table[hash_value];

    //going through linked list as long as cursor is not equal to NULL
    while (cursor != 0)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned long total = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        total = tolower(word[i]) + total;
    }
    return total % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO Open file: dictionary
    FILE* file = fopen(dictionary,"r");
    {
        //Return NULL if it cannot be opened
        if (file == NULL)
        {
            printf("Unable to open %s.\n", dictionary);
            return false;
        }

        //Declaring word variable
        char word[LENGTH+1];

        //Scan dictionary for srings up until EndOfFile (EOF)
        while (fscanf(file, "%s", word) != EOF)
        {
            //allocating extra memory for each word
            node *n = malloc(sizeof(node));

            //return false if NULL
            if (n == NULL)
            {
            return false;
            }

            //copy word into node
            strcpy(n->word, word);
            hash_value = hash(word);
            n->next = table[hash_value];
            table[hash_value] = n;
            word_count++;
        }
        fclose(file);
        return true;
    }
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (word_count > 0)
    {
        return word_count;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    for (int i = 0; i < N; i++)
    {
        //setting cursor to the start of linked list
        node *cursor = table[i];

        //if cursor is not NULL free up memory
        while (cursor != NULL)
        {
            //Create temp
            node *tmp = cursor;
            //move cursor to next node
            cursor = cursor->next;
            //free up temp
            free(tmp);
        }
        if (cursor == NULL && i == N - 1)
        {
            return true;
        }
    }
    return false;
}
