// buffover.c

// This example is used in Section 21.4.1 of Lecture 21 to demonstrate
// how buffer overflow can cause this program to crash.

#include <stdio.h>

int main() {
    foo();
}

int foo(){
    char buffer[5]; char ch; int i = 0; 
    printf("Say something: ");
    while ((ch = getchar()) != '\n')  buffer[i++] = ch;
    buffer[i] = '\0';
    printf("You said: %s\n", buffer);
    return 0;
}
