// belldcf.c - belldc with FLINT multiplication on several cores: exact Bell orbit with divide and conquer,
// checkpoints, horizon pruning, distance to HALT.  Same orbit, same checkpoints and log lines as belldc.c.
// The big products use FLINT's fft_small multiplication (flint_mpn_mul), which runs on up to 8 threads.
//
// The orbit is computed in TM1 coordinates: a Bell starts at 0^inf 1^k F> S 0^inf, the next Bell has
//   k' = 3*floor(k/2) + c,   (S', c) = f(S, bit 1 of k)      (table in tab.txt / tab_names.txt).
// Bell numbers, checkpoint names and the progress log use the Bell numbering of TM2 (see README.md).
//
// Compile: gcc -O3 -march=native -o belldcf belldcf.c -lflint -lmpfr -lgmp -lpthread -lm   (sudo apt install libflint-dev)
// Usage:   ./belldcf [-t TARGET [-p]] [-i INTERVAL] [-b B] [-m] [-j N | -j auto[:MAX]]
//   -t TARGET    Bell number at which the run stops (a checkpoint is written there);
//                without -t the run goes on until HALT or until it is interrupted (Ctrl-C)
//   -p           horizon pruning towards TARGET: k is kept mod 2^((TARGET - Bell) + 128)
//   -i INTERVAL  write a checkpoint at every Bell number divisible by INTERVAL (default 1000000000);
//                the previous intermediate checkpoint is deleted, the start and target checkpoints are kept,
//                and with -p also the last exact checkpoint before pruning starts (Bell about TARGET/1.585)
//   -b B         fixed block size in Bells; default: B = (bits of k)/8, at least 2^20
//   -m           memory saving: B = (bits of k)/32 and smaller pieces in the big product (a little slower)
//   -j N         use N threads for the big multiplications (default: all cores; FLINT uses at most 8 per product)
//   -j auto      adapt the number of threads to the load of the computer: before each block of Bells (and at
//                most once a minute) it uses the cores that the other programs leave free (from the 1-minute
//                load average), at least 1; -j auto:MAX limits this to MAX threads
//          ./belldc init BELL K S             write a first checkpoint (K < 2^64, S = the word with its leading 1)
// Checkpoints are the same files as for bellntt / bellnttp (bell_<N>_chkpt.txt, pruned: bell_<N>_pchkpt.txt
// with a line "horizon T"), so the programs can continue each other's runs.  With -p, checkpoints are written
// as normal (exact) chkpt files until pruning really cuts bits of k, i.e. up to about Bell TARGET/1.585;
// older pchkpt files from that phase are recognised as exact when read and can be continued beyond TARGET.
//
// Method. Write k = q*2^(B+2) + r with r < 2^(B+2). The first B Bells depend only on r (each Bell reads
// bit 1 and shifts by one bit), and after them k = q*3^B*4 + r_B, where r_B is r after B Bells.
//   * top level: one big product q*3^B per block of B Bells (GMP multiplication);
//   * r_B is computed recursively in the same way: B Bells = B/2 Bells on the low B/2+2 bits, one product,
//     then B/2 Bells on the result (divide and conquer, cost about M(B)*log B instead of B^2);
//   * at the bottom, blocks of at most 32 Bells are simulated on a 64-bit word.
// Horizon pruning: k' mod 2^j depends only on k mod 2^(j+1), so k mod 2^((T - Bell) + margin) is enough to
// follow the orbit (states S and KCHECK = k mod 2^64) up to Bell T.
// D = distance to HALT: d(S) = smallest number of Bells from S to a HALT entry of the table; D = smallest d
// reached so far (stored in the checkpoints).
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
#define PROGLABEL "belldcf-1 (bb6 vampire family)"

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

