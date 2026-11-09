import glev2,sys,re
M,st,pre,unit,m,a=sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],int(sys.argv[5]),int(sys.argv[6])
if pre=='-': pre=''
g=glev2.G2(M,st,pre,unit,m,a); form=re.compile(r'1{2,}(01{2,})*')
for n in [int(x) for x in sys.argv[7].split(',')]:
    bad=[]
    for b in range(2,int(sys.argv[8])):
        r,W2=g.pm(n,'1'*b+sys.argv[9],'3000000000')
        if W2 is None: bad.append('%s@%d'%(r,b))
        elif not (form.fullmatch(W2) or W2==''): bad.append(b)
    print(n,n%m,bad[:30])
