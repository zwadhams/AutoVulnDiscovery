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
  while (x >= y)
  {
    puts("zach's test while loop");
    y++;
  }
  
  if (x > y) {
    int i = 0;
  }
  else{
    int i = 1;
    //x++;
  }
  x++;
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