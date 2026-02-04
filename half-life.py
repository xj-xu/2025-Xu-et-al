def autocorr_half_life(t, y):
    """
    Compute autocorrelation-based half-life for a single time series.
    Returns tau_1/2 in the same units as t.
    """
    y = np.asarray(y)
    t = np.asarray(t)

    y0 = y - np.mean(y)
    acf_full = np.correlate(y0, y0, mode='full')
    acf = acf_full[acf_full.size // 2:]  # keep non-negative lags
    acf = acf / acf[0]
    dt = np.median(np.diff(t))
    lags = np.arange(len(acf)) * dt
    acf_env = np.abs(acf)
    acf_env[0] = 1.0

    # first time where envelope drops below 0.5
    idx = np.where(acf_env <= 0.5)[0]
    if len(idx) == 0:
        return np.nan  # no crossing

    k = idx[0]
    if k == 0:
        return lags[0]

    # linear interpolation
    t0, t1 = lags[k-1], lags[k]
    y0, y1 = acf_env[k-1], acf_env[k]
    tau_half = t0 + (0.5 - y0) * (t1 - t0) / (y1 - y0)
    return tau_half


def population_autocorr_half_life(excel_file):
    """
    Loop over N columns in an Excel file, compute autocorr half-life
    for each, and return (taus, mean, sem).
    Assumes readtrace(excel_file, column=i) exists.
    """
    taus = []
    N = len(pd.read_excel(excel_file, sheet_name=0,header=None).values[0,:])
    for i in range(N):
        exp,t,x1,x2,bg1,bg2,dnp = readtrace(excel_file, ci=i)
        tau = autocorr_half_life(t, x2)
        taus.append(tau)

    taus = np.array(taus, dtype=float)

    # drop NaNs (failed fits)
    valid = ~np.isnan(taus)
    taus_valid = taus[valid]

    n_valid = len(taus_valid)
    if n_valid == 0:
        raise ValueError("No no oopsy! No valid half-life estimates (all NaN).")

    mean_tau = np.mean(taus_valid)
    sem_tau = np.std(taus_valid, ddof=1) / np.sqrt(n_valid)

    print(f"N valid traces = {n_valid}")
    print(f"Half-life: {mean_tau:.3g} ± {sem_tau:.3g} (mean ± SEM)")

    return taus_valid, mean_tau, sem_tau