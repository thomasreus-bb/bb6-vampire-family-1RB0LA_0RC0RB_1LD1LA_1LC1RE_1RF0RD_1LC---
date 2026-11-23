"""dm90.py - DeepMind acceleration for BB6 candidate 90
1RB1LB_1LC1LA_1RD0LB_1RA1RE_1RF0RD_---1RD (cryptids repo, BB6
Accelerations README, section 2.2).  State E(a, L, d, R): state E reads 0
between encStack(a::L) on the left and encStack(d::R) on the right
(stacks listed from the head outward, entry x = 1^(x+1), separated by
single 0).  Lists: index 0 = next to the head.  step() returns the next
state or None for HALT.  Start: (1, [], 0, []) after 6 TM steps."""

def mu(x): return 'A' if x % 2 == 0 else 'B'

def eta(d, R):
    i = 0
    while True:
        if i == len(R):
            if d % 2: return None
            return (0, [0]*(d//2 + 1) + [1], 0, [])
        e = R[i]; i += 1
        if d % 2: return (0, [0]*(d//2) + [1], e, R[i:])
        d = e + d + 4

def drain(m, L, d, R):
    R = list(R)
    i = 0; pre = []          # pre: entries pushed on R, in push order
    while True:
        if i == len(L):
            Rn = pre[::-1] + R
            if m == 'A': return eta(d + 1, Rn)
            if m == 'B': return eta(d, Rn)
            return (1, [], d, Rn)
        x = L[i]; i += 1
        if m == 'A': m, d = mu(x), x + d + 2
        elif m == 'B':
            if x == 0: m, d = 'BR', d + 1
            else: pre.append(d + 1); m, d = mu(x - 1), x - 1
        else:
            if x == 0: pre.append(d); d = 0
            else: pre.append(d); pre.append(0); m, d = mu(x - 1), x - 1

def step(a, L, d, R):
    if d == 0:
        if not R: return drain(mu(a + 3), L, a + 3, [0])
        return drain(mu(a + 1), L, a + R[0] + 4, R[1:])
    if d % 2:
        if not R: return None
        if d == 1: return (a + 3, L, R[0], R[1:])
        return (0, [0]*((d - 3)//2) + [a + 3] + L, R[0], R[1:])
    L2 = [0]*((d - 2)//2) + [a + 3] + L
    if not R: return drain('A', L2, 0, [0])
    return drain('A', L2, R[0] + 1, R[1:])
