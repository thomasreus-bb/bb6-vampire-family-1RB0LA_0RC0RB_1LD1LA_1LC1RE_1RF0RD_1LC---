// belldco.c - exact Bell orbit with k on disk ("out of core"): the memory no longer grows with k.
// Same orbit, checkpoints and log lines as belldc.c / belldcf.c, so the programs can continue each other's runs.
// FLINT multiplication on several threads as in belldcf.c.
//
// The orbit is computed in TM1 coordinates: a Bell starts at 0^inf 1^k F> S 0^inf, the next Bell has
//   k' = 3*floor(k/2) + c,   (S', c) = f(S, bit 1 of k)      (table in tab.txt / tab_names.txt).
// Bell numbers, checkpoint names and the progress log use the Bell numbering of TM2 (see README.md).
//
// Compile: gcc -O3 -march=native -o belldco belldco.c -lflint -lmpfr -lgmp -lpthread -lm   (needs FLINT >= 3)
// Usage:   ./belldco [-t TARGET [-p]] [-i INTERVAL] [-M GB] [-w DIR] [-j N | -j auto[:MAX]] [-b B]
//   -t, -p, -i   as in belldc (target, horizon pruning, checkpoint interval)
//   -M GB        memory budget for the parts kept in RAM (default 4); it sets the largest block of Bells
//                (GB * 2^30 / 6 Bells per block; measured about 5 bytes per Bell, so the peak stays near the budget)
//   -w DIR       directory for the two work files with k in binary (default: the current directory);
//                each is as large as k (8 bytes per 64 bits), e.g. 46 GB at Bell 6.3e11
//   -j N, auto   threads as in belldcf (default: all cores)
//   -b B         fixed block size in Bells (default: bits of k / 8, at most the -M limit)
//          ./belldco init BELL K S          write a first checkpoint (K < 2^64)
// Disk space: two work files of the size of k plus the checkpoints (hex text, 2 times the size of k each;
// the start checkpoint, the newest one and with -p the last exact one are kept).
//
// Method. As in belldc: k = q*2^(B+2) + r, after B Bells k = q*3^B*4 + r_B.  Here q stays on disk: it is read
// in chunks, each chunk is multiplied by 3^B in RAM and the product is written in order to the second work
// file (the upper part of each chunk product is carried into the next).  This streamed product runs in its
// own thread while the main thread computes r_B in RAM (divide and conquer with FLINT, as in belldcf).
// Finally r_B is added at the bottom of the new file.  One block reads k once and writes it once.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <dirent.h>
#include <limits.h>
#include <ctype.h>
#include <gmp.h>
#include <unistd.h>
#include <pthread.h>
#include <malloc.h>
#include <flint/flint.h>
#include <flint/mpn_extras.h>
typedef uint64_t u64;
#define LEAF 32
#define PMARGIN 128
#define PROGLABEL "belldco-1 (bb6 vampire family)"

static int n; static int *nxt,*cc,*dist; static char **names;
static int dmin=INT_MAX; static long long dminbell=-1, dsince=-1;
static long long gbell=0;                 // Bell number of the next Bell to be simulated
static int halted=0, haltS=-1; static long long haltbell=-1;
static long long horizon=0;               // > 0: pruned run towards this Bell
static int cut=0;                         // 1 once pruning has actually cut bits of k (before that k is exact)
static char orbit[64]="?";
static u64 p3[LEAF+1];
static int bdiv=8;                        // block size = (bits of k) / bdiv; -m: 32 (less memory)

/* ---------- multiplication with FLINT, threads ---------- */
#define FMUL_MIN 2000                      // below this many limbs (both factors together) use GMP
static __thread mpz_t FT; static __thread int FTi=0;   // result buffer of fmul (one per thread)
// r = a*b (r may be a or b)
static void fmul(mpz_t r,const mpz_t a,const mpz_t b){
  size_t an=mpz_size(a), bn=mpz_size(b);
  if(an==0||bn==0){ mpz_set_ui(r,0); return; }
  if(an+bn<FMUL_MIN){ mpz_mul(r,a,b); return; }
  if(!FTi){ mpz_init(FT); FTi=1; }
  int sg=mpz_sgn(a)*mpz_sgn(b);
  const mpz_srcptr x= an>=bn? a:b, y= an>=bn? b:a; size_t xn= an>=bn? an:bn, yn= an>=bn? bn:an;
  mp_limb_t*T=mpz_limbs_write(FT,(mp_size_t)(xn+yn));
  flint_mpn_mul(T,mpz_limbs_read(x),(mp_size_t)xn,mpz_limbs_read(y),(mp_size_t)yn);
  size_t tn=xn+yn; while(tn>0&&T[tn-1]==0) tn--;
  mpz_limbs_finish(FT,(mp_size_t)tn); if(sg<0) mpz_neg(FT,FT);
  mpz_swap(r,FT); if(mpz_size(r)>4096) mpz_realloc2(FT,64); }   // free the old factor at once (memory as with GMP)
