"""Run no. #133 (= 1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_---1LE started in state C, i.e. the table of
1RB0LC_1LC0RE_1LD1LB_1LA1LD_1RF0RA_---1RE mirrored, states CDABEF) with the accelerator of the #581 proof."""
import sys, time
P='/tmp/bbe/holdouts/1RB1RD_1RC1RB_1LD0RA_1RA0LE_1LF0LC_---1LE/py'
sys.path.insert(0, P); sys.path.insert(0, '/tmp/bbe/tools/py')
import accel
from rl import RL, Halt
from canon import canon, show
def run(start_state, tlimit, report=10):
    a = accel.Acc(); a.r = RL(accel.M, state=start_state)
    t0 = time.time(); nxt = report
    try:
        while time.time() - t0 < tlimit:
            a.advance()
            if a.visits >= nxt:
                c = canon(a.r.segs())
                print('visits ~1e%d steps ~1e%d jumps %d direct %d tokens %d t=%.0f | %s' % (len(str(a.visits))-1,
                      len(str(a.r.steps))-1, a.jumps, a.direct, len(c), time.time()-t0, show(c)[:220])); sys.stdout.flush()
                nxt = a.visits * 10**int(sys.argv[3] if len(sys.argv)>3 else 3)
        return a, False
    except Halt:
        return a, True
if __name__ == '__main__':
    st = int(sys.argv[1]); tl = float(sys.argv[2])
    a, h = run(st, tl)
    print('HALT' if h else 'no halt yet', 'visits', a.visits, 'steps ~1e%d' % (len(str(a.r.steps))-1), 'jumps', a.jumps, 'direct', a.direct)
    print('tape:', show(canon(a.r.segs()))[:600])
