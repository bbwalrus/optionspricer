import numpy as np

def monte_carlo(S, K, T, r, sigma, option_type="call", simulations=10000):
    """
    Monte Carlo simulation for European option pricing.

    Parameters:
        S : float : Spot price
        K : float : Strike price
        T : float : Time to maturity
        r : float : Risk-free interest rate
        sigma : float : Volatility
        option_type : str : 'call' or 'put'
        simulations : int : Number of random paths

    Returns:
        float : Estimated option price
    """
    Z = np.random.standard_normal(simulations)
    ST = S * np.exp((r - 0.5 * sigma**2) * T + sigma * np.sqrt(T) * Z)

    if option_type == "call":
        payoffs = np.maximum(ST - K, 0)
    else:
        payoffs = np.maximum(K - ST, 0)

    return np.exp(-r * T) * np.mean(payoffs)