static int jauto=0, jmax=0, jcur=1, ncpu=1; static double jlast=-1e9;
static double now();
static void set_threads(int j){ if(j<1) j=1; if(jmax>0&&j>jmax) j=jmax; if(j!=jcur){ flint_set_num_threads(j); jcur=j; } }
// -j auto: free cores = cores - (1-minute load average - our own threads), checked at most once a minute
static void update_threads(void){
  if(!jauto) return;
  double t=now(); if(t-jlast<60) return; jlast=t;
  double la=0; FILE*f=fopen("/proc/loadavg","r"); if(f){ if(fscanf(f,"%lf",&la)!=1) la=0; fclose(f); }
  double other=la-jcur; if(other<0) other=0;
  int j=(int)(ncpu-other+0.5); int old=jcur; set_threads(j);
  if(jcur!=old){ time_t n=time(NULL); char ts[32]; strftime(ts,sizeof ts,"%Y-%m-%d %H:%M:%S",localtime(&n));
    printf("%s  threads %d -> %d (load %.2f, %d cores)\n",ts,old,jcur,la,ncpu); fflush(stdout); } }

static double now(){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+1e-9*ts.tv_nsec; }

/* ---------- divide and conquer ---------- */
static mpz_t R[80];                                   // low parts, one per recursion depth
static struct { long long h; mpz_t v; } P3[80][2];    // cache of 3^h, two values per depth
static int p3next[80];
static const mpz_t* pow3(long long h,int d){
  for(int i=0;i<2;i++) if(P3[d][i].h==h) return (const mpz_t*)&P3[d][i].v;
  int i=p3next[d]; p3next[d]^=1; P3[d][i].h=h; mpz_ui_pow_ui(P3[d][i].v,3,(unsigned long)h);
  return (const mpz_t*)&P3[d][i].v; }

// at most LEAF Bells on x, in place
static void leaf(mpz_t x,int*S,int m){
  int w=m+2; u64 r=mpz_getlimbn(x,0)&(((u64)1<<w)-1);
  mpz_fdiv_q_2exp(x,x,w);
  int st=*S, done=0;
  for(int j=0;j<m;j++){
    if(dist[st]<dmin){ dmin=dist[st]; dminbell=gbell; }
    int idx=2*st+(int)((r>>1)&1); int t=nxt[idx];
    if(t<0){ halted=t; haltbell=gbell; haltS=st; break; }
    r=3*(r>>1)+(u64)cc[idx]; st=t; gbell++; done++; }
  *S=st;
  if(halted) return;
  mpz_mul_ui(x,x,(unsigned long)p3[done]); mpz_mul_2exp(x,x,2); mpz_add_ui(x,x,(unsigned long)r); }

// m Bells on x, in place (exact)
// The product of the high part with 3^h does not depend on the h Bells on the low part, so for large numbers
// it runs in a second thread while the low part is advanced (task parallelism; PAR_MIN = smallest size in bits).
#define PAR_MIN (1<<21)
static volatile int ntask=0;               // running product threads
static int maxtask(void){ return jcur>1? jcur-1:0; }
typedef struct { mpz_ptr x; mpz_srcptr p; } mjob;
static void* mthread(void*a){ mjob*j=a; fmul(j->x,j->x,j->p); mpz_mul_2exp(j->x,j->x,2); mpz_clear(FT); FTi=0; flint_cleanup(); return NULL; }
static void adv(mpz_t x,int*S,long long m,int d){
  if(m<=LEAF){ leaf(x,S,(int)m); return; }
  long long h=m/2; mp_bitcnt_t w=(mp_bitcnt_t)h+2;
  mpz_fdiv_r_2exp(R[d],x,w); mpz_fdiv_q_2exp(x,x,w);
  const mpz_t*pw=pow3(h,d); pthread_t th; mjob job={x,*pw}; int par=0;
  if((long long)mpz_sizeinbase(x,2)>=PAR_MIN){
    if(__sync_add_and_fetch(&ntask,1)<=maxtask() && pthread_create(&th,NULL,mthread,&job)==0) par=1;
    else __sync_sub_and_fetch(&ntask,1); }
  adv(R[d],S,h,d+1);
  if(par){ pthread_join(th,NULL); __sync_sub_and_fetch(&ntask,1); }
  if(halted) return;
  if(!par){ fmul(x,x,*pw); mpz_mul_2exp(x,x,2); }
  mpz_add(x,x,R[d]);
  adv(x,S,m-h,d+1); }

/* ---------- checkpoints (same format as bellntt / bellnttp) ---------- */
static u64 fnv(u64 h,const char*p,size_t k){ for(size_t i=0;i<k;i++){ h^=(unsigned char)p[i]; h*=1099511628211ULL; } return h; }
static const u64 FNV0=14695981039346656037ULL;
static const char HX[]="0123456789ABCDEF";
static long long bitlen(const mpz_t k){ return mpz_sgn(k)?(long long)mpz_sizeinbase(k,2):1; }
static void ckpt_name_h(char*buf,size_t sz,long long bell,int pruned){ snprintf(buf,sz,pruned?"checkpoints/bell_%lld_pchkpt.txt":"checkpoints/bell_%lld_chkpt.txt",bell); }

/* ---------- k on disk ----------
   A k file holds k as little-endian 64-bit limbs (limb 0 first); nl = number of limbs, top limb nonzero
   (k = 0 is stored as one zero limb). */
#include <fcntl.h>
#include <sys/stat.h>
#include <errno.h>
typedef struct { char path[512]; int fd; long long nl; } kfile;
static char wdir[400]=".";
static long long memlimit=4LL<<30;        // -M: memory budget for the in-RAM parts, bytes

