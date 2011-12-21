#include<stdio.h>

void main() 
{
  double s_x = 0.0, s_y = 0.0, s_z = 0.0;
  double a_x = 0.1, a_y = 0.2, a_z = 0.3;
  
  //long start = System.nanoTime();
  for(long long i = 0; i < 3000000000l; i++) {
    s_x += a_x;
    s_y += a_y;
    s_z += a_z;
  }
  //long end = System.nanoTime();
  
  printf("Hello World! %3.2f %3.2f %3.2f", s_x, s_y, s_z);
}

