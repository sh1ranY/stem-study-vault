# S01 — Original demonstration lecture: RC step response

Authority: authored demonstration. Version: 1. No university or examination-board affiliation.

## Circuit and assumptions

An ideal DC source Vs connects through a resistor R to a node. An ideal capacitor C connects from that node to ground; the source return is also grounded. At t = 0 the source changes from zero to Vs. R and C are positive constants. Unless stated otherwise, the initial capacitor voltage is zero. The output vc is the node voltage relative to ground. Current i flows through R into the capacitor's positive terminal. Ignore parasitics, leakage and loading.

## Governing equation

Kirchhoff's voltage law gives Vs = Ri + vc. The passive-sign-convention capacitor relation is i = C dvc/dt. Therefore RC dvc/dt + vc = Vs for t >= 0.

## Solution and time constant

For zero initial voltage, vc(t) = Vs(1 - exp(-t/(RC))). The time constant is tau = RC, in seconds. At one time constant, vc reaches about 63.2% of its final value. The response approaches Vs asymptotically.

## General initial condition

If vc(0) = V0, then vc(t) = Vs + (V0 - Vs)exp(-t/(RC)). This expression applies to the stated constant-source, first-order ideal model. V0 need not be zero.
