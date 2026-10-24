// accsim.c - accelerated simulator for Turing machines (bbchallenge notation, any number of states/symbols).
// Macro machine with blocks of K cells and run-length encoded tape; "chain steps": when the head in state q
// moves through a run s^c and every block of it is passed in the same way (same state, same direction), the
// whole run is rewritten in one operation.  A sweep across a long uniform block therefore costs one operation.
// usage: accsim TM K maxops [report_every_ops]
// Output: periodic lines with operations, log10(steps), tape as run-length list (long runs only), and HALT.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <limits.h>
typedef long long ll;
static int ns,nsym,K; static int W[16][16],D[16][16],N[16][16];
typedef struct { int s; ll c; } run;
typedef struct { run*a; ll n,cap; } stack;
static void push(stack*S,int s,ll c){ if(c<=0) return; if(S->n&&S->a[S->n-1].s==s){ S->a[S->n-1].c+=c; return; }
  if(S->n==S->cap){ S->cap=S->cap?2*S->cap:1024; S->a=realloc(S->a,S->cap*sizeof(run)); } S->a[S->n].s=s; S->a[S->n].c=c; S->n++; }
// macro transition cache: key (q, dir, block) -> (q', dir', block', steps) ; dir 0 = moving right (enter at left edge), 1 = moving left
typedef struct { int done,q2,d2,s2; ll steps; int halt,loop; } tr;
static tr*TC; static int NB;
static int pw[8];
static tr* trans(int q,int d,int s){
  tr*t=&TC[(q*2+d)*NB+s]; if(t->done) return t; t->done=1;
  int cell[8]; for(int i=0;i<K;i++) cell[i]=(s/pw[i])%nsym;
  int h= d==0?0:K-1; ll st=0;
  for(;;){
    if(h<0||h>=K) break;
    int b=cell[h]; if(N[q][b]<0){ t->halt=1; t->q2=q; t->s2=s; t->steps=st; return t; }
    cell[h]=W[q][b]; h+=D[q][b]; q=N[q][b]; st++;
    if(st>100000){ t->loop=1; return t; } }
  int s2=0; for(int i=0;i<K;i++) s2+=cell[i]*pw[i];
  t->q2=q; t->d2= h>=K?0:1; t->s2=s2; t->steps=st; return t; }

/* ---------- repetition acceleration ----------
   At every turn of the head a snapshot is stored: state, direction, all runs.  If the last three snapshots with
   distance p (p = 1..PMAX turns) have the same structure (same symbols, same number of runs) and the run counts
   change by the same amounts twice, with the same number of operations in between, the repetition is applied
   r times at once: counts += r*delta, steps += r*s1 + ds*r(r+1)/2 (steps per repetition grow linearly), where
   r keeps every decreasing run above a safety margin.  If no run decreases, the pattern grows forever. */
#define HMAX 64
#define PMAX 24
typedef struct { int q,d; ll nl,nr; run*l,*r; ll ops; long double steps; } snap;
static snap H[HMAX]; static ll hn=0;
static ll njump=0; static long double nrep=0;
static int bouncer=0;
static void snap_store(stack*L,stack*R,int q,int d,ll ops,long double steps){
  snap*S=&H[hn%HMAX]; free(S->l); free(S->r);
  S->q=q; S->d=d; S->nl=L->n; S->nr=R->n; S->l=malloc((L->n+1)*sizeof(run)); S->r=malloc((R->n+1)*sizeof(run));
  memcpy(S->l,L->a,L->n*sizeof(run)); memcpy(S->r,R->a,R->n*sizeof(run)); S->ops=ops; S->steps=steps; hn++; }
static int same_shape(snap*a,snap*b){ if(a->q!=b->q||a->d!=b->d||a->nl!=b->nl||a->nr!=b->nr) return 0;
  for(ll i=0;i<a->nl;i++) if(a->l[i].s!=b->l[i].s) return 0;
  for(ll i=0;i<a->nr;i++) if(a->r[i].s!=b->r[i].s) return 0; return 1; }
