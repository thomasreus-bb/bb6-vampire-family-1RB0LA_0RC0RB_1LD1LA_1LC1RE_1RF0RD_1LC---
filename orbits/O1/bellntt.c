// bellntt.c - exact Bell orbit with checkpoints (block method, own NTT multiplication, no GMP).
//
// The orbit is computed in TM1 coordinates: a Bell starts at 0^inf 1^k F> S 0^inf, the next Bell has
//   k' = 3*floor(k/2) + c,   (S', c) = f(S, bit 1 of k)      (table in tab.txt / tab_names.txt).
// Bell numbers, checkpoint names and the progress log use the Bell numbering of TM2 (see README.md).
//
// Compile: gcc -O3 -march=native -fopenmp -o bellntt bellntt.c      (without -fopenmp: one core)
// Usage:   ./bellntt TARGET [INTERVAL [B]]
//          ./bellntt init BELL K S            write a first checkpoint (K < 2^64, S = the word with its leading 1)
//   TARGET    Bell number at which the run stops (a checkpoint is written there)
//   INTERVAL  write a checkpoint at every Bell number divisible by INTERVAL (default 10000000);
//             the previous intermediate checkpoint is deleted, the start and target checkpoints are kept
//   B         block size in Bells (default 2000000; only the speed depends on it)
// The run starts from the checkpoint with the highest Bell number in checkpoints/ that can be read.
// Files: tab.txt, tab_names.txt, orbit.txt (label), checkpoints/bell_<N>_chkpt.txt, progress.log.
//
// Method: k_new = ((k >> (B+2)) * 3^B) << 2  +  R, where R follows from the lowest B+2 bits of k by B single
// steps (in sub-blocks of 40 Bells). Only the big product (k >> (B+2)) * 3^B is computed with the NTT
// (two primes, Chinese remainder theorem).
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <dirent.h>
#ifdef _OPENMP
#include <omp.h>
#endif
typedef unsigned __int128 u128; typedef uint64_t u64; typedef uint32_t u32;
#define M 40

static int n; static int *nxt,*cc; static long long *vis; static char **names;

/* ---------- Montgomery arithmetic for primes < 2^63 ---------- */
typedef struct { u64 p,pinv,r1,r2,w24; u64 *rt,*irt; u64 *fp; } Pr;
static Pr pr[2];
static inline u64 mm(u64 a,u64 b,const Pr*q){
  u128 t=(u128)a*b; u64 m=(u64)t*q->pinv; u64 u=(u64)((t+(u128)m*q->p)>>64); return u>=q->p?u-q->p:u; }
static u64 powmod(u64 a,u64 e,u64 p){ u64 r=1; a%=p; while(e){ if(e&1) r=(u64)((u128)r*a%p); a=(u64)((u128)a*a%p); e>>=1; } return r; }
static void pr_init(Pr*q,u64 p,u64 w24){
  q->p=p; q->w24=w24; u64 inv=p; for(int i=0;i<6;i++) inv*=2-p*inv; q->pinv=(u64)0-inv;
  q->r1=(u64)(((u128)1<<64)%p); q->r2=(u64)((u128)q->r1*q->r1%p); q->rt=q->irt=q->fp=NULL; }
static inline u64 tom(u64 a,const Pr*q){ return mm(a,q->r2,q); }
static int tables_lg=0;
static void build_tables(int lg){ // twiddle factors for all stages up to transform length 2^lg (lg <= 24)
  size_t T=(size_t)1<<lg;
  for(int i=0;i<2;i++){ Pr*q=&pr[i]; free(q->rt); free(q->irt); q->rt=malloc(T*8); q->irt=malloc(T*8);
    for(size_t half=1;half<T;half<<=1){
      // root of unity of order 2*half: w24^(2^24/(2*half))
      u64 om=powmod(q->w24,((u64)1<<24)/(2*half),q->p), oi=powmod(om,q->p-2,q->p);
      u64 omm=tom(om,q), oim=tom(oi,q);
      q->rt[half]=q->r1; q->irt[half]=q->r1;
      for(size_t j=1;j<half;j++){ q->rt[half+j]=mm(q->rt[half+j-1],omm,q); q->irt[half+j]=mm(q->irt[half+j-1],oim,q); }
    } }
  tables_lg=lg; }
