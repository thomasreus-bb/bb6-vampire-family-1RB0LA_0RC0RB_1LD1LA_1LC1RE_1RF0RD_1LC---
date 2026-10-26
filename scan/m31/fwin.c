#include <stdio.h>
#include <stdlib.h>
static const char*M="1RB1RF_1RC0LD_1LB1RA_1RE1LE_0RC0LB_0RB---";
int W[6][2],D[6][2],N[6][2];
#define SZ 4000000
unsigned char tp[SZ];
int main(int c,char**v){ long long NS=atoll(v[1]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long p=SZ/2; int q=0; long long st=0, nf=0; long long cnt[1<<12]={0}; long long cc[1<<10]={0};
 while(st<NS){ int b=tp[p];
  if(q==2&&b==1){ int w=0; for(int k=-4;k<=5;k++) w=w*2+tp[p+k]; cc[w>>0 & 1023]++; }
  if(q==5){ nf++; int w=0; for(int k=-6;k<=5;k++) w=w*2+tp[p+k]; cnt[w]++; }
  if(N[q][b]<0){printf("HALT %lld\n",st);return 0;} tp[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; st++; }
 printf("F entered %lld times in %lld steps\n",nf,NS);
 for(int w=0;w<4096;w++) if(cnt[w]){ printf("F window (cells p-6..p+5, head at 7th): "); for(int k=11;k>=0;k--) putchar('0'+((w>>k)&1)); printf("  %lld\n",cnt[w]); }
 printf("C reading 1, windows p-4..p+5:\n");
 for(int w=0;w<1024;w++) if(cc[w]){ for(int k=9;k>=0;k--) putchar('0'+((w>>k)&1)); printf("  %lld\n",cc[w]); }
}
