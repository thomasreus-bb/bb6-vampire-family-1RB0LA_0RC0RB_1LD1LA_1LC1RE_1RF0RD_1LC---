import subprocess
for j in range(1,9):
    t='0001'+'01'*j+'00001'; h=[]
    for n in range(1,1500):
        r=subprocess.run(['./syn18',str(n),t],capture_output=True,text=True,timeout=60).stdout.split()
        if r[0]!=str(r[0]) or not r[0].isdigit(): h.append((n,r[0]))
    print('R%d'%j, h)
