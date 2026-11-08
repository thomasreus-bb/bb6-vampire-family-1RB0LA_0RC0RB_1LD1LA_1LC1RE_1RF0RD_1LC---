# no. 30 as a nested recursion (checked against direct simulation, see f30.c and test30.py):
#   G(n) = (3n+7)/2              for odd n
#   G(n) = n + G(1 + G(n/2 - 2)) for even n
# evaluating G(0) (only reached from G(4)) is the HALT; an even n that calls itself again never returns (Loop).
# the machine evaluates n -> G(n) forever, starting at n = 1.
# G is evaluated with an explicit stack, so deep recursions are no problem.
class Halt(Exception): pass
class Loop(Exception): pass
calls=0
maxdepth=0
active=set()
def G(n):
    global calls,maxdepth
    stack=[]          # frames [m, stage]
    while True:
        calls+=1
        # descend
        while n%2==0:
            if n==0: raise Halt()
            if n in active: raise Loop(n)
            active.add(n); stack.append([n,0]); n=n//2-2; calls+=1
        v=(3*n+7)//2
        if len(stack)>maxdepth: maxdepth=len(stack)
        # ascend
        while stack:
            f=stack[-1]
            if f[1]==0:
                f[1]=1; n=1+v; break
            stack.pop(); active.discard(f[0]); v=f[0]+v
        else:
            return v
