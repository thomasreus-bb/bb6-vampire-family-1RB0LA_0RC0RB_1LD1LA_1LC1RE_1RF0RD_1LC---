/* Fast macro simulator for BB(6) candidate no. 16 = 1RB1LF_1RC1RF_0LD1RE_---1LC_0RB1RE_1LA0LE.
 *
 * Configuration at a right record in state C (head on the 0 right of the written part):
 *     P 1^a (01)^b [0]      P empty ("E mode", m = -1)  or  P = 1(10)^m ("L mode", m >= 3)
 * Macro rules (found from data, checked against direct simulation, see the no. 16 chapter of scan/bell_candidates.md):
 *   E(u,X): smallest M = 1,2,4,.. with a' = (2M-1)u - X - 2 >= 0, b' = X + 1 - (M-1)u,
 *           steps (M-1)(2M-1)u^2 - 3(M-1)uX + 3X^2/2 - 8(M-1)u + 6X + 6 + 2 log2 M;
 *           if a' = 0 ("A0 event") the machine goes on to (2b'-1, 1), + 3 - 2b' steps.
 *   a even, or a >= 2b+1:     (m, E(a+2, 2b))
 *   a odd,  a < 2b,  d = 2b+1-a:
 *     E mode: a = 1 -> HALT;  d = 2 -> (4b+3, 1), 6b^2+20b+14 steps;  d = 4 -> (2, 2b-1), 6b^2+5;
 *             else  m' = a+2, E(1, d-3)  + 3a^2/2 + 9a + 12 steps
 *     L mode: d = 2 -> E mode (2m+4b+1, 1), 6b^2+4m+8b+7 steps;
 *             else  E mode, E(2m+2a+6, 2b-3-a)  + 3a^2/2 + 4m + 7a + 19/2 steps
 *   canonical form: L mode with a = 1 is the same tape as E mode (2, b+m).
 * HALT happens exactly when an A0 event in E mode gives b' = B = 2^(k+1) - k - 1 (then the
 * doubling steps from (2B-1,1) end in a = 1).
 *
 * usage: sim16 EXP [VERBOSE]   simulate up to 10^EXP steps (EXP <= 36)
 *   prints every A0 event: steps, mode, size S = a+2b, B, and for E-mode events the distance
 *   of B to the nearest halting value 2^(k+1)-k-1.  VERBOSE=1 prints every macro step.     */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
typedef __int128 I;
typedef unsigned __int128 U;
static void pr(U x){char s[50];int i=49;s[i]=0;if(!x)s[--i]='0';while(x){s[--i]='0'+(int)(x%10);x/=10;}fputs(s+i,stdout);}
static void prs(I x){if(x<0){putchar('-');x=-x;}pr((U)x);}
static U steps=0; static long long a0cnt[2]={0,0};
static int verbose=0;
static I nearH(I B){ /* signed distance to nearest 2^(k+1)-k-1 */
  I best=-1; I bd=0;
  for(int k=0;k<120;k++){ I h=((I)1<<(k+1))-k-1; I dd=B-h; I ad=dd<0?-dd:dd;
    if(best<0||ad<best){best=ad;bd=dd;} if(h>2*B+10)break;}
  return bd;
}
/* returns 1 if A0 happened, sets *pa,*pb, adds steps (doubled: steps2) */
static U st2; /* twice the steps of the current macro step */
static int E(I u,I X,I*pa,I*pb,I*pB){
  I M=1; int k=0;
  while((2*M-1)*u-X-2<0){M*=2;k++;}
  I a2=(2*M-1)*u-X-2, b2=X+1-(M-1)*u;
  if(b2<1){printf("ERROR b'<1\n");exit(2);}
  st2+=(U)(2*((M-1)*(2*M-1)*u*u-3*(M-1)*u*X-8*(M-1)*u+6*X+6+2*k)+3*X*X);
  if(a2==0){ st2+=(U)(2*(3-2*b2)); *pB=b2; *pa=2*b2-1; *pb=1; return 1; }
  *pa=a2; *pb=b2; return 0;
}
int main(int argc,char**argv){
  int EXP=argc>1?atoi(argv[1]):20; verbose=argc>2?atoi(argv[2]):0;
  U lim=1; for(int i=0;i<EXP;i++)lim*=10;
  /* start: the first L-mode record of the run from blank tape (step 459): m=7, a=6, b=1 */
  I m=7,a=6,b=1; steps=459;
  long long nmac=0; U nextdec=1000; int dec=3;
  while(steps<lim){
    I na,nb,B=0; int ev=0; I nm=m; st2=0;
    if((a&1)==0||a>=2*b+1){ ev=E(a+2,2*b,&na,&nb,&B); }
    else{
      I d=2*b+1-a;
      if(m<0){
        if(a==1){printf("HALT at step ");pr(steps);printf("\n");return 0;}
        if(d==2){na=4*b+3;nb=1;st2=(U)(2*(6*b*b+20*b+14));}
        else if(d==4){na=2;nb=2*b-1;st2=(U)(2*(6*b*b+5));}
        else{nm=a+2; ev=E(1,d-3,&na,&nb,&B); st2+=(U)(3*a*a+18*a+24);}
      }else{
        nm=-1;
        if(d==2){na=2*m+4*b+1;nb=1;st2=(U)(2*(6*b*b+4*m+8*b+7));
          /* E mode (2B-1,1) with B = m+2b+1: halts iff B = 2^(k+1)-k-1 */
          printf("LD2 step ");pr(steps+st2/2);printf(" B=");prs(m+2*b+1);printf(" distH=");prs(nearH(m+2*b+1));printf("\n");}
        else{ev=E(2*m+2*a+6,2*b-3-a,&na,&nb,&B); st2+=(U)(3*a*a+8*m+14*a+19);}
      }
    }
    steps+=st2/2; nmac++;
    if(nm>=0&&na==1){na=2;nb=nb+nm;nm=-1;}
    if(ev){
      int md=nm<0?0:1; a0cnt[md]++;
      printf("A0 %s step ",md?"L":"E"); pr(steps);
      printf(" S="); prs(na+2*nb); printf(" B="); prs(B);
      if(!md){printf(" distH="); prs(nearH(B));}
      printf("\n");
    }
    m=nm;a=na;b=nb;
    if(steps>=nextdec){printf("1e%d steps: macro=%lld S=",dec,nmac);prs(a+2*b);printf(" m=");prs(m);printf("\n");fflush(stdout);
      while(steps>=nextdec){nextdec*=10;dec++;}}
    if(verbose){pr(steps);printf(" m=");prs(m);printf(" a=");prs(a);printf(" b=");prs(b);printf("\n");}
  }
  printf("END steps="); pr(steps); printf(" macro=%lld m=",nmac); prs(m); printf(" a="); prs(a);
  printf(" b="); prs(b); printf(" S="); prs(a+2*b); printf(" A0 events E=%lld L=%lld\n",a0cnt[0],a0cnt[1]);
  return 0;
}
