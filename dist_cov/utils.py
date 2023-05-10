import numpy as np


def param_range(flatchain, alpha=0.05):
    if flatchain.ndim != 1:
        raise ValueError("only pass data for 1 param")

    if alpha <= 0 or alpha >= 1:
        raise ValueError("alpha must be in 0...1 (exclusive)")

    # these bounds are always two-sided
    q = alpha / 2
    return np.nanquantile(flatchain, q=[0.5, q, 1 - q])


def fmt_param_range(flatchain, alpha=0.05, precision=3):
    be, lb, ub = param_range(flatchain, alpha=alpha)

    if not isinstance(precision, int) or precision < 1:
        raise ValueError("precision must be a positive int")

    p = precision

    return f"{be: 0.{p}f} ({lb: 0.{p}f} to {ub: 0.{p}f})"
