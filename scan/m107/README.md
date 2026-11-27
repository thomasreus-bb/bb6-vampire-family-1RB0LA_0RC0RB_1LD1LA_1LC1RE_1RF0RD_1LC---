# No. 107 (`1RB1LD_0RC1RC_1RD0RE_0LA0LF_0RF---_1RA1LA`): exact event orbit and halting horizon (27 Nov 2026)

TM as given (not mirrored). Events = left records in states A, D, F. Tools: `scan/orbit_tools/`
(`runorb.py`, `horizon.py`, `orbit.py`). `orb107.txt`: one line per event (event, state, W, log10 n, u, S).

**Event form.** `W u^n S` with the long periodic run u ∈ {`101`, `011`}, a growing prefix W and a short suffix S
(`100`, `00`, `0100`). In the learned rules n' = (3n + c)/2 in some residue classes and n' = n + c in others
("3/2 Bell").

**Exact orbit:** 3,000 events, n ≈ 10^268 at the end. No HALT.
Learned rules: 1,091 along the orbit, 2,897 after the horizon runs (moduli 1 to 32). **No rule has a HALT entry
in any residue class.**

**Halting horizon (Markov chain over the learned rules, uniform residues):** over 300 sampled orbit keys,
P(HALT within 2 events) = 0 and P(HALT within 4 events) = 0.

**Coin model:** 0 halts in 20,000 macro steps.

**Word search for the HALT condition.** HALT needs the prefix W to end in `...0100` directly in front of the long
011-run. W never has this tail along the orbit (the last four cells of W are `0110` in 2,332 events, `1010` in
576, shorter W in the rest), so the overlap between the reachable prefixes and the halting prefixes is empty in
all observed events.

**Assessment.** No sign of a lottery: HALT is not reachable within 4 events from any sampled configuration, and
the halting tail does not occur. **Probably nonhalting**, or HALT is far away from the observed orbit. There is no
basis for a HALT probability above 90 %.
