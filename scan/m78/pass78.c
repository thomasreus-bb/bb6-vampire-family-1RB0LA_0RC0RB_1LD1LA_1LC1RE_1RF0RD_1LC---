/* pass78 TM q maxsteps : tape on stdin, head at cell 0 in state q. Runs until the next LEFT record in state E (after step 10)
   or HALT. Tracks turning points of deep excursions (min head position between two right records, measured from the
   left end lo). Prints every turning point below 400 cells as "T pos", and at the end "END status steps len" and the tape. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int W[8][2],D[8][2],NX[8][2];
int main(int c,char**v){ const char*M=v[1]; int q=v[2][0]-'A'; long long mx=atoll(v[3]);
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){NX[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;NX[i][b]=x[2]-'A';}
 static char buf[1<<24]; if(!fgets(buf,sizeof buf,stdin)) return 1; long L=strlen(buf); while(L&&(buf[L-1]=='\n'))L--;
 long SZ=(L+1000)*16+(1<<22); unsigned char*t=calloc(SZ,1); long base=SZ/4; for(long i=0;i<L;i++) t[base+i]=buf[i]-'0';
 long p=base,lo=base,hi=base+L-1,mn=p; long long s=0;
 for(;s<mx;s++){ int b=t[p]; if(NX[q][b]<0){printf("END HALT %lld %ld\n",s,hi-lo+1);return 0;} t[p]=W[q][b]; p+=D[q][b]; q=NX[q][b];
   if(p<mn)mn=p;
   if(p>hi){hi=p; if(mn-lo<400 && hi-mn>20) printf("T %ld\n",mn-lo); mn=p;}
   if(p<lo){lo=p; if(q==4 && s>10){ printf("END REC %lld %ld\n",s+1,hi-lo+1); for(long i=lo;i<=hi;i++) putchar('0'+t[i]); putchar('\n'); return 0;} }
   if(p<2||p>SZ-3){printf("END TAPE\n");return 0;} }
 printf("END MAX %lld\n",s); }
