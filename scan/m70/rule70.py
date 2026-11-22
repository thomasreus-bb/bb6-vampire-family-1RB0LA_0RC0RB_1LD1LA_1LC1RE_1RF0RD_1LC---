# check the two main level rules of no. 70 (level start S = 1 |x| m |g1| b1 |g2| ...  in state A, x = 6y):
#  x = 2 mod 4, g1 >= 7: -> 1 |3x/2-3| m+12 |g1-6| b1 ...
#  x = 0 mod 4, g1 >= 5: -> 1 |3x/2-6| 11 |m-3| 4 |g1-4| b1 ...
import subprocess,random,sys
random.seed(int(sys.argv[1])); N=int(sys.argv[2]); bad=0
for it in range(N):
    x=6*random.randint(2,100); m=random.choice([11,17,21,23,27,35,47]); g1=random.randint(7,40)
    rest=[]
    for j in range(random.randint(1,5)): rest+=[random.randint(2,16) if j==0 else random.randint(1,30), random.randint(2,16)]
    rest=rest[1:] if False else rest
    # rest starts with b1
    rest=[random.randint(2,16)]+[v for j in range(random.randint(0,4)) for v in (random.randint(1,30),random.randint(2,16))]
    tape=[1,x,m,g1]+rest
    o=subprocess.run(['./syn70','0',' '.join(map(str,tape)),'200000000'],capture_output=True,text=True).stdout.strip()
    got=list(map(int,o.split(':')[1].split())) if 'z0=0' in o else o
    exp=[1,3*x//2-3,m+12,g1-6]+rest if x%4==2 else [1,3*x//2-6,11,m-3,4,g1-4]+rest
    if got!=exp:
        bad+=1
        if bad<6: print(tape,'->',got,'expected',exp)
print(N,'starts, mismatches',bad)
