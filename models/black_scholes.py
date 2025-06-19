import math
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type="call"):
    """
    Black-Scholes option pricing formula for European options.

    Parameters:
        S : float : Spot price
        K : float : Strike price
        T : float : Time to maturity (in years)
        r : float : Risk-free interest rate
        sigma : float : Volatility (std dev of returns)
        option_type : str : 'call' or 'put'

    Returns:
        float : Option price
    """
    d1 = (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == "call":
        return S * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    else:
        raise ValueError("option_type must be 'call' or 'put'")
