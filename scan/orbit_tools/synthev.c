/* synth TM q headoff maxsteps : reads tape string (0/1) from stdin, head at headoff in state q,
   runs until the head moves left of cell 0 (a new left record) or HALT or maxsteps.
   prints: STATUS q steps | tape-from-new-left-end (as 0/1 string, trimmed of trailing zeros beyond hi) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int q=v[2][0]-'A'; long off=atol(v[3]); long long mx=atoll(v[4]); const char*EVS=c>5?v[5]:"ABCDEF";
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 static char buf[1<<26]; if(!fgets(buf,sizeof buf,stdin)) return 1; long L=strlen(buf); while(L&&(buf[L-1]=='\n'||buf[L-1]=='\r'))L--;
 long SZ=(L+1000)*8+(1<<20); unsigned char*t=calloc(SZ,1); long base=SZ/2; for(long i=0;i<L;i++) t[base+i]=buf[i]-'0';
 long p=base+off, lo=base, hi=base+L-1; long long s=0;
 for(;s<mx;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %c %lld\n",'A'+q,s);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
   if(p>hi)hi=p; if(p<lo && !strchr(EVS,(char)(65+q))){lo=p;} else if(p<lo){ printf("REC %c %lld ",'A'+q,s+1); for(long i=p;i<=hi;i++) putchar('0'+t[i]); putchar('\n'); return 0;}
   if(p<2||p>SZ-3){printf("TAPE\n");return 0;} }
 printf("MAX\n"); }
