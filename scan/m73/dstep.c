// dstep.c -- direct simulation between left-edge configurations of M = mirrored 1RB1LF_1LC1RD_1RA1LA_0RA0RE_0RC---_1RF0LC
//
// D-configuration: state D, head on the blank cell directly left of the leftmost 1.
// A tape is given as the list of its runs of ones (a run of length 0 stands for "00").
// "in F" below means: all runs = 0 or 2 (mod 3), first run > 0, last run = 0 (mod 3) and > 0.
//
// usage (after: gcc -O2 -o dstep dstep.c):
//   dstep step  [MAXSTEPS] < lines "r1 r2 ..."   one line per tape; prints the next D-configuration ("D r1 r2 ...")
//                                                 or HALT / MAX / EDGE
//   dstep start S MAXSTEPS                       run M from the blank tape in start state S (A, B or C) and report
//                                                 all D-configurations: first one in F, number in F / not in F after it
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char*M="1LB1RF_1RC1LD_1LA1RA_0LA0LE_0LC---_1LF0RC";
static int Wr[8][2],Dr[8][2],Nx[8][2];
#define SZ (1L<<26)
static unsigned char t[SZ];
static void init(void){ for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){Nx[i][b]=-1;continue;} Wr[i][b]=x[0]-'0';Dr[i][b]=x[1]=='R'?1:-1;Nx[i][b]=x[2]-'A';} }
// membership of the tape cells [first..last] in F
static int infam(long first,long last){ long run=0; int nruns=0;
  for(long i=first;i<=last+1;i++){ if(i<=last&&t[i]) run++; else { if(run%3==1) return 0; if(nruns==0&&run==0) return 0; if(i>last&&(run%3!=0||run==0)) return 0; nruns++; run=0; } }
  return 1; }
int main(int c,char**v){ init();
 if(c>1&&!strcmp(v[1],"start")){ int q=v[2][0]-'A'; long long maxs=atoll(v[3]);
   long p=SZ/2,lo=p,hi=p,first=p+1; long long in=0,out=0,firstin=-1,lastout=-1; int started=0;
   for(long long s=0;s<maxs;s++){ int b=t[p]; if(Nx[q][b]<0){printf("HALT at step %lld\n",s+1);return 0;} t[p]=Wr[q][b]; if(Wr[q][b]&&p<first)first=p;
     p+=Dr[q][b]; q=Nx[q][b]; if(p<lo)lo=p; if(p>hi)hi=p; if(p<=1||p>=SZ-2){printf("EDGE at step %lld\n",s+1);break;}
     if(q==3&&p<first){ while(first<=hi&&!t[first])first++;
       if(p==first-1){ long h=hi; while(h>p&&!t[h])h--; int f=infam(first,h);
         if(f){ in++; if(!started){started=1; firstin=s+1; printf("first D-configuration in F after %lld steps: ",s+1); long run=0; for(long i=first;i<=h+1;i++){ if(t[i])run++; else {printf("%ld ",run);run=0;} } printf("\n"); } }
         else if(started){ out++; lastout=s+1; } } } }
   printf("start state %s, %lld steps: D-configurations in F: %lld, not in F (after the first one in F): %lld\n",v[2],maxs,in,out); return 0; }
 long long maxs=c>2?atoll(v[2]):4000000000LL; static char line[1<<22];
 while(fgets(line,sizeof line,stdin)){ char*s=line; long base=SZ/4,p=base,x=base+1,lo=p,hi;
   for(;;){ char*e; long r=strtol(s,&e,10); if(e==s)break; s=e; for(long i=0;i<r;i++) t[x++]=1; x++; }
   hi=x; long first=base+1; int q=3,done=0;
   for(long long st=0;st<maxs;st++){ int b=t[p]; if(Nx[q][b]<0){printf("HALT\n");done=1;break;} t[p]=Wr[q][b]; if(Wr[q][b]&&p<first)first=p;
     p+=Dr[q][b]; q=Nx[q][b]; if(p<lo)lo=p; if(p>hi)hi=p; if(p<=1||p>=SZ-2){printf("EDGE\n");done=1;break;}
     if(q==3&&p<first){ while(first<=hi&&!t[first])first++;
       if(p==first-1){ long h=hi; while(h>p&&!t[h])h--; printf("D"); long run=0; for(long i=first;i<=h+1;i++){ if(t[i])run++; else {printf(" %ld",run);run=0;} } printf("\n"); done=1; break; } } }
   if(!done) printf("MAX\n");
   memset(t+lo-1,0,hi-lo+3); }
 return 0; }
