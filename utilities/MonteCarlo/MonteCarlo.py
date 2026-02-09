import numpy as np
from scipy.optimize import minimize

class MonteCarlo:
    def __init__(self, data: np.array, n_sim: int, len_sim: int, mean_reversion_bool: bool):
        self.data = data
        
        self.n_sim = n_sim
        self.len_sim = len_sim
        self.mean_reversion_bool = mean_reversion_bool
        self.speed = 0.1

    def run(self) -> float:
        if self.mean_reversion_bool:
            delta = self.mean_reversion()
        else:
            delta = self.standard_monte_carlo()
        return delta
   
    def standard_monte_carlo(self):
        returns = self.log_returns(self.data)
        avg = np.mean(returns)
        std = np.std(returns, ddof=1)
        
        eps = np.random.standard_normal((self.len_sim + 1, self.n_sim))
        price_array = np.zeros((self.len_sim+1, self.n_sim))
        price_array[0, :] = self.n_sim * [self.data[-1]]

        for idx in range(1, self.len_sim):
            price_array[idx, :] = avg * price_array[idx-1, :] + std*eps[idx-1, :]

        if np.sum(price_array[-1,:] > self.data[-1]) > self.n_sim/2:
            delta = 1.
        else:
            delta = 0.
        return delta

    def mean_reversion(self):
        #mu, theta, sigma = self.estimate_ou_mle(self.data)
        results = self.simulate_ou_process(mu=10, theta=5, sigma=0.2, n_sim=self.n_sim, 
                            n_steps=self.len_sim, x0=self.data[0])
        if np.sum(results[-1,:] > self.data[-1]) > self.n_sim/2:
            delta=1.
        else:
            delta=0.
        return delta


    def log_returns(data: np.array) -> np.array:
        log_returns = np.log(data[1:] / data[:-1])
        return log_returns

    @staticmethod
    def estimate_ou_mle(data: np.array, dt: float=1/252):
        """
        Estimate OU parameters using Maximum Likelihood Estimation.
        
        Parameters:
        data : array-like, time series of the process
        dt : float, time step between observations (in years)
        
        Returns:
        mu, theta, sigma : estimated parameters
        """
        n = len(data)
        X = np.array(data)
        
        # Create lagged series
        X_t = X[1:]      # X(t)
        X_tm1 = X[:-1]   # X(t-1)
        
        # MLE estimates have closed-form solutions for OU process
        # Using regression: X_t = a + b * X_{t-1} + error
        
        # Perform linear regression: X_t = alpha + beta * X_{t-1}
        A = np.vstack([np.ones_like(X_tm1), X_tm1]).T
        beta, alpha = np.linalg.lstsq(A, X_t, rcond=None)[0]
        
        # Extract parameters
        # X_t = alpha + beta * X_{t-1} corresponds to:
        # alpha = μ(1 - exp(-θΔt))
        # beta = exp(-θΔt)
        
        theta = -np.log(beta) / dt  # speed of mean reversion
        mu = alpha / (1 - beta)     # long-term mean
        sigma = np.sqrt(2 * theta / (1 - beta**2) * np.var(X_t - (alpha + beta * X_tm1)))
        
        return mu, theta, sigma
        
    @staticmethod
    def simulate_ou_process(mu: float=0, theta: float=5, sigma: float=0.2, dt: float=1/252, n_sim: int=10, 
                            n_steps: int=1000, x0: float=0):
        """Simulate OU process."""
        X = np.zeros((n_steps, n_sim))
        X[0, :] = n_sim * [x0]
        dW = np.random.normal(mu, np.sqrt(dt), (n_steps, n_sim))
        for t in range(1, n_steps):
            X[t, :] = X[t-1, :] + theta*(mu - X[t-1, :])*dt + sigma*dW[t-1, :]
        return X