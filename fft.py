import numpy as np

def fft(ROI_profile, timeinterval, periodlimit=60, radius=3):
    """
    FFT spectrum.

    Inputs
    ------
    ROI_profile   : 1D array (time series)
    timeinterval  : sampling interval (s)
    periodlimit   : only search for periods < periodlimit (s)
    radius        : local neighborhood radius for peak detection

    Returns
    -------
    peakT   : dominant period (s)
    peakP   : power at dominant peak
    period  : period axis (s)
    power   : power spectrum (single-sided, no extra normalization)
    """
    ROI_profile = np.asarray(ROI_profile, float)
    ll = len(ROI_profile)

    # Hann window to reduce spectral leakage
    n_idx = np.arange(ll)
    hann = 0.5 - 0.5 * np.cos(2 * np.pi * n_idx / (ll - 1))
    ROI_profile = ROI_profile * hann

    # Rough normalization using order statistics (keeps plots comparable across cells)
    prof_sorted = np.sort(ROI_profile)
    prof_min = np.mean(prof_sorted[:10])
    prof_max = np.mean(prof_sorted[-2:])
    ROI_profile = (ROI_profile - prof_min) / (prof_max - prof_min)

    # FFT with zero-padding
    n = 2048  # if your traces get longer than this, bump to next power of 2
    Y = np.fft.rfft(ROI_profile, n=n)
    power = (Y * np.conj(Y)).real / n  # single-sided power
    freq = np.fft.rfftfreq(n, d=timeinterval)  # Hz

    # Convert to period axis (avoid division by zero at DC)
    period = np.full_like(freq, np.inf, dtype=float)
    period[1:] = 1.0 / freq[1:]

    # Only consider periods shorter than periodlimit
    valid = period < periodlimit
    first = np.where(valid)[0][0]
    last = len(power)  # rfft already stops at Nyquist

    # Find local maxima (radius neighborhood) within the valid period range
    allpeaks = []
    for i in range(first + radius, last - radius):
        if np.all(power[i] >= power[i - radius : i + radius + 1]):
            allpeaks.append(i)
    allpeaks = np.array(allpeaks, dtype=int)

    # Keep only peaks above 2% of max power in the valid range (your original criterion)
    if allpeaks.size == 0:
        return np.nan, np.nan, period, power

    thresh = 0.02 * np.max(power[first:last])
    largepeaks = allpeaks[power[allpeaks] > thresh]

    if largepeaks.size == 0:
        return np.nan, np.nan, period, power

    # Choose the strongest peak
    i0 = largepeaks[np.argmax(power[largepeaks])]
    peakT = period[i0]
    peakP = power[i0]

    return peakT, peakP, period, power