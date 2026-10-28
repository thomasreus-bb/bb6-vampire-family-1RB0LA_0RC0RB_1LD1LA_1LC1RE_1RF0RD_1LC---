// compare one Bell of the core with F0=1RB (TM2b) from P (10)^n 11 F> and F0=1LC (TM2b') from P (10)^(n+1) 11 F>
// prints: P n | result_b | result_b'   (result: P' n' or HALT)
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
// core: A 1RB0LA, B 0RC0RB, C 1LD1LA, D 1LC1RE, E 1RF0RD, F0 variant, F1 halt
static int W[6][2]={{1,0},{0,0},{1,1},{1,1},{1,0},{1,0}}, Dd[6][2]={{1,-1},{1,1},{-1,-1},{-1,1},{1,1},{0,0}}, N[6][2]={{1,0},{2,1},{3,0},{2,4},{5,3},{-1,-1}};
static unsigned char tp[200000];
static int bell(const char*P,int n,int variant,char*outP,int*outn,long*steps){
  memset(tp,0,sizeof tp); int p=1000; int L=1000;
  for(const char*c=P;*c&&strcmp(P,"e");c++) tp[p++]=*c-'0';
  for(int i=0;i<n;i++){tp[p++]=1;tp[p++]=0;} tp[p++]=1; tp[p++]=1;
  int q=5; long st=0;
  // F0 transition
  if(variant==0){ W[5][0]=1;Dd[5][0]=1;N[5][0]=1; } else { W[5][0]=1;Dd[5][0]=-1;N[5][0]=2; }
  for(;;){ int b=tp[p]; if(N[q][b]<0) return 1;
    tp[p]=W[q][b]; p+=Dd[q][b]; q=N[q][b]; st++;
    if(q==5&&tp[p]==0&&st>1){ // Bell end?  check tape: P' (10)^m 11 F> 0^inf
      int r=p-1; // expect 11 at r-1,r
      int ok=1; for(int j=p;j<p+50;j++) if(tp[j]) ok=0;
      if(ok&&tp[r]==1&&tp[r-1]==1){ int j=r-2,m=0; while(j>=1&&tp[j]==0&&tp[j-1]==1){m++;j-=2;}
        int a=1; while(a<j&&tp[a]==0) a++;
        int k=0; for(int x=a;x<=j;x++) outP[k++]='0'+tp[x]; outP[k]=0; if(!k) strcpy(outP,"e");
        *outn=m; *steps=st; return 0; } }
    if(st>100000000) return 2; }
}
int main(int c,char**v){ char line[256]; int n0=atoi(v[1]);
  while(fgets(line,sizeof line,stdin)){ line[strcspn(line,"\n")]=0; if(!*line) continue;
    for(int n=n0;n<n0+2;n++){ char Pa[200],Pb[200]; int na,nb; long sa,sb;
      int ra=bell(line,n,0,Pa,&na,&sa), rb=bell(line,n+1,1,Pb,&nb,&sb);
      int agree = (ra==rb) && (ra!=0 || (!strcmp(Pa,Pb) && nb==na+1));
      printf("%s %d | %s | %s | %s\n",line,n, ra?(ra==1?"HALT":"TO"):Pa, rb?(rb==1?"HALT":"TO"):Pb, agree?"agree":"DIFF");
      if(!ra&&!rb&&agree) {} } }
}