static int write_ckpt(long long bell,const mpz_t k,int s,long long from,double secs){
  char name[256],tmpn[300]; ckpt_name_h(name,sizeof name,bell,cut); snprintf(tmpn,sizeof tmpn,"%s.tmp",name);
  long long bits=bitlen(k); size_t nd=(size_t)(bits+3)/4; if(nd==0) nd=1;
  char lb[64],ls[128],lh[64]=""; snprintf(lb,sizeof lb,"bell %lld\n",bell); snprintf(ls,sizeof ls,"S 1%s\n",names[s]);
  if(cut) snprintf(lh,sizeof lh,"horizon %lld\n",horizon);
  u64 h=fnv(FNV0,lb,strlen(lb)); h=fnv(h,ls,strlen(ls)); h=fnv(h,lh,strlen(lh)); h=fnv(h,"k_hex ",6);
  time_t now_t=time(NULL); char d[16],t[16]; strftime(d,sizeof d,"%Y-%m-%d",localtime(&now_t)); strftime(t,sizeof t,"%H:%M:%S",localtime(&now_t));
  FILE*f=fopen(tmpn,"w"); if(!f){ perror(tmpn); return -1; }
  fprintf(f,"# bellntt checkpoint\ndate %s\ntime %s\nprogram %s\norbit %s\n%s%s%sk_bits %lld\nk_hex ",d,t,PROGLABEL,orbit,lb,ls,lh,bits);
  const mp_limb_t*L=mpz_limbs_read(k); size_t nl=mpz_size(k);
  static char buf[1<<20]; size_t bp=0;
  for(size_t i=0;i<nd;i++){ size_t dg=nd-1-i; size_t li=dg/16; u64 limb=li<nl?(u64)L[li]:0;
    buf[bp++]=HX[(limb>>(4*(dg%16)))&15];
    if(bp==sizeof buf){ h=fnv(h,buf,bp); fwrite(buf,1,bp,f); bp=0; } }
  if(bp){ h=fnv(h,buf,bp); fwrite(buf,1,bp,f); }
  h=fnv(h,"\n",1); fputc('\n',f);
  if(dmin<INT_MAX) fprintf(f,"dmin %d at_bell %lld since_bell %lld\n",dmin,dminbell,dsince);
  if(from>=0&&bell>from) fprintf(f,"time_per_bell %.3e s (average over Bells %lld-%lld, run time %.3f s)\n",secs/(double)(bell-from),from,bell,secs);
  fprintf(f,"checksum %016llx\n",(unsigned long long)h);
  if(ferror(f)){ fprintf(stderr,"%s: write error (disk full?)\n",tmpn); fclose(f); remove(tmpn); return -1; }
  if(fclose(f)){ perror(tmpn); remove(tmpn); return -1; }
  if(rename(tmpn,name)){ perror(name); return -1; }
  return 0; }