static void ntt_fwd(u64*a,size_t T,const Pr*q){
  u64 p=q->p;
  for(size_t half=T>>1;half;half>>=1){
    const u64*rt=q->rt+half;
    for(size_t i=0;i<T;i+=2*half){ u64*x=a+i,*y=a+i+half;
      for(size_t j=0;j<half;j++){ u64 u=x[j],v=y[j]; u64 s=u+v; if(s>=p)s-=p; u64 d=u+p-v; if(d>=p)d-=p; x[j]=s; y[j]=mm(d,rt[j],q); } } } }
static void ntt_inv(u64*a,size_t T,const Pr*q){
  u64 p=q->p;
  for(size_t half=1;half<T;half<<=1){
    const u64*rt=q->irt+half;
    for(size_t i=0;i<T;i+=2*half){ u64*x=a+i,*y=a+i+half;
      for(size_t j=0;j<half;j++){ u64 u=x[j],v=mm(y[j],rt[j],q); u64 s=u+v; if(s>=p)s-=p; u64 d=u+p-v; if(d>=p)d-=p; x[j]=s; y[j]=d; } } } }

/* ---------- long numbers (64-bit limbs, little endian) ---------- */
static void mul_small(u64*a,size_t*len,u64 m){ u64 c=0; for(size_t i=0;i<*len;i++){ u128 t=(u128)a[i]*m+c; a[i]=(u64)t; c=(u64)(t>>64);} if(c) a[(*len)++]=c; }
static void pow3(u64*P,size_t*plen,long long m){ P[0]=1; *plen=1; u64 p40=1; for(int i=0;i<M;i++)p40*=3;
  for(long long i=0;i<m/M;i++) mul_small(P,plen,p40); u64 r=1; for(int i=0;i<m%M;i++) r*=3; if(r>1) mul_small(P,plen,r); }
static int ceillog2(size_t x){ int l=0; while(((size_t)1<<l)<x) l++; return l; }

