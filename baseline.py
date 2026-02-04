import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve


def baseline_asls(y, lam=1e6, p=0.01, niter=10):
    """
    Asymmetric least-squares (AsLS) baseline estimation
    following Eilers & Boelens.

    y     : 1D signal
    lam   : smoothness parameter (larger -> smoother baseline)
    p     : asymmetry parameter (smaller -> baseline stays below peaks)
    niter : number of reweighting iterations
    """
    y = np.asarray(y, float)
    n = len(y)

    # second-difference operator (penalizes curvature)
    D = sparse.diags([1, -2, 1], [0, 1, 2], shape=(n - 2, n))
    w = np.ones(n)

    for _ in range(niter):
        W = sparse.diags(w, 0)
        Z = W + lam * (D.T @ D)
        z = spsolve(Z, w * y)

        # points above baseline are down-weighted
        w = p * (y > z) + (1 - p) * (y <= z)

    return z