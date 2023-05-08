
import numpy as np
import scipy.stats as ss
from scipy.optimize import minimize


class distribution_with_covariate:
    """parent class for a distribution with covariate"""

    # set the distribution, e.g. `ss.norm`
    distribution = None

    def __init__(self, data, cov):

        self.data = data
        self.cov = cov

    def _inital_guess(self):
        """initial guess of the params for self.fit"""

        raise NotImplementedError()

    def get_params(self, args, cov):
        """apply covariates to params

        Parameters
        ----------
        args : parameters
            Parameters of the function.
        cov : float
            Covariate for which to evaluate the parameters

        Notes
        -----
        This translates the covariates into

        """

        raise NotImplementedError(
            "Must return `loc, scale`, or  `shape, loc, scale` (in this order)"
        )

    def prior(self, args):
        """prior on the paramters - overwrite if necessary"""

        return 0

    def loglike(self, args):
        """log-likelihood

        Parameters
        ----------
        args : parameters
            Parameters for which to evaluate the function.

        Notes
        -----
        Must return -inf if the function is undefined for the passed args.

        """

        params = self.get_params(args, self.cov)

        logpdfsum = self.distribution.logpdf(self.data, *params).sum()

        # maybe add prior
        logpdfsum += self.prior(args)

        # must return -inf on invalid input
        if np.isnan(logpdfsum):
            return -np.inf
        else:
            return logpdfsum

    def neg_loglike(self, args):
        """negative log likelihood (for fit)"""

        return -self.loglike(args)

    def fit(self):
        """make a first fit (to initialize walkers)

        Returns
        -------
        params : array of parameters
            Parameters of the best estimate of the parameters

        Raises
        ------
        ValueError if not estimate can be found.

        Notes
        -----
        This is often the hardest to generalize.
        """

        inital_guess = self._inital_guess()

        # find the best estimate by minimalizing the log likelyhood
        m = minimize(
            self.neg_loglike,
            x0=inital_guess,
            method="Nelder-Mead",
            options={"xtol": 1e-5},
        )

        if m.success:
            return m.x
        else:
            raise ValueError("Could not obtain an initial fit.")

    def predict(self, args, cov):
        """predict given a set of params and covariates (the location)"""

        params = self.get_params(args, cov)

        # return loc
        return params[-1]

    def cdf(self, event, args, cov):
        """cummulative distribution function

        Parameters
        ----------
        event : float
            Quantiles (for which to evaluate the function).
        args : parameters
            Parameters of the function.
        cov : float
            Covariate for which to evaluate the parameters
        """

        params = self.get_params(args, cov)

        return self.distribution.cdf(event, *params)

    def ppf(self, q, args, cov):
        """Percent point function (inverse of cdf)

        Parameters
        ----------
        q : array_like
            lower tail probability
        args : parameters
            Parameters of the function.
        cov : float
            Covariate for which to evaluate the parameters
        """

        params = self.get_params(args, cov)

        return self.distribution.ppf(q, *params)

    def sf(self, event, args, cov):
        """survival function (1 - cdf)

        Parameters
        ----------
        event : float
            Quantiles (for which to evaluate the function).
        args : parameters
            Parameters of the function.
        cov : float
            Covariate for which to evaluate the parameters
        """

        params = self.get_params(args, cov)

        return self.distribution.sf(event, *params)

    def isf(self, q, args, cov):
        """Inverse survival function (inverse of sf)

        Parameters
        ----------
        q : array_like
            lower tail probability
        args : parameters
            Parameters of the function.
        cov : float
            Covariate for which to evaluate the parameters

        """

        params = self.get_params(args, cov)

        return self.distribution.isf(q, *params)


class norm_cov:
    """normal distribution with covariate for the location

    Parameters
    ----------
    data : 1D array
        Array of data to fit.
    cov : 1D array
        Array of data to use as covariate.

    Notes
    -----
    model:
    - mu = b0 + b1 * cov
    - sigma = scale
    """

    distribution = ss.norm

    def get_params(self, args, cov):
        """apply covariates to params

        Parameters
        ----------
        args : parameters
            Parameters of the function.
        cov : float
            Covariate for which to evaluate the parameters

        """

        b0, b1, scale = np.asarray(args).T
        loc = b0 + b1 * cov

        return loc, scale

    def _inital_guess(self):
        """initial guess of the params for self.fit"""

        return [np.mean(self.data), 0, np.std(self.data)]


class norm_cov_scale_climexp(distribution_with_covariate):
    """normal distribution with covariate (for location & scale)

    Parameters
    ----------
    data : 1D array
        Array of data to fit.
    cov : 1D array
        Array of data to use as covariate.


    Notes
    -----
    According to the Climate Explorer with:
    - $\mu' = \mu exp(\alpha T / \mu)$
    - $\sigma' = \sigma \exp(\alpha T / \mu)$

    model:
    - loc (mu) = loc0 * exp(a * cov / loc0)
    - scale (sigma) = scale0 * exp(a * cov / loc0)
    """

    def get_params(self, args, cov):
        """apply covariates to params

        Parameters
        ----------
        args : parameters
            Parameters of the function.
        cov : float
            Covariate for which to evaluate the parameters

        """

        loc0, scale0, a = np.asarray(args).T

        # calculate loc & scale for each value of covariate
        loc = loc0 * np.exp(a * cov / loc0)
        scale = scale0 * np.exp(a * cov / loc0)

        # loc0 cannot be 0, and scale must be > 0
        if loc0 == 0 or (scale <= 0).any():
            return np.nan, np.nan

        return loc, scale


    def _inital_guess(self):
        """initial guess of the params for self.fit"""

        return [np.mean(self.data), np.std(self.data), 0]


class gev_cov(distribution_with_covariate):
    """ GEV distribution with covariate for location

    Parameters
    ----------
    data : 1D array
        Array of data to fit.
    cov : 1D array
        Array of data to use as covariate.
    constrain : float or None, default: None
        If set applies a constrain to the shape parameter.

    Notes
    -----
    Model:
    - shape = shape
    - mu = b0 + b1 * cov
    - sigma = scale

    Shape:
    - The shape has a different sign convention than scipy

    Constrain:
    - the constrain sets a gaussian prior for the shape parameter
    - constrain /2 = standard deviation of this gaussian prior
    """

    distribution = ss.genextreme

    def __init__(self, data, cov, constrain=None):

        self.data = data
        self.cov = cov

        # normal distribution with sd=0 is not valid
        if np.isclose(constrain, 0):
            print("setting constrain to None")
            constrain = None

        if constrain is not None:

            # need to half the constrain to be consistent with climate explorer
            constrain /= 2

            def _prior(self, args):

                # return logpdf of a normal distribution
                # pass shape (args[0])
                return ss.norm(loc=0, scale=constrain).logpdf(args[0])

            # overwrite the default priot
            self.prior = _prior

    def _inital_guess(self):
        return [-0.15, np.mean(self.data), 0, np.std(self.data)]

    def get_params(self, args, cov):

        shape, b0, b1, scale = np.asarray(args).T

        # different sign convention than scipy!
        shape = -shape
        loc = b0 + b1 * cov

        return shape, loc, scale
