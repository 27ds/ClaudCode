"""
Subplots template: plot complex numbers side by side with matplotlib.

Layout (2 x 2 grid from plt.subplots):
  [0, 0]  Argand diagram of a and b (rectangular form as vectors)
  [0, 1]  a + b, a * b, and the conjugate of a
  [1, 0]  All n-th roots of a on their circle
  [1, 1]  Powers z**k tracing a spiral

Run directly to open the figure and save it as complex_subplots.png.
Requires: pip install matplotlib numpy
"""

import cmath
import math

import matplotlib.pyplot as plt
import numpy as np

from complex_numbers import add, conjugate, modulus, multiply, nth_roots, power

# Fixed categorical order: series 1, 2, 3 ... (never cycled)
SERIES = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
TEXT = "#3d3d3a"
GRID = "#e4e3dc"


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def style_axes(ax: plt.Axes, title: str) -> None:
    """Common look for a complex-plane subplot."""
    ax.set_title(title, loc="left", fontsize=11, color=TEXT)
    ax.axhline(0, color=GRID, linewidth=1, zorder=0)
    ax.axvline(0, color=GRID, linewidth=1, zorder=0)
    ax.grid(True, color=GRID, linewidth=0.6, zorder=0)
    ax.set_xlabel("Re", color=TEXT)
    ax.set_ylabel("Im", color=TEXT)
    ax.set_aspect("equal", adjustable="datalim")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(colors=TEXT, labelsize=8)


def fmt(z: complex) -> str:
    """Short a+bj string with 2 decimals."""
    return f"{z.real:.2f}{z.imag:+.2f}j"


def draw_vector(ax: plt.Axes, z: complex, color: str, label: str | None,
                start: complex = 0j) -> None:
    """Arrow from `start` to `start + z`, labelled at its tip."""
    ax.annotate(
        "", xy=(start.real + z.real, start.imag + z.imag),
        xytext=(start.real, start.imag),
        arrowprops=dict(arrowstyle="-|>", color=color, lw=2),
    )
    tip = start + z
    ax.plot(tip.real, tip.imag, "o", color=color, markersize=6,
            markeredgecolor="white", markeredgewidth=1.5)
    if label:
        ax.annotate(label, (tip.real, tip.imag), textcoords="offset points",
                    xytext=(6, 6), fontsize=8, color=TEXT)


# --------------------------------------------------------------------------
# Individual subplots
# --------------------------------------------------------------------------

def plot_argand(ax: plt.Axes, a: complex, b: complex) -> None:
    draw_vector(ax, a, SERIES[0], f"a = {a}")
    draw_vector(ax, b, SERIES[1], f"b = {b}")
    style_axes(ax, "Argand diagram")


def plot_operations(ax: plt.Axes, a: complex, b: complex) -> None:
    draw_vector(ax, a, SERIES[0], "a")
    draw_vector(ax, b, SERIES[1], None, start=a)  # b drawn head-to-tail
    draw_vector(ax, add(a, b), SERIES[2], f"a + b = {add(a, b)}")
    draw_vector(ax, conjugate(a), SERIES[3], f"conj(a) = {conjugate(a)}")
    style_axes(ax, f"Operations  (a*b = {multiply(a, b)})")


def plot_roots(ax: plt.Axes, z: complex, n: int) -> None:
    roots = nth_roots(z, n)
    radius = modulus(z) ** (1 / n)
    t = np.linspace(0, 2 * math.pi, 200)
    ax.plot(radius * np.cos(t), radius * np.sin(t),
            color=GRID, linewidth=1.5, zorder=1)
    ax.plot([r.real for r in roots], [r.imag for r in roots], "o",
            color=SERIES[0], markersize=8,
            markeredgecolor="white", markeredgewidth=2, zorder=3)
    for i, r in enumerate(roots):
        ax.annotate(f"k={i}", (r.real, r.imag), textcoords="offset points",
                    xytext=(6, 6), fontsize=8, color=TEXT)
    style_axes(ax, f"{n} roots of {z}  (|r| = {radius:.3f})")


def plot_powers(ax: plt.Axes, z: complex, k_max: int) -> None:
    pts = [power(z, k) for k in range(k_max + 1)]
    ax.plot([p.real for p in pts], [p.imag for p in pts], "-o",
            color=SERIES[1], linewidth=2, markersize=6,
            markeredgecolor="white", markeredgewidth=1.5)
    for k, p in enumerate(pts):
        ax.annotate(f"z^{k}", (p.real, p.imag), textcoords="offset points",
                    xytext=(6, 4), fontsize=8, color=TEXT)
    r, theta = cmath.polar(z)
    style_axes(ax, f"Powers of z = {fmt(z)}  (r={r:.2f}, θ={math.degrees(theta):.0f}°)")


# --------------------------------------------------------------------------
# Figure
# --------------------------------------------------------------------------

def make_figure() -> plt.Figure:
    a = complex(3, 4)
    b = complex(1, -2)

    fig, axes = plt.subplots(2, 2, figsize=(11, 10), constrained_layout=True)
    fig.suptitle("Complex numbers in subplots", fontsize=14, color=TEXT)

    plot_argand(axes[0, 0], a, b)
    plot_operations(axes[0, 1], a, b)
    plot_roots(axes[1, 0], a, n=5)
    plot_powers(axes[1, 1], cmath.rect(1.15, math.radians(40)), k_max=8)
    return fig


if __name__ == "__main__":
    fig = make_figure()
    fig.savefig("complex_subplots.png", dpi=120)
    plt.show()
