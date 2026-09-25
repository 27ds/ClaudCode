"""
Gauss'sche Glockenkurve fuer das Blutdruckbeispiel (Aufgabe 02).

- x-Achse von 0 bis 250 mmHg
- Erwartungswert mu = 127 mmHg, Standardabweichung sigma = 7 mmHg
- Wahrscheinlichkeit, einen Wert von 140 mmHg zu messen
- Vergleich: Standardabweichung halbiert bzw. verdoppelt
"""

import numpy as np
import matplotlib.pyplot as pl
import scipy.stats as stats


# Parameter :
x_mess = [125, 129, 140, 121, 127]  # Messwerte aus Aufgabe 02
mu = 127      # Erwartungswert [mmHg]
sigma = 7     # Standardabweichung [mmHg]
x_wert = 140  # gesuchter Messwert [mmHg]

# Kennwerte der Messreihe (zur Kontrolle)
N = len(x_mess)
x_M = np.mean(x_mess)                       # Mittelwert
x_S = np.std(x_mess, ddof=1)                # Standardabweichung (Stichprobe, N-1)
x_Sf = x_S / np.sqrt(N)                     # Standardfehler
x_Med = np.median(x_mess)                   # Median
x_FWHM = 2 * np.sqrt(2 * np.log(2)) * sigma  # Halbwertsbreite der Glockenkurve

# Wahrscheinlichkeit fuer 140 mmHg
# Bei einer stetigen Verteilung ist P(X = 140) exakt 0. Da auf 1 mmHg genau
# gemessen wird, bedeutet "140 mmHg messen": 139.5 <= X < 140.5
dichte_140 = stats.norm.pdf(x_wert, mu, sigma)  # Wahrscheinlichkeitsdichte [1/mmHg]
p_140 = stats.norm.cdf(x_wert + 0.5, mu, sigma) - stats.norm.cdf(x_wert - 0.5, mu, sigma)
p_ab_140 = stats.norm.sf(x_wert, mu, sigma)     # P(X >= 140)

# Output
print("Mittelwert Messreihe:       %.2f mmHg" % x_M)
print("Standardabweichung Messr.:  %.2f mmHg" % x_S)
print("Standardfehler:             %.2f mmHg" % x_Sf)
print("Median:                     %.2f mmHg" % x_Med)
print("Halbwertsbreite (sigma=7):  %.2f mmHg" % x_FWHM)
print()
print("Dichte f(140):              %.5f 1/mmHg" % dichte_140)
print("P(139.5 <= X < 140.5):      %.5f  (= %.2f %%)" % (p_140, 100 * p_140))
print("P(X >= 140):                %.5f  (= %.2f %%)" % (p_ab_140, 100 * p_ab_140))
print()

# Berechnung Normalverteilung
x = np.linspace(0, 250, 2000)

pl.figure(figsize=(10, 6))
for s, farbe in [(sigma / 2, 'tab:green'), (sigma, 'tab:blue'), (2 * sigma, 'tab:red')]:
    y = stats.norm.pdf(x, mu, s)  # Wahrscheinlichkeitsdichte
    pl.plot(x, y, color=farbe, label=r'$\sigma$ = %.1f mmHg' % s)
    print("sigma = %4.1f mmHg: Maximum f(mu) = %.4f 1/mmHg, FWHM = %.1f mmHg"
          % (s, stats.norm.pdf(mu, mu, s), 2 * np.sqrt(2 * np.log(2)) * s))

# Markierung 140 mmHg (auf der Kurve mit sigma = 7)
pl.axvline(mu, color='gray', linestyle='--', linewidth=1, label=r'$\mu$ = %d mmHg' % mu)
pl.plot(x_wert, dichte_140, 'ko', label='f(140) = %.4f' % dichte_140)

pl.title('Normalverteilung Blutdruck')
pl.xlabel('Blutdruck [mmHg]')
pl.ylabel('Wahrscheinlichkeitsdichte [1/mmHg]')
pl.xlim(0, 250)
pl.grid(True)
pl.legend()
pl.savefig('gauss_blutdruck.png', dpi=120)
pl.show()

# Interpretation:
# - sigma halbiert  -> Kurve doppelt so hoch und halb so breit (schmaler, spitzer).
# - sigma verdoppelt -> Kurve halb so hoch und doppelt so breit (flacher).
# Die Flaeche unter der Kurve bleibt immer 1; das Maximum liegt immer bei mu.