/* ---------- product hi * P with the NTT, result as 32-bit digits in out ---------- */
static u64 *tmp[2]; static u128 *bufc,*tailc; static size_t tmpcap=0;
static int fp_lg=-1; static long long fp_m=-1; static size_t fp_lp=0;
static size_t mul_ntt(const u64*h,size_t hl,const u64*P,size_t plen,long long m,u64*out){
  size_t hc=2*hl; size_t lp=2*plen; if((P[plen-1]>>32)==0) lp--;
  int lgstd=ceillog2(4*lp), lgneed=ceillog2(hc+lp), lgmin=ceillog2(2*lp+2);
  int lg=lgstd<lgneed?lgstd:lgneed; if(lg<lgmin) lg=lgmin; if(lg<4) lg=4;
  if(lg>tables_lg){ if(lg>24){ fprintf(stderr,"transform length too large\n"); exit(1);} build_tables(lg); }
  size_t T=(size_t)1<<lg, c=T-lp+1;
  if(T>tmpcap){ for(int i=0;i<2;i++){ free(tmp[i]); tmp[i]=malloc(T*8);} free(bufc); free(tailc); bufc=malloc(T*16); tailc=malloc(T*16); tmpcap=T; }
  if(fp_lg!=lg||fp_m!=m||fp_lp!=lp){
    for(int i=0;i<2;i++){ free(pr[i].fp); pr[i].fp=malloc(T*8); u64*f=pr[i].fp; memset(f,0,T*8);
      for(size_t j=0;j<lp;j++) f[j]=(P[j>>1]>>((j&1)*32))&0xffffffffULL;
      ntt_fwd(f,T,&pr[i]); for(size_t j=0;j<T;j++) f[j]=tom(f[j],&pr[i]); }
    fp_lg=lg; fp_m=m; fp_lp=lp; }
  u64 invM=tom(powmod(pr[0].p%pr[1].p,pr[1].p-2,pr[1].p),&pr[1]);
  u64 tinv0=tom(powmod(T,pr[0].p-2,pr[0].p),&pr[0]), tinv1=tom(powmod(T,pr[1].p-2,pr[1].p),&pr[1]);
  u32*o=(u32*)out; size_t pos=0; u128 carry=0; memset(tailc,0,(lp>1?lp-1:1)*16);
  for(size_t start=0;start<hc;start+=c){
    size_t cl=hc-start<c?hc-start:c;
#ifdef _OPENMP
#pragma omp parallel for num_threads(2)
#endif
    for(int q=0;q<2;q++){
      u64*t=tmp[q]; for(size_t j=0;j<cl;j++){ size_t idx=start+j; t[j]=(h[idx>>1]>>((idx&1)*32))&0xffffffffULL; }
      memset(t+cl,0,(T-cl)*8);
      ntt_fwd(t,T,&pr[q]); const u64*f=pr[q].fp; for(size_t j=0;j<T;j++) t[j]=mm(t[j],f[j],&pr[q]);
      ntt_inv(t,T,&pr[q]); u64 ti=q?tinv1:tinv0; size_t L=cl+lp-1; for(size_t j=0;j<L;j++) t[j]=mm(t[j],ti,&pr[q]); }
    size_t L=cl+lp-1;
    for(size_t j=0;j<L;j++){
      u64 r1=tmp[0][j], r2=tmp[1][j]; u64 d=r2>=r1?r2-r1:r2+pr[1].p-r1; u64 u=mm(d,invM,&pr[1]);
      u128 x=(u128)r1+(u128)pr[0].p*u; if(j<lp-1) x+=tailc[j]; bufc[j]=x; }
    for(size_t j=0;j<cl;j++){ u128 v=bufc[j]+carry; o[pos++]=(u32)v; carry=v>>32; }
    for(size_t j=0;j<lp-1;j++) tailc[j]=bufc[cl+j];
  }
  for(size_t j=0;j<lp-1;j++){ u128 v=tailc[j]+carry; o[pos++]=(u32)v; carry=v>>32; }
  while(carry){ o[pos++]=(u32)carry; carry>>=32; }
  if(pos&1) o[pos++]=0;
  return pos/2; // number of 64-bit limbs
}

/* ---------- one sub-block of m <= 40 Bells (as in bellrun.c of the TM1 repository) ---------- */
static void blk(u64*k,size_t*lenp,int*sp,int m,long long*cntp,int*stopp){
  size_t len=*lenp; u128 L=k[0]; int st=*sp,cnt=0,stop=0;
  for(int j=0;j<m;j++){ vis[st]++; int idx=2*st+(int)((L&3)>>1); int t=nxt[idx]; if(t<0){stop=t;break;} L=3*(L>>1)+cc[idx]; st=t; cnt++; }
  *cntp=cnt; *sp=st; if(stop){ *stopp=stop; *lenp=len; k[0]=(u64)L; return; }
  u64 mul=1; for(int i=0;i<cnt;i++) mul*=3; int sh=64-cnt;
  u64 carry=0,prev=0; size_t q=len-1;
  for(size_t i=0;i<=q;i++){ u64 p; if(i<q){ u128 t=(u128)k[i+1]*mul+carry; p=(u64)t; carry=(u64)(t>>64);} else { p=carry; carry=0; }
    u64 out=(p<<sh)|(sh?(prev>>(64-sh)):0); prev=p; k[i]=out; }
  size_t nl=q+1; { u64 lo=prev>>(64-sh); if(lo){ k[nl++]=lo; } }
  if(nl==0){ nl=1; k[0]=0; }
  { u128 t=(u128)k[0]+(u64)L; k[0]=(u64)t; u128 c2=(t>>64)+(u64)(L>>64);
    if(nl<2){ k[1]=0; nl=2; }
    t=(u128)k[1]+(u64)c2; k[1]=(u64)t; u128 c3=(t>>64)+(u64)(c2>>64);
    size_t i=2; while(c3){ if(i>=nl){ k[i]=0; nl=i+1; } t=(u128)k[i]+(u64)c3; k[i]=(u64)t; c3=(t>>64)+(u64)(c3>>64); i++; } }
  len=nl; while(len>1&&k[len-1]==0) len--; *lenp=len;
}
static double now(){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+1e-9*ts.tv_nsec; }

