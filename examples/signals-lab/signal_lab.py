"""Deterministic numerical checks for signals and systems.

This lab checks selected hand-derived Fourier-transform, convolution and
sampling results. It deliberately uses NumPy plus Matplotlib and selects a
non-interactive backend so it can run in CI or from a terminal without a display.

Run from this directory:
python3 signal_lab.py --check-only --json
"""
from pathlib import Path
import argparse
import json
import sys

try:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError as exc:  # pragma: no cover - environment guidance
    raise SystemExit(
        "Missing dependency. Install with: pip install numpy matplotlib"
    ) from exc


OUT = Path(__file__).resolve().parent
FIGURES = (
    "p3_transform_pair.png",
    "p3_convolution_theorem.png",
    "p3_sampling_aliasing.png",
)


def assert_close(name, actual, expected, atol, results):
    """Record a deterministic numerical assertion and fail loudly."""
    error = float(np.max(np.abs(np.asarray(actual) - np.asarray(expected))))
    passed = error <= atol
    results[name] = {"passed": passed, "max_abs_error": error, "atol": atol}
    if not passed:
        raise AssertionError(f"{name}: error {error:.6g} exceeds {atol:.6g}")


def transform_pair_check(write_figures, results):
    """Check exp(-2|t|) <-> 4/(4+w^2) with a quadrature CTFT."""
    dt = 0.002
    t = np.arange(-10.0, 10.0 + dt, dt)
    x = np.exp(-2.0 * np.abs(t))
    omega = np.linspace(-12.0, 12.0, 241)
    numeric = np.trapezoid(x[None, :] * np.exp(-1j * omega[:, None] * t), t, axis=1)
    analytic = 4.0 / (4.0 + omega**2)
    assert_close("ctft_exp_two_sided", numeric, analytic, 2.0e-5, results)

    energy_time = np.trapezoid(np.abs(x) ** 2, t)
    omega_energy = np.linspace(-200.0, 200.0, 200001)
    spectrum_energy = 4.0 / (4.0 + omega_energy**2)
    energy_freq = np.trapezoid(np.abs(spectrum_energy) ** 2, omega_energy) / (2.0 * np.pi)
    assert_close("parseval_exp_two_sided_time", energy_time, 0.5, 3.0e-6, results)
    assert_close("parseval_exp_two_sided_frequency", energy_freq, 0.5, 1.0e-6, results)

    if write_figures:
        fig, axes = plt.subplots(2, 1, figsize=(9, 6))
        axes[0].plot(t, x)
        axes[0].set(xlabel="t (s)", ylabel="x(t)", title="x(t)=exp(-2|t|)")
        axes[1].plot(omega, analytic, label="analytic")
        axes[1].plot(omega, numeric.real, "--", label="numerical CTFT")
        axes[1].set(xlabel="omega (rad/s)", ylabel="X(omega)", title="CTFT pair check")
        for axis in axes:
            axis.grid(True)
        axes[1].legend()
        fig.tight_layout()
        fig.savefig(OUT / FIGURES[0], dpi=160)
        plt.close(fig)


