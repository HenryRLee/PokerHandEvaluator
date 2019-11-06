#include <iostream>
#include "include/phevaluator/phevaluator.h"

int main(){
  std::cout << "Hello World!" << std::endl;
  for(int a = 0; a < 48; a++) {
    std::cout << "CARD NUMBER: " << a << std::endl;
    for(int b = a + 1; b < 49; b++) {
      for(int c = b + 1; c < 50; c++) {
        for(int d = c + 1; d < 51; d++) {
          for(int e = d + 1; e < 52; e++) {
            phevaluator::EvaluateCards(a, b, c, d, e);
          }
        }
      }
    }
  }
  std::cout << "Bye World!" << std::endl;
}
