#include <stdio.h>
#include <stdlib.h>
static const char*M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---";
int W[6][2],D[6][2],N[6][2];
#define SZ 4000000
unsigned char tp[SZ];
int main(int c,char**v){ long long NS=atoll(v[1]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long p=SZ/2,lo=p,hi=p; int q=0,d0=1; long long st=0; int nb=0;
 while(st<NS){ int b=tp[p]; int d=D[q][b]; tp[p]=W[q][b]; p+=d; q=N[q][b]; st++;
  if(d!=d0) putchar(d>0?'A'+q:'a'+q);   // uppercase: turned to the right (at a left end); lowercase: turned left
  d0=d; if(p<lo){lo=p; putchar('L');}
  if(p>hi){ hi=p; if(q==0){ nb++; printf("\n"); } } }
}
