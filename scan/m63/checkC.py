# Compile first: gcc -O2 -o synC synC.c   Usage: python3 checkC.py 98 | 63r
# check the wiki rules of Marco Dos Santos for no. 98, and the same rules for no. 63 (renamed A->D,B->B,C->C,D->E,E->A,F->F)
import subprocess,re,sys
M={'98':'1RB1LA_1LC0RE_1LF1LD_1RE0LC_1LB1RA_---0LA','63r':'1RB1LA_1LC0RE_1LF1LD_1RB0LC_1LB1RA_---0LA'}
def parse(n,s):
    m=re.fullmatch(r'(1+?)((?:01)*)(1*)011',s) if s.startswith('101') else re.fullmatch(r'(1{4,})((?:01)*)(1*)011',s)
    if not m: return ('?',n,s[:40])
    ones=len(m.group(1)); c=len(m.group(2))//2; d=len(m.group(3))
    # split ones into b+4 and nothing (d belongs to the tail only if (01)^c > 0)
    if c==0: return (n-1,'b+d=',ones+d-4)
    if ones<4: return (n-1-2,ones-4+3,c,d)   # intermediate with b<0: one more step a-2, b+3
    return (n-1,ones-4,c,d)
def norm(a,b,c,d):
    if c==0: return (a,'b+d=',b+4+d-4)
    return (a,b,c,d)
def wiki(a,b,c,d):
    if c==0 and d==6: b,d=b+3,3
    if a>=2: return (a-2,b+3,c,d)
    if c>=2: return (a+b+4,3,c-2,d)
    if c==1 and d==6: return (a+b+4,0,3,3)
    if c==0:
        if b%2==0: return (a,0,b//2+3,3)
        if a==0: return 'HALT'
        return (6,3,(b-1)//2,3)
    # c==1,d==3
    if b%2==1: return (a,0,(b-1)//2+3,6)
    if a==0: return 'HALT'
    if b==0: return (6,0,3,3)
    return (6,3,(b-2)//2,6)
name=sys.argv[1]; T=M[name]; bad=n=0
for a in range(0,12):
  for b in range(0,16):
    for c in range(0,8):
      for d in (3,6):
        o=subprocess.run(['./synC',T,str(a),str(b),str(c),str(d),'100000000'],capture_output=True,text=True).stdout.split()
        got='HALT' if o[0]=='HALT' else (parse(int(o[1]),o[2]) if o[0] not in('MAX','OVF') else o[0])
        w=wiki(a,b,c,d); exp=w if w=='HALT' else norm(*w)
        n+=1
        if got!=exp:
            bad+=1
            if bad<=25: print(name,(a,b,c,d),'machine:',got,' wiki:',exp)
print(name,n,'starts, mismatches',bad)
