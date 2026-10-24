import subprocess,random,collections
TM='1RB---_0RC0RD_1LD1RB_0LE0LC_1RA0LF_1LD1LE'
random.seed(5); cnt=collections.Counter(); hits=[]
for i in range(int(__import__('sys').argv[1])):
    n=random.randint(300,1500); m=random.randint(1,60)
    T='01'*m+'00'
    o=subprocess.run(['./bstep',TM,'R','C','1','-',T,str(n),'1.15','2000','4000000000'],capture_output=True,text=True).stdout.split()
    cnt[o[0]]+=1
    if o[0]=='HALT': hits.append((n,m))
print(cnt); print('halting configs (n, m):',hits[:30])
