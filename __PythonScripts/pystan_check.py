import pystan
import matplotlib.pyplot

## Ensuring Pystan correctly compiles
model_code = 'parameters {real y;} model {y ~ normal(0,1);}'
model = pystan.StanModel(model_code=model_code)
y = model.sampling().extract()['y']
y.mean()  # with luck the result will be near 0

y.plot()

## 8 Schools Demo

schools_code = """
data {
    int<lower=0> J; // number of schools
    vector[J] y; // estimated treatment effects
    vector<lower=0>[J] sigma; // s.e. of effect estimates
}
parameters {
    real mu;
    real<lower=0> tau;x
    vector[J] eta;
}
transformed parameters {
    vector[J] theta;
    theta = mu + tau * eta;
}
model {
    eta ~ normal(0, 1);
    y ~ normal(theta, sigma);
}
"""

schools_dat = {'J': 8,
               'y': [28, 8, -3, 7, -1, 1, 18, 12],
               'sigma': [15, 10, 16, 11, 9, 11, 10, 18]}

sm = pystan.StanModel(model_code=schools_code)

# the object fit, returned from function stan, stores samples from the posterior distribution.
# The fit object has a number of methods, including plot and extract.
# We can also print the fit object and receive a summary of the posterior samples
# as well as the log-posterior (which has the name lp__).
fit = sm.sampling(data=schools_dat, iter=1000, chains=4)

# Once a model is compiled, we can use the StanModel object multiple times.
# This saves us time compiling the C++ code for the model
fit2 = sm.sampling(data=schools_dat, iter=10000, chains=4)

# The method extract extracts samples into a dictionary of arrays for parameters of interest, or just an array.
la = fit.extract(permuted=True)  # return a dictionary of arrays
mu = la['mu']

## return an array of three dimensions: iterations, chains, parameters
a = fit.extract(permuted=False)
