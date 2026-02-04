import numpy as np
import matplotlib.pyplot as plt


def xcorr(x, y, dt, ploton=False, savefig=False, figname=None):
    """
    Cross-correlation of two time series.

    Computes the discrete cross-correlation and returns the phase lag
    (in seconds) corresponding to the maximum correlation.

    x, y : 1D arrays
    dt   : sampling interval (s)
    """
    x = np.asarray(x)
    y = np.asarray(y)
    nt = len(x)

    # time window for plotting (s)
    xlimt = 30

    # cross-correlation (centered)
    cross_corr = np.correlate(x, y, mode='same')
    time_lags = dt * np.arange(-nt // 2 + 1, nt // 2 + 1)

    # phase lag at peak correlation
    phase_lag = time_lags[np.argmax(cross_corr)]

    # rescale correlation to [-1, 1] for visualization
    cross_corr = (
        2 * (cross_corr - np.min(cross_corr))
        / (np.max(cross_corr) - np.min(cross_corr))
        - 1
    )

    if ploton:
        fs = 60
        fig, ax = plt.subplots(figsize=(8, 8), dpi=100)

        ax.plot(time_lags, cross_corr, color='black', linewidth=5)
        ax.scatter(
            phase_lag,
            cross_corr[np.argmax(cross_corr)],
            s=500,
            c='black',
            marker='o'
        )
        ax.axvline(phase_lag, color='r', linestyle='--')
        ax.axvline(0, color='black', linestyle='--')

        ax.set_xlabel('Phase lag (s)', fontsize=fs)
        ax.set_ylabel('Corr. coeff.', fontsize=fs)
        ax.set_xlim(-xlimt, xlimt)
        ax.set_xticks([-xlimt + 10, 0, xlimt - 10])
        ax.set_yticks([])
        ax.set_title(f'{phase_lag:.0f} s', fontsize=fs / 2)

        ax.tick_params(width=5, length=15)
        plt.xticks(fontsize=fs)

        for spine in ax.spines.values():
            spine.set_linewidth(5)

        fig.tight_layout()
        if savefig and figname is not None:
            plt.savefig(figname)
        plt.show()
        plt.close()

    return phase_lag