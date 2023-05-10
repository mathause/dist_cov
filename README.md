# Distributions with covariates

Authors: Mathias Hauser<sup>1</sup>, Dominik Schumacher<sup>1</sup>, Sonia I. Seneviratne<sup>1</sup>

<sup>1</sup>Institute for Atmospheric and Climate Science, Department of Environmental Systems Science, ETH Zurich, Zurich, Switzerland

Conditional distributions with covariates

**Warning**: this package does currently not have any tests.

## Approach

We use distributions where one (or more) parameter is dependent on a covariate - e.g. the global mean temperature ($T_{glob}$). for the normal distribution model the mean ($\mu$) and standard deviation ($\sigma$) as follows:

$\mu' = \beta_0 + \beta_1 * T_{glob}$

$\sigma' = \sigma$

As no such distribution is available in python we adapt distributions in scipy (e.g. [scipy.stats.norm](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html)).


## Installation

### Dependencies

dist_cov depends on the python packages emcee, numpy, and scipy. To run the examples corner.py, matplotlib, and xarray are required as well.


### Install development version

dist_cov is not available from pypi or conda-forge, therefore it needs to be installed using pip directly from github.

```bash
pip install git+https://github.com/mathause/dist_cov
```

To run the examples also install:

```bash
pip install corner matplotlib xarray
```

### Install latest released version

Go to the [newest release on github](https://github.com/mathause/dist_cov/releases/latest), copy the URL of the `*.tar.gz` source file at the botton and then use pip to install it (i.e., `pip install ...`).

## Documentation

Documentation is sparse, but check the [examples](./examples).

## Citing dist_cov

Please cite Hauser et al. ([2017](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1002/2017EF000612)) if you are using dist_cov.

## History

This code was originally developed for Hauser et al. ([2017](https://agupubs.onlinelibrary.wiley.com/doi/abs/10.1002/2017EF000612)) based on the approach described in Coles ([2001](https://link.springer.com/book/10.1007/978-1-4471-3675-0); Chapter 3).
It has been employed in several rapid attribution studies under the auspices of the world weather attribution group, namely:
- Siberian heatwave of 2020 (Ciavarella et al., [2020](https://www.worldweatherattribution.org/siberian-heatwave-of-2020-almost-impossible-without-climate-change/) and Ciavarella et al., [2021](https://link.springer.com/article/10.1007/s10584-021-03052-w))
- Western North American heat wave of 2021 (Philip et al., [2021](https://www.worldweatherattribution.org/western-north-american-extreme-heat-virtually-impossible-without-human-caused-climate-change/) and Philip et al., [2022](https://esd.copernicus.org/articles/13/1689/2022/))
- Indian heat wave of 2022 (Zachariah, et al., [2022](https://www.worldweatherattribution.org/climate-change-made-devastating-early-heat-in-india-and-pakistan-30-times-more-likely/) and Zachariah et al., in review)
- UK heatwave of 2022 (Zachariah et al. [2022](https://www.worldweatherattribution.org/without-human-caused-climate-change-temperatures-of-40c-in-the-uk-would-have-been-extremely-unlikely/))
- Northern Hemisphere droughts of 2022 (Schumacher et al., [2022](https://www.worldweatherattribution.org/high-temperatures-exacerbated-by-climate-change-made-2022-northern-hemisphere-droughts-more-likely/) and Schumacher et al., in review)

It further builds the starting point for modelling extremes in MESMER-X (Quilcaille et al., [2022](https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2022GL099012)).


## License

This project is published under a MIT license.


## References

- Ciavarella, A., Cotterill, D., Stott, P., ... Hauser, M., et al. Prolonged Siberian heat of 2020 almost impossible without human influence. Climatic Change 166, 9 (2021). https://doi.org/10.1007/s10584-021-03052-w
- Coles, S. (2001), An Introduction to Statistical Modeling of Extreme Values, vol. 208, Springer, London.
- Hauser, M., Gudmundsson, L., Orth, R., Jézéquel, A., Haustein, K., Vautard, R., van Oldenborgh, G.J., Wilcox, L. and Seneviratne, S.I. (2017), Methods and Model Dependency of Extreme Event Attribution: The 2015 European Drought. Earth's Future, 5: 1034-1043. https://doi.org/10.1002/2017EF000612
- Philip, S. Y., Kew, S. F., van Oldenborgh, G. J., Anslow, F. S., Seneviratne, S. I., Vautard, R., Coumou, D., Ebi, K. L., Arrighi, J., Singh, R., van Aalst, M., Pereira Marghidan, C., Wehner, M., Yang, W., Li, S., Schumacher, D. L., Hauser, M., Bonnet, R., Luu, L. N., Lehner, F., Gillett, N., Tradowsky, J. S., Vecchi, G. A., Rodell, C., Stull, R. B., Howard, R., and Otto, F. E. L.: Rapid attribution analysis of the extraordinary heat wave on the Pacific coast of the US and Canada in June 2021, Earth Syst. Dynam., 13, 1689–1713, https://doi.org/10.5194/esd-13-1689-2022, 2022.
- Quilcaille, Y., Gudmundsson, L., Beusch, L., Hauser, M., & Seneviratne, S. I. (2022). Showcasing MESMER-X: Spatially resolved emulation of annual maximum temperatures of Earth System Models. Geophysical Research Letters, 49, e2022GL099012. https://doi.org/10.1029/2022GL099012
