// do the runs of one TM table from state A and from state Q (blank tape) meet in the same configuration (up to translation)?
// usage: meet TM Q N1 N2   -> takes the configuration of run 1 after N1 steps and looks for it in run 2 within N2 steps, and vice versa
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],N[8][2];
#define SZ 60000000
typedef struct { unsigned char*t; long p,lo,hi; int q; long ones; long long st; int halted; } run;
static void init(run*r,int q){ r->t=calloc(SZ,1); r->p=SZ/2; r->lo=r->hi=r->p; r->q=q; r->ones=0; r->st=0; r->halted=0; }
static int step(run*r){ int b=r->t[r->p]; if(N[r->q][b]<0){ r->halted=1; return 0; } int w=W[r->q][b]; r->ones+=w-b; r->t[r->p]=w; r->p+=D[r->q][b]; r->q=N[r->q][b]; r->st++;
  if(r->p<r->lo) r->lo=r->p; if(r->p>r->hi) r->hi=r->p; if(r->p<2||r->p>SZ-3){ fprintf(stderr,"tape full\n"); exit(1);} return 1; }
static long leftone(run*r){ long i=r->lo; while(i<=r->hi&&!r->t[i]) i++; return i; }
static long rightone(run*r){ long i=r->hi; while(i>=r->lo&&!r->t[i]) i--; return i; }
typedef struct { unsigned char*w; long len,hoff; int q; long ones; } cfg;
static cfg snap(run*r){ cfg c; long a=leftone(r),b=rightone(r); if(a>b){a=b=r->p;} c.len=b-a+1; c.w=malloc(c.len); memcpy(c.w,r->t+a,c.len); c.hoff=r->p-a; c.q=r->q; c.ones=r->ones; return c; }
static long long search(run*r,cfg*c,long long N2){
  // cheap filters first; the left end is tracked lazily
  while(r->st<N2){ if(!step(r)) return -1;
    if(r->q==c->q && r->ones==c->ones){ long a=leftone(r); if(r->p-a==c->hoff){ long b=rightone(r); if(b-a+1==c->len && !memcmp(r->t+a,c->w,c->len)) return r->st; } } }
  return -2; }
int main(int argc,char**argv){ const char*M=argv[1]; int Q=argv[2][0]-'A'; long long N1=atoll(argv[3]), N2=atoll(argv[4]);
  for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
  for(int dir=0;dir<2;dir++){ run a,b; init(&a,dir?Q:0); init(&b,dir?0:Q);
    while(a.st<N1) if(!step(&a)) break;
    if(a.halted){ printf("run from %c halts at %lld\n",'A'+(dir?Q:0),a.st); free(a.t); free(b.t); continue; }
    cfg c=snap(&a); long long s=search(&b,&c,N2);
    printf("config of run from %c at step %lld (width %ld): ",'A'+(dir?Q:0),N1,c.len);
    if(s>=0) printf("reached by run from %c at step %lld\n",'A'+(dir?0:Q),s); else printf(s==-1?"other run halted\n":"not found within %lld steps\n",N2);
    free(a.t); free(b.t); free(c.w); }
}
