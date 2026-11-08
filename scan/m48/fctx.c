// fctx STEPS : direct simulation of no. 48; every time state F is entered (from E reading 1), record the
// 8 cells around the head (4 left of the cell F will read, that cell, 3 right). Prints counts per context
// and the first/last step for each. HALT happens when F reads a 1.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
const char*M="1RB1RD_1LC0LE_1LD0LB_0RB0RA_1RD1LF_0LC---";
long long cnt[1<<16],first[1<<16],last[1<<16];
int main(int c,char**v){ double n=atof(v[1]); unsigned char W[12],N[12]; signed char D[12];
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b;int k=2*i+b; if(x[0]=='-'){N[k]=255;continue;} W[k]=x[0]-'0';D[k]=x[1]=='R'?1:-1;N[k]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=calloc(SZ,1); long p=SZ/2; int q=0;
 for(long long s=0;s<n;s++){ int k=2*q+t[p]; if(N[k]==255){printf("HALT %lld\n",s+1);break;} t[p]=W[k]; p+=D[k]; q=N[k];
  if(q==5){ int h=0; for(int j=-4;j<=3;j++) h=h*2+t[p+j]; if(!cnt[h])first[h]=s+1; cnt[h]++; last[h]=s+1; } }
 for(int h=0;h<256;h++) if(cnt[h]){ for(int j=7;j>=0;j--){ if(j==3)putchar('['); putchar('0'+((h>>j)&1)); if(j==3)putchar(']');} printf(" %lld first %lld last %lld\n",cnt[h],first[h],last[h]); }
}
