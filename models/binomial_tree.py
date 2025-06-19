import math

def binomial_tree(S, K, T, r, sigma, N=100, option_type="call", american=False):
    """
    Binomial tree option pricing for European or American options.

    Parameters:
        S : float : Spot price
        K : float : Strike price
        T : float : Time to maturity
        r : float : Risk-free interest rate
        sigma : float : Volatility
        N : int : Number of time steps
        option_type : str : 'call' or 'put'
        american : bool : True for American, False for European

    Returns:
        float : Option price
    """
    dt = T / N
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u
    p = (math.exp(r * dt) - d) / (u - d)
    discount = math.exp(-r * dt)

    # Initialize asset prices at maturity
    prices = [S * (u ** j) * (d ** (N - j)) for j in range(N + 1)]

    # Calculate option value at maturity
    if option_type == "call":
        values = [max(price - K, 0) for price in prices]
    else:
        values = [max(K - price, 0) for price in prices]

    # Step backwards through the tree
    for i in range(N - 1, -1, -1):
        for j in range(i + 1):
            exercise = 0
            price = S * (u ** j) * (d ** (i - j))
            values[j] = discount * (p * values[j + 1] + (1 - p) * values[j])
            if american:
                if option_type == "call":
                    exercise = max(price - K, 0)
                else:
                    exercise = max(K - price, 0)
                values[j] = max(values[j], exercise)

    return values[0]
