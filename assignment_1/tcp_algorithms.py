import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


def plot(x1_values, x2_values, threshold, chart_title='x2 vs x1'):
    plt.figure(figsize=(6, 4))
    plt.plot(x1_values, x2_values, label="Iteration data")
    plt.plot([0, threshold], [threshold, 0], label='Efficiency Line', linestyle='--', color='red')
    plt.plot([0, threshold], [0, threshold], label='Fairness Line', linestyle='--', color='green')


    plt.xlabel('x1')
    plt.ylabel('x2')
    plt.title(chart_title)
    upper_limit = max([x1_values.max(), x2_values.max(), threshold])
    plt.xlim(0, int(upper_limit)+1)
    plt.ylim(0, int(upper_limit)+1)
    plt.legend()
    plt.grid(True)
    plt.show()


def aimd(x1:float, x2:float, alpha:float=1, beta:float=0.5, threshold:int=12, iterations:int=100):
    x1_values = np.zeros(iterations) 
    x2_values = np.zeros(iterations) 

    for i in tqdm(range(iterations)): 
        if x1+x2 <= threshold:
            x1 += alpha
            x2 += alpha

        else:
            x1 *= beta
            x2 *=beta

        x1_values[i] = x1 
        x2_values[i] = x2 

    return x1_values, x2_values


def dctcp(x1:float, x2:float, alpha:float=1, g:float=0.1, threshold:int=12, iterations:int=100):
    x1_values = np.zeros(iterations) 
    x2_values = np.zeros(iterations)

    a = 0

    for i in tqdm(range(iterations)): 
        if x1+x2 <= threshold:
            # Follow additive increment from AIMD
            x1 += alpha
            x2 += alpha

        else:
            # Get fraction of marked packets
            marked = x1+x2-threshold
            f = marked/(x1+x2)

            # Apply formula
            a = (1-g) * a + g * f
            x1 *= (1-a/2)
            x2 *= (1-a/2)

        x1_values[i] = x1 
        x2_values[i] = x2 

    return x1_values, x2_values


def cubic(x1: float, x2: float, C: float = 0.4, beta: float = 0.8, threshold: int = 12, iterations: int = 100):
    x1_values = np.zeros(iterations)
    x2_values = np.zeros(iterations)

    # Initialize W_max and time elapsed since last congestion
    x1_max, x2_max = x1, x2
    t = 0

    for i in tqdm(range(iterations)):
        if x1 + x2 <= threshold:
            # Compute K
            k1 = (x1_max * (1-beta) / C) ** (1/3)
            k2 = (x2_max * (1-beta) / C) ** (1/3)

            # Apply cubic formula
            x1 = x1_max + C * (t-k1)
            x2 = x2_max + C * (t-k2)
            t += 1
        else:
            # If congested, set new W_max values before decreasing value
            x1_max = x1
            x2_max = x2
            x1 *= beta
            x2 *= beta
            t = 0

        x1_values[i] = x1
        x2_values[i] = x2

    return x1_values, x2_values