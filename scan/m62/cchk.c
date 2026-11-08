// cchk M STEPS : at right records in state C, print step, c (leading 1s), b ((01) pairs after "1^c 0") and t, whenever c changes
#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; double n=atof(v[2]); int q=0;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=4000000; unsigned char*t=calloc(SZ,1); long p=SZ/10,lo=p,hi=p; long lastc=-1;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s+1);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b];
  if(p<lo)lo=p;
  if(p>hi){ hi=p; if(q==2){ long i=lo; while(i<hi&&!t[i])i++; long a=i; while(t[i])i++; long cc=i-a;
     if(cc!=lastc){ lastc=cc; i++; long bb=0; while(i+1<hi&&t[i]==0&&t[i+1]==1){bb++;i+=2;} long ones=0; while(i<hi&&t[i]){ones++;i++;}
       printf("%lld c=%ld b=%ld ones=%ld rest=%ld\n",s+1,cc,bb,ones,hi-i); fflush(stdout);} } } }
 printf("END\n"); }
