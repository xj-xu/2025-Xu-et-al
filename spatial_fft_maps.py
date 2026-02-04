import numpy as np
import matplotlib.pyplot as plt
import skimage.io as io
import csv
import time


def load_tif_and_build_roi_traces(
    tif_path,
    bg_csv_path,
    roiw=20,
):
    """
    Load a TIF stack (t, y, x) and build ROI-averaged time series on a square grid.

    tif_path     : path to .tif stack (time-lapse)
    bg_csv_path  : csv with two columns [time, background] (header allowed)
    roiw         : ROI width in pixels (square ROIs)

    Returns
    -------
    Inor : (nroi, nt) normalized ROI traces
    tarr : (nt,) time array (s)
    dt   : mean sampling interval (s)
    par  : ROIs per row/col (grid is par x par)
    """
    # read tif stack: shape = (time, height, width)
    im = io.imread(tif_path)

    # read background time series from csv
    xbg, ybg = [], []
    with open(bg_csv_path, "r") as csvfile:
        lines = csv.reader(csvfile, delimiter=",")
        next(lines)  # skip header
        for row in lines:
            xbg.append(float(row[0]))
            ybg.append(float(row[1]))

    tarr = np.array(xbg)
    dt = np.mean(np.diff(tarr))
    nt = len(tarr)

    # grid partitioning (assumes square field of view)
    par = int(im.shape[1] / roiw)  # ROIs per row
    nroi = par ** 2

    # raw ROI intensities
    I = np.zeros((nroi, nt))
    i = 0
    pixlist = [roiw * a for a in range(par)]
    for top in pixlist:
        for left in pixlist:
            I[i, :] = np.mean(im[:, top:top + roiw, left:left + roiw], axis=(1, 2))
            i += 1

    # normalize using background trace
    Ibg = np.array(ybg)
    Ibg = Ibg - np.min(Ibg)

    Inor = np.zeros((nroi, nt))
    for i in range(nroi):
        Inor[i] = (I[i] - Ibg) / (np.mean(I[i]) - Ibg)

    return Inor, tarr, dt, par


def plot_all_roi_traces(Inor, tarr, par, savefig=False, outpath=None):
    """
    Plot all ROI traces on a par x par grid (quick sanity check).
    """
    fig, axs = plt.subplots(par, par, figsize=(30, 30), sharex=True, sharey=True, dpi=100)

    i = 0
    for col in range(par):
        for row in range(par):
            axs[col, row].plot(tarr, Inor[i], color="black", linewidth=1)
            for axis in ["bottom", "left", "top", "right"]:
                axs[row, col].spines[axis].set_linewidth(0)
            i += 1

    plt.yticks([])
    plt.xticks([])
    fig.tight_layout()

    if savefig and outpath is not None:
        plt.savefig(outpath)

    plt.show()
    plt.close()


def spatial_fft_maps(
    Inor,
    dt,
    par,
    threshold=0.0,
    savefig=False,
    prefix=None,
    fft=None,
):
    """
    Compute spatial maps of dominant period and peak power across a ROI grid.

    Dependencies:
      fft(trace, dt) -> (peakT, peakP)
    where peakT is the dominant period in seconds, peakP is peak power.

    Inputs
    ------
    Inor      : (nroi, nt) normalized ROI traces
    dt        : sampling interval (s)
    par       : grid dimension (par x par)
    threshold : power threshold for filtered period map (set to 0 to skip)
    fft       : function handle, e.g. fft(trace, dt)

    Returns
    -------
    peakTs : (nroi,) peak period per ROI (s)
    peakPs : (nroi,) peak power per ROI
    """
    if fft is None:
        raise ValueError("Please pass fft=... (a function that returns peakT, peakP).")

    start_time = time.time()

    N = Inor.shape[0]
    peakTs = np.zeros(N)
    peakPs = np.zeros(N)

    for i in range(N):
        peakTs[i], peakPs[i] = fft(Inor[i], dt)

    print("Time taken for FFT:", time.time() - start_time, "seconds")

    # --- period map ---
    fig, ax = plt.subplots(1, 1, figsize=(10, 8), dpi=100)
    field = ax.imshow(peakTs.reshape(par, par))
    ax.set_title("Peak period", fontsize=30)
    ax.set_xticks([])
    ax.set_yticks([])
    cbar = plt.colorbar(field)
    cbar.ax.tick_params(labelsize=30)
    cbar.set_label(r"$T_{\mathrm{peak}}$ (s)", fontsize=30)
    fig.tight_layout()
    if savefig and prefix is not None:
        plt.savefig(prefix + "_periodmap.png")
    plt.show()
    plt.close()

    # --- power map ---
    fig, ax = plt.subplots(1, 1, figsize=(10, 8), dpi=100)
    field = ax.imshow(peakPs.reshape(par, par), cmap="gray")
    ax.set_title("Power of peak period", fontsize=30)
    ax.set_xticks([])
    ax.set_yticks([])
    cbar = plt.colorbar(field)
    cbar.ax.tick_params(labelsize=30)
    cbar.set_label(r"$P_{\mathrm{peak}}$", fontsize=30)
    fig.tight_layout()
    if savefig and prefix is not None:
        plt.savefig(prefix + "_powermap.png")
    plt.show()
    plt.close()

    # --- filtered period map ---
    if threshold > 0:
        peakTsfiltered = np.array(peakTs)
        peakTsfiltered[peakPs < threshold] = 0

        fig, ax = plt.subplots(1, 1, figsize=(10, 8), dpi=100)
        field = ax.imshow(peakTsfiltered.reshape(par, par), cmap="gist_earth")
        ax.set_title(r"$T_{\mathrm{peak}}$ with $P_{\mathrm{thres}}$ = %.3f" % threshold, fontsize=30)
        ax.set_xticks([])
        ax.set_yticks([])
        cbar = plt.colorbar(field)
        cbar.ax.tick_params(labelsize=30)
        cbar.set_label(r"$T_{\mathrm{peak}}$ (s)", fontsize=30)
        fig.tight_layout()
        if savefig and prefix is not None:
            plt.savefig(prefix + "_periodmap_Pthres=%.4f.png" % threshold)
        plt.show()
        plt.close()

    return peakTs, peakPs