def convolution_check(write_figures, results):
    """Check rect(t/2)*rect(t/4) and Y(w)=X(w)H(w)."""
    dt = 0.002
    t = np.arange(-4.0, 4.0 + dt, dt)
    x = (np.abs(t) < 1.0).astype(float)
    h = (np.abs(t) < 2.0).astype(float)
    y = np.convolve(x, h, mode="full") * dt
    ty = np.arange(2.0 * t[0], 2.0 * t[-1] + dt, dt)[: len(y)]
    analytic_y = np.where(
        np.abs(ty) <= 1.0,
        2.0,
        np.where(np.abs(ty) < 3.0, 3.0 - np.abs(ty), 0.0),
    )
    # Boundary pixels differ by one rectangle endpoint; exclude a narrow grid halo.
    mask = (np.abs(np.abs(ty) - 1.0) > 2.5 * dt) & (np.abs(np.abs(ty) - 3.0) > 2.5 * dt)
    assert_close("rect_convolution_time", y[mask], analytic_y[mask], 4.1e-3, results)

    omega = np.linspace(-12.0, 12.0, 241)
    numeric_y = np.trapezoid(y[None, :] * np.exp(-1j * omega[:, None] * ty), ty, axis=1)
    analytic_Y = 8.0 * np.sinc(omega / np.pi) * np.sinc(2.0 * omega / np.pi)
    assert_close("rect_convolution_frequency", numeric_y, analytic_Y, 1.3e-2, results)
    assert_close("rect_convolution_area", np.trapezoid(y, ty), 8.0, 1.3e-2, results)

    if write_figures:
        fig, axes = plt.subplots(2, 1, figsize=(9, 6))
        axes[0].plot(ty, y, label="numerical convolution")
        axes[0].plot(ty, analytic_y, "--", label="overlap-length result")
        axes[0].set(xlabel="t (s)", ylabel="y(t)", title="Rectangular-pulse convolution")
        axes[1].plot(omega, analytic_Y, label="X(omega)H(omega)")
        axes[1].plot(omega, numeric_y.real, "--", label="CTFT of numerical y")
        axes[1].set(xlabel="omega (rad/s)", ylabel="Y(omega)", title="Convolution theorem")
        for axis in axes:
            axis.grid(True)
            axis.legend()
        fig.tight_layout()
        fig.savefig(OUT / FIGURES[1], dpi=160)
        plt.close(fig)


def sampling_check(write_figures, results):
    """Check 1300 Hz sampled at 2000 Hz aliases to 700 Hz."""
    fs = 2000.0
    n = np.arange(0, 2000)
    original_samples = np.cos(2.0 * np.pi * 1300.0 * n / fs)
    alias_samples = np.cos(2.0 * np.pi * 700.0 * n / fs)
    assert_close("sampling_alias_identity", original_samples, alias_samples, 3.0e-12, results)

    spectrum = np.fft.rfft(original_samples)
    frequencies = np.fft.rfftfreq(len(n), d=1.0 / fs)
    peak_hz = float(frequencies[np.argmax(np.abs(spectrum))])
    assert_close("sampling_alias_fft_peak_hz", peak_hz, 700.0, 1.0e-12, results)

    fs_safe = 8000.0
    desired = np.array([1000.0, 3200.0])
    normalized = 2.0 * np.pi * desired / fs_safe
    assert_close("sampling_normalized_frequencies", normalized, [np.pi / 4.0, 0.8 * np.pi], 1.0e-14, results)

    if write_figures:
        fig, axes = plt.subplots(2, 1, figsize=(9, 6))
        axes[0].plot(n[:20], original_samples[:20], "o-", label="1300 Hz samples")
        axes[0].plot(n[:20], alias_samples[:20], "x--", label="700 Hz samples")
        axes[0].set(xlabel="sample n", ylabel="amplitude", title="Identical undersampled sequences")
        axes[1].stem(frequencies, np.abs(spectrum) / len(n), basefmt=" ")
        axes[1].set(xlim=(0, 1000), xlabel="frequency (Hz)", ylabel="|X[k]|/N", title="FFT peak at 700 Hz alias")
        for axis in axes:
            axis.grid(True)
        axes[0].legend()
        fig.tight_layout()
        fig.savefig(OUT / FIGURES[2], dpi=160)
        plt.close(fig)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-only", action="store_true", help="run assertions without writing PNG files")
    parser.add_argument("--json", action="store_true", help="print machine-readable assertion results")
    args = parser.parse_args(argv)

    results = {}
    write_figures = not args.check_only
    transform_pair_check(write_figures, results)
    convolution_check(write_figures, results)
    sampling_check(write_figures, results)
    summary = {"checks": len(results), "passed": sum(item["passed"] for item in results.values()), "results": results}
    if args.json:
        print(json.dumps(summary, indent=2, sort_keys=True))
    else:
        print(f"ELEC270 P3 numerical checks: {summary['passed']}/{summary['checks']} passed")
        if write_figures:
            print("Wrote: " + ", ".join(str(OUT / name) for name in FIGURES))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        sys.exit(1)
