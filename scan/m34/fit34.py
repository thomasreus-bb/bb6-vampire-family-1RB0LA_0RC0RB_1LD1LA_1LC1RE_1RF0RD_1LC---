import subprocess,sys
sys.path.insert(0,'../m50'); import fast50
T='1RB1RB_1LC0RE_---1LD_1LA1LB_1RA1LF_0LE1LE'
res={}
for a in range(0,40):
  for c in range(0,40):
    o=subprocess.run(['./syn34',str(a),str(c),'2000000',T],capture_output=True,text=True).stdout.split()
    res[(a,c)]=o
import pickle; pickle.dump(res,open('syn34.pkl','wb'))
same=diff=0
for (a,c),o in sorted(res.items()):
    r50=fast50.step(a,c)
    r=None if o[0]=='HALT' else ('?' if o[0] in('MAX','OVF') else (int(o[0]),int(o[1])))
    if r==r50: same+=1
    else:
        diff+=1
        if diff<60: print(a,c,'34:',r,' 50:',r50)
print('same',same,'diff',diff)
