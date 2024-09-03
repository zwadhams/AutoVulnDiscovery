#include <string.h>
#include <stdio.h>
#include <unistd.h>

void first128(char *str) {
  char buffer[128];
  strcpy(buffer, str);
  printf("%s\n", buffer);
}

int main(int argc, char **argv) {
  static char input[1024];
  while (read(STDIN_FILENO, input, 1024) > 0) {
    first128(input);
  }
  return 0;
}