// try to jump; returns 1 if applied
static int try_jump(stack*L,stack*R,ll*ops,long double*steps,ll maxops){
  if(hn<3) return 0;
  snap*c=&H[(hn-1)%HMAX];
  for(int p=1;p<=PMAX&&2*p<hn&&2*p<HMAX;p++){
    snap*b=&H[(hn-1-p)%HMAX],*a=&H[(hn-1-2*p)%HMAX];
    if(!same_shape(c,b)||!same_shape(b,a)) continue;
    ll dops=c->ops-b->ops; if(dops!=b->ops-a->ops||dops<=0) continue;
    int ok=1, anydec=0, anychg=0; ll r=LLONG_MAX/4; ll margin=dops+2;
    for(int side=0;side<2&&ok;side++){ ll n= side?c->nr:c->nl; run*C=side?c->r:c->l,*Bq=side?b->r:b->l,*A=side?a->r:a->l;
      for(ll i=0;i<n;i++){ ll d1=C[i].c-Bq[i].c, d2=Bq[i].c-A[i].c; if(d1!=d2){ ok=0; break; }
        if(d1){ anychg=1; if(C[i].c<margin){ ok=0; break; } }
        if(d1<0){ anydec=1; ll rr=(C[i].c-margin)/(-d1); if(rr<r) r=rr; } } }
    if(!ok||!anychg) continue;
    if(!anydec){ bouncer=1; return 0; }
    if(r<1) continue;
    if(r>(maxops-*ops)/dops) r=(maxops-*ops)/dops; if(r<1) return 0;
    long double s1=c->steps-b->steps, s0=b->steps-a->steps, ds=s1-s0;
    for(int side=0;side<2;side++){ stack*S=side?R:L; run*C=side?c->r:c->l,*Bq=side?b->r:b->l;
      for(ll i=0;i<S->n;i++) S->a[i].c+= r*(C[i].c-Bq[i].c); }
    *steps+= (long double)r*s1 + ds*(long double)r*(long double)(r+1)/2;
    if(getenv("ACC_DEBUG")){ printf("JUMP r=%lld p=%d dops=%lld state %c%s |",r,p,dops,'A'+c->q,c->d?"<":">");
      for(ll i=0;i<c->nl;i++){ for(int j=0;j<K;j++) printf("%d",(c->l[i].s/pw[j])%nsym); printf("^%lld(%+lld) ",c->l[i].c-r*0,c->l[i].c-b->l[i].c); }
      printf("[h] "); for(ll i=c->nr-1;i>=0;i--){ for(int j=0;j<K;j++) printf("%d",(c->r[i].s/pw[j])%nsym); printf("^%lld(%+lld) ",c->r[i].c,c->r[i].c-b->r[i].c); } printf("\n"); }
    *ops+= r*dops; njump++; nrep+=r; hn=0; return 1; }
  return 0; }

static void show(stack*L,stack*R,int q,int d,ll ops,double lsteps,ll minc){
  printf("ops %lld  log10(steps) %.4f  state %c%s  |",ops,lsteps,'A'+q,d?"<":">");
  // left stack from far end to head, then right stack from head to far end; runs with count >= minc shown with count
  for(ll i=0;i<L->n;i++){ run*r=&L->a[i]; for(int j=0;j<K;j++) printf("%d",(r->s/pw[j])%nsym); if(r->c>1) printf("^%lld",r->c); printf(" "); }
  printf("[head] ");
  for(ll i=R->n-1;i>=0;i--){ run*r=&R->a[i]; for(int j=0;j<K;j++) printf("%d",(r->s/pw[j])%nsym); if(r->c>1) printf("^%lld",r->c); printf(" "); }
  printf("\n"); fflush(stdout); }
