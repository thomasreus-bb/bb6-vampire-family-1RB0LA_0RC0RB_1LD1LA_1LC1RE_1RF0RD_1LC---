/* sim35: fast simulator for no. 35 (1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA).
   Tape = doubly linked list of runs (symbol, length). Exact TM steps, plus
   - chain steps: state C moving right over 1s, state E moving left over 1s (whole run at once);
   - loop jump: in state A on a single 0 between 1^X and 1^Y 00 1^Z, one round is
     (X, Y, Z) -> (X+2, Y-3, Z+1) in 2Y+16 steps (checked in round35.py); k rounds are done at once.
   Step counts are exact (128-bit). Output: every new left record in state E (or every n-th), as run list.
   usage: sim35 maxsteps_exponent [print_every] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned __int128 u128;
typedef struct Run { int sym; long long len; struct Run *prev,*next; } Run;
static Run* newrun(int s,long long l){ Run*r=malloc(sizeof(Run)); r->sym=s; r->len=l; r->prev=r->next=NULL; return r; }
static Run *head_run; static long long off;   /* head is at cell 'off' (0-based) inside head_run */
static Run *leftmost, *rightmost;
static void ensure_left(void){ if(!head_run->prev){ Run*r=newrun(0,1000000); r->next=head_run; head_run->prev=r; leftmost=r; } }
static void ensure_right(void){ if(!head_run->next){ Run*r=newrun(0,1000000); r->prev=head_run; head_run->next=r; rightmost=r; } }
static void merge(Run*a){ /* merge a with a->next if same symbol */
  Run*b=a->next; if(b && b->sym==a->sym){ a->len+=b->len; a->next=b->next; if(b->next) b->next->prev=a; else rightmost=a; if(head_run==b){head_run=a; off+=a->len-b->len;} free(b);} }
static void write_cell(int v){
  Run*r=head_run; if(r->sym==v) return;
  /* split r into [0,off) v [off+1,len) */
  long long L=r->len;
  if(L==1){ r->sym=v; }
  else if(off==0){ Run*n=newrun(r->sym,L-1); n->next=r->next; if(r->next) r->next->prev=n; else rightmost=n; n->prev=r; r->next=n; r->len=1; r->sym=v; }
  else if(off==L-1){ Run*n=newrun(v,1); n->next=r->next; if(r->next) r->next->prev=n; else rightmost=n; n->prev=r; r->next=n; r->len=L-1; head_run=n; off=0; r=n; }
  else { Run*m=newrun(v,1), *n=newrun(r->sym,L-off-1); n->next=r->next; if(r->next) r->next->prev=n; else rightmost=n; n->prev=m; m->next=n; m->prev=r; r->next=m; r->len=off; head_run=m; off=0; r=m; }
  /* merge with neighbours */
  if(r->next) { long long o=off; merge(r); off=o; }
  if(r->prev && r->prev->sym==r->sym){ Run*p=r->prev; long long o=p->len+off; merge(p); head_run=p; off=o; }
}
static void move(int d){
  if(d>0){ if(off+1<head_run->len) off++; else { ensure_right(); head_run=head_run->next; off=0; } }
  else   { if(off>0) off--; else { ensure_left(); head_run=head_run->prev; off=head_run->len-1; } }
}
int T[6][2][3];
static void print_tape(void){
  Run*r=leftmost; while(r && r->sym==0) r=r->next;
  Run*z=rightmost; while(z && z->sym==0) z=z->prev;
  for(;r;r=r->next){ if(r->sym) printf("%lld",r->len); else printf(r->len==1?" ":(r->len==2?" | ":" |%lld| "),r->len); if(r==z) break; }
}
static void p128(u128 x){ char b[64]; int i=63; b[i]=0; if(!x){printf("0");return;} while(x){ b[--i]='0'+(int)(x%10); x/=10;} printf("%s",b+i); }
int main(int argc,char**argv){
  const char*M="1RB---_0RC0LD_1LB1RC_0LE0LF_1RD1LE_1RF1RA";
  for(int s=0;s<6;s++)for(int b=0;b<2;b++){const char*p=M+7*s+3*b; if(p[2]=='-'){T[s][b][2]=-1;continue;} T[s][b][0]=p[0]-'0';T[s][b][1]=p[1]=='R'?1:-1;T[s][b][2]=p[2]-'A';}
  int ex=atoi(argv[1]); u128 MAX=1; for(int i=0;i<ex;i++) MAX*=10; long long every=argc>2?atoll(argv[2]):1;
  head_run=newrun(0,2000000); leftmost=rightmost=head_run; off=1000000;
  long long pos=0, lo=0; long long nrec=0; u128 steps=0; int s=0; long long loops=0;
  if(argc>3){ /* start configuration: tokens 'a|b c d' = 1^a 00 1^b 0 1^c 0 1^d ; state E on the blank left of it */
    Run*z=head_run; z->len=1000000; Run*last=z; const char*p=argv[3];
    while(*p){ if(*p>='0'&&*p<='9'){ long long v=strtoll(p,(char**)&p,10); Run*r=newrun(1,v); last->next=r; r->prev=last; last=r;
                 while(*p==' ') p++; if(*p=='|'){ p++; Run*q=newrun(0,2); last->next=q;q->prev=last; last=q; } else if(*p){ Run*q=newrun(0,1); last->next=q;q->prev=last; last=q; } }
               else p++; }
    Run*e=newrun(0,1000000); last->next=e; e->prev=last; rightmost=e; head_run=z; off=z->len-1; s=4; pos=0; lo=0; }
  while(steps<MAX){
    int b=head_run->sym;
    if(s==2 && b==1){ long long k=head_run->len-off; steps+=k; pos+=k; off=head_run->len-1; move(1); continue; }   /* C over 1s */
    if(s==4 && b==1){ long long k=off+1; steps+=k; pos-=k; off=0; move(-1); if(pos<lo){ lo=pos; nrec++; if(nrec%every==0){ printf("L "); p128(steps); printf(" stE: "); print_tape(); printf("\n"); fflush(stdout);} } continue; }       /* E over 1s */
    if(s==0 && b==0 && head_run->len==1 && head_run->prev && head_run->prev->sym==1 && head_run->next && head_run->next->sym==1){
      Run*Y=head_run->next, *Zs=Y->next;
      if(Zs && Zs->sym==0 && Zs->len==2 && Zs->next && Zs->next->sym==1 && Y->len>=7){
        long long y=Y->len, k=(y-4)/3;
        steps += (u128)(2*k*y - 3*k*(k-1) + 16*k);
        head_run->prev->len += 2*k; Y->len -= 3*k; Zs->next->len += k; pos += 2*k; loops++;
        continue; } }
    if(T[s][b][2]<0){ printf("HALT at step "); p128(steps); printf("\n"); return 0; }
    write_cell(T[s][b][0]); int d=T[s][b][1]; move(d); pos+=d; s=T[s][b][2]; steps++;
    if(pos<lo){ lo=pos; if(s==4){ nrec++; if(nrec%every==0){ printf("L "); p128(steps); printf(" stE: "); print_tape(); printf("\n"); fflush(stdout);} } }
  }
  printf("END steps "); p128(steps); printf(" left records %lld loop jumps %lld\n",nrec,loops); return 0; }
