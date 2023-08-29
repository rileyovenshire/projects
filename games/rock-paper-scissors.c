/*
My first project in C, I used GfG as a guide: https://www.geeksforgeeks.org/rock-paper-scissor-in-c/


standard rules: 
- Rock beats Scissors
- Scissors beats Paper
- Paper beats Rock
*/

// libraries 
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>

// function for the game
int game(char player, char computer)
{

    // if computer and user choose the same
    if (player == computer)
        return -1;

// Rock vs. Paper --------------------------------------------------

    // if player choses rock and computer chooses paper - player L
    if (player == 'R' && computer == 'P')
        return 0;

    // if reverse; player picks paper and computer chooses rock - player W
    else if (player == 'P' && computer == 'R')
    return 1;

// Rock vs. Scisssors --------------------------------------------------

    // if player chooses rock and computer chooses scissors - player W
    if (player == 'R' && computer == 'S')
        return 1;

    // if player chooses scissors and computer chooses rock - player L
    else if (player == 'S' && computer == 'R')
        return 0;

// Scissors vs. Paper --------------------------------------------------
    // if player chooses paper and computer chooses scissors - player L
    if (player == 'P' && computer == 'S')
        return 0;

    else if (player == 'S' && computer == 'P')
        return 1;
}

// driver code
int main()
{
    // random number
    int num;

    // store variables
    char player;
    char computer;
    char result;

    // pick that random number
    srand(time(NULL));

    // make random number less than 100 and divide that by 100
    num = rand() % 100;

    // 0-32, computer chooses Paper
    if (num < 33)
        computer = 'P';

    // 33-65, computer chooses Rock
    else if (num > 33 && num < 66)
        computer = 'R';

    // 66-100, computer chooses Scissors
    else
        computer = 'S';



    // display instructions
    printf("\n\n\n\n\t\t\t\tEnter P for PAPER, R for ROCK, and S for SCISSORS\n\t\t\t\t\t\t\t");

    // take the user's input
    scanf("%c", &player);

    // call the gameplay function
    result = game(player, computer);

    // draw
    if (result == -1) {
        printf("\n\n\t\t\t\tTie!\n");
    }

    // player wins
    else if (result == 1) {
        printf("\n\n\t\t\t\tCongratulations, you won!\n");
    }

    // player loses
    else {
        printf("\n\n\t\t\t\tOpe, you lost!\n");
    }

    // show resuls
    printf("\t\t\t\tYour choice: %c and Computer's choice: %c\n",player, computer);
 
    return 0;

}   
