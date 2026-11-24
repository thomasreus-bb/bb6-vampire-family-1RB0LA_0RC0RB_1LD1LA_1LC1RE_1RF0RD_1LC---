/* usage: cut86 K0 KEEP NRECORDS STEPLIMIT, e.g. ./cut86 3000 4 300 2000000000 */
/* end test: take the aligned configurations of no. 70 / no. 86 at record K0, delete the stack runs from index A up to the
   right ends (keep the first A runs), so that the head soon reaches the different right ends; then run both and compare
   every record (all runs except the right ends) for N records.  Reports equal/mismatch/halt. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
#define W (1L<<24)
static int nw[2][6][2],nd[2][6][2],nq[2][6][2];
static void parse(int k,const char*M){for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b;
 if(x[0]=='-'){nq[k][i][b]=-1;continue;}nw[k][i][b]=x[0]-'0';nd[k][i][b]=x[1]=='R'?1:-1;nq[k][i][b]=x[2]-'A';}}
typedef struct{unsigned char*t;ll h,lo,hi,n;int q,halt;}TM;
static int QS[2]={0,1};
static ll LIM;
static int rec(int k,TM*m){for(ll s=0;s<LIM;s++){int b=m->t[m->h];int q=nq[k][m->q][b];if(q<0){m->halt=1;return 1;}m->t[m->h]=nw[k][m->q][b];m->h+=nd[k][m->q][b];m->q=q;m->n++;
 if(m->h>m->hi)m->hi=m->h; if(m->h<m->lo){m->lo=m->h; if(m->q==QS[k])return 0;} if(m->h<5||m->h>W-5)return 2;}return 3;}
static int rle(TM*m,ll*out){int n=0;ll x=m->lo;while(x<=m->hi){int v=m->t[x];ll c=0;while(x<=m->hi&&m->t[x]==v){c++;x++;}out[n++]=v?c:-c;}return n;}
static void build(TM*m,ll*R,int n,ll head_off){memset(m->t,0,W);ll x=W/4;m->lo=x;for(int i=0;i<n;i++){ll c=R[i]<0?-R[i]:R[i];for(ll j=0;j<c;j++)m->t[x++]=R[i]>0;}m->hi=x-1;m->h=m->lo+head_off;}
static ll A[1<<16],B[1<<16],C[1<<16],D[1<<16];
int main(int c,char**v){parse(0,"1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE");parse(1,"1RB0RE_1RC0RF_1LD1RA_1LB1LD_1RA1LB_---0LD");
 ll K0=atoll(v[1]);int KEEP=atoi(v[2]);ll N=atoll(v[3]);LIM=atoll(v[4]);
 TM m[2];for(int k=0;k<2;k++){m[k].t=calloc(W,1);m[k].h=m[k].lo=m[k].hi=W/2;m[k].q=0;m[k].n=0;m[k].halt=0;}
 LIM=1LL<<62; for(ll j=0;j<K0;j++)rec(0,&m[0]); for(ll j=0;j<K0-10;j++)rec(1,&m[1]); LIM=atoll(v[4]);
 int na=rle(&m[0],A),nb=rle(&m[1],B);
 if(na-4!=nb-2||memcmp(A,B,8*(na-4))){printf("not aligned\n");return 1;}
 if(KEEP>na-4)KEEP=na-4; KEEP&=~1; /* keep an even number of runs (ends with a gap or block?) */
 /* new tapes: first KEEP runs, then the right ends */
 int n0=0,n1=0; for(int i=0;i<KEEP;i++){A[n0++]=A[i];} for(int i=na-4;i<na;i++)A[n0++]=A[i];
 for(int i=0;i<KEEP;i++){B[n1++]=B[i];} for(int i=nb-2;i<nb;i++)B[n1++]=B[i];
 ll hoff=m[0].h-m[0].lo; build(&m[0],A,n0,hoff); build(&m[1],B,n1,hoff); 
 for(ll r=0;r<N;r++){int e0=rec(0,&m[0]),e1=rec(1,&m[1]);
  if(m[0].halt||m[1].halt){printf("K0 %lld keep %d: HALT 70:%d 86:%d after %lld records\n",K0,KEEP,m[0].halt,m[1].halt,r);return 0;}
  if(e0||e1){printf("K0 %lld keep %d: limit (%d %d) after %lld records\n",K0,KEEP,e0,e1,r);return 0;}
  na=rle(&m[0],C);nb=rle(&m[1],D);
  /* find right ends: compare everything except a tail; accept if prefix equal up to min length - tails */
  int i=0;while(i<na&&i<nb&&C[i]==D[i])i++;
  if(i<na-6||i<nb-6){printf("K0 %lld keep %d: DIVERGE after %lld records (equal %d of %d/%d runs); tails 70:",K0,KEEP,r,i,na,nb);for(int j=i;j<na&&j<i+8;j++)printf(" %lld",C[j]);printf(" 86:");for(int j=i;j<nb&&j<i+8;j++)printf(" %lld",D[j]);printf("\n");return 0;}
 }
 printf("K0 %lld keep %d: equal for %lld records; tails 70:",K0,KEEP,N);na=rle(&m[0],C);nb=rle(&m[1],D);for(int j=(na>6?na-6:0);j<na;j++)printf(" %lld",C[j]);printf(" 86:");for(int j=(nb>6?nb-6:0);j<nb;j++)printf(" %lld",D[j]);printf("\n");}