/* ---------- checkpoints ----------
   A checkpoint is a small text file checkpoints/bell_<N>_chkpt.txt for one Bell N:
     # bellntt checkpoint
     date 2026-10-18
     time 11:52:29
     program bellntt-ckpt-1 (bb6 vampire family)
     orbit O2
     bell 1000001
     S 11                    the word S of TM1 coordinates (with its leading 1)
     k_bits 584968
     k_hex 1F3A...           k in hexadecimal, most significant digit first
     checksum 0123456789abcdef
   The checksum is the 64-bit FNV-1a hash of the three lines "bell ...", "S ..." and "k_hex ..." (each with its
   newline), written as 16 hex digits. It protects against typing errors and damaged files.          */
#define PROGLABEL "bellntt-ckpt-1 (bb6 vampire family)"
static char orbit[64]="?";
static int bitlen(const u64*k,size_t len){ return (int)(64*(len-1)+64-__builtin_clzll(k[len-1]|1)); }
static void ckpt_name(char*buf,size_t sz,long long bell){ snprintf(buf,sz,"checkpoints/bell_%lld_chkpt.txt",bell); }
static u64 fnv(u64 h,const char*p,size_t n){ for(size_t i=0;i<n;i++){ h^=(unsigned char)p[i]; h*=1099511628211ULL; } return h; }
static const u64 FNV0=14695981039346656037ULL;
static const char HX[]="0123456789ABCDEF";

static int write_ckpt(long long bell,const u64*k,size_t len,int s){
  char name[256],tmpn[300]; ckpt_name(name,sizeof name,bell); snprintf(tmpn,sizeof tmpn,"%s.tmp",name);
  // hex digits of k, most significant first, without leading zeros
  int bits=bitlen(k,len); size_t nd=(bits+3)/4; if(nd==0) nd=1;
  char*hx=malloc(nd+1); for(size_t i=0;i<nd;i++){ size_t d=nd-1-i; hx[i]=HX[(k[d/16]>>(4*(d%16)))&15]; } hx[nd]=0;
  char lb[64],ls[128]; snprintf(lb,sizeof lb,"bell %lld\n",bell); snprintf(ls,sizeof ls,"S 1%s\n",names[s]);
  u64 h=fnv(FNV0,lb,strlen(lb)); h=fnv(h,ls,strlen(ls)); h=fnv(h,"k_hex ",6); h=fnv(h,hx,nd); h=fnv(h,"\n",1);
  time_t now_t=time(NULL); char d[16],t[16]; strftime(d,sizeof d,"%Y-%m-%d",localtime(&now_t)); strftime(t,sizeof t,"%H:%M:%S",localtime(&now_t));
  FILE*f=fopen(tmpn,"w"); if(!f){ perror(tmpn); free(hx); return -1; }
  fprintf(f,"# bellntt checkpoint\ndate %s\ntime %s\nprogram %s\norbit %s\n%s%sk_bits %d\nk_hex %s\nchecksum %016llx\n",
          d,t,PROGLABEL,orbit,lb,ls,bits,hx,(unsigned long long)h);
  free(hx);
  if(fclose(f)){ perror(tmpn); return -1; }
  if(rename(tmpn,name)){ perror(name); return -1; }
  return 0;
}

