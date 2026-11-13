// ev42: reads lines "X a b" (tape (10)^a 1^b), "Z c e" (00 (10)^c 1^e) or "M c e" ((10)^3 11 0 (10)^c 1^e),
// head on the blank cell left of the tape, state A; runs no. 42 to the next new leftmost cell in state A.
// prints "X x y", "Z x y", "HALT steps", "OTHER ..." or "MAX", plus the steps.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char*TM="1RB0RF_1LC0RA_1LD1LB_0LE---_1LA0LA_1RE1LD";
int W[8][2],D[8][2],N[8][2];
int main(int argc,char**argv){ long long maxs=argc>1?atoll(argv[1]):100000000000LL;
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=TM+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 long SZ=1L<<27; unsigned char*t=malloc(SZ); char ty[4]; long x,y;
 while(scanf("%3s %ld %ld",ty,&x,&y)==3){
  memset(t,0,SZ); long base=SZ/2, p=base, i=base+1;
  if(ty[0]=='Z'){i+=2;}
  if(ty[0]=='M'){ for(int k=0;k<3;k++){t[i]=1;i+=2;} t[i++]=1;t[i++]=1; i++; }
  for(long k=0;k<x;k++){t[i]=1;i+=2;} for(long k=0;k<y;k++)t[i++]=1;
  long hi=i-1, lo=p; int q=0; long long s; int done=0;
  for(s=0;s<maxs;s++){ int b=t[p]; if(N[q][b]<0){printf("HALT %lld\n",s);done=1;break;}
    t[p]=W[q][b]; p+=D[q][b]; q=N[q][b]; if(p>hi)hi=p;
    if(p<lo){ lo=p; if(q==0){ // parse lo+1..hi
        long j=lo+1; char k='X'; if(t[j]==0&&t[j+1]==0){k='Z';j+=2;}
        long a=0; while(j+1<=hi && t[j]==1 && t[j+1]==0 && !(j+2>hi)){ // (10) pairs, but a pair 10 followed by end is ambiguous; treat as pair
            a++; j+=2; }
        long b2=0; while(j<=hi && t[j]==1){b2++;j++;}
        while(hi>j && t[hi]==0) hi--;
        if(j>hi) printf("%c %ld %ld %lld\n",k,a,b2,s+1); else { printf("OTHER %lld ",s+1); for(long u=lo+1;u<=hi&&u<lo+200;u++)putchar('0'+t[u]); printf("\n"); }
        done=1; break; } }
  }
  if(!done) printf("MAX\n");
  fflush(stdout);
 }
}