// read a checkpoint (streaming: the k_hex line can have billions of digits)
static int read_ckpt(const char*name,long long*bell,mpz_t k,int*s,long long*hor,int*dm,long long*dmb,long long*dms){
  FILE*f=fopen(name,"r"); if(!f) return -1;
  char line[4096]; long long b=-1,kb=-1; char S[256]=""; char lb[4100]="",ls[4100]="",lh[4100]="";
  unsigned long long cs=0; int have_cs=0, have_k=0; u64 hk=0; *hor=0; *dm=INT_MAX; *dmb=-1; *dms=-1;
  for(;;){
    int c=getc_unlocked(f); if(c==EOF) break;
    size_t p=0; line[p++]=(char)c;
    while(p<6&&c!='\n'&&(c=getc_unlocked(f))!=EOF) line[p++]=(char)c;
    if(p==6&&!memcmp(line,"k_hex ",6)){
      if(kb<1){ fclose(f); return -1; }
      size_t nd=(size_t)(kb+3)/4, nl=(nd+15)/16;
      mp_limb_t*L=mpz_limbs_write(k,(mp_size_t)nl); memset(L,0,nl*sizeof(mp_limb_t));
      u64 h=fnv(FNV0,lb,strlen(lb)); h=fnv(h,ls,strlen(ls)); h=fnv(h,lh,strlen(lh)); h=fnv(h,"k_hex ",6);
      size_t i=0; static char buf[1<<16]; size_t bp=0;
      while((c=getc_unlocked(f))!=EOF&&c!='\n'&&c!='\r'){
        int v=(c>='0'&&c<='9')?c-'0':(c>='A'&&c<='F')?c-'A'+10:(c>='a'&&c<='f')?c-'a'+10:-1;
        if(v<0||i>=nd){ fclose(f); return -1; }
        size_t dg=nd-1-i; L[dg/16]|=(mp_limb_t)v<<(4*(dg%16)); i++;
        buf[bp++]=(char)c; if(bp==sizeof buf){ h=fnv(h,buf,bp); bp=0; } }
      if(bp) h=fnv(h,buf,bp);
      h=fnv(h,"\n",1);
      if(c=='\r') c=getc_unlocked(f);
      if(i!=nd){ fclose(f); return -1; }
      mpz_limbs_finish(k,(mp_size_t)nl); hk=h; have_k=1; continue; }
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
  if(bitlen(k)!=kb){ fprintf(stderr,"%s: k_bits does not match\n",name); return -1; }
  *bell=b; *s=si; return 0; }

static int cmp_desc(const void*a,const void*b){ long long x=*(const long long*)a,y=*(const long long*)b; return x<y?1:x>y?-1:0; }

static void log_progress(long long bell,const mpz_t k,int s,double t,const char*what){
  u64 k0=mpz_getlimbn(k,0), k1=mpz_getlimbn(k,1);
  u64 nlow=(k0>>1)|(k1<<63); const char*sp=names[s]; char P[128]; int L=(int)strlen(sp)-1;
  for(int i=0;i<L;i++) P[i]=sp[L-i];
  P[L]=0;
  char dinfo[128]; if(dmin<INT_MAX) snprintf(dinfo,sizeof dinfo,"  d %d D %d (Bell %lld)",dist[s],dmin,dminbell); else snprintf(dinfo,sizeof dinfo,"  d %d",dist[s]);
  char pinfo[64]=""; if(horizon>0) snprintf(pinfo,sizeof pinfo,"  pruned to %lld",horizon);
  char line[512]; time_t now_t=time(NULL); char ts[32]; strftime(ts,sizeof ts,"%Y-%m-%d %H:%M:%S",localtime(&now_t));
  long long bl=bitlen(k);
  snprintf(line,sizeof line,"%s  %s  bell %lld  time %.0fs  KCHECK %llu %lld %s  TM2: n mod 2^64 = %llu, bits %lld, P = %s%s%s\n",
           ts,what,bell,t,(unsigned long long)k0,bl,names[s],(unsigned long long)nlow,bl-1,L?P:"e",dinfo,pinfo);
  fputs(line,stdout); fflush(stdout);
  FILE*f=fopen("progress.log","a"); if(f){ fputs(line,f); fclose(f); } }

// q = q * pw in place, in chunks of q from the top down (memory: q + product + one chunk product,
// instead of q + product + the work space of one huge multiplication)
static void mul_inplace(mpz_t q,const mpz_t pw){
  size_t qn=mpz_size(q), vn=mpz_size(pw);
  if(qn==0) return;
  if(qn<=2*vn){ fmul(q,q,pw); return; }
  size_t rn=qn+vn+1, c=(bdiv>8)?vn/2:vn; if(c<1) c=1;
  mp_limb_t*Q=mpz_limbs_modify(q,(mp_size_t)rn); memset(Q+qn,0,(rn-qn)*sizeof(mp_limb_t));
  const mp_limb_t*PW=mpz_limbs_read(pw);
  mp_limb_t*T=malloc((c+vn+1)*sizeof(mp_limb_t)), *CB=malloc(c*sizeof(mp_limb_t));
  if(!T||!CB){ fprintf(stderr,"out of memory in the product\n"); exit(1); }
  size_t nch=(qn+c-1)/c;
  for(size_t i=nch;i-->0;){
    size_t off=i*c, len=qn-off<c?qn-off:c;
    memcpy(CB,Q+off,len*sizeof(mp_limb_t)); memset(Q+off,0,len*sizeof(mp_limb_t));
    size_t len2=len; while(len2>0&&CB[len2-1]==0) len2--;
    if(len2==0) continue;
    if(vn>=len2) flint_mpn_mul(T,PW,(mp_size_t)vn,CB,(mp_size_t)len2); else flint_mpn_mul(T,CB,(mp_size_t)len2,PW,(mp_size_t)vn);
    size_t tn=vn+len2;
    mp_limb_t cy=mpn_add_n(Q+off,Q+off,T,(mp_size_t)tn);
    for(size_t j=off+tn;cy&&j<rn;j++){ Q[j]+=1; cy=(Q[j]==0); } }
  free(T); free(CB);
  mpz_limbs_finish(q,(mp_size_t)rn); }

typedef struct { mpz_ptr q; mpz_srcptr pw; } tjob;
static void* qthread(void*a){ tjob*j=a; mul_inplace(j->q,j->pw); if(FTi){ mpz_clear(FT); FTi=0; } flint_cleanup(); return NULL; }

// horizon pruning: keep k mod 2^((horizon - bell) + PMARGIN)
static void prune_k(mpz_t k,long long bell){
  if(horizon<=0) return;
  long long keep=(horizon-bell)+PMARGIN; if(keep<PMARGIN) keep=PMARGIN;
  if(bitlen(k)>keep){ mpz_fdiv_r_2exp(k,k,(mp_bitcnt_t)keep); cut=1; } }

int main(int argc,char**argv){
  int init=argc>1&&!strcmp(argv[1],"init");
  long long target=LLONG_MAX, interval=1000000000LL, B=0; int prune=0; int jset=0;
  ncpu=(int)sysconf(_SC_NPROCESSORS_ONLN); if(ncpu<1) ncpu=1;
  // memory: return freed blocks to the system at once and limit per-thread heaps (less fragmentation)
  mallopt(M_MMAP_THRESHOLD,1<<20); mallopt(M_TRIM_THRESHOLD,1<<20); mallopt(M_ARENA_MAX,2);
  if(!init){
    for(int i=1;i<argc;i++){
      if(!strcmp(argv[i],"-t")&&i+1<argc) target=atoll(argv[++i]);
      else if(!strcmp(argv[i],"-i")&&i+1<argc) interval=atoll(argv[++i]);
      else if(!strcmp(argv[i],"-b")&&i+1<argc) B=atoll(argv[++i]);
      else if(!strcmp(argv[i],"-p")) prune=1;
      else if(!strcmp(argv[i],"-m")) bdiv=32;
      else if(!strcmp(argv[i],"-j")&&i+1<argc){ i++; if(!strncmp(argv[i],"auto",4)){ jauto=1; if(argv[i][4]==':') jmax=atoi(argv[i]+5); } else { jset=atoi(argv[i]); if(jset<1){ fprintf(stderr,"-j needs a number >= 1 or auto\n"); return 2; } } }
      else { fprintf(stderr,"usage: %s [-t TARGET [-p]] [-i INTERVAL] [-b B] [-m] [-j N|auto[:MAX]]   or   %s init BELL K S\n",argv[0],argv[0]); return 2; } } }
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
  mpz_t k,q,r,pw; mpz_inits(k,q,r,pw,NULL); long long pwB=-1;

  if(init){
    if(argc!=5){ fprintf(stderr,"usage: %s init BELL K S\n",argv[0]); return 2; }
    int si=-1; if(argv[4][0]=='1') for(int i=0;i<n;i++) if(!strcmp(names[i],argv[4]+1)) si=i;
    if(si<0){ fprintf(stderr,"word %s not in tab_names.txt\n",argv[4]); return 1; }
    mpz_set_str(k,argv[3],10); if(mpz_sgn(k)<=0){ fprintf(stderr,"K must be positive\n"); return 1; }
    if(write_ckpt(atoll(argv[2]),k,si,-1,0)) return 1;
    log_progress(atoll(argv[2]),k,si,0,"init   "); return 0; }

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
    if(read_ckpt(nm,&bell,k,&s,&hor,&dm,&dmb,&dms)==0&&bell==cb){
      // A "pruned" checkpoint written before pruning actually started is exact: there k is far below
      // 2^((horizon - Bell) + 128) (a cut k would have about that many bits).  Use it as a full checkpoint.
      if(hor>0&&bitlen(k)+64<(hor-bell)+PMARGIN){
        printf("note: %s is exact (written before pruning cut any bits), used as a full checkpoint\n",nm); hor=0; }
      if(hor>0&&!(prune&&target<=hor)){
        fprintf(stderr,"skipping %s: pruned towards Bell %lld, usable only with -p and -t <= %lld\n",nm,hor,hor); bell=-1; continue; }
      strcpy(startname,nm); if(hor>0) cut=1;
      if(dm<INT_MAX){ dmin=dm; dminbell=dmb; dsince=dms; } else dsince=bell;
      break; }
    fprintf(stderr,"skipping unreadable checkpoint %s\n",nm); bell=-1; }
  if(bell<0){ fprintf(stderr,"no readable checkpoint in checkpoints/\n"); return 1; }
  char bdesc[64]; if(B) snprintf(bdesc,sizeof bdesc,"%lld",B); else snprintf(bdesc,sizeof bdesc,"automatic (bits of k / %d, at least 2^20)",bdiv);
  if(target==LLONG_MAX) printf("orbit %s: start %s (Bell %lld), no target (until HALT or interruption), checkpoint every %lld Bells, B = %s\n",orbit,startname,bell,interval,bdesc);
  else printf("orbit %s: start %s (Bell %lld), target Bell %lld, checkpoint every %lld Bells, B = %s\n",orbit,startname,bell,target,interval,bdesc);
  if(horizon>0) printf("horizon pruning towards Bell %lld: k is kept mod 2^((%lld - Bell) + %d)\n",horizon,horizon,PMARGIN);
  if(jauto) printf("threads: automatic (1 to %d, %d cores)\n",jmax>0?jmax:ncpu,ncpu); else printf("threads: %d (%d cores)\n",jcur,ncpu);
  { int mx=0; for(int i=0;i<n;i++) if(dist[i]<INT_MAX/2&&dist[i]>mx) mx=dist[i];
    printf("distance to HALT: d(S) between 1 and %d over the %d words of the table\n",mx,n); }
  if(bell>=target){ printf("start Bell %lld is not below the target, nothing to do\n",bell); return 0; }
  prune_k(k,bell);
  double t0=now(), tlow=0, tmul=0;
  long long nextck=(bell/interval+1)*interval; char prevname[256]=""; int prevcut=0;
  long long lastck_bell=bell, prevck_bell=bell; double lastck_time=now(), prevck_time=0;
  log_progress(bell,k,s,0,"start  ");
  while(bell<target){
    update_threads();
    long long nb=B?B:bitlen(k)/bdiv; if(!B&&nb<(1LL<<20)) nb=1LL<<20;
    if(target-bell<nb) nb=target-bell;
    if(nextck-bell<nb) nb=nextck-bell;
    mp_bitcnt_t w=(mp_bitcnt_t)nb+2;
    double ta=now();
    mpz_fdiv_r_2exp(r,k,w); mpz_fdiv_q_2exp(q,k,w); mpz_realloc2(k,64);
    if(horizon>0){ long long keepq=(horizon-(bell+nb))+PMARGIN-2; if(keepq<1) keepq=1;
      if(bitlen(q)>keepq){ mpz_fdiv_r_2exp(q,q,(mp_bitcnt_t)keepq); cut=1; } }
    if(pwB!=nb){ mpz_ui_pow_ui(pw,3,(unsigned long)nb); pwB=nb; }
    // the big product q*3^nb runs in its own thread while the low part is advanced
    pthread_t tq; tjob jq={q,pw}; int parq=0;
    if(jcur>1){
      if(__sync_add_and_fetch(&ntask,1)<=maxtask() && pthread_create(&tq,NULL,qthread,&jq)==0) parq=1;
      else __sync_sub_and_fetch(&ntask,1); }
    gbell=bell; adv(r,&s,nb,0);
    double tb=now(); tlow+=tb-ta;
    if(parq){ pthread_join(tq,NULL); __sync_sub_and_fetch(&ntask,1); }
    if(halted){
      char msg[256]; snprintf(msg,sizeof msg,"%s at Bell %lld: S_pascal = %s\n",halted==-1?"HALT":"UNKNOWN STATE (word not in the table)",haltbell,names[haltS]);
      fputs(msg,stdout); char hn[256]; snprintf(hn,sizeof hn,"checkpoints/%s_bell_%lld.txt",halted==-1?"HALT":"UNKNOWN",haltbell);
      FILE*h=fopen(hn,"w"); if(h){ fprintf(h,"orbit %s\n%s",orbit,msg); fclose(h); }
      FILE*g=fopen("progress.log","a"); if(g){ fprintf(g,"%s",msg); fclose(g); }
      return 0; }
    for(int dd=0;dd<80;dd++){ mpz_realloc2(R[dd],64); for(int ii=0;ii<2;ii++) if(P3[dd][ii].h>LEAF*64){ P3[dd][ii].h=-1; mpz_realloc2(P3[dd][ii].v,64); } }
    if(!parq) mul_inplace(q,pw);
    mpz_swap(k,q); mpz_realloc2(q,64); mpz_mul_2exp(k,k,2); mpz_add(k,k,r);
    if(bdiv>8) flint_cleanup();   // -m: free FLINT's thread-local FFT buffers after each block
    bell+=nb; prune_k(k,bell);
    tmul+=now()-tb;
    if(bell==nextck||bell==target){
      double span=now()-lastck_time; long long from=lastck_bell; double secs=span;
      if(bell-lastck_bell<interval/2&&prevck_bell<lastck_bell){ from=prevck_bell; secs=prevck_time+span; }
      log_progress(bell,k,s,now()-t0,bell==target?"target ":"ckpt   ");
      // the KCHECK line is logged first, so it is not lost if the checkpoint cannot be written (e.g. disk full)
      if(write_ckpt(bell,k,s,from,secs)){
        char msg[300]; snprintf(msg,sizeof msg,"checkpoint at Bell %lld could NOT be written (disk full?); the previous checkpoint is kept; continuing\n",bell);
        fputs(msg,stderr); FILE*g=fopen("progress.log","a"); if(g){ fputs(msg,g); fclose(g); }
        if(bell==target) return 1; }
      else {
        prevck_bell=lastck_bell; prevck_time=span; lastck_bell=bell; lastck_time=now();
        // the previous intermediate checkpoint is deleted, except the last exact one before pruning starts
        if(prevname[0]&&!(prevcut==0&&cut==1)) remove(prevname);
        if(prevname[0]&&prevcut==0&&cut==1) printf("keeping %s (last exact checkpoint before pruning)\n",prevname);
        if(bell<target){ ckpt_name_h(prevname,sizeof prevname,bell,cut); prevcut=cut; } else prevname[0]=0;
      }
      if(bell==nextck) nextck+=interval; }
  }
  printf("no halt up to Bell %lld; time %.1fs (low part %.1fs, products %.1fs)\n",bell,now()-t0,tlow,tmul);
  return 0; }
