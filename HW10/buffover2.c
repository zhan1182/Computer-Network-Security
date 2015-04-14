// buffover2.c

// This example is used in Section 21.5 of Lecture 21 to
// demonstrate how even an innocent looking program can be 
// made to produce incorrect results through buffer overflow.

#include <stdio.h>

int main() {
    while(1) foo();
}

int foo(){
    unsigned int yy = 0;
    char buffer[5]; char ch; int i = 0; 
    printf("Say something: ");
    while ((ch = getchar()) != '\n')  {
        buffer[i++] = ch;
    }
    buffer[i] = '\0';
    printf("You said: %s\n", buffer);
    printf("The variable yy: %d\n", yy);
    return 0;
}
