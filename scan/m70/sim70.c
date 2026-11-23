/* sim70.c - fast macro simulator for BB(6) holdout no. 70
 *   1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE   (also no. 86 started in state B)
 *
 * Bell start: state A on a blank cell, tape  1 0^x 1^m 0^g1 1^b1 0^g2 1^b2 ...
 * State: the number x and the stack S = [m, g1, b1, g2, b2, ...].
 * Every Bell follows a rule  x' = 3x/2 + c,  new stack prefix = constants; c and the new prefix depend only on
 * x mod 12 (more bits if needed) and on a short prefix of S.  Rules are learned on the fly: the Bell is simulated
 * directly for 5 small x of the same residue class, with only the prefix on the tape (same method as macro70.py).
 *
 * Arithmetic: x grows by about 0.585 bits per Bell.  Bells are done in batches of L Bells using only the low
 * bits of x; the full x is updated once per batch: x_L = (3^L x + D) / 2^L.  No external library is needed.
 *
 * Observed and logged: blocks of odd length 9, 7, 5, 3, 1 appearing among the first three stack blocks
 * (the way to HALT is 9 -> 7 -> 5 -> 3 -> 1 -> HALT); every appearance of 7, 5, 3, 1 goes to events70.txt.
 *
 * Compile:  gcc -O2 -o sim70 sim70.c
 * Run:      ./sim70                 (continues from sim70.ck if it exists; Ctrl-C saves and stops)
 * Options:  -r SEC   report interval (default 60)      -s SEC   checkpoint interval (default 600)
 *           -n BELL  stop at this Bell and print check values      -L N  batch length (default 2048)
 *           -f       start fresh (ignore the checkpoint)
 * Check values of the Python run (watch70.py) at Bell 4663800:
 *   bits 2728153, x mod 2^64 = 0x58106550ccb57c0e, stack 2616485 entries, hash 884327361506333381
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>
#include <time.h>
typedef uint64_t u64; typedef unsigned __int128 u128; typedef uint32_t u32;

/* ------------------------------------------------------------------ TM and direct level simulation */
static const char *TM="1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE";
static int tw[6][2],td[6][2],tq[6][2];
#define TW (1<<22)
static unsigned char tape[TW];
static void tm_init(void){
  for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=TM+7*i+3*b;
    if(x[0]=='-'){tq[i][b]=-1;continue;} tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
}
enum {R_OK=0,R_HALT=1,R_OUT=2,R_MAX=3};
/* one Bell from a Bell start; tok = 1, x, m, g1, b1, ... ; lim = cell index (from the tape start) the head must
   not reach, or -1.  On R_OK: out[] = blocks of the new Bell start (starting with ones), off = position of its
   first cell relative to the old tape start, z0 = zeros between head and that cell. */
static int level_sim(const long *tok,int ntok,long lim,long *out,int *nout,int maxout,long *z0,long *off){
  long p=TW/4, base=p+1, x=base; int one=1;
  for(int i=0;i<ntok;i++){ for(long k=0;k<tok[i];k++) tape[x++]=one; one=!one; }
  long lo=p, hi=x, maxx=x; int q=0; long long MX=400000000LL; int res=R_MAX;
  for(long long st=1;st<=MX;st++){
    int b=tape[p]; if(tq[q][b]<0){res=R_HALT;break;}
    tape[p]=tw[q][b]; p+=td[q][b]; q=tq[q][b];
    if(p>hi){hi=p; if(hi>maxx)maxx=hi;}
    if(lim>=0 && p-base>=lim){res=R_OUT;break;}
    if(p<2||p>TW-3){res=R_MAX;break;}
    if(p<lo){ lo=p; if(q==0){
      long y=p+1; while(y<=hi&&!tape[y])y++;
      if(y<hi && tape[y] && !tape[y+1]){
        long y2=y+1; while(y2<=hi&&!tape[y2])y2++; long L2=0; while(y2+L2<=hi&&tape[y2+L2])L2++;
        if(!(y2-y-1==6 && L2==4)){
          *z0=y-p-1; *off=y-base; int k=0; long yy=y;
          while(yy<=hi){ long L=0; int bb=tape[yy]; while(yy<=hi&&tape[yy]==bb){L++;yy++;} if(yy>hi&&bb==0)break;
            if(k>=maxout){res=R_MAX;goto done;} out[k++]=L; }
          *nout=k; res=R_OK; break; }}}}
  }
done:
  memset(tape+lo,0,(size_t)(maxx-lo+2));
  return res;
}

