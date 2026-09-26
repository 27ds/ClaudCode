"""
Wavelettransformation eines Chirp-Signals.

1. Signal in Zeit- und Frequenzdomaene plotten, Fourier- mit
   Wavelettransformation vergleichen (zunehmende Frequenz)
2. Signal mit abnehmender Frequenz
3. Signal mit abnehmender Frequenz + Rauschen
"""

import matplotlib.pyplot as plt
import numpy as np
import pywt
from numpy.fft import rfft, rfftfreq


def gaussian(x, x0, sigma):
    return np.exp(-np.power((x - x0) / sigma, 2.0) / 2.0)


def make_chirp(t, t0, a, abnehmend=False):
    if abnehmend:
        frequency = (a * (1 - t + t0)) ** 2  # laeuft rueckwaerts -> Frequenz nimmt ab
    else:
        frequency = (a * (t + t0)) ** 2
    # Phase = Integral der Frequenz (cumsum = diskretes Integral).
    # sin(2*pi*f*t) waere nur fuer konstante Frequenz korrekt.
    dt = np.diff(t).mean()
    phase = 2 * np.pi * np.cumsum(frequency) * dt
    chirp = np.sin(phase)
    return chirp, frequency


def make_signal(t, abnehmend=False):
    chirp1, frequency1 = make_chirp(t, 0.2, 9, abnehmend)
    chirp2, frequency2 = make_chirp(t, 0.1, 5, abnehmend)
    chirp = chirp1 + 0.6 * chirp2
    chirp *= gaussian(t, 0.5, 0.2)
    return chirp, frequency1, frequency2


def analysieren(time, chirp, frequency1, frequency2, titel):
    sampling_period = np.diff(time).mean()

    # CWT
    wavelet = "cmor1.5-1.0"
    # logarithmische Skalen, wie von Torrence & Compo vorgeschlagen:
    widths = np.geomspace(1, 1024, num=100)
    cwtmatr, freqs = pywt.cwt(chirp, widths, wavelet, sampling_period=sampling_period)
    # Betrag des komplexen Resultats
    cwtmatr = np.abs(cwtmatr[:-1, :-1])

    # Fourier Transformation
    yf = rfft(chirp)
    xf = rfftfreq(len(chirp), sampling_period)

    fig, axs = plt.subplots(3, 1, figsize=(9, 10))
    fig.suptitle(titel)

    # Zeitdomaene
    axs[0].plot(time, chirp)
    axs[0].set_xlabel("Zeit [s]")
    axs[0].set_ylabel("Signal")
    axs[0].set_title("Zeitdomaene")
    axs[0].grid(True)

    # Wavelet (Zeit + Frequenz)
    pcm = axs[1].pcolormesh(time, freqs, cwtmatr)
    axs[1].plot(time, frequency1, "w--", linewidth=1, label="wahre Frequenzen")
    axs[1].plot(time, frequency2, "w--", linewidth=1)
    axs[1].set_yscale("log")
    axs[1].set_ylim(freqs.min(), 500)
    axs[1].set_xlabel("Zeit [s]")
    axs[1].set_ylabel("Frequenz [Hz]")
    axs[1].set_title("Kontinuierliche Wavelet Transformation (Scaleogramm)")
    axs[1].legend(loc="upper right")
    fig.colorbar(pcm, ax=axs[1])

    # Frequenzdomaene (Fourier)
    axs[2].semilogx(xf, np.abs(yf))
    axs[2].set_xlim(1, 500)
    axs[2].set_xlabel("Frequenz [Hz]")
    axs[2].set_ylabel("Amplitude")
    axs[2].set_title("Fourier Transformation")
    axs[2].grid(True)

    fig.tight_layout()
    return fig


# generate signal
time = np.linspace(0, 1, 2000)

# 1. zunehmende Frequenz (Original)
chirp, f1, f2 = make_signal(time, abnehmend=False)
analysieren(time, chirp, f1, f2, "Chirp mit zunehmender Frequenz")

# 2. abnehmende Frequenz
chirp_ab, f1_ab, f2_ab = make_signal(time, abnehmend=True)
analysieren(time, chirp_ab, f1_ab, f2_ab, "Chirp mit abnehmender Frequenz")

# 3. abnehmende Frequenz + Rauschen
rausch_amplitude = 0.5
rng = np.random.default_rng(0)  # fester Seed -> reproduzierbar
chirp_rausch = chirp_ab + rausch_amplitude * rng.normal(size=len(time))
analysieren(time, chirp_rausch, f1_ab, f2_ab,
            "Chirp mit abnehmender Frequenz + Rauschen (Amplitude %.1f)" % rausch_amplitude)

plt.show()

# Vergleich:
# - Die Fourier Transformation zeigt nur, WELCHE Frequenzen vorkommen, nicht WANN.
#   Zunehmender und abnehmender Chirp haben (fast) das gleiche Fourierspektrum.
# - Das Scaleogramm zeigt Zeit UND Frequenz: man sieht, ob die Frequenz steigt oder faellt.
# - Weisses Rauschen verteilt sich ueber alle Frequenzen. In der FFT hebt es den
#   ganzen Untergrund an, im Scaleogramm bleiben die Chirp-Baender gut sichtbar,
#   weil das Rauschen ueber Zeit und Frequenz verschmiert ist.
