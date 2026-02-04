import numpy as np
from scipy.signal import find_peaks


def find_oscillation_peaks(x, t, dt, peakT, f=0.6, Athres=1.0):
    """
    Find peaks in an oscillatory time series.
    
    Inputs
    ------
    x      : 1D array (signal, typically already normalized)
    t      : 1D array (time axis, same length as x)
    dt     : sampling interval (s)
    peakT  : dominant period (s) from FFT
    f      : fraction of peakT used to enforce min peak separation (default 0.6)
    Athres : minimum peak height threshold (default 1.0)

    Returns
    -------
    peaks     : indices of peaks
    peaktime  : t[peaks]
    peakamp   : x[peaks]
    """
    x = np.asarray(x, float)
    t = np.asarray(t, float)

    # min peak distance in samples
    p2p = int((f * peakT) / dt)
    p2p = max(p2p, 1)

    peaks, props = find_peaks(x, height=Athres, distance=p2p)
    peaktime = t[peaks]
    peakamp = x[peaks]

    return peaks, peaktime, peakamp, props