/* ------------------------------------------------------------------ rule cache */
enum {T_OK=1,T_HALT=2,T_DEEPER=3,T_MOD=4};
typedef struct { u32 koff,klen; int type; long c; u32 qoff,nq; int lp,inf; } Rule;
static u32 *kpool; static size_t kn=0,kcap=0; static long *qpool; static size_t qn=0,qcap=0;
static Rule *rules; static size_t nrules=0,rcap=0; static int64_t *htab; static size_t hsize=0;
static u64 hkey(const u32*k,int n){ u64 h=1469598103934665603ULL; for(int i=0;i<n;i++){h^=k[i];h*=1099511628211ULL;h^=h>>29;} return h; }
static void hput(size_t idx){ Rule*r=&rules[idx]; u64 h=hkey(kpool+r->koff,r->klen)&(hsize-1); while(htab[h]>=0)h=(h+1)&(hsize-1); htab[h]=idx; }
static long hget(const u32*k,int n){
  if(!hsize) return -1; u64 h=hkey(k,n)&(hsize-1);
  while(htab[h]>=0){ Rule*r=&rules[htab[h]]; if(r->klen==(u32)n && !memcmp(kpool+r->koff,k,n*4)) return htab[h]; h=(h+1)&(hsize-1);} return -1; }
static size_t addrule(const u32*k,int n,Rule r){
  if(kn+n>kcap){kcap=kcap?kcap*2:1<<20; while(kn+n>kcap)kcap*=2; kpool=realloc(kpool,kcap*4);}
  memcpy(kpool+kn,k,n*4); r.koff=kn; r.klen=n; kn+=n;
  if(nrules==rcap){rcap=rcap?rcap*2:1<<14; rules=realloc(rules,rcap*sizeof(Rule));}
  rules[nrules]=r;
  if(2*(nrules+1)>hsize){ size_t ns=hsize?hsize*2:1<<15; free(htab); htab=malloc(ns*sizeof(int64_t)); hsize=ns;
    for(size_t i=0;i<hsize;i++)htab[i]=-1; for(size_t i=0;i<nrules;i++)hput(i);}
  hput(nrules); return nrules++;
}
static long nlearned=0;
/* learn the rule for residue r mod M and prefix P (np entries); inf = P is the whole stack */
static Rule learn(long r,long M,const u32*P,int np,int inf){
  Rule R; memset(&R,0,sizeof R); R.lp=np; R.inf=inf;
  long k=(60-r)/M+1; if(k<1)k=1;
  static long tok[4096], out[5][4096]; int nout[5]; long z0[5],off[5],xs[5]; int res[5];
  if(np+2>4096){fprintf(stderr,"prefix too long\n");exit(1);}
  long sumP=0; for(int i=0;i<np;i++) sumP+=P[i];
  for(int t=0;t<5;t++){
    xs[t]=r+M*(k+t); tok[0]=1; tok[1]=xs[t]; for(int i=0;i<np;i++)tok[2+i]=P[i];
    long lim=inf?-1:1+xs[t]+sumP;
    res[t]=level_sim(tok,np+2,lim,out[t],&nout[t],4096,&z0[t],&off[t]);
  }
  int nh=0,nok=0,nout_=0; for(int t=0;t<5;t++){ if(res[t]==R_HALT)nh++; if(res[t]==R_OK)nok++; if(res[t]==R_OUT)nout_++; }
  if(nh==5){R.type=T_HALT;return R;}
  if(nout_){R.type=T_DEEPER;return R;}
  if(nok<5){R.type=T_MOD;return R;}
  for(int t=0;t<5;t++) if(z0[t]!=0||out[t][0]!=1||nout[t]!=nout[0]||nout[t]<2){R.type=T_MOD;return R;}
  /* vec = out[1..] + (tail gap) ; vec[0] = x' */
  int nv=nout[0]-1+(inf?0:1);
  static long vec[5][4097];
  for(int t=0;t<5;t++){ long s=0; for(int i=0;i<nout[t];i++)s+=out[t][i];
    for(int i=1;i<nout[t];i++)vec[t][i-1]=out[t][i];
    if(!inf) vec[t][nv-1]=(1+xs[t]+sumP)-(off[t]+s); }
  long c=vec[0][0]-3*xs[0]/2;
  for(int t=0;t<5;t++){ if(xs[t]%2 || vec[t][0]-3*xs[t]/2!=c){R.type=T_MOD;return R;}
    for(int i=1;i<nv;i++) if(vec[t][i]!=vec[0][i]||vec[t][i]<0){R.type=T_MOD;return R;} }
  if(((c%3)+3)%3!=0){fprintf(stderr,"rule with c not divisible by 3 (c=%ld): x mod 3 would change, not supported\n",c);exit(1);}
  if(nv-1+qn>qcap){qcap=qcap?qcap*2:1<<20; while(nv-1+qn>qcap)qcap*=2; qpool=realloc(qpool,qcap*sizeof(long));}
  R.qoff=qn; R.nq=nv-1; for(int i=1;i<nv;i++)qpool[qn++]=vec[0][i];
  R.type=T_OK; R.c=c; nlearned++; return R;
}

/* ------------------------------------------------------------------ stack (reversed: front at the end) */
static u32 *S; static size_t top=0,scap=0;
static void spush(u32 v){ if(top==scap){scap=scap?scap*2:1<<20; S=realloc(S,scap*4);} S[top++]=v; }

/* x mod M for M = 12*2^j, from the exact low bits (x is always divisible by 3) */
static long xmod(u64 low,long M){ long m2=M/3; long r=(long)(low&(u64)(m2-1)); while(r%3)r+=m2; return r; }

/* find the rule for the current state */
static Rule *findrule(u64 low){
  static u32 key[8192]; static u32 P[8192];
  for(int d=0;;d++){
    int np,inf;
    if((size_t)(2*d+1)<top){ np=2*d+2; inf=0; } else { np=(int)top; inf=1; }
    if(np>8000){fprintf(stderr,"prefix too long\n");exit(1);}
    for(int i=0;i<np;i++) P[i]=S[top-1-i];
    long M=12; Rule *rr=NULL;
    while(M<=768){
      long r=xmod(low,M);
      key[0]=(u32)M; key[1]=(u32)r; key[2]=(u32)inf; key[3]=(u32)np; memcpy(key+4,P,np*4);
      long id=hget(key,np+4);
      if(id<0){ Rule R=learn(r,M,P,np,inf); id=addrule(key,np+4,R); }
      rr=&rules[id];
      if(rr->type==T_MOD){M*=2;continue;}
      break;
    }
    if(rr->type==T_MOD){fprintf(stderr,"no rule found (modulus)\n");exit(1);}
    if(rr->type==T_DEEPER){ if(inf){fprintf(stderr,"no rule found (depth)\n");exit(1);} continue; }
    return rr;
  }
}
static void apply(Rule*r){
  static u32 outv[1<<16]; int no=0;
  if(r->inf) top=0; else top-=r->lp;
  long *q=qpool+r->qoff; int nq=r->nq;
  outv[no++]=(u32)q[0]; int i=1;
  while(i+1<nq){ long g=q[i],b=q[i+1]; if(g==0) outv[no-1]+=(u32)b; else {outv[no++]=(u32)g; outv[no++]=(u32)b;} i+=2; }
  if(i<nq){ long g=q[i]; if(g==0&&top>0){ outv[no-1]+=S[--top]; } else outv[no++]=(u32)g; }
  for(int j=no-1;j>=0;j--) spush(outv[j]);
}

