#include <cstdio>

#include "shared.h"
#include "static.h"

int main(int argc, char *argv[]) {
  printf("%s\n", shared_library_function());
  printf("%s\n", static_library_function());
  return 0;
}
