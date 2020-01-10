import pystan

## Fitting hierarchical bayesian model for prediction of speed/accuracy on mean estimation task for circular data


schools_code = """
data {
    int<lower=0> J; // number of schools
    vector[J] y; // estimated treatment effects
    vector<lower=0>[J] sigma; // s.e. of effect estimates
}
parameters {
    real mu;
    real<lower=0> tau;
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
fit = sm.sampling(data=schools_dat, iter=1000, chains=4)

resMu_code = """
data {
    int<lower=0> J; // mean absolute error
    vector[J] y; // estimated treatment effects
    vector<lower=0>[J] sigma; // s.e. of effect estimates
}
parameters {
    real mu;
    real<lower=0> tau;
    vector[J] eta;
}
transformed parameters {
    vector[J] theta;
    theta = mu + tau * eta;
}
model {

}    
"""

# 1. Probability of the response mu given RT

# Question to ask: what distribution does each parameter fall under?
# Note: it doesn't make sense to try to predict RT AND MAE does it?

#  P(stimDur, est_mu, noise, RT | res_mu) =
#   P(res_mu | RT)*P(RT | stimDur, est_mu, noise) *?P(est_mu)*P(noise)*P(stimDur)

# parameters on which to build predictive model of res_mu
# RT (gamma), due to overthinking,
# est_mu (sinusoidal relationship to MAE)
# SNR (linear relationship to MAE)

schools_dat = {'J': 8,
               'y': [28, 8, -3, 7, -1, 1, 18, 12],
               'sigma': [15, 10, 16, 11, 9, 11, 10, 18]}
