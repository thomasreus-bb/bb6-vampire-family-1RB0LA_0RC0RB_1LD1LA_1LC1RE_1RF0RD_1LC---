/* no. 70 (records in state A) vs no. 86 (records in state B): every new leftmost cell in that state is a record.
   Phase 1: find the record shift d (86 record j+d <-> 70 record j) such that the run-length tapes agree except for the
   last few runs (the right ends).  Phase 2: check every record up to N steps of no. 70.  Also reports the right ends
   and the largest head excursion to the right (distance to the first differing run). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef long long ll;
#define W (1L<<27)
static int nw[2][6][2],nd[2][6][2],nq[2][6][2];
static void parse(int k,const char*M){for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b;
 if(x[0]=='-'){nq[k][i][b]=-1;continue;}nw[k][i][b]=x[0]-'0';nd[k][i][b]=x[1]=='R'?1:-1;nq[k][i][b]=x[2]-'A';}}
typedef struct{unsigned char*t;ll h,lo,hi,n,maxr;int q;}TM;
static int QS[2]={0,1};
static void rec(int k,TM*m){for(;;){int b=m->t[m->h];int q=nq[k][m->q][b];m->t[m->h]=nw[k][m->q][b];m->h+=nd[k][m->q][b];m->q=q;m->n++;
 if(m->h>m->hi)m->hi=m->h; if(m->h>m->maxr)m->maxr=m->h; if(m->h<m->lo){m->lo=m->h; if(m->q==QS[k])return;}}}
static int rle(TM*m,ll*out){int n=0;ll x=m->lo;while(x<=m->hi){int v=m->t[x];ll c=0;while(x<=m->hi&&m->t[x]==v){c++;x++;}out[n++]=v?c:-c;}return n;}
static ll A[1<<20],B[1<<20];
int main(int c,char**v){parse(0,"1RB1RF_1LC1RD_1LA1LC_1RA0RE_1RD1LA_---0LE");parse(1,"1RB0RE_1RC0RF_1LD1RA_1LB1LD_1RA1LB_---0LD");
 ll N=atoll(v[1]),K0=atoll(v[2]);int TA=atoi(v[3]),TB=atoi(v[4]); /* runs at the right end ignored: TA for 70, TB for 86 */
 TM m[2];for(int k=0;k<2;k++){m[k].t=calloc(W,1);m[k].h=m[k].lo=m[k].hi=m[k].maxr=W/2;m[k].q=0;m[k].n=0;}
 for(ll j=0;j<K0;j++)rec(0,&m[0]);
 int na=rle(&m[0],A); ll d=-1;
 for(ll j=0;j<K0+200;j++){rec(1,&m[1]);int nb=rle(&m[1],B);
   if(na-TA==nb-TB&&!memcmp(A,B,sizeof(ll)*(na-TA))){d=j+1-K0;break;}}
 if(d<-1000){printf("no match\n");return 1;}
 printf("70 record %lld (step %lld) = 86 record %lld (step %lld): equal except the right ends; record shift %lld\n",K0,m[0].n,K0+d,m[1].n,d);
 printf("right end 70:");for(int i=na-TA;i<na;i++)printf(" %lld",A[i]);
 {int nb=rle(&m[1],B);printf(" | right end 86:");for(int i=nb-TB;i<nb;i++)printf(" %lld",B[i]);printf("\n");}
 ll recs=0,minfree=1LL<<60;
 while(m[0].n<N){ll w0=m[0].hi; m[0].maxr=m[0].h; m[1].maxr=m[1].h; rec(0,&m[0]);rec(1,&m[1]);recs++;
  na=rle(&m[0],A);int nb=rle(&m[1],B);
  if(na-TA!=nb-TB||memcmp(A,B,sizeof(ll)*(na-TA))||memcmp(A+na-TA,A+na-TA,0)){printf("MISMATCH after %lld records, step70 %lld\n",recs,m[0].n);return 1;}
  /* right end of 70 starts at cell hi - (sum of the last TA runs) + 1 */
  ll tail=0;for(int i=na-TA;i<na;i++)tail+=(A[i]<0?-A[i]:A[i]); ll free=(m[0].hi-tail)-m[0].maxr; if(free<minfree)minfree=free;
  if((recs&(recs-1))==0||m[0].n>=N){printf("records %lld, step70 %lld, step86 %lld: equal; right end 70:",recs,m[0].n,m[1].n);for(int i=na-TA;i<na;i++)printf(" %lld",A[i]);
   printf(" / 86:");for(int i=nb-TB;i<nb;i++)printf(" %lld",B[i]);printf("; closest approach of the head to the right end so far: %lld cells\n",minfree);fflush(stdout);}
 }}
