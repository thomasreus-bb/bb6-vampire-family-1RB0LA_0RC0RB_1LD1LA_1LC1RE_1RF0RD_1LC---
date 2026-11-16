import subprocess,sys
M=sys.argv[1]; H=[]
for t in range(0,64):
    for N in range(1,160):
        r=subprocess.run(['./syn2',M,str(N),str(t),'50000000','D'],capture_output=True,text=True).stdout.split()
        if r[0]=='HALT': H.append((N,t))
print(len(H),"halting; with N>3:",[h for h in H if h[0]>3])
