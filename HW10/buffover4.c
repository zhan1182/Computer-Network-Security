// buffover4.c

// This example is used in Section 21.6 of Lecture 21 to
// demonstrate how the buffer overflow vulnerability in 
// the function foo() can be used to cause the execution 
// of bar() even though there is no explicit call to bar()
// anywhere in the code shown below.

#include <stdio.h>
#include <string.h>

void foo(char *s) {
    char buf[4]; 
    strcpy(buf, s); 
    printf("You entered: %s", buf);
}

void bar() {
  printf("\n\nWhat? I was not supposed to be called!\n\n");
  fflush(stdout);
}

int main(int argc, char *argv[]) {
  if (argc != 2) {
    printf("Usage: %s some_string", argv[0]);
    return 2;
  }
  foo(argv[1]);
  return 0;    
}
