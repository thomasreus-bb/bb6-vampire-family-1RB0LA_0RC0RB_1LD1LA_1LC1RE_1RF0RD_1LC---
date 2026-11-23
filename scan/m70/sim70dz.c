/* sim70dz.c - as sim70dc.c, but the deep part of the stack is stored compressed (1 byte per entry + zlib)
 *            and the accesses to it are counted.
 * sim70dc.c - fast macro simulator for BB(6) holdout no. 70, divide and conquer with GMP, deep stack on disk
 *   1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE   (also no. 86 started in state B)
 *
 * Same Bells, rules and results as sim70.c (see there): Bell start = state A on a blank cell, tape
 * 1 0^x 1^m 0^g1 1^b1 ... ; every Bell is x' = 3x/2 + c with c and the new stack prefix depending only on
 * x mod 12 (more bits if needed) and a short prefix of the stack; rules are learned on the fly by direct simulation.
 *
 * Differences to sim70.c:
 *  - x is a GMP number and is advanced by divide and conquer as in belldc.c: m Bells on x = the first m/2 Bells on
 *    the low m/2 + 12 bits (recursively), one product with 3^(m/2), then the second half; at the bottom at most
 *    24 Bells on one 64-bit word.  Cost about M(n) log n instead of n^2.
 *  - the deep part of the stack is moved to the file sim70dz.stack (append only; only the front part stays in RAM).
 *    Keep this file together with the checkpoint sim70dz.ck.
 *
 * Compile:  gcc -O3 -march=native -o sim70dz sim70dz.c -lgmp -lz   (sudo apt install libgmp-dev zlib1g-dev)
 * Files:    sim70dz.ck (checkpoint), sim70dz.stack (compressed deep stack, keep both together), events70dz.txt
 * Stack chunks on disk: each entry as 1 byte (255 = escape, then 4 bytes), the chunk compressed with zlib level 1
 * (about 10 times smaller than 4-byte entries).  The report shows how often and how deep the run reads them back.
 * Run:      ./sim70dz            continues from sim70dz.ck if it exists; Ctrl-C: stops after the current block,
 *                                writes the checkpoint (this can take a while for large x)
 * Options:  -t BELL   stop at this Bell (and print check values)      -f   start fresh
 *           -b B      Bells per block (default: bits of x / 8, between 2^16 and 2^26)
 *           -r SEC    report interval (default 60)    -s SEC  checkpoint interval (default 1800)
 *           -M MB     RAM for the stack front in MB (default 512; the rest goes to sim70dz.stack)
 *           -d        discard the deep stack instead of writing it (no disk use).  So far the run has never read
 *                     back a part of the stack that left RAM (see "disk reads" in the report); if it ever needs a
 *                     discarded part, the program stops with a message (the result up to there stays exact).
 * Check values (identical to sim70.c and the Python run) at Bell 4663800:
 *   bits 2728153, x mod 2^64 = 0x58106550ccb57c0e, stack 2616485 entries, hash 884327361506333381
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include <fcntl.h>
#include <gmp.h>
#include <zlib.h>
typedef uint64_t u64; typedef unsigned __int128 u128; typedef uint32_t u32; typedef int64_t i64;
/* ------------------------------------------------------------------ TM and direct level simulation */
static const char *TM="1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE";
static int tw[6][2],td[6][2],tq[6][2];
#define TW (1<<22)
static unsigned char tape[TW];
static void tm_init(void){
  for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=TM+7*i+3*b;
    if(x[0]=='-'){tq[i][b]=-1;continue;} tw[i][b]=x[0]-'0';td[i][b]=x[1]=='R'?1:-1;tq[i][b]=x[2]-'A';}
}
enum {LV_OK=0,LV_HALT=1,LV_OUT=2,LV_MAX=3};
/* one Bell from a Bell start; tok = 1, x, m, g1, b1, ... ; lim = cell index (from the tape start) the head must
   not reach, or -1.  On LV_OK: out[] = blocks of the new Bell start (starting with ones), off = position of its
   first cell relative to the old tape start, z0 = zeros between head and that cell. */