static void die(const char*m){ fprintf(stderr,"%s: %s\n",m,strerror(errno)); exit(1); }
static void kf_open(kfile*f,const char*name,int create){
  snprintf(f->path,sizeof f->path,"%s/%s",wdir,name);
  f->fd=open(f->path,create?(O_RDWR|O_CREAT|O_TRUNC):O_RDWR,0644); if(f->fd<0) die(f->path); f->nl=0; }
static void kf_pread(kfile*f,u64*buf,long long n,long long at){
  char*p=(char*)buf; size_t want=(size_t)n*8; off_t off=(off_t)at*8;
  while(want){ ssize_t g=pread(f->fd,p,want,off); if(g<0){ if(errno==EINTR) continue; die("read k file"); }
    if(g==0){ memset(p,0,want); break; } p+=g; want-=(size_t)g; off+=g; } }
static void kf_pwrite(kfile*f,const u64*buf,long long n,long long at){
  const char*p=(const char*)buf; size_t want=(size_t)n*8; off_t off=(off_t)at*8;
  while(want){ ssize_t g=pwrite(f->fd,p,want,off); if(g<0){ if(errno==EINTR) continue; die("write k file (disk full?)"); }
    p+=g; want-=(size_t)g; off+=g; } }
static u64 kf_limb(kfile*f,long long i){ u64 v=0; if(i<f->nl) kf_pread(f,&v,1,i); return v; }
static void kf_setlen(kfile*f,long long nl){ // strip zero top limbs (looking down from nl) and truncate the file
  while(nl>1&&kf_limb(&(kfile){.fd=f->fd,.nl=nl},nl-1)==0) nl--;
  if(nl<1) nl=1; f->nl=nl; if(ftruncate(f->fd,(off_t)nl*8)) die("truncate k file"); }
static long long kf_bits(kfile*f){ u64 t=kf_limb(f,f->nl-1); if(!t) return 1; return (f->nl-1)*64+64-__builtin_clzll(t); }
static void kf_from_mpz(kfile*f,const mpz_t x){ size_t n=mpz_size(x);
  if(n==0){ u64 z=0; kf_pwrite(f,&z,1,0); f->nl=1; } else { kf_pwrite(f,(const u64*)mpz_limbs_read(x),(long long)n,0); f->nl=(long long)n; }
  if(ftruncate(f->fd,(off_t)f->nl*8)) die("truncate k file"); }
// read the lowest nlimbs limbs into x
static void kf_low_mpz(kfile*f,mpz_t x,long long nlimbs){ if(nlimbs>f->nl) nlimbs=f->nl;
  mp_limb_t*L=mpz_limbs_write(x,(mp_size_t)nlimbs); kf_pread(f,(u64*)L,nlimbs,0);
  long long t=nlimbs; while(t>0&&L[t-1]==0) t--; mpz_limbs_finish(x,(mp_size_t)t); }
// keep k mod 2^bits (pruning); returns 1 if nonzero bits were removed
static int kf_trunc_bits(kfile*f,long long bits){
  long long full=bits/64, rb=bits%64, nl=f->nl; int removed=0;
  if((long long)nl*64<=bits) return 0;
  long long keepl=full+(rb?1:0);
  // removed limbs above keepl: nonzero? (top limb is nonzero by invariant, so yes if nl>keepl)
  if(nl>keepl) removed=1;
  if(rb){ u64 t=kf_limb(f,full); u64 m=((u64)1<<rb)-1; if(t&~m) removed=1; t&=m; kf_pwrite(f,&t,1,full); }
  f->nl=keepl; kf_setlen(f,keepl); return removed; }

/* ---------- checkpoints with k on disk (same file format as belldc) ---------- */
static char wbuf[1<<20];
static int write_ckpt_kf(long long bell,kfile*K,int s,long long from,double secs){
  char name[256],tmpn[300]; ckpt_name_h(name,sizeof name,bell,cut); snprintf(tmpn,sizeof tmpn,"%s.tmp",name);
  long long bits=kf_bits(K); long long nd=(bits+3)/4; if(nd==0) nd=1;
  char lb[64],ls[128],lh[64]=""; snprintf(lb,sizeof lb,"bell %lld\n",bell); snprintf(ls,sizeof ls,"S 1%s\n",names[s]);
  if(cut) snprintf(lh,sizeof lh,"horizon %lld\n",horizon);
  u64 h=fnv(FNV0,lb,strlen(lb)); h=fnv(h,ls,strlen(ls)); h=fnv(h,lh,strlen(lh)); h=fnv(h,"k_hex ",6);
  time_t now_t=time(NULL); char d[16],t[16]; strftime(d,sizeof d,"%Y-%m-%d",localtime(&now_t)); strftime(t,sizeof t,"%H:%M:%S",localtime(&now_t));
  FILE*f=fopen(tmpn,"w"); if(!f){ perror(tmpn); return -1; }
  fprintf(f,"# bellntt checkpoint\ndate %s\ntime %s\nprogram %s\norbit %s\n%s%s%sk_bits %lld\nk_hex ",d,t,PROGLABEL,orbit,lb,ls,lh,bits);
  // digits from the top: digit dg (0 = lowest) is nibble dg%16 of limb dg/16
  const long long CH=1<<16; u64*L=malloc(CH*8); size_t bp=0; long long have_lo=-1,have_hi=-1;
  for(long long i=0;i<nd;i++){ long long dg=nd-1-i, li=dg/16;
    if(li<have_lo||li>have_hi){ have_hi=li; have_lo=li-CH+1; if(have_lo<0) have_lo=0; kf_pread(K,L,have_hi-have_lo+1,have_lo); }
    u64 limb=L[li-have_lo]; wbuf[bp++]=HX[(limb>>(4*(dg%16)))&15];
    if(bp==sizeof wbuf){ h=fnv(h,wbuf,bp); fwrite(wbuf,1,bp,f); bp=0; } }
  if(bp){ h=fnv(h,wbuf,bp); fwrite(wbuf,1,bp,f); }
  free(L);
  h=fnv(h,"\n",1); fputc('\n',f);
  if(dmin<INT_MAX) fprintf(f,"dmin %d at_bell %lld since_bell %lld\n",dmin,dminbell,dsince);
  if(from>=0&&bell>from) fprintf(f,"time_per_bell %.3e s (average over Bells %lld-%lld, run time %.3f s)\n",secs/(double)(bell-from),from,bell,secs);
  fprintf(f,"checksum %016llx\n",(unsigned long long)h);
  if(ferror(f)){ fprintf(stderr,"%s: write error (disk full?)\n",tmpn); fclose(f); remove(tmpn); return -1; }
  if(fclose(f)){ perror(tmpn); return -1; }
  if(rename(tmpn,name)){ perror(name); return -1; }
  return 0; }

