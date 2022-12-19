#include <stdio.h>
#include <stdlib.h>
int main(int argc,char *argv[])
{
  int i, j;
  int len = 20;

  double a[20][20];

  #pragma omp parallel for private(i ,j )
  for (i=0; i< len; i++){
    #pragma omp parallel for private(j )
    for (j=0; j<len; j++){
      a[i][j] = (i * len + j + 0.5);
    }
  }

  for (i = 0; i < len - 1; i += 1) {
    #pragma omp parallel for
    for (j = 0; j < len ; j += 1) {
      a[i][j] += a[i + 1][j];
    }
  }

  for (i=0; i< len; i++){
    for (j=0; j<len; j++){
      printf("%lf",a[i][j]);
    }
  }

  printf ("a[10][10]=%f\n", a[10][10]);
  return 0;
}
