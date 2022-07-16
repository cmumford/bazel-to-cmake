#include <iostream>

#include "sum.h"

int main(int argc, char** argv) {
    int x = 3;
    int y = 4;
  std::cout << "The sum of " << x << " and " << y << " = " << addints(x, y) << std::endl;
  return 0;
}