// read a checkpoint into the k file K (streaming)
static int read_ckpt_kf(const char*name,long long*bell,kfile*K,int*s,long long*hor,int*dm,long long*dmb,long long*dms){
  FILE*f=fopen(name,"r"); if(!f) return -1;
  char line[4096]; long long b=-1,kb=-1; char S[256]=""; char lb[4100]="",ls[4100]="",lh[4100]="";
  unsigned long long cs=0; int have_cs=0, have_k=0; u64 hk=0; *hor=0; *dm=INT_MAX; *dmb=-1; *dms=-1;
  for(;;){
    int c=getc_unlocked(f); if(c==EOF) break;
    size_t p=0; line[p++]=(char)c;
    while(p<6&&c!='\n'&&(c=getc_unlocked(f))!=EOF) line[p++]=(char)c;
    if(p==6&&!memcmp(line,"k_hex ",6)){
      if(kb<1){ fclose(f); return -1; }
      long long nd=(kb+3)/4, nl=(nd+15)/16;
      if(ftruncate(K->fd,0)) die("truncate k file");
      u64 h=fnv(FNV0,lb,strlen(lb)); h=fnv(h,ls,strlen(ls)); h=fnv(h,lh,strlen(lh)); h=fnv(h,"k_hex ",6);
      // limbs are produced from the top down; collect them in a buffer and write it at its place
      const long long CH=1<<16; u64*L=malloc(CH*8); long long top=nl-1, cnt=0; u64 cur=0;
      long long i=0; size_t bp=0;
      while((c=getc_unlocked(f))!=EOF&&c!='\n'&&c!='\r'){
        int v=(c>='0'&&c<='9')?c-'0':(c>='A'&&c<='F')?c-'A'+10:(c>='a'&&c<='f')?c-'a'+10:-1;
        if(v<0||i>=nd){ free(L); fclose(f); return -1; }
        long long dg=nd-1-i; cur|=(u64)v<<(4*(dg%16)); i++;
        if(dg%16==0){ L[CH-1-cnt]=cur; cnt++; cur=0;
          if(cnt==CH){ kf_pwrite(K,L,CH,top-CH+1); top-=CH; cnt=0; } }
        wbuf[bp++]=(char)c; if(bp==sizeof wbuf){ h=fnv(h,wbuf,bp); bp=0; } }
      if(cnt) kf_pwrite(K,L+CH-cnt,cnt,top-cnt+1);
      free(L);
      if(bp) h=fnv(h,wbuf,bp);
      h=fnv(h,"\n",1);
      if(c=='\r') c=getc_unlocked(f);
      if(i!=nd){ fclose(f); return -1; }
      K->nl=nl; hk=h; have_k=1; continue; }
    if(c!='\n'&&c!=EOF){ while((c=getc_unlocked(f))!=EOF&&c!='\n'){ if(p<sizeof line-2) line[p++]=(char)c; } }
    line[p<sizeof line-1?p:sizeof line-1]=0;
    if(p&&line[p-1]!='\n'){ line[p]='\n'; line[p+1]=0; }
    if(!strncmp(line,"bell ",5)){ b=atoll(line+5); snprintf(lb,sizeof lb,"%s",line); }
    else if(!strncmp(line,"S ",2)){ sscanf(line+2,"%255s",S); snprintf(ls,sizeof ls,"%s",line); }
    else if(!strncmp(line,"horizon ",8)){ *hor=atoll(line+8); snprintf(lh,sizeof lh,"%s",line); }
    else if(!strncmp(line,"k_bits ",7)) kb=atoll(line+7);
    else if(!strncmp(line,"dmin ",5)){ if(sscanf(line+5,"%d at_bell %lld since_bell %lld",dm,dmb,dms)<1) *dm=INT_MAX; }
    else if(!strncmp(line,"checksum ",9)){ cs=strtoull(line+9,NULL,16); have_cs=1; }
  }
  fclose(f);
  if(b<0||!S[0]||!have_k||!have_cs||S[0]!='1') return -1;
  if(hk!=cs){ fprintf(stderr,"%s: checksum does not match\n",name); return -1; }
  int si=-1; for(int i=0;i<n;i++) if(!strcmp(names[i],S+1)) si=i;
  if(si<0){ fprintf(stderr,"%s: word S = %s is not in the table\n",name,S); return -1; }
  kf_setlen(K,K->nl);
  if(kf_bits(K)!=kb){ fprintf(stderr,"%s: k_bits does not match\n",name); return -1; }
  *bell=b; *s=si; return 0; }

