/* coinc TM q W u S NB R K seed [dumpevery] : coin model in C.
   macro step: tape = W u^n S with n = NB + rand()%R, head at cell 0 in state q, run until a new left record or HALT.
   parse the result: longest periodic run (period 1..4, >= 6 reps) -> W' u' n' S'.  Continue from (q',W',u',S').
   After HALT restart from the start configuration.  Prints counts and halting words. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int Wt[8][2],D[8][2],N[8][2];
static unsigned char *t; static long SZ;
static char W0[100000],U0[16],S0[100000]; static int q0;
static char W[1<<20],U[16],S[1<<20]; static int q;
static unsigned long long rs=88172645463325252ULL; static unsigned long long rnd(){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return rs; }
int main(int c,char**v){ const char*M=v[1];
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} Wt[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 q0=v[2][0]-'A'; strcpy(W0,strcmp(v[3],"-")?v[3]:""); strcpy(U0,v[4]); strcpy(S0,strcmp(v[5],"-")?v[5]:"");
 long NB=atol(v[6]),R=atol(v[7]); long long K=atoll(v[8]); rs+=atoll(v[9])*7919; long dump=c>10?atol(v[10]):0; const char*EVS=c>11?v[11]:"ABCDEF"; long MODN=c>12?atol(v[12]):1, RESN=c>13?atol(v[13]):0;
 SZ=1L<<26; t=malloc(SZ); unsigned char*str=malloc(SZ);
 q=q0; strcpy(W,W0); strcpy(U,U0); strcpy(S,S0);
 long long halts=0, other=0, grow=0; double lg=0; long long totsteps=0;
 for(long long k=0;k<K;k++){
   long n=NB+(long)(rnd()%R)*MODN; n+= ((RESN-n)%MODN+MODN)%MODN; long lw=strlen(W),lu=strlen(U),ls=strlen(S);
   long L=lw+n*lu+ls; long base=SZ/2-L/2; memset(t+base-4*L-1000,0,9*L+2000);
   long p=base; for(long i=0;i<lw;i++) t[p++]=W[i]-'0'; for(long j=0;j<n;j++) for(long i=0;i<lu;i++) t[p++]=U[i]-'0'; for(long i=0;i<ls;i++) t[p++]=S[i]-'0';
   long lo=base, hi=base+L-1; p=base; int st=q; long long s=0, mx=60LL*n*n+1000000; int res=0;
   for(;s<mx;s++){ int b=t[p]; if(N[st][b]<0){res=1;break;} t[p]=Wt[st][b]; p+=D[st][b]; st=N[st][b]; if(p>hi)hi=p; if(p<lo){lo=p; if(strchr(EVS,'A'+st)){res=2;break;}} if(hi-base>4*L+500){res=3;break;} }
   totsteps+=s;
   if(res==1){ halts++; printf("HALT k=%lld state %c n=%ld W=%s U=%s S=%s\n",k,'A'+q,n,W,U,S); fflush(stdout); q=q0; strcpy(W,W0); strcpy(U,U0); strcpy(S,S0); continue; }
   if(res!=2){ other++; q=q0; strcpy(W,W0); strcpy(U,U0); strcpy(S,S0); continue; }
   long len=hi-p+1; for(long i=0;i<len;i++) str[i]=t[p+i];
   /* parse: longest run */
   long bp=0,bn=0,bs=0;
   for(int per=1;per<=4;per++){ long i=0; while(i+per<len){ if(str[i]==str[i+per]){ long j=i; while(j+per<len&&str[j]==str[j+per]) j++; long nn=(j+per-i)/per; if(nn>=6&&nn*per>bn*bp){bp=per;bn=nn;bs=i;} i=j+1;} else i++; } }
   if(!bn){ other++; q=q0; strcpy(W,W0); strcpy(U,U0); strcpy(S,S0); continue; }
   for(long i=0;i<bs;i++) W[i]='0'+str[i]; W[bs]=0;
   for(long i=0;i<bp;i++) U[i]='0'+str[bs+i]; U[bp]=0;
   long se=bs+bn*bp; for(long i=se;i<len;i++) S[i-se]='0'+str[i]; S[len-se]=0;
   q=st; if(bn>1.2*n) grow++; lg+= __builtin_log((double)bn/n);
   if(dump && k%dump==0){ printf("k=%lld %c n=%ld->%ld W=%s U=%s S=%s\n",k,'A'+q,n,bn,W,U,S); }
 }
 printf("END K=%lld halts=%lld other=%lld grow=%lld meanlog=%.4f avgsteps=%.0f\n",K,halts,other,grow,lg/K,(double)totsteps/K);
}
