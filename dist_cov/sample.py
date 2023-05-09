import warnings

import emcee


def glm_mcmc(model, n_walker=50, burn_in=500, production=1000, print_info=True):
    warnings.warn(
        "`glm_mcmc` is deprecated, please use `run_mcmc` instead (which no longer "
        "returns the `model` )"
    )

    sampler = run_mcmc(
        model,
        n_walker=n_walker,
        burn_in=burn_in,
        production=production,
        print_info=print_info,
    )

    return model, sampler


def run_mcmc(model, n_walker=50, burn_in=500, production=1000, print_info=True):
    """mcmc sample a scipy-derived distribution using emcee

    Parameters
    ----------
    model : distribution
        Distribution to sample. Requires at least the `fit` and `loglike` methods.
    n_walker : int, default: 50
        Number of parallel walkers to sample.
    burn_in : int, default: 500
        Number of burn in steps to perform before the actual sampling. Ensures the
        starting positions are properly distributed.
    production : int, default: 1000
        Number of production steps to run.
    print_info : bool, default: True
        Whether to show debug info.
    """

    # run model with mcmc

    # best estimate (MLE)
    params = model.fit()

    # get params as starting point
    ndim = len(params)

    # set up the MCMC algorithm
    sampler = emcee.EnsembleSampler(n_walker, ndim, model.loglike)

    # starting positions as ball around best estimate
    p0 = emcee.utils.sample_ball(params, ndim * [0.0001], n_walker)

    if print_info:
        print("Running burn-in...")

    p1, _, _ = sampler.run_mcmc(p0, burn_in)
    sampler.reset()

    if print_info:
        print("Running production...")

    sampler.run_mcmc(p1, production)

    return sampler