static int cmp_desc(const void*a,const void*b){ long long x=*(const long long*)a,y=*(const long long*)b; return x<y?1:x>y?-1:0; }

static void log_progress_kf(long long bell,kfile*K,int s,double t,const char*what){
  u64 k0=kf_limb(K,0), k1=kf_limb(K,1);
  u64 nlow=(k0>>1)|(k1<<63); const char*sp=names[s]; char P[128]; int L=(int)strlen(sp)-1;
  for(int i=0;i<L;i++) P[i]=sp[L-i];
  P[L]=0;
  char dinfo[128]; if(dmin<INT_MAX) snprintf(dinfo,sizeof dinfo,"  d %d D %d (Bell %lld)",dist[s],dmin,dminbell); else snprintf(dinfo,sizeof dinfo,"  d %d",dist[s]);
  char pinfo[64]=""; if(horizon>0) snprintf(pinfo,sizeof pinfo,"  pruned to %lld",horizon);
  char line[512]; time_t now_t=time(NULL); char ts[32]; strftime(ts,sizeof ts,"%Y-%m-%d %H:%M:%S",localtime(&now_t));
  long long bl=kf_bits(K);
  snprintf(line,sizeof line,"%s  %s  bell %lld  time %.0fs  KCHECK %llu %lld %s  TM2: n mod 2^64 = %llu, bits %lld, P = %s%s%s\n",
           ts,what,bell,t,(unsigned long long)k0,bl,names[s],(unsigned long long)nlow,bl-1,L?P:"e",dinfo,pinfo);
  fputs(line,stdout); fflush(stdout);
  FILE*f=fopen("progress.log","a"); if(f){ fputs(line,f); fclose(f); } }

/* ---------- one block of nb Bells with k on disk ----------
   k = q*2^w + r (w = nb+2).  New k = q*3^nb*4 + r_nb.  The product is streamed: q is read from the k file in
   chunks of C limbs, each chunk is multiplied by P = 3^nb in RAM and the result is written in order to the new
   file (the upper vn limbs of each chunk product are carried into the next one).  Meanwhile the main thread
   advances r in RAM.  With pruning only the limbs below 2^keep are produced (keep = (horizon - Bell) + 128). */
typedef struct { kfile*src; kfile*dst; long long ws; int wt; mpz_srcptr P; long long limZ; long long C; int qcut; double t; } sjob;
static void* stream_product(void*a){
  sjob*J=a; double t0=now();
  kfile*src=J->src,*dst=J->dst; long long ws=J->ws; int wt=J->wt;
  long long qn=src->nl-ws; if(qn<1) qn=1;                   // limbs of q (the top one may be 0)
  long long vn=(long long)mpz_size(J->P); const u64*PW=(const u64*)mpz_limbs_read(J->P);
  long long C=J->C;
  long long limY=J->limZ;                                     // Y limbs needed: Z_j uses Y_j and Y_{j-1}
  long long qlim=qn; if(limY<qlim) qlim=limY;                // q limbs that matter
  u64*in=malloc((C+1)*8), *A=malloc(C*8), *T=malloc((C+vn+1)*8), *carry=calloc(vn+1,8);
  const long long OB=1<<17; u64*ob=malloc(OB*8); long long obn=0, zpos=0; u64 prev=0;  // Z = Y<<2, prev = last Y limb
  if(!in||!A||!T||!carry||!ob){ fprintf(stderr,"out of memory in the streamed product\n"); exit(1); }
  if(ftruncate(dst->fd,0)) die("truncate k file");
#define EMITY(y) do{ u64 _y=(y); if(zpos<J->limZ){ ob[obn++]=(_y<<2)|(prev>>62); zpos++; if(obn==OB){ kf_pwrite(dst,ob,obn,zpos-obn); obn=0; } } prev=_y; }while(0)
  long long yout=0;                                           // Y limbs emitted
  for(long long off=0; off<qlim && yout<limY; off+=C){
    long long len=qlim-off<C?qlim-off:C;
    // q limbs off..off+len-1 = bits of src from limb ws+off with shift wt
    kf_pread(src,in,len+1,ws+off);
    if(ws+off+len+1>src->nl){ long long valid=src->nl-(ws+off); if(valid<0) valid=0; for(long long i=valid;i<len+1;i++) in[i]=0; }
    for(long long i=0;i<len;i++) A[i]= wt? (in[i]>>wt)|(in[i+1]<<(64-wt)) : in[i];
    long long an=len; while(an>0&&A[an-1]==0) an--;
    long long tn;
    if(an==0){ memset(T,0,(len+vn)*8); tn=len+vn; }
    else { if(an>=vn) flint_mpn_mul(T,A,an,PW,vn); else flint_mpn_mul(T,PW,vn,A,an);
      tn=an+vn; for(long long i=tn;i<len+vn;i++) T[i]=0; tn=len+vn; }
    // add the carry (vn limbs) into T
    u64 cy=0; for(long long i=0;i<vn;i++){ unsigned __int128 sum=(unsigned __int128)T[i]+carry[i]+cy; T[i]=(u64)sum; cy=(u64)(sum>>64); }
    for(long long i=vn;cy&&i<tn;i++){ T[i]+=cy; cy=(T[i]==0); }
    for(long long i=0;i<len&&yout<limY;i++,yout++) EMITY(T[i]);
    memcpy(carry,T+len,vn*8); }
  // the rest: the carry limbs (only needed without cut, or up to limY)
  for(long long i=0;i<vn&&yout<limY;i++,yout++) EMITY(carry[i]);
  if(yout<limY) EMITY(0);                                     // the top two bits of the last Y limb
  if(obn) kf_pwrite(dst,ob,obn,zpos-obn);
  dst->nl=zpos; if(dst->nl<1){ u64 z=0; kf_pwrite(dst,&z,1,0); dst->nl=1; }
  kf_setlen(dst,dst->nl);
#undef EMITY
  free(in); free(A); free(T); free(carry); free(ob);
  flint_cleanup(); J->t=now()-t0; return NULL; }

