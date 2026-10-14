# Signals and systems numerical lab / 信号与系统数值实验

A standalone Python companion to handwritten derivations, adapted from a personal learning script. No university slides, assignment statements or personal learning records are included. AI-assisted learning material; these numerical checks do not establish teaching effectiveness.

## Run

Python 3.10+ is recommended. From this directory, preferably in a virtual environment:

```sh
python3 -m pip install -r requirements.txt
python3 signal_lab.py --check-only --json
python3 signal_lab.py
```

The first command mode checks without writing figures. The second creates three PNGs beside the script. Matplotlib uses a non-interactive backend. NumPy 2 is required for `np.trapezoid`.

## Experiments

1. Compare the numerical continuous-time Fourier transform of `exp(-2|t|)` with `4/(4+ω²)` and check Parseval energy.
2. Compare rectangular-pulse convolution with its overlap-length expression and frequency-domain product.
3. Show why a 1300 Hz cosine sampled at 2000 Hz matches a 700 Hz sequence; confirm the FFT peak and normalized frequencies.

[Transform and energy](p3_transform_pair.png) · [Convolution](p3_convolution_theorem.png) · [Aliasing](p3_sampling_aliasing.png)

Finite integration windows and grids introduce approximation error. The rectangular-pulse test excludes small boundary neighborhoods; tolerances are explicit in the script. Passing checks establishes consistency for these chosen cases, not a proof for every input. See [recorded results](validation.json).

中文：先运行检查，再看图与手算结果是否一致。改变采样频率、积分区间或时间步长时，应同时理解误差和容差；不要仅以程序通过代替推导。脚本是独立示例，不依赖私人知识库路径，也不代表整门课的覆盖。

Verified on 14 October 2026: **9/9 checks passed**, Python 3.12 with NumPy 2.5.4 and Matplotlib 3.11.2. The three output plots were visually inspected.