// read a checkpoint; returns 0 on success, -1 if the file is missing or damaged
static int read_ckpt(const char*name,long long*bell,u64**k,size_t*len,size_t extra,int*s){
  FILE*f=fopen(name,"r"); if(!f) return -1;
  char*line=NULL; size_t cap=0; ssize_t r; long long b=-1; char S[256]=""; char*hx=NULL; size_t nd=0;
  unsigned long long cs=0; int have_cs=0, kb=-1; char lb[64]="",ls[300]="";
  while((r=getline(&line,&cap,f))>0){
    if(!strncmp(line,"bell ",5)){ b=atoll(line+5); snprintf(lb,sizeof lb,"%s",line); }
    else if(!strncmp(line,"S ",2)){ sscanf(line+2,"%255s",S); snprintf(ls,sizeof ls,"%s",line); }
    else if(!strncmp(line,"k_bits ",7)) kb=atoi(line+7);
    else if(!strncmp(line,"k_hex ",6)){ nd=0; hx=malloc(r); for(ssize_t i=6;i<r;i++){ char c=line[i]; if(c=='\n'||c=='\r') break; hx[nd++]=c; } }
    else if(!strncmp(line,"checksum ",9)){ cs=strtoull(line+9,NULL,16); have_cs=1; }
  }
  free(line); fclose(f);
  if(b<0||!S[0]||!hx||!nd||!have_cs||S[0]!='1'){ free(hx); return -1; }
  u64 h=fnv(FNV0,lb,strlen(lb)); h=fnv(h,ls,strlen(ls)); h=fnv(h,"k_hex ",6); h=fnv(h,hx,nd); h=fnv(h,"\n",1);
  if(h!=cs){ fprintf(stderr,"%s: checksum does not match\n",name); free(hx); return -1; }
  int si=-1; for(int i=0;i<n;i++) if(!strcmp(names[i],S+1)) si=i;
  if(si<0){ fprintf(stderr,"%s: word S = %s is not in the table\n",name,S); free(hx); return -1; }
  size_t l=(nd+15)/16; u64*a=calloc(l+extra+8,8); if(!a){ free(hx); return -1; }
  for(size_t i=0;i<nd;i++){ char c=hx[nd-1-i]; int v=(c>='0'&&c<='9')?c-'0':(c>='A'&&c<='F')?c-'A'+10:(c>='a'&&c<='f')?c-'a'+10:-1;
    if(v<0){ free(hx); free(a); return -1; } a[i/16]|=(u64)v<<(4*(i%16)); }
  free(hx); while(l>1&&a[l-1]==0) l--;
  if(kb>=0&&bitlen(a,l)!=kb){ fprintf(stderr,"%s: k_bits does not match\n",name); free(a); return -1; }
  *bell=b; *k=a; *len=l; *s=si; return 0;
}

static int cmp_desc(const void*a,const void*b){ long long x=*(const long long*)a,y=*(const long long*)b; return x<y?1:x>y?-1:0; }

static void log_progress(long long bell,const u64*k,size_t len,int s,double t,const char*what){
  // TM2 coordinates: n = floor(k/2), P = (S without its leading 11) read backwards
  u64 nlow=(k[0]>>1)|(len>1?k[1]<<63:0); const char*sp=names[s]; char P[128]; int L=(int)strlen(sp)-1;
  for(int i=0;i<L;i++) P[i]=sp[L-i];
  P[L]=0;
  char line[512]; time_t now_t=time(NULL); char ts[32]; strftime(ts,sizeof ts,"%Y-%m-%d %H:%M:%S",localtime(&now_t));
  snprintf(line,sizeof line,"%s  %s  bell %lld  time %.0fs  KCHECK %llu %d %s  TM2: n mod 2^64 = %llu, bits %d, P = %s\n",
           ts,what,bell,t,(unsigned long long)k[0],bitlen(k,len),names[s],(unsigned long long)nlow,bitlen(k,len)-1,L?P:"e");
  fputs(line,stdout); fflush(stdout);
  FILE*f=fopen("progress.log","a"); if(f){ fputs(line,f); fclose(f); }
}

