import sys
import os
import streamlit as st
import matplotlib as plt
import numpy as np

# idk this fixed the import error
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# import models
from models.black_scholes import black_scholes
from models.binomial_tree import binomial_tree
from models.monte_carlo import monte_carlo

# title and layout
st.set_page_config(page_title="Options Price Visualizer", layout="centered")
st.title("📈 Options Pricing Visualizer")

# sidebar for input parameters
st.sidebar.header("Option Parameters")

S = st.sidebar.number_input("Spot Price (S)", value=100.0)
K = st.sidebar.number_input("Strike Price (K)", value=100.0)
T = st.sidebar.number_input("Time to Maturity (T, in years)", value=1.0, min_value=0.01)
r = st.sidebar.number_input("Risk-Free Rate (r)", value=0.05, format="%.4f")
sigma = st.sidebar.number_input("Volatility (σ)", value=0.2, format="%.4f")
option_type = st.sidebar.selectbox("Option Type", ["call", "put"])
model = st.sidebar.selectbox("Pricing Model", ["Black-Scholes", "Binomial Tree", "Monte Carlo"])

# config for other models
if model == "Binomial Tree":
    steps = st.sidebar.slider("Number of Steps (N)", 10, 500, 100)
    is_american = st.sidebar.checkbox("American Style", value=False)
if model == "Monte Carlo":
    sims = st.sidebar.slider("Simulations", 1000, 50000, 10000, step=1000)

# calculate option price based on selected model
st.subheader("Option Price")
if model == "Black-Scholes":
    price = black_scholes(S, K, T, r, sigma, option_type)
elif model == "Binomial Tree":
    price = binomial_tree(S, K, T, r, sigma, steps, option_type, is_american)
elif model == "Monte Carlo":
    price = monte_carlo(S, K, T, r, sigma, option_type, sims)

# price
st.metric("Price", f"${price:.2f}")

# plotting option price vs. strike price
st.subheader("📊 Option Price vs. Strike Price")

# generate range of strike prices for plotting
K_values = np.linspace(S * 0.5, S * 1.5, 50)
prices = []

for K_val in K_values:
    if model == "Black-Scholes":
        price = black_scholes(S, K_val, T, r, sigma, option_type)
    elif model == "Binomial Tree":
        price = binomial_tree(S, K_val, T, r, sigma, steps, option_type, is_american)
    elif model == "Monte Carlo":
        price = monte_carlo(S, K_val, T, r, sigma, option_type, sims)
    prices.append(price)

# plot
fig, ax = plt.subplots()
ax.plot(K_values, prices, label=f"{option_type.capitalize()} Price")
ax.axvline(K, color='gray', linestyle='--', label="Current Strike")
ax.set_xlabel("Strike Price (K)")
ax.set_ylabel("Option Price")
ax.set_title("Option Price vs. Strike Price")
ax.legend()
st.pyplot(fig)