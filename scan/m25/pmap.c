// pmap TAPE_RIGHT MAXSTEPS: start at P = 0^inf 1 0 A> 0 TAPE_RIGHT, run to the next P config (left part exactly "10", A on 0)
// prints: P <steps> <right part after the head cell>  or HALT/MAX
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M="1RB0LE_1LC0RD_0RA1LD_0LC1RA_1LF1LA_---1LA"; const char*T=v[1]; long long n=atoll(v[2]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<26; unsigned char*t=calloc(SZ,1); long p=SZ/2; long L=strlen(T);
 t[p-2]=1; t[p-1]=0; t[p]=0; for(long i=0;i<L;i++) t[p+1+i]=T[i]-'0';
 int q=0; long lo=p-2, hi=p+L;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
  if(p<lo)lo=p; if(p>hi)hi=p;
  if(q==0 && t[p]==0 && t[p-1]==0 && t[p-2]==1 && t[p+1]==1){ int ok=1; for(long i=lo;i<p-2;i++) if(t[i]){ok=0;break;}
    if(ok && s>0){ printf("P %lld ",s+1); long h=hi; while(h>p&&!t[h])h--; for(long i=p+1;i<=h;i++) putchar('0'+t[i]); printf("\n"); return 0;} } }
 printf("MAX\n"); }
