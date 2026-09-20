"""
Complex number template: create, convert between notations, and calculate.

Notations covered:
  - Rectangular / Cartesian:  a + bj
  - Polar (r, theta):         r * (cos(theta) + j*sin(theta))
  - Exponential:              r * e^(j*theta)

Run directly to see a demo of conversions and arithmetic.
"""

import cmath
import math


# --------------------------------------------------------------------------
# Conversions between writing styles
# --------------------------------------------------------------------------

def rect_to_polar(z: complex) -> tuple[float, float]:
    """a + bj  ->  (r, theta_radians)"""
    r, theta = cmath.polar(z)
    return r, theta


def polar_to_rect(r: float, theta: float) -> complex:
    """(r, theta_radians)  ->  a + bj"""
    return cmath.rect(r, theta)


def rect_to_exponential_str(z: complex) -> str:
    """a + bj  ->  'r * e^(j*theta)' as a readable string"""
    r, theta = cmath.polar(z)
    return f"{r:.4f} * e^(j*{theta:.4f})"


def polar_to_polar_str(r: float, theta: float, degrees: bool = False) -> str:
    """(r, theta)  ->  'r * (cos(theta) + j*sin(theta))' as a readable string"""
    angle = math.degrees(theta) if degrees else theta
    unit = "deg" if degrees else "rad"
    return f"{r:.4f} * (cos({angle:.4f}{unit}) + j*sin({angle:.4f}{unit}))"


def deg_to_rad(degrees: float) -> float:
    return math.radians(degrees)


def rad_to_deg(radians: float) -> float:
    return math.degrees(radians)


# --------------------------------------------------------------------------
# Basic calculations
# --------------------------------------------------------------------------

def add(a: complex, b: complex) -> complex:
    return a + b


def subtract(a: complex, b: complex) -> complex:
    return a - b


def multiply(a: complex, b: complex) -> complex:
    return a * b


def divide(a: complex, b: complex) -> complex:
    return a / b


def conjugate(z: complex) -> complex:
    return z.conjugate()


def modulus(z: complex) -> float:
    """|z|, the distance from the origin"""
    return abs(z)


def argument(z: complex, degrees: bool = False) -> float:
    """angle (theta) of z relative to the positive real axis"""
    theta = cmath.phase(z)
    return math.degrees(theta) if degrees else theta


def power(z: complex, n: float) -> complex:
    return z ** n


def nth_roots(z: complex, n: int) -> list[complex]:
    """All n complex nth-roots of z."""
    r, theta = cmath.polar(z)
    r_root = r ** (1 / n)
    return [
        cmath.rect(r_root, (theta + 2 * math.pi * k) / n)
        for k in range(n)
    ]


# --------------------------------------------------------------------------
# Demo
# --------------------------------------------------------------------------

def _demo() -> None:
    a = complex(3, 4)       # 3 + 4j
    b = complex(1, -2)      # 1 - 2j

    print("=== Writing styles for a =", a, "===")
    r, theta = rect_to_polar(a)
    print(f"Rectangular : {a}")
    print(f"Polar       : r={r:.4f}, theta={theta:.4f} rad ({rad_to_deg(theta):.2f} deg)")
    print(f"Polar (str) : {polar_to_polar_str(r, theta)}")
    print(f"Exponential : {rect_to_exponential_str(a)}")
    print(f"Back to rect from polar: {polar_to_rect(r, theta)}")

    print("\n=== Basic arithmetic with a =", a, "and b =", b, "===")
    print(f"a + b = {add(a, b)}")
    print(f"a - b = {subtract(a, b)}")
    print(f"a * b = {multiply(a, b)}")
    print(f"a / b = {divide(a, b)}")
    print(f"conjugate(a) = {conjugate(a)}")
    print(f"|a| (modulus)   = {modulus(a):.4f}")
    print(f"arg(a) (radians) = {argument(a):.4f}")
    print(f"arg(a) (degrees) = {argument(a, degrees=True):.2f}")

    print("\n=== Powers and roots ===")
    print(f"a ** 2 = {power(a, 2)}")
    print(f"a ** 0.5 (principal sqrt) = {power(a, 0.5)}")
    print("All cube roots of a:")
    for i, root in enumerate(nth_roots(a, 3)):
        print(f"  root[{i}] = {root}")


if __name__ == "__main__":
    _demo()
