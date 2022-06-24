#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    //Start by saying if score1 one is bigger then print player 1 is the winner
    //REMEMBER to always end "words" with a \n .. example: ("example sentence.\n"); othewrise look below for use case
    if(score1 > score2)
    {
    printf("Player 1 wins!\n");
    }
    //Made the else if , so if score2 is bigger then print player 2 is the winner.
    else if(score1 < score2)
    {
    printf("Player 2 wins!\n");
    }
    //Think of how it will go if an outcome is a tie or related
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    //keeps track of score
    int score = 0;

    //int i=0, represent index of the character in the word
    //len=strlen , is to acces how long the string"word" is
    // i<len, is saying to keep repeating as long as the integer from word is less than the amount of letters in the word
    // i++ ,is increasing i by one everytime loop completes an ineration (identifies letters number and value)
    for(int i = 0, len = strlen(word); i < len; i++)
    {
        if (isupper(word[i]))
            {
            score += POINTS[word[i] - 'A'];
            }
        else if (islower(word[i]))
            {
            score += POINTS[word[i] - 'a'];
            }
    }
    return score;
}
