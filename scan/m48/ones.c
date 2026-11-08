// ones STEPS : direct simulation of no. 48; report every time a write creates a run of >= 4 ones,
// and the maximal run of ones ever seen. (HALT needs state C moving left onto the right end of 1111.)
#include <stdio.h>
#include <stdlib.h>
const char*M="1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---";
int main(int c,char**v){ double n=atof(v[1]); unsigned char W[12],N[12]; signed char D[12];
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b;int k=2*i+b; if(x[0]=='-'){N[k]=255;continue;} W[k]=x[0]-'0';D[k]=x[1]=='R'?1:-1;N[k]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/2; int q=0; int maxrun=0; long long n4=0;
 for(long long s=0;s<n;s++){ int k=2*q+t[p]; if(N[k]==255){printf("HALT %lld\n",s+1);break;}
  int w=W[k]; long pp=p; t[p]=w; p+=D[k]; q=N[k];
  if(w){ long a=pp,b=pp; while(t[a-1])a--; while(t[b+1])b++; int r=b-a+1; if(r>maxrun){maxrun=r; printf("new max run %d at step %lld\n",r,s+1);} if(r>=4){ n4++; if(n4<=20) { printf("run %d at step %lld context ",r,s+1); for(long j=a-6;j<=b+6;j++)putchar('0'+t[j]); printf(" state %c\n",'A'+q);} } } }
 printf("runs>=4: %lld, max run %d\n",n4,maxrun); }