// add x (in RAM) to the k file
static void kf_add_mpz(kfile*f,const mpz_t x){
  long long xn=(long long)mpz_size(x); if(xn==0) return;
  const u64*X=(const u64*)mpz_limbs_read(x);
  long long n=xn; u64*B=malloc((n+1)*8); kf_pread(f,B,n,0); if(f->nl<n){ for(long long i=f->nl;i<n;i++) B[i]=0; }
  u64 cy=0; for(long long i=0;i<n;i++){ unsigned __int128 s=(unsigned __int128)B[i]+X[i]+cy; B[i]=(u64)s; cy=(u64)(s>>64); }
  kf_pwrite(f,B,n,0); free(B);
  long long i=n; while(cy){ u64 v=kf_limb(f,i); v+=1; cy=(v==0); kf_pwrite(f,&v,1,i); i++; }
  long long nl=f->nl>i?f->nl:i; if(nl<n) nl=n; kf_setlen(f,nl); }

int main(int argc,char**argv){
  int init=argc>1&&!strcmp(argv[1],"init");
  long long target=LLONG_MAX, interval=1000000000LL, B=0; int prune=0; int jset=0;
  ncpu=(int)sysconf(_SC_NPROCESSORS_ONLN); if(ncpu<1) ncpu=1;
  mallopt(M_MMAP_THRESHOLD,1<<20); mallopt(M_TRIM_THRESHOLD,1<<20); mallopt(M_ARENA_MAX,2);
  if(!init){
    for(int i=1;i<argc;i++){
      if(!strcmp(argv[i],"-t")&&i+1<argc) target=atoll(argv[++i]);
      else if(!strcmp(argv[i],"-i")&&i+1<argc) interval=atoll(argv[++i]);
      else if(!strcmp(argv[i],"-b")&&i+1<argc) B=atoll(argv[++i]);
      else if(!strcmp(argv[i],"-p")) prune=1;
      else if(!strcmp(argv[i],"-M")&&i+1<argc){ double g=atof(argv[++i]); if(g<0.25){ fprintf(stderr,"-M needs at least 0.25 (GB)\n"); return 2; } memlimit=(long long)(g*(1<<30)); }
      else if(!strcmp(argv[i],"-w")&&i+1<argc) snprintf(wdir,sizeof wdir,"%s",argv[++i]);
      else if(!strcmp(argv[i],"-j")&&i+1<argc){ i++; if(!strncmp(argv[i],"auto",4)){ jauto=1; if(argv[i][4]==':') jmax=atoi(argv[i]+5); } else { jset=atoi(argv[i]); if(jset<1){ fprintf(stderr,"-j needs a number >= 1 or auto\n"); return 2; } } }
      else { fprintf(stderr,"usage: %s [-t TARGET [-p]] [-i INTERVAL] [-M GB] [-w DIR] [-j N|auto[:MAX]] [-b B]   or   %s init BELL K S\n",argv[0],argv[0]); return 2; } } }
  if(jauto){ jcur=0; set_threads(1); jcur=1; jlast=-1e9; } else { int j=jset?jset:ncpu; flint_set_num_threads(j); jcur=j; }
  if(target<=0||interval<=0||B<0){ fprintf(stderr,"TARGET, INTERVAL and B must be positive\n"); return 2; }
  if(prune&&target==LLONG_MAX){ fprintf(stderr,"-p needs a target (-t TARGET)\n"); return 2; }
  if(prune) horizon=target;
  { FILE*f=fopen("orbit.txt","r"); if(f){ if(fscanf(f,"%63s",orbit)!=1) strcpy(orbit,"?"); fclose(f);} }
  FILE*f=fopen("tab.txt","r"); if(!f||fscanf(f,"%d",&n)!=1){ fprintf(stderr,"cannot read tab.txt\n"); return 1; }
  nxt=malloc(sizeof(int)*2*n); cc=malloc(sizeof(int)*2*n);
  for(int i=0;i<n;i++){ int a,b,c,d; if(fscanf(f,"%d %d %d %d",&a,&b,&c,&d)!=4) return 1; nxt[2*i]=a;cc[2*i]=b;nxt[2*i+1]=c;cc[2*i+1]=d; } fclose(f);
  names=malloc(sizeof(char*)*n); f=fopen("tab_names.txt","r"); if(!f){ fprintf(stderr,"cannot read tab_names.txt\n"); return 1; }
  for(int i=0;i<n;i++){ names[i]=malloc(64); if(fscanf(f,"%63s",names[i])!=1) return 1; } fclose(f);
  dist=malloc(sizeof(int)*n); for(int i=0;i<n;i++) dist[i]=INT_MAX/2;
  for(int ch=1;ch;){ ch=0; for(int i=0;i<n;i++) for(int b=0;b<2;b++){ int t=nxt[2*i+b];
      int v=(t==-1)?1:(t>=0&&dist[t]<INT_MAX/2?dist[t]+1:INT_MAX/2); if(v<dist[i]){ dist[i]=v; ch=1; } } }
  p3[0]=1; for(int i=1;i<=LEAF;i++) p3[i]=p3[i-1]*3;
  for(int d=0;d<80;d++){ mpz_init(R[d]); for(int i=0;i<2;i++){ P3[d][i].h=-1; mpz_init(P3[d][i].v); } }
  mpz_t r,pw; mpz_inits(r,pw,NULL); long long pwB=-1;
  kfile KA,KB; kfile*K=&KA,*K2=&KB;
  kf_open(&KA,"belldco_k_a.bin",1); kf_open(&KB,"belldco_k_b.bin",1);

  if(init){
    if(argc!=5){ fprintf(stderr,"usage: %s init BELL K S\n",argv[0]); return 2; }
    int si=-1; if(argv[4][0]=='1') for(int i=0;i<n;i++) if(!strcmp(names[i],argv[4]+1)) si=i;
    if(si<0){ fprintf(stderr,"word %s not in tab_names.txt\n",argv[4]); return 1; }
    mpz_set_str(r,argv[3],10); if(mpz_sgn(r)<=0){ fprintf(stderr,"K must be positive\n"); return 1; }
    kf_from_mpz(K,r);
    if(write_ckpt_kf(atoll(argv[2]),K,si,-1,0)) return 1;
    log_progress_kf(atoll(argv[2]),K,si,0,"init   "); remove(KA.path); remove(KB.path); return 0; }

  // start checkpoint: highest Bell number that can be read and fits the run
  static long long cand[100000]; int nc=0;
  DIR*dir=opendir("checkpoints"); if(!dir){ fprintf(stderr,"no directory checkpoints/\n"); return 1; }
  struct dirent*e; while((e=readdir(dir))&&nc<100000){ long long b; char rest[16];
    if(sscanf(e->d_name,"bell_%lld_chkpt.tx%15s",&b,rest)==2&&!strcmp(rest,"t")) cand[nc++]=2*b;
    else if(sscanf(e->d_name,"bell_%lld_pchkpt.tx%15s",&b,rest)==2&&!strcmp(rest,"t")) cand[nc++]=2*b+1; }
  closedir(dir); qsort(cand,nc,sizeof(long long),cmp_desc);
  long long bell=-1; int s=0; char startname[256]="";
  for(int i=0;i<nc;i++){ char nm[256]; long long cb=cand[i]>>1; int cp=(int)(cand[i]&1); ckpt_name_h(nm,sizeof nm,cb,cp);
    long long hor; int dm; long long dmb,dms;
    if(read_ckpt_kf(nm,&bell,K,&s,&hor,&dm,&dmb,&dms)==0&&bell==cb){
      if(hor>0&&kf_bits(K)+64<(hor-bell)+PMARGIN){
        printf("note: %s is exact (written before pruning cut any bits), used as a full checkpoint\n",nm); hor=0; }
      if(hor>0&&!(prune&&target<=hor)){
        fprintf(stderr,"skipping %s: pruned towards Bell %lld, usable only with -p and -t <= %lld\n",nm,hor,hor); bell=-1; continue; }
      strcpy(startname,nm); if(hor>0) cut=1;
      if(dm<INT_MAX){ dmin=dm; dminbell=dmb; dsince=dms; } else dsince=bell;
      break; }
    fprintf(stderr,"skipping unreadable checkpoint %s\n",nm); bell=-1; }
  if(bell<0){ fprintf(stderr,"no readable checkpoint in checkpoints/\n"); return 1; }
  long long nbmax=memlimit/6;                                 // Bells per block from the memory budget (measured: about 5 bytes per Bell of a block)
  char bdesc[96]; if(B) snprintf(bdesc,sizeof bdesc,"%lld",B); else snprintf(bdesc,sizeof bdesc,"automatic (bits of k / 8, at most %lld for -M %.2f GB)",nbmax,memlimit/(double)(1<<30));
  if(target==LLONG_MAX) printf("orbit %s: start %s (Bell %lld), no target (until HALT or interruption), checkpoint every %lld Bells, B = %s\n",orbit,startname,bell,interval,bdesc);
  else printf("orbit %s: start %s (Bell %lld), target Bell %lld, checkpoint every %lld Bells, B = %s\n",orbit,startname,bell,target,interval,bdesc);
  if(horizon>0) printf("horizon pruning towards Bell %lld: k is kept mod 2^((%lld - Bell) + %d)\n",horizon,horizon,PMARGIN);
  if(jauto) printf("threads: automatic (1 to %d, %d cores)\n",jmax>0?jmax:ncpu,ncpu); else printf("threads: %d (%d cores)\n",jcur,ncpu);
  printf("k on disk: %s/belldco_k_a.bin and _b.bin (now %.2f GB each at most)\n",wdir,kf_bits(K)/8.0/(1<<30));
  { int mx=0; for(int i=0;i<n;i++) if(dist[i]<INT_MAX/2&&dist[i]>mx) mx=dist[i];
    printf("distance to HALT: d(S) between 1 and %d over the %d words of the table\n",mx,n); }
  if(bell>=target){ printf("start Bell %lld is not below the target, nothing to do\n",bell); return 0; }
  if(horizon>0){ long long keep=(horizon-bell)+PMARGIN; if(keep<PMARGIN) keep=PMARGIN; if(kf_trunc_bits(K,keep)) cut=1; }
  double t0=now(), tlow=0, tmul=0, tio=0;
  long long nextck=(bell/interval+1)*interval; char prevname[256]=""; int prevcut=0;
  long long lastck_bell=bell, prevck_bell=bell; double lastck_time=now(), prevck_time=0;
  log_progress_kf(bell,K,s,0,"start  ");
  while(bell<target){
    update_threads();
    long long bits=kf_bits(K);
    long long nb=B?B:bits/8; if(!B&&nb>nbmax) nb=nbmax; if(!B&&nb<(1LL<<20)) nb=1LL<<20;
    if(target-bell<nb) nb=target-bell;
    if(nextck-bell<nb) nb=nextck-bell;
    long long w=nb+2, ws=w/64; int wt=(int)(w%64);
    double ta=now();
    kf_low_mpz(K,r,ws+1); mpz_fdiv_r_2exp(r,r,(mp_bitcnt_t)w);
    long long keep=LLONG_MAX/4, limZ=LLONG_MAX/4; int qcut=0;
    if(horizon>0){ keep=(horizon-(bell+nb))+PMARGIN; if(keep<PMARGIN) keep=PMARGIN;
      long long keepq=keep-2; if(keepq<1) keepq=1;
      if(bits-w>keepq){ qcut=1; cut=1; limZ=(keep+63)/64; } }
    if(pwB!=nb){ mpz_ui_pow_ui(pw,3,(unsigned long)nb); pwB=nb; }
    long long vn=(long long)mpz_size(pw); long long C=vn<(1<<14)?(1<<14):vn;
    // the streamed product q*3^nb*4 (disk -> disk) runs in its own thread while the low part is advanced
    sjob J={K,K2,ws,wt,pw,limZ,C,qcut,0}; pthread_t th;
    __sync_add_and_fetch(&ntask,1);
    if(pthread_create(&th,NULL,stream_product,&J)){ fprintf(stderr,"cannot start a thread\n"); return 1; }
    gbell=bell; adv(r,&s,nb,0);
    double tb=now(); tlow+=tb-ta;
    pthread_join(th,NULL); __sync_sub_and_fetch(&ntask,1);
    tmul+=J.t;
    if(halted){
      char msg[256]; snprintf(msg,sizeof msg,"%s at Bell %lld: S_pascal = %s\n",halted==-1?"HALT":"UNKNOWN STATE (word not in the table)",haltbell,names[haltS]);
      fputs(msg,stdout); char hn[256]; snprintf(hn,sizeof hn,"checkpoints/%s_bell_%lld.txt",halted==-1?"HALT":"UNKNOWN",haltbell);
      FILE*h=fopen(hn,"w"); if(h){ fprintf(h,"orbit %s\n%s",orbit,msg); fclose(h); }
      FILE*g=fopen("progress.log","a"); if(g){ fprintf(g,"%s",msg); fclose(g); }
      remove(KA.path); remove(KB.path); return 0; }
    for(int dd=0;dd<80;dd++){ mpz_realloc2(R[dd],64); for(int ii=0;ii<2;ii++) if(P3[dd][ii].h>LEAF*64){ P3[dd][ii].h=-1; mpz_realloc2(P3[dd][ii].v,64); } }
    double tc=now();
    kf_add_mpz(K2,r); mpz_realloc2(r,64);
    if(horizon>0&&kf_trunc_bits(K2,keep)) cut=1;
    { kfile*t=K; K=K2; K2=t; }
    if(ftruncate(K2->fd,0)) die("truncate k file"); K2->nl=0;
    flint_cleanup();
    tio+=now()-tc;
    bell+=nb;
    if(bell==nextck||bell==target){
      double span=now()-lastck_time; long long from=lastck_bell; double secs=span;
      if(bell-lastck_bell<interval/2&&prevck_bell<lastck_bell){ from=prevck_bell; secs=prevck_time+span; }
      if(write_ckpt_kf(bell,K,s,from,secs)) return 1;
      prevck_bell=lastck_bell; prevck_time=span; lastck_bell=bell; lastck_time=now();
      if(prevname[0]&&!(prevcut==0&&cut==1)) remove(prevname);
      if(prevname[0]&&prevcut==0&&cut==1) printf("keeping %s (last exact checkpoint before pruning)\n",prevname);
      if(bell<target){ ckpt_name_h(prevname,sizeof prevname,bell,cut); prevcut=cut; } else prevname[0]=0;
      log_progress_kf(bell,K,s,now()-t0,bell==target?"target ":"ckpt   ");
      if(bell==nextck) nextck+=interval; }
  }
  printf("no halt up to Bell %lld; time %.1fs (low part %.1fs, streamed products %.1fs in parallel, final add %.1fs)\n",bell,now()-t0,tlow,tmul,tio);
  remove(KA.path); remove(KB.path);
  return 0; }
