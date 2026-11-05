/* lazy44: one macro step C(m, r) -> next C configuration of the machine TM, for an UNKNOWN word r.
   The tape is 10 1^m followed by r; cells of r are read lazily: when the head reads a cell of r that
   has not been read before, the run is split into the two cases 0 and 1 (depth-first search).
   Each leaf is printed as
      LEAF <read prefix of r> -> C <k> <word after the 1-block> [*]     (* = unread rest of r follows)
      HALT <read prefix>      |   DEEP <read prefix>   (more than D cells of r read)   |   LONG <prefix>
   usage: lazy44 TM m D [maxsteps]       (head starts on the blank left of the tape, state A) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define W 20000
int T[6][2][3];
typedef struct { unsigned char t[W]; long h, lo, hi, known; int s; long long n; long minpos; } Cfg;
long maxback=0; long maxback_exit=0;   /* known = number of r cells read */
long R0; int D; long long MX;
long long nleaf=0, nhalt=0, ndeep=0, nlong=0;
static void out_prefix(Cfg*c){ for(long i=0;i<c->known;i++) putchar('0'+c->t[R0+i]); }
static void dfs(Cfg*c){
  for(;;){
    long h=c->h;
    if(h>=R0+c->known){ /* unread cell of r */
      { long bk=R0+c->known-c->minpos; if(c->minpos>=R0){ if(bk>maxback) maxback=bk; } else { if(bk>maxback_exit) maxback_exit=bk; } c->minpos=c->h; }
      if(c->known>=D){ ndeep++; printf("DEEP "); out_prefix(c); printf("\n"); return; }
      Cfg*d=malloc(sizeof(Cfg)); memcpy(d,c,sizeof(Cfg)); d->t[R0+d->known]=1; d->known++; dfs(d); free(d);
      c->t[R0+c->known]=0; c->known++; continue; }
    int b=c->t[h];
    if(T[c->s][b][2]<0){ nhalt++; printf("HALT "); out_prefix(c); printf("\n"); return; }
    c->t[h]=T[c->s][b][0]; c->h+=T[c->s][b][1]; c->s=T[c->s][b][2]; c->n++; if(c->h<c->minpos) c->minpos=c->h;
    if(c->n>MX){ nlong++; printf("LONG "); out_prefix(c); printf("\n"); return; }
    if(c->h<=0||c->h>=W-1){ printf("TAPE\n"); exit(1);}
    if(c->h<c->lo){ c->lo=c->h;
      if(c->s==0 && c->n>1){ /* left record in state A: is it 10 1^k w with w = '' / 0... ? */
        long a=c->h+1; long q;
        if(c->t[a]==1 && c->t[a+1]==0){ q=a+2; long k=0; while(c->t[q]==1 && q<R0+c->known){k++;q++;}
          int ok=0; if(q>=R0+c->known) ok=2; else if(c->t[q]==0) ok=1;
          if(k>=4 && ok){ nleaf++; printf("LEAF "); out_prefix(c); printf(" -> C %ld ",k);
            /* word after the ones up to the last known cell */
            long z=R0+c->known-1; for(long i=q;i<=z;i++) putchar('0'+c->t[i]);
            printf("%s %lld\n", "*", c->n); return; } } } }
    if(c->h>c->hi) c->hi=c->h;
  } }
int main(int argc,char**argv){
  const char*M=argv[1]; long m=atol(argv[2]); D=atoi(argv[3]); MX=argc>4?atoll(argv[4]):100000000LL;
  for(int s=0;s<6;s++)for(int b=0;b<2;b++){const char*p=M+7*s+3*b; if(p[2]=='-'){T[s][b][2]=-1;continue;} T[s][b][0]=p[0]-'0';T[s][b][1]=p[1]=='R'?1:-1;T[s][b][2]=p[2]-'A';}
  Cfg*c=calloc(1,sizeof(Cfg)); long p=5000; c->t[p++]=1; c->t[p++]=0; for(long i=0;i<m;i++) c->t[p++]=1; R0=p;
  c->h=4999; c->lo=4999; c->hi=p; c->s=0; c->t[R0]=0; c->known=1; c->minpos=R0; dfs(c);  /* r starts with 0 (canonical form) */
  fprintf(stderr,"leaves %lld halt %lld deep %lld long %lld  max backtrack inside r %ld\n",nleaf,nhalt,ndeep,nlong,maxback); return 0; }
