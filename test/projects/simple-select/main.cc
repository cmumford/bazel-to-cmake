#include <iostream>

#include "message.h"

int main(int argc, char** argv) {
  std::cout << "Message: \"" << get_message() << '"' << std::endl;
  return 0;
}
