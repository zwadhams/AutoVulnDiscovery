#include <stdio.h>
#include <stdlib.h>

int y_init;

int
f() {
  return y_init;
}

int
test(int x) {
  int y = f();
  if (x > y) {
    int i = 0;
    while (i < 10) {
      x--;
      i++;
    }

    if (x == y) {
      puts("nope");
      return 0;
    } else {
      if (x < y) {
        // Get here
        puts("got it!");
        return 1;
      } else {
        puts("not here");
        return 0;
      }
    }
  }
  puts("wrong way");
  return 0;
}

int
main(int argc, char *argv[]) {
  int x = atol(argv[1]);
  y_init = atol(argv[2]);
  int result = test(x);

  printf("result: %d\n", result);

  return 0;
}