/* ------------------------------------------------------------------ big numbers (little-endian u64 limbs) */
static u64 *X; static size_t xn=0,xcap=0;
static void xreserve(size_t n){ if(n>xcap){ xcap=n*2+16; X=realloc(X,xcap*8);} }
static void trim(u64*a,size_t*n){ while(*n>0&&a[*n-1]==0)(*n)--; }
static size_t bits(const u64*a,size_t n){ if(!n)return 0; return 64*(n-1)+(64-__builtin_clzll(a[n-1])); }

/* ------------------------------------------------------------------ statistics, checkpoint */
static u64 level=0; static long long created[5],firstl[5],lastl[5]; static long minodd=1000000000;
static const int ODD[5]={1,3,5,7,9};
static FILE *evf;
static void oddfront(int cnt[5]){ for(int k=0;k<5;k++)cnt[k]=0;
  for(int j=1;j<=3;j++){ size_t idx=2*j; if(idx>=top)break; u32 b=S[top-1-idx];
    if((b&1)&&b<=9){ cnt[b/2]++; } } }
static volatile sig_atomic_t stopflag=0; static void onsig(int s){(void)s;stopflag=1;}
static const char *CK="sim70.ck";
static void save(void){
  char tmp[64]; snprintf(tmp,64,"%s.tmp",CK); FILE*f=fopen(tmp,"wb"); if(!f){perror("checkpoint");return;}
  fwrite("SIM70CK1",1,8,f); fwrite(&level,8,1,f); fwrite(created,8,5,f); fwrite(firstl,8,5,f); fwrite(lastl,8,5,f);
  fwrite(&minodd,sizeof minodd,1,f); u64 n=xn; fwrite(&n,8,1,f); fwrite(X,8,xn,f); u64 t=top; fwrite(&t,8,1,f); fwrite(S,4,top,f);
  fclose(f); rename(tmp,CK);
}
static int load(void){
  FILE*f=fopen(CK,"rb"); if(!f)return 0; char m[8]; if(fread(m,1,8,f)!=8||memcmp(m,"SIM70CK1",8)){fclose(f);return 0;}
  u64 n,t; if(fread(&level,8,1,f)!=1)goto bad; if(fread(created,8,5,f)!=5)goto bad; if(fread(firstl,8,5,f)!=5)goto bad; if(fread(lastl,8,5,f)!=5)goto bad;
  if(fread(&minodd,sizeof minodd,1,f)!=1)goto bad; if(fread(&n,8,1,f)!=1)goto bad; xreserve(n); xn=n; if(fread(X,8,n,f)!=n)goto bad;
  if(fread(&t,8,1,f)!=1)goto bad; scap=t*2+16; S=realloc(S,scap*4); top=t; if(fread(S,4,t,f)!=t)goto bad;
  fclose(f); return 1;
bad: fprintf(stderr,"checkpoint damaged\n"); exit(1);
}
static double now(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+ts.tv_nsec*1e-9; }
static void report(double rate){
  printf("Bell %llu (about 10^%.4g steps) | x %zu bits | stack %zu | rules %zu (%ld learned) | %.0f Bells/s\n",
    (unsigned long long)level,0.352*level,bits(X,xn),top,nrules,nlearned,rate);
  printf("   odd blocks near the front:"); for(int k=4;k>=0;k--) printf("  %d: %lld",ODD[k],created[k]);
  printf("  | smallest seen: %s",minodd<1000000000?"":"-"); if(minodd<1000000000)printf("%ld",minodd);
  for(int k=3;k>=0;k--) if(created[k]) printf("  | %d first at %lld, last at %lld",ODD[k],firstl[k],lastl[k]);
  printf("\n"); fflush(stdout);
}

