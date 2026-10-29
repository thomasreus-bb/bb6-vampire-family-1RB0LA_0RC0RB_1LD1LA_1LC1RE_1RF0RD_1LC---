#include <stdio.h>
#include <stdlib.h>
int W[8][2],D[8][2],N[8][2];
int main(int c,char**v){ const char*M=v[1]; int q=v[2][0]-'A'; long long n=atoll(v[3]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=40000000; unsigned char*t=calloc(SZ,1); long p=SZ/2,lo=p,hi=p;
 for(long long s=0;s<n;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; if(p<lo)lo=p; if(p>hi)hi=p; }
 long a=lo; while(!t[a])a++; long e=hi; while(!t[e])e--;
 printf("state %c head %ld width %ld |",'A'+q,p-a,e-a+1);
 long i=a; while(i<=e){ long j=i; while(j<=e&&t[j]==t[i]) j++; if(j-i>1||t[i]) printf(" %c%ld",t[i]?'1':'0',j-i); else printf(" 0"); i=j; } printf("\n"); }
