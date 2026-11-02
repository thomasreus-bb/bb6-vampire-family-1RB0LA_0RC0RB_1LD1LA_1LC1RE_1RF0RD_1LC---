// one Bell from config  [0] P 1^N S  (head on the 0, state C, nothing to the left)
// prints:  P' N' S' steps   or HALT steps  or NONE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[6][2],D[6][2],N[6][2];
int main(int argc,char**argv){ const char*M=argv[1]; const char*P=argv[2]; long n=atol(argv[3]); const char*S=argv[4]; long long maxs=atoll(argv[5]);
 if(!strcmp(P,"-"))P=""; if(!strcmp(S,"-"))S="";
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long L=8*n+100000; unsigned char*t=calloc(L,1); long h=L/4, lo=h, x=h+1;
 for(const char*p=P;*p;p++) t[x++]=*p-'0'; for(long i=0;i<n;i++) t[x++]=1; for(const char*p=S;*p;p++) t[x++]=*p-'0';
 long hi=x; int s=2;
 for(long long k=0;k<maxs;k++){ int b=t[h]; if(N[s][b]<0){ printf("HALT %lld %c%d\n",k,'A'+s,b); return 0;} t[h]=W[s][b]; h+=D[s][b]; s=N[s][b];
   if(h>hi) hi=h; if(h<2||h>L-3){ printf("NONE\n"); return 0; }
   if(h<lo){ lo=h; if(s==2){ long r=hi; while(r>h&&!t[r]) r--;
       // longest run of ones in h+1..r
       long bs=-1,bl=0,cs=-1,cl=0; for(long y=h+1;y<=r;y++){ if(t[y]){ if(cl==0) cs=y; cl++; if(cl>bl){bl=cl;bs=cs;} } else cl=0; }
       if(bs>=0 && bs-(h+1)<=4 && bl>=n/2){ char Pp[64],Sp[4096]; int a=0; for(long y=h+1;y<bs;y++) Pp[a++]='0'+t[y]; Pp[a]=0; a=0; for(long y=bs+bl;y<=r&&a<4000;y++) Sp[a++]='0'+t[y]; Sp[a]=0;
         printf("%s %ld %s %lld\n",*Pp?Pp:"-",bl,*Sp?Sp:"-",k+1); return 0; } } } }
 printf("NONE\n"); }