/* ------------------------------------------------------------------ main loop */
int main(int argc,char**argv){
  double rep=60,sav=600; u64 stopat=0; int L=2048,fresh=0;
  for(int i=1;i<argc;i++){
    if(!strcmp(argv[i],"-r")&&i+1<argc)rep=atof(argv[++i]); else if(!strcmp(argv[i],"-s")&&i+1<argc)sav=atof(argv[++i]);
    else if(!strcmp(argv[i],"-n")&&i+1<argc)stopat=strtoull(argv[++i],0,10); else if(!strcmp(argv[i],"-L")&&i+1<argc)L=atoi(argv[++i]);
    else if(!strcmp(argv[i],"-f"))fresh=1; else {fprintf(stderr,"usage: %s [-r sec] [-s sec] [-n bell] [-L batch] [-f]\n",argv[0]);return 1;} }
  if(L<64)L=64; L=(L/64)*64;
  tm_init(); signal(SIGINT,onsig); signal(SIGTERM,onsig);
  if(fresh||!load()){ level=0; xreserve(4); X[0]=30; xn=1; top=0; spush(4); spush(18); spush(11);
    for(int k=0;k<5;k++){created[k]=0;firstl[k]=lastl[k]=-1;} minodd=1000000000; }
  else printf("continuing from %s at Bell %llu\n",CK,(unsigned long long)level);
  evf=fopen("events70.txt","a");
  /* batch buffers */
  int NB=L/64+4;                                   /* low part: B = 64*NB bits, exact bits left after a batch >= 256 */
  int ND=(int)((1.585*L+256)/64)+2;                /* D in two's complement */
  u64 *xl=calloc(NB+1,8), *D=calloc(ND+1,8), *tmp=calloc(NB+2,8);
  /* 3^L */
  size_t pn=1; u64 *P3=calloc(ND+1,8); P3[0]=1;
  for(int i=0;i<L;i++){ u64 cy=0; for(size_t j=0;j<pn;j++){ u128 t=(u128)P3[j]*3+cy; P3[j]=(u64)t; cy=(u64)(t>>64);} if(cy)P3[pn++]=cy; }
  u64 *P3p=calloc(ND+1,8);
  double t0=now(), tl=t0, ts=t0; u64 l0=level; int halted=0;
  while(!stopflag && !halted){
    /* low bits of x */
    for(int i=0;i<NB;i++) xl[i]= (size_t)i<xn?X[i]:0;
    memset(D,0,(ND+1)*8);
    int Li=0;
    for(;Li<L;Li++){
      if(stopat && level>=stopat) break;
      int before[5],after[5]; oddfront(before);
      Rule *r=findrule(xl[0]);
      if(r->type==T_HALT){ halted=1; break; }
      apply(r); level++;
      oddfront(after);
      for(int k=0;k<5;k++){ int d=after[k]-before[k]; if(d>0){ created[k]+=d; if(firstl[k]<0)firstl[k]=level; lastl[k]=level;
          if(ODD[k]<minodd)minodd=ODD[k];
          if(ODD[k]<=7&&evf){ fprintf(evf,"Bell %llu: block %d appeared near the front\n",(unsigned long long)level,ODD[k]); fflush(evf);} } }
      long d2=2*r->c;                               /* x' = (3x + d2)/2 */
      /* xl = (3*xl + d2) >> 1  (mod 2^(64 NB)) */
      { u64 cy=0; u64 add=(u64)d2, ext=d2<0?~0ULL:0;
        for(int i=0;i<NB;i++){ u128 t=(u128)xl[i]*3+cy+(i==0?add:ext); /* sign extension of d2 */
          tmp[i]=(u64)t; cy=(u64)(t>>64); }
        for(int i=0;i<NB;i++) xl[i]=(tmp[i]>>1)|(i+1<NB?tmp[i+1]<<63:0); }
      /* D = 3*D + d2 * 2^Li */
      { u64 cy=0; for(int i=0;i<ND;i++){ u128 t=(u128)D[i]*3+cy; D[i]=(u64)t; cy=(u64)(t>>64); }
        int w=Li/64, sh=Li%64; u64 lo=((u64)d2)<<sh; u64 hi=sh?(u64)(d2>>(64-sh)):(d2<0?~0ULL:0);
        u64 ext=d2<0?~0ULL:0; u128 t; u64 c2=0;
        for(int i=w;i<ND;i++){ u64 a=(i==w)?lo:(i==w+1)?hi:ext; t=(u128)D[i]+a+c2; D[i]=(u64)t; c2=(u64)(t>>64); } }
    }
    if(Li>0){
      /* x = (3^Li x + D) >> Li */
      u64 *Pm=P3; size_t pm=pn;
      if(Li<L){ memset(P3p,0,(ND+1)*8); P3p[0]=1; pm=1; for(int i=0;i<Li;i++){ u64 cy=0; for(size_t j=0;j<pm;j++){u128 t=(u128)P3p[j]*3+cy;P3p[j]=(u64)t;cy=(u64)(t>>64);} if(cy)P3p[pm++]=cy; } Pm=P3p; }
      size_t yn=xn+pm+2; if((size_t)ND+2>yn) yn=ND+2;
      u64 *Y=calloc(yn,8);
      for(size_t j=0;j<pm;j++){ u64 cy=0; u64 b=Pm[j]; for(size_t i=0;i<xn;i++){ u128 t=(u128)X[i]*b+Y[i+j]+cy; Y[i+j]=(u64)t; cy=(u64)(t>>64);} size_t k=xn+j; while(cy){ u128 t=(u128)Y[k]+cy; Y[k]=(u64)t; cy=(u64)(t>>64); k++; } }
      { u64 ext=(D[ND-1]>>63)?~0ULL:0; u64 cy=0; for(size_t i=0;i<yn;i++){ u64 a=(i<(size_t)ND)?D[i]:ext; u128 t=(u128)Y[i]+a+cy; Y[i]=(u64)t; cy=(u64)(t>>64);} }
      /* shift right by Li */
      int w=Li/64, sh=Li%64; size_t nn=yn-w; xreserve(nn+1);
      for(size_t i=0;i<nn;i++){ u64 a=Y[i+w], b=(i+w+1<yn)?Y[i+w+1]:0; X[i]=sh?((a>>sh)|(b<<(64-sh))):a; }
      xn=nn; trim(X,&xn); free(Y);
      if(X[0]!=xl[0]){ fprintf(stderr,"internal error: low bits disagree at Bell %llu\n",(unsigned long long)level); return 2; }
    }
    double t=now();
    if(t-tl>=rep){ report((level-l0)/(t-t0)); tl=t; }
    if(t-ts>=sav){ save(); ts=t; }
    if(stopat && level>=stopat) break;
  }
  double t=now(); report((level-l0)/(t-t0+1e-9));
  if(halted){ printf("*** HALT at Bell %llu (the Bell after this one halts) ***\n",(unsigned long long)level); if(evf)fprintf(evf,"HALT at Bell %llu\n",(unsigned long long)level); }
  if(stopat && level>=stopat){
    u64 h=0; for(size_t i=0;i<top;i++){ h=(u64)(((u128)h*1000003+S[i])%(((u128)1)<<61)); }
    printf("check values at Bell %llu: bits %zu, x mod 2^64 = 0x%016llx, stack %zu entries, hash %llu\n",
      (unsigned long long)level,bits(X,xn),(unsigned long long)X[0],top,(unsigned long long)h);
  }
  save(); printf("checkpoint written (%s)\n",CK);
  return 0;
}