int main(int argc,char**argv){
  if(argc<2){ fprintf(stderr,"usage: %s TARGET [INTERVAL [B]]   or   %s init BELL K S\n",argv[0],argv[0]); return 2; }
  int init=!strcmp(argv[1],"init");
  long long target=init?1:atoll(argv[1]);
  long long interval=argc>2?atoll(argv[2]):10000000LL;
  long long B=argc>3?atoll(argv[3]):2000000LL;
  if(target<=0||interval<=0||B<=0){ fprintf(stderr,"TARGET, INTERVAL and B must be positive\n"); return 2; }
  { FILE*f=fopen("orbit.txt","r"); if(f){ if(fscanf(f,"%63s",orbit)!=1) strcpy(orbit,"?"); fclose(f);} }
  FILE*f=fopen("tab.txt","r"); if(!f||fscanf(f,"%d",&n)!=1){ fprintf(stderr,"cannot read tab.txt\n"); return 1; }
  nxt=malloc(sizeof(int)*2*n); cc=malloc(sizeof(int)*2*n);
  for(int i=0;i<n;i++){ int a,b,c,d; if(fscanf(f,"%d %d %d %d",&a,&b,&c,&d)!=4) return 1; nxt[2*i]=a;cc[2*i]=b;nxt[2*i+1]=c;cc[2*i+1]=d; } fclose(f);
  names=malloc(sizeof(char*)*n); f=fopen("tab_names.txt","r"); if(!f){ fprintf(stderr,"cannot read tab_names.txt\n"); return 1; }
  for(int i=0;i<n;i++){ names[i]=malloc(64); if(fscanf(f,"%63s",names[i])!=1) return 1; } fclose(f);
  vis=calloc(n,8);
  pr_init(&pr[0],9223372036636672001ULL,510271893463106651ULL);
  pr_init(&pr[1],9223372036737335297ULL,2419180138865645092ULL);

  if(init){
    if(argc!=5){ fprintf(stderr,"usage: %s init BELL K S\n",argv[0]); return 2; }
    int si=-1; if(argv[4][0]=='1') for(int i=0;i<n;i++) if(!strcmp(names[i],argv[4]+1)) si=i;
    if(si<0){ fprintf(stderr,"word %s not in tab_names.txt\n",argv[4]); return 1; }
    u64 k0=strtoull(argv[3],NULL,10); if(!k0){ fprintf(stderr,"K must be positive\n"); return 1; }
    if(write_ckpt(atoll(argv[2]),&k0,1,si)) return 1;
    log_progress(atoll(argv[2]),&k0,1,si,0,"init   "); return 0; }

  // find the start checkpoint: highest Bell number that can be read
  long long cand[100000]; int nc=0;
  DIR*dir=opendir("checkpoints"); if(!dir){ fprintf(stderr,"no directory checkpoints/\n"); return 1; }
  struct dirent*e; while((e=readdir(dir))&&nc<100000){ long long b; char rest[16];
    if(sscanf(e->d_name,"bell_%lld_chkpt.tx%15s",&b,rest)==2&&!strcmp(rest,"t")) cand[nc++]=b; }
  closedir(dir); qsort(cand,nc,sizeof(long long),cmp_desc);
  size_t capK=(size_t)(0.6*target/64)+4*(size_t)(B/64)+8192;
  u64*k=NULL; size_t len=0; int s=0; long long bell=-1; char startname[256]="";
  for(int i=0;i<nc;i++){ char nm[256]; ckpt_name(nm,sizeof nm,cand[i]);
    if(read_ckpt(nm,&bell,&k,&len,capK,&s)==0&&bell==cand[i]){ strcpy(startname,nm); break; }
    fprintf(stderr,"skipping unreadable checkpoint %s\n",nm); bell=-1; }
  if(bell<0){ fprintf(stderr,"no readable checkpoint in checkpoints/\n"); return 1; }
  if(capK<len+8) capK=len+8;
  { u64*kk=realloc(k,(capK+8)*8); if(!kk){ fprintf(stderr,"out of memory\n"); return 1; } k=kk; memset(k+len,0,(capK+8-len)*8); }
  printf("orbit %s: start %s (Bell %lld), target Bell %lld, checkpoint every %lld Bells, B = %lld\n",orbit,startname,bell,target,interval,B);
  if(bell>=target){ printf("start Bell %lld is not below the target, nothing to do\n",bell); return 0; }
  u64*hi=calloc(capK+8,8),*out=calloc(capK*2+8192,8);
  size_t capL=(size_t)(1.7*(B+2)/64)+4096; u64*L=calloc(capL,8),*P=calloc(capL,8);
  if(!hi||!out||!L||!P){ fprintf(stderr,"out of memory\n"); return 1; }
  size_t plen=0; long long Pm=-1;
  double t0=now(),tlow=0,tmul=0;
  long long nextck=(bell/interval+1)*interval; char prevname[256]="";
  log_progress(bell,k,len,s,0,"start  ");
  while(bell<target){
    long long m=B; if(target-bell<m) m=target-bell; if(nextck-bell<m) m=nextck-bell;
    size_t W=m+2, wl=(W+63)/64;
    double ta=now();
    size_t Ll=len<wl?len:wl; memcpy(L,k,Ll*8); if(len>=wl&&(W&63)) L[wl-1]&=((u64)1<<(W&63))-1;
    while(Ll>1&&L[Ll-1]==0) Ll--;
    size_t off=W>>6; int sh=W&63; size_t hl=0;
    if(len>off){ hl=len-off; for(size_t i=0;i<hl;i++){ u64 v=k[off+i]>>sh; if(sh&&off+i+1<len) v|=k[off+i+1]<<(64-sh); hi[i]=v; } while(hl>0&&hi[hl-1]==0) hl--; }
    int st=s; long long rem=m;
    while(rem>0){ int mmx=rem<M?(int)rem:M; long long c=0; int stp=0; blk(L,&Ll,&st,mmx,&c,&stp); bell+=c; rem-=c;
      if(stp){
        char msg[256]; snprintf(msg,sizeof msg,"%s at Bell %lld: S_pascal = %s, k mod 4 = %d\n",stp==-1?"HALT":"UNKNOWN STATE (word not in the table)",bell,names[st],(int)(L[0]&3));
        fputs(msg,stdout); char hn[256]; snprintf(hn,sizeof hn,"checkpoints/%s_bell_%lld.txt",stp==-1?"HALT":"UNKNOWN",bell);
        FILE*h=fopen(hn,"w"); if(h){ fprintf(h,"orbit %s\n%s",orbit,msg); fclose(h); }
        FILE*g=fopen("progress.log","a"); if(g){ fprintf(g,"%s",msg); fclose(g); }
        return 0; } }
    double tb=now(); tlow+=tb-ta;
    if(hl==0){ memcpy(k,L,Ll*8); len=Ll; }
    else {
      if(Pm!=m){ pow3(P,&plen,m); Pm=m; }
      size_t ol=mul_ntt(hi,hl,P,plen,m,out);
      u64 carry=0,prevhi=0; size_t i=0;
      for(i=0; i<ol||i<Ll||carry||prevhi; i++){ u64 v=(i<ol)?out[i]:0; u64 lo=(v<<2)|prevhi; prevhi=v>>62; u128 sum=(u128)lo+(i<Ll?L[i]:0)+carry; k[i]=(u64)sum; carry=(u64)(sum>>64); }
      len=i; while(len>1&&k[len-1]==0) len--;
    }
    tmul+=now()-tb; s=st;
    if(bell==nextck||bell==target){
      if(write_ckpt(bell,k,len,s)) return 1;
      if(prevname[0]) remove(prevname);                       // drop the previous intermediate checkpoint
      if(bell<target) ckpt_name(prevname,sizeof prevname,bell); else prevname[0]=0;
      log_progress(bell,k,len,s,now()-t0,bell==target?"target ":"ckpt   ");
      if(bell==nextck) nextck+=interval;
    }
  }
  printf("no halt up to Bell %lld; time %.1fs (low part %.1fs, products %.1fs)\n",bell,now()-t0,tlow,tmul);
  return 0;
}