static int level_sim(const long *tok,int ntok,long lim,long *out,int *nout,int maxout,long *z0,long *off){
  long p=TW/4, base=p+1, x=base; int one=1;
  for(int i=0;i<ntok;i++){ for(long k=0;k<tok[i];k++) tape[x++]=one; one=!one; }
  long lo=p, hi=x, maxx=x; int q=0; long long MX=400000000LL; int res=LV_MAX;
  for(long long st=1;st<=MX;st++){
    int b=tape[p]; if(tq[q][b]<0){res=LV_HALT;break;}
    tape[p]=tw[q][b]; p+=td[q][b]; q=tq[q][b];
    if(p>hi){hi=p; if(hi>maxx)maxx=hi;}
    if(lim>=0 && p-base>=lim){res=LV_OUT;break;}
    if(p<2||p>TW-3){res=LV_MAX;break;}
    if(p<lo){ lo=p; if(q==0){
      long y=p+1; while(y<=hi&&!tape[y])y++;
      if(y<hi && tape[y] && !tape[y+1]){
        long y2=y+1; while(y2<=hi&&!tape[y2])y2++; long L2=0; while(y2+L2<=hi&&tape[y2+L2])L2++;
        if(!(y2-y-1==6 && L2==4)){
          *z0=y-p-1; *off=y-base; int k=0; long yy=y;
          while(yy<=hi){ long L=0; int bb=tape[yy]; while(yy<=hi&&tape[yy]==bb){L++;yy++;} if(yy>hi&&bb==0)break;
            if(k>=maxout){res=LV_MAX;goto done;} out[k++]=L; }
          *nout=k; res=LV_OK; break; }}}}
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
  int nh=0,nok=0,nout_=0; for(int t=0;t<5;t++){ if(res[t]==LV_HALT)nh++; if(res[t]==LV_OK)nok++; if(res[t]==LV_OUT)nout_++; }
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

/* ------------------------------------------------------------------ stack: RAM front + disk part */
/* logical stack (deepest first): disk segments seg[0..nseg), then RAM S[0..top); the front (top of stack) is S[top-1].
   The disk file is append only: spilled chunks are appended, chunks read back are just dropped from the segment
   list, so a checkpoint stays valid whatever happens later. */
static u32 *S; static size_t top=0,scap=0;
typedef struct { u64 off,clen,len; } Seg;     /* file offset, compressed bytes, entries */
static Seg *seg; static size_t nseg=0,segcap=0; static u64 Dn=0, fileend=0; static int sfd=-1;
static const char *SF="sim70dz.stack";
static u64 nreload=0, reloaded=0, Dpeak=0, maxdepth=0; static size_t CH=16u<<20; static int discard=0, anydiscard=0;
static size_t RAMHI=128u<<20;                       /* entries kept in RAM before spilling (set by -M) */
static void sopen(void){ if(sfd<0){ sfd=open(SF,O_RDWR|O_CREAT,0644); if(sfd<0){perror(SF);exit(1);} } }
static unsigned char *zbuf=NULL,*ebuf=NULL; static size_t zcap=0,ecap=0;
static void spill(void){                            /* move the deepest CH entries of the RAM part to disk, compressed */
  size_t L=CH; if(L>top/2) L=top/2;
  if(discard){                                     /* -d: do not keep the deep stack (it has never been read back) */
    if(nseg==segcap){segcap=segcap?segcap*2:64; seg=realloc(seg,segcap*sizeof(Seg));}
    seg[nseg].off=~0ULL; seg[nseg].clen=0; seg[nseg].len=L; nseg++; Dn+=L; if(Dn>Dpeak)Dpeak=Dn; anydiscard=1;
    memmove(S,S+L,(top-L)*4); top-=L; return; }
  sopen();
  if(ecap<L*5+16){ ecap=L*5+16; ebuf=realloc(ebuf,ecap); }
  size_t e=0; for(size_t i=0;i<L;i++){ u32 v=S[i]; if(v<255) ebuf[e++]=(unsigned char)v; else { ebuf[e++]=255; memcpy(ebuf+e,&v,4); e+=4; } }
  uLongf zl=compressBound(e); if(zcap<zl){ zcap=zl; zbuf=realloc(zbuf,zcap); }
  if(compress2(zbuf,&zl,ebuf,e,1)!=Z_OK){ fprintf(stderr,"zlib compress error\n"); exit(1); }
  size_t done=0; while(done<zl){ ssize_t w=pwrite(sfd,zbuf+done,zl-done,(off_t)(fileend+done)); if(w<=0){perror("stack file write");exit(1);} done+=w; }
  if(nseg==segcap){segcap=segcap?segcap*2:64; seg=realloc(seg,segcap*sizeof(Seg));}
  seg[nseg].off=fileend; seg[nseg].clen=zl; seg[nseg].len=L; nseg++; fileend+=zl; Dn+=L; if(Dn>Dpeak)Dpeak=Dn;
  memmove(S,S+L,(top-L)*4); top-=L;
}
static u64 bell; static void save_and_exit(void);
static void readseg(const Seg*g,u32*dst){            /* decode a whole segment into dst (g->len entries) */
  if(zcap<g->clen){ zcap=g->clen; zbuf=realloc(zbuf,zcap); }
  size_t done=0; while(done<g->clen){ ssize_t r=pread(sfd,zbuf+done,g->clen-done,(off_t)(g->off+done)); if(r<=0){perror("stack file read");exit(1);} done+=r; }
  uLongf el=g->len*5+16; if(ecap<el){ ecap=el; ebuf=realloc(ebuf,ecap); }
  if(uncompress(ebuf,&el,zbuf,g->clen)!=Z_OK){ fprintf(stderr,"zlib uncompress error (stack file damaged?)\n"); exit(1); }
  size_t e=0; for(u64 i=0;i<g->len;i++){ unsigned char c=ebuf[e++]; if(c<255) dst[i]=c; else { memcpy(&dst[i],ebuf+e,4); e+=4; } }
}
static void reload(size_t want){                    /* bring whole segments back below the RAM part */
  while(top<want && nseg>0){
    Seg g=seg[nseg-1]; u64 L=g.len;
    if(g.off==~0ULL){ fprintf(stderr,"\n*** the run needs a part of the stack that was discarded (-d) at Bell %llu.\n    Continue from an earlier checkpoint without -d. ***\n",(unsigned long long)bell); save_and_exit(); }
    if(top+L>scap){ scap=(top+L)*2; S=realloc(S,scap*4); }
    memmove(S+L,S,top*4); readseg(&g,S);
    top+=L; Dn-=L; nseg--;
    nreload++; reloaded+=L; if(Dpeak-Dn>maxdepth) maxdepth=Dpeak-Dn;
  }
}
static inline void ensure(size_t k){ if(top<k && Dn) reload(k); }
static void spush(u32 v){ if(top==scap){scap=scap?scap*2:1<<20; S=realloc(S,scap*4);} S[top++]=v; }
static inline u64 stotal(void){ return Dn+top; }

/* x mod M for M = 12*2^j, from the exact low bits (x is always divisible by 3) */
static long xmod(u64 low,long M){ long m2=M/3; long r=(long)(low&(u64)(m2-1)); while(r%3)r+=m2; return r; }

static Rule *findrule(u64 low){
  static u32 key[8192]; static u32 P[8192];
  for(int d=0;;d++){
    int np,inf;
    ensure((size_t)(2*d+4));
    if((u64)(2*d+1)<stotal()){ np=2*d+2; inf=0; } else { np=(int)top; inf=1; }
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
  if(r->inf){ top=0; } else top-=r->lp;
  long *q=qpool+r->qoff; int nq=r->nq;
  outv[no++]=(u32)q[0]; int i=1;
  while(i+1<nq){ long g=q[i],b=q[i+1]; if(g==0) outv[no-1]+=(u32)b; else {outv[no++]=(u32)g; outv[no++]=(u32)b;} i+=2; }
  if(i<nq){ long g=q[i]; if(g==0){ ensure(1); if(top>0) outv[no-1]+=S[--top]; else outv[no++]=(u32)g; } else outv[no++]=(u32)g; }
  for(int j=no-1;j>=0;j--) spush(outv[j]);
  if(top>RAMHI) spill();
}

/* ------------------------------------------------------------------ statistics */
static long long created[5],firstl[5],lastl[5]; static long minodd=1000000000;
static const int ODD[5]={1,3,5,7,9};
static FILE *evf; static int halted=0;
static void oddfront(int cnt[5]){ for(int k=0;k<5;k++)cnt[k]=0; ensure(8);
  for(int j=1;j<=3;j++){ size_t idx=2*j; if(idx>=top)break; u32 b=S[top-1-idx]; if((b&1)&&b<=9) cnt[b/2]++; } }

/* one Bell: returns c, or sets halted */
static long onebell(u64 low){
  int before[5],after[5]; oddfront(before);
  Rule *r=findrule(low);
  if(r->type==T_HALT){ halted=1; return 0; }
  apply(r); bell++;
  oddfront(after);
  for(int k=0;k<5;k++){ int d=after[k]-before[k]; if(d>0){ created[k]+=d; if(firstl[k]<0)firstl[k]=(long long)bell; lastl[k]=(long long)bell;
      if(ODD[k]<minodd)minodd=ODD[k];
      if(ODD[k]<=7&&evf){ fprintf(evf,"Bell %llu: block %d appeared near the front\n",(unsigned long long)bell,ODD[k]); fflush(evf);} } }
  return r->c;
}

/* ------------------------------------------------------------------ divide and conquer on x */
#define LEAF 24
#define MB 12                    /* extra low bits: rules may need x mod 2^8 (M up to 768) */
static mpz_t R[80];
static struct { long long h; mpz_t v; } P3[80][2]; static int p3next[80];
static const __mpz_struct* pow3(long long h,int d){
  for(int i=0;i<2;i++) if(P3[d][i].h==h) return P3[d][i].v;
  int i=p3next[d]; p3next[d]^=1; P3[d][i].h=h; mpz_ui_pow_ui(P3[d][i].v,3,(unsigned long)h); return P3[d][i].v; }
static void leaf(mpz_t x,int m){
  int w=m+MB; mpz_fdiv_r_2exp(R[79],x,(mp_bitcnt_t)w); i64 r=(i64)mpz_getlimbn(R[79],0);
  mpz_fdiv_q_2exp(x,x,(mp_bitcnt_t)w);
  int done=0;
  for(int j=0;j<m;j++){
    long c=onebell((u64)r); if(halted) break;
    r=3*(r>>1)+c; done++;           /* x is even at every Bell; r is the low part, may become negative */
  }
  if(halted) return;
  u64 p=1; for(int j=0;j<done;j++)p*=3;
  mpz_mul_ui(x,x,(unsigned long)p); mpz_mul_2exp(x,x,(mp_bitcnt_t)(w-done));
  mpz_set_si(R[79],(long)r); mpz_add(x,x,R[79]);
}
static void adv(mpz_t x,long long m,int d){
  if(m<=LEAF){ leaf(x,(int)m); return; }
  long long h=m/2; mp_bitcnt_t w=(mp_bitcnt_t)(h+MB);
  mpz_fdiv_r_2exp(R[d],x,w); mpz_fdiv_q_2exp(x,x,w);
  adv(R[d],h,d+1); if(halted) return;
  mpz_mul(x,x,pow3(h,d)); mpz_mul_2exp(x,x,w-(mp_bitcnt_t)h); mpz_add(x,x,R[d]);
  adv(x,m-h,d+1);
}

/* ------------------------------------------------------------------ checkpoint */
static mpz_t X;
static volatile sig_atomic_t stopflag=0; static void onsig(int s){(void)s;stopflag=1;}
static const char *CK="sim70dz.ck";
static void save(void){
  if(sfd>=0) fdatasync(sfd);
  char tmp[64]; snprintf(tmp,64,"%s.tmp",CK); FILE*f=fopen(tmp,"wb"); if(!f){perror("checkpoint");return;}
  fwrite("S70DZ001",1,8,f); fwrite(&bell,8,1,f); fwrite(created,8,5,f); fwrite(firstl,8,5,f); fwrite(lastl,8,5,f);
  fwrite(&minodd,sizeof minodd,1,f); fwrite(&Dn,8,1,f); fwrite(&fileend,8,1,f);
  u64 ns=nseg; fwrite(&ns,8,1,f); fwrite(seg,sizeof(Seg),nseg,f);
  u64 t=top; fwrite(&t,8,1,f); fwrite(S,4,top,f); mpz_out_raw(f,X);
  fwrite(&nreload,8,1,f); fwrite(&reloaded,8,1,f); fwrite(&Dpeak,8,1,f); fwrite(&maxdepth,8,1,f);
  if(ferror(f)||fclose(f)){ fprintf(stderr,"checkpoint write error (disk full?)\n"); remove(tmp); return; }
  rename(tmp,CK);
}
static void save_and_exit(void){ fflush(stdout); exit(3); }
static int load(void){
  FILE*f=fopen(CK,"rb"); if(!f)return 0; char m[8]; if(fread(m,1,8,f)!=8||memcmp(m,"S70DZ001",8)){fclose(f);return 0;}
  u64 ns,t;
  if(fread(&bell,8,1,f)!=1||fread(created,8,5,f)!=5||fread(firstl,8,5,f)!=5||fread(lastl,8,5,f)!=5||fread(&minodd,sizeof minodd,1,f)!=1
     ||fread(&Dn,8,1,f)!=1||fread(&fileend,8,1,f)!=1||fread(&ns,8,1,f)!=1) goto bad;
  segcap=ns+64; seg=realloc(seg,segcap*sizeof(Seg)); nseg=ns; if(fread(seg,sizeof(Seg),ns,f)!=ns) goto bad;
  if(fread(&t,8,1,f)!=1) goto bad; scap=t*2+(1<<20); S=realloc(S,scap*4); top=t; if(fread(S,4,t,f)!=t) goto bad;
  if(!mpz_inp_raw(X,f)) goto bad;
  if(fread(&nreload,8,1,f)!=1||fread(&reloaded,8,1,f)!=1||fread(&Dpeak,8,1,f)!=1||fread(&maxdepth,8,1,f)!=1) goto bad;
  fclose(f); if(Dn){ sopen(); if(lseek(sfd,0,SEEK_END)<(off_t)fileend){fprintf(stderr,"%s is shorter than the checkpoint expects\n",SF);exit(1);} }
  return 1;
bad: fprintf(stderr,"checkpoint damaged\n"); exit(1);
}
static double now(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+ts.tv_nsec*1e-9; }
static void report(double rate){
  printf("Bell %llu (about 10^%.4g steps) | x %zu bits | stack %llu (RAM %zu, disk %llu = %.2f GB file) | rules %zu (%ld learned) | %.0f Bells/s\n",
    (unsigned long long)bell,0.352*bell,mpz_sizeinbase(X,2),(unsigned long long)stotal(),top,(unsigned long long)Dn,fileend/1e9,nrules,nlearned,rate);
  printf("   disk reads: %llu chunks, %llu entries; deepest read %llu entries below the highest disk level\n",(unsigned long long)nreload,(unsigned long long)reloaded,(unsigned long long)maxdepth);
  printf("   odd blocks near the front:"); for(int k=4;k>=0;k--) printf("  %d: %lld",ODD[k],created[k]);
  printf("  | smallest seen: "); if(minodd<1000000000)printf("%ld",minodd); else printf("-");
  for(int k=3;k>=0;k--) if(created[k]) printf("  | %d first at %lld, last at %lld",ODD[k],firstl[k],lastl[k]);
  printf("\n"); fflush(stdout);
}
static void checkvalues(void){
  u64 h=0; u128 MOD=((u128)1)<<61;
  for(size_t sg=0;sg<nseg;sg++) if(seg[sg].off==~0ULL){ printf("check values at Bell %llu: bits %zu, x mod 2^64 = 0x%016llx, stack %llu entries, hash not available (deep stack discarded with -d)\n",
      (unsigned long long)bell,mpz_sizeinbase(X,2),(unsigned long long)mpz_getlimbn(X,0),(unsigned long long)stotal()); return; }
  for(size_t sg=0;sg<nseg;sg++){ u32 *buf=malloc(seg[sg].len*4); readseg(&seg[sg],buf);
    for(u64 i=0;i<seg[sg].len;i++) h=(u64)(((u128)h*1000003+buf[i])%MOD); free(buf); }
  for(size_t i=0;i<top;i++) h=(u64)(((u128)h*1000003+S[i])%MOD);
  printf("check values at Bell %llu: bits %zu, x mod 2^64 = 0x%016llx, stack %llu entries, hash %llu\n",
    (unsigned long long)bell,mpz_sizeinbase(X,2),(unsigned long long)mpz_getlimbn(X,0),(unsigned long long)stotal(),(unsigned long long)h);
}

/* ------------------------------------------------------------------ main */
int main(int argc,char**argv){
  double rep=60,sav=1800; u64 target=0; long long B0=0; int fresh=0; long ramMB=512;
  for(int i=1;i<argc;i++){
    if(!strcmp(argv[i],"-r")&&i+1<argc)rep=atof(argv[++i]); else if(!strcmp(argv[i],"-s")&&i+1<argc)sav=atof(argv[++i]);
    else if(!strcmp(argv[i],"-t")&&i+1<argc)target=strtoull(argv[++i],0,10); else if(!strcmp(argv[i],"-b")&&i+1<argc)B0=atoll(argv[++i]);
    else if(!strcmp(argv[i],"-M")&&i+1<argc)ramMB=atol(argv[++i]); else if(!strcmp(argv[i],"-f"))fresh=1; else if(!strcmp(argv[i],"-d"))discard=1;
    else {fprintf(stderr,"usage: %s [-t bell] [-b bells_per_block] [-r sec] [-s sec] [-M MB] [-f] [-d]\n",argv[0]);return 1;} }
  RAMHI=(size_t)ramMB*(1u<<20)/4/2; if(RAMHI<(1u<<20))RAMHI=1u<<20;   /* half of the budget: room for growth */
  CH=RAMHI/4; if(CH<(1u<<18))CH=1u<<18;
  tm_init(); signal(SIGINT,onsig); signal(SIGTERM,onsig);
  for(int i=0;i<80;i++){ mpz_init(R[i]); mpz_init(P3[i][0].v); mpz_init(P3[i][1].v); P3[i][0].h=P3[i][1].h=-1; }
  mpz_init(X);
  if(fresh||!load()){ bell=0; mpz_set_ui(X,30); top=0; Dn=0; nseg=0; fileend=0; spush(4); spush(18); spush(11);
    for(int k=0;k<5;k++){created[k]=0;firstl[k]=lastl[k]=-1;} minodd=1000000000;
    if(fresh) unlink(SF); }
  else printf("continuing from %s at Bell %llu\n",CK,(unsigned long long)bell);
  evf=fopen("events70dz.txt","a");
  double t0=now(), tl=t0, ts=t0; u64 b0=bell;
  while(!stopflag && !halted){
    if(target && bell>=target) break;
    long long bits=(long long)mpz_sizeinbase(X,2);
    long long B=B0?B0:bits/8; if(!B0){ if(B<(1LL<<16))B=1LL<<16; if(B>(1LL<<26))B=1LL<<26; }
    if(target && (u64)B>target-bell) B=(long long)(target-bell);
    adv(X,B,0);
    double t=now();
    if(t-tl>=rep){ report((bell-b0)/(t-t0)); tl=t; }
    if(t-ts>=sav){ save(); ts=t; }
  }
  double t=now(); report((bell-b0)/(t-t0+1e-9));
  if(halted){ printf("*** HALT: the Bell after Bell %llu halts ***\n",(unsigned long long)bell); if(evf)fprintf(evf,"HALT after Bell %llu\n",(unsigned long long)bell); }
  if(target && bell>=target) checkvalues();
  save(); printf("checkpoint written (%s, stack file %s)\n",CK,SF);
  return 0;
}