int main(int argc,char**argv){
  const char*M=argv[1]; K=atoi(argv[2]); ll maxops=atoll(argv[3]); ll every=argc>4?atoll(argv[4]):0; int accel=argc>5?atoi(argv[5]):1;
  ns=1; for(const char*p=M;*p;p++) if(*p=='_') ns++; nsym=(int)(strchr(M,'_')-M)/3;
  for(int i=0;i<ns;i++)for(int b=0;b<nsym;b++){const char*x=M+(3*nsym+1)*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
  pw[0]=1; for(int i=1;i<=K;i++) pw[i]=pw[i-1]*nsym; NB=pw[K];
  TC=calloc((size_t)ns*2*NB,sizeof(tr));
  stack L={0},R={0}; int q=0,d=0; ll ops=0;
  ll maxspan=argc>9?atoll(argv[9]):LLONG_MAX;
  if(argc>8&&strcmp(argv[7],"-")){
    const char*cs=argv[7]; ll n=strlen(cs); q=argv[8][0]-'A'; d=0;
    // blocks to the left of the head cell, aligned so that the head cell starts a block
    ll h=n-1; ll nb=(h+K-1)/K;
    for(ll b=nb-1;b>=0;b--){ int s=0; for(int i=0;i<K;i++){ ll pos=h-(b+1)*K+i; int v= pos>=0? cs[pos]-'0':0; s+=v*pw[i]; } push(&L,s,1); }
    int s=cs[h]-'0'; push(&R,s,1); } long double steps=0; // steps as double (log scale reporting)
  // L: blocks left of the head (top = nearest), R: blocks right of the head (top = nearest).  The head stands
  // between them; d=0: it will enter the top of R from its left edge; d=1: the top of L from its right edge.
  // Block digits: cell i of a block is digit i (i=0 leftmost).
  ll nextrep=every;
  ll realops=0, maxreal=argc>6?atoll(argv[6]):LLONG_MAX;
  while(ops<maxops&&realops<maxreal){ realops++;
    stack*F= d==0?&R:&L, *B= d==0?&L:&R;
    int s=0; ll c=1;
    if(F->n){ s=F->a[F->n-1].s; c=F->a[F->n-1].c; } else { s=0; c=1; }   // beyond the visited tape: blank blocks (one at a time)
    tr*t=trans(q,d,s);
    if(t->loop){ printf("LOOP inside a block (state %c), ops %lld\n",'A'+q,ops); return 0; }
    if(t->halt){
      // partial block: the head halts inside the block
      steps+=t->steps; printf("HALT  ops %lld  steps %.0Lf (log10 %.4f)\n",ops,steps,(double)log10l(steps>0?steps:1)); show(&L,&R,q,d,ops,(double)log10l(steps>0?steps:1),2); return 0; }
    if(t->q2==q && t->d2==d){ // chain step over the whole run
      if(F->n){ F->n--; } push(B,t->s2,c); steps+=(long double)t->steps*(long double)c; }
    else {
      if(F->n){ if(--F->a[F->n-1].c==0) F->n--; }
      if(t->d2==d) push(B,t->s2,1); else push(F,t->s2,1);
      steps+=t->steps; int turned=(t->d2!=d); q=t->q2; d=t->d2;
      if(turned&&accel){ snap_store(&L,&R,q,d,ops+1,steps); if(try_jump(&L,&R,&ops,&steps,maxops)){ } } }
    ops++;
    if(maxspan<LLONG_MAX&&(realops&1023)==0){ ll cells=0; for(ll i=0;i<L.n;i++) cells+=L.a[i].c; for(ll i=0;i<R.n;i++) cells+=R.a[i].c; if(cells*K>maxspan){ printf("SPAN %lld cells reached, log10(steps) %.4f, real ops %lld, jumps %lld\n",cells*K,(double)log10l(steps>0?steps:1),realops,njump); return 0; } }
    if(every&&ops>=nextrep){ show(&L,&R,q,d,ops,(double)log10l(steps>0?steps:1),2); nextrep+=every; } }
  printf("no halt within %lld operations (%lld real), steps %.6Le, log10(steps) %.4f, %lld jumps over %.4Lg repetitions\n",ops,realops,steps,(double)log10l(steps>0?steps:1),njump,nrep);
  show(&L,&R,q,d,ops,(double)log10l(steps>0?steps:1),2); return 0; }
