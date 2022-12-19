#include <stdio.h>
#include <stdlib.h>
int main(int argc,char *argv[])
{
  int i, j;
  int len = 20;

  double a[20][20];

  #pragma omp parallel for private(i ,j )
  for (i=0; i< len; i++){
    for (j=0; j<len; j++){
      a[i][j] = (i * len + j + 0.5);
    }
  }
}
