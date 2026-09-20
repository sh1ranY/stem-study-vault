# S02 — Original demonstration practice sheet

Authority: authored demonstration. Version: 1. Questions and final answers are original examples for this repository, not official assessment material.

## P1

A series RC circuit has R = 2 kiloohms and C = 50 microfarads. A 12 V step is applied at t = 0; the capacitor starts uncharged. (a) Find the time constant. (b) Find the capacitor voltage at t = 0.1 s. (c) Explain what doubling R does to the final voltage and the time taken to reach a fixed fraction of it.

## P2

For R = 1 kiloohm, C = 100 microfarads and a 5 V step with zero initial capacitor voltage, find the first time the output reaches 90% of its final voltage. Does it ever reach exactly 5 V at a finite time in this model?

## P3

An ideal series RC circuit has a constant 5 V source for t >= 0, time constant 0.1 s and initial capacitor voltage 2 V. (a) Find vc(t). (b) Find vc(0.1 s). (c) If the initial voltage were 7 V instead, would the voltage initially rise or fall? Explain using the governing equation.

## Final answers

P1: (a) 0.1 s; (b) approximately 7.585 V; (c) final voltage stays 12 V, and the time to any fixed fraction strictly between 0 and 1 doubles.

P2: approximately 0.23026 s. Exact final voltage is approached only in the limit as t tends to infinity.

P3: (a) vc(t) = 5 - 3 exp(-t/0.1) V; (b) approximately 3.896 V; (c) falls, since the initial derivative is (5-7)/0.1 = -20 V/s.
