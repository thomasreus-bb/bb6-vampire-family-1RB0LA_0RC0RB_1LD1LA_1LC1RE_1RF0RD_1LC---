#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// bands of 1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE: a band runs from one new-left-cell event (state C) to the next
static const char*M="1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE";
int W[6][2],D[6][2],N[6][2];
#define SZ 20000000
unsigned char tp[SZ];
int main(int c,char**v){int NB=atoi(v[1]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long p=SZ/2,lo=p,hi=p; int q=0,d0=1; long long st=0; int nb=0; char tw[64]; int tl=0; char word[100000]; int wl=0; int last2=-1; long cnt=0;
 while(nb<NB){ int b=tp[p]; if(N[q][b]<0){printf("HALT at step %lld\n",st);return 0;}
  int d=D[q][b]; tp[p]=W[q][b]; p+=d; q=N[q][b]; st++;
  if(d!=d0){ tw[tl++]='A'+q; if(tl==2){ tw[2]=0; int code=tw[0]*256+tw[1];
      if(code==last2) cnt++; else { if(last2>=0) wl+=sprintf(word+wl,"%c%c%ld ",last2>>8,last2&255,cnt); last2=code; cnt=1; } tl=0; } }
  d0=d; if(p>hi)hi=p;
  if(p<lo){ lo=p; if(q==2){ if(last2>=0) wl+=sprintf(word+wl,"%c%c%ld ",last2>>8,last2&255,cnt); last2=-1;cnt=0;tl=0;
     // parse tape: 0 (01)^a [0 01] (11)^b [1]
     long i=lo+1; long a=0; while(tp[i]==0&&tp[i+1]==1){a++;i+=2;} int sep=0; if(tp[i]==0&&tp[i+1]==0&&tp[i+2]==1){sep=1;i+=3;}
     long bb=0; while(i+1<=hi&&tp[i]==1&&tp[i+1]==1){bb++;i+=2;} int e=0; if(i<=hi&&tp[i]==1){e=1;i++;} int rest=hi-i+1;
     nb++; printf("%d %lld %ld a=%ld sep=%d b=%ld e=%d rest=%d | %s\n",nb,st,hi-lo+1,a,sep,bb,e,rest,word); fflush(stdout); wl=0; word[0]=0; } }
 }
}
