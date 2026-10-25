#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static const char*M="1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE";
int W[6][2],D[6][2],N[6][2]; unsigned char tp[1<<16];
// run one band from config; return 0 halt, 1 ok (fills next config), 2 other
int band(int a,int sep,int b,int e,int*o,long long*steps){
  memset(tp,0,sizeof tp); int p=20000,lo=p,i=p; tp[i++]=0; for(int k=0;k<a;k++){tp[i++]=0;tp[i++]=1;}
  if(sep){tp[i++]=0;tp[i++]=0;tp[i++]=1;} for(int k=0;k<b;k++){tp[i++]=1;tp[i++]=1;} if(e)tp[i++]=1; int hi=i-1;
  int q=2; long long st=0;
  while(st<100000000){ int c=tp[p]; if(N[q][c]<0){*steps=st;return 0;} int d=D[q][c]; tp[p]=W[q][c]; p+=d; q=N[q][c]; st++;
    if(p>hi)hi=p; if(p<lo){ lo=p; if(q==2){ int j=lo+1,A=0; while(tp[j]==0&&tp[j+1]==1){A++;j+=2;} int S=0; if(tp[j]==0&&tp[j+1]==0&&tp[j+2]==1){S=1;j+=3;}
        int B=0; while(j+1<=hi&&tp[j]==1&&tp[j+1]==1){B++;j+=2;} int E=0; if(j<=hi&&tp[j]==1){E=1;j++;} o[0]=A;o[1]=S;o[2]=B;o[3]=E; *steps=st; return j==hi+1?1:2; } } }
  return 3; }
int main(int c,char**v){
 for(int i=0;i<6;i++)for(int b=0;b<2;b++){const char*x=M+7*i+3*b; if(x[0]=='-'){N[i][b]=-1;continue;} W[i][b]=x[0]-'0';D[i][b]=x[1]=='R'?1:-1;N[i][b]=x[2]-'A';}
 int R=atoi(v[1]);
 for(int a=0;a<=R;a++)for(int sep=0;sep<2;sep++)for(int b=0;b<=3*R;b++)for(int e=0;e<2;e++){int o[4];long long st; int r=band(a,sep,b,e,o,&st);
   if(r==1) printf("%d %d %d %d -> %d %d %d %d\n",a,sep,b,e,o[0],o[1],o[2],o[3]); else printf("%d %d %d %d -> R%d %lld\n",a,sep,b,e,r,st);}
}
