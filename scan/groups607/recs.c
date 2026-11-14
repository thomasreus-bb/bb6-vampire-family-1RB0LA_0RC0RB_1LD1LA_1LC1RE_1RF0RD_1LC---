// recs TM Q N EVERY MAXW: run TM from the blank tape in state Q for N steps; at every EVERY-th record
// (new leftmost or rightmost cell) print the step, the side (L/R), the state and the tape lo..hi (if width <= MAXW).
#include <stdio.h>
#include <stdlib.h>
int W[6][2],D[6][2],X[6][2];
int main(int c,char**v){ const char*M=v[1]; int q=v[2][0]-'A'; long long N=atoll(v[3]); long ev=atol(v[4]); long maxw=atol(v[5]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){X[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;X[i][b]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p; long nrec=0;
 for(long long s=0;s<N;s++){ int b=t[p]; if(X[q][b]<0){printf("HALT %lld\n",s);return 0;}
   t[p]=W[q][b]; p+=D[q][b]; q=X[q][b];
   if(p<1||p>=SZ-1){printf("EDGE %lld\n",s);return 0;}
   int side=0; if(p<lo){lo=p;side='L';} else if(p>hi){hi=p;side='R';}
   if(side){ nrec++; printf("%lld %c %c ",s,side,'A'+q); if(nrec%ev==0 && hi-lo<maxw){for(long i=lo;i<=hi;i++)putchar('0'+t[i]);} else printf("-"); putchar('\n'); } }
 printf("END %ld\n",hi-lo+1); }
