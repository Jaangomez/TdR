import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from sklearn.neighbors import NearestNeighbors

# Load the audio data
sample_rate, data = wavfile.read('Sounds/recording5.wav')
data = data / np.max(np.abs(data))  # Normalize the data

def average_mutual_information(data, max_lag):
    N = len(data)
    ami = np.zeros(max_lag)
    for lag in range(1, max_lag + 1):
        P1 = data[:-lag]
        P2 = data[lag:]
        p1 = np.histogram(P1, bins=100, density=True)[0]
        p2 = np.histogram(P2, bins=100, density=True)[0]
        p12 = np.histogram2d(P1, P2, bins=100, density=True)[0]
        p12 /= np.sum(p12)
        ami[lag - 1] = np.sum([p12[i, j] * np.log(p12[i, j] / (p1[i] * p2[j] + 1e-10) + 1e-10)
                               for i in range(100) for j in range(100) if p12[i, j] > 0])
    return ami

# Calculate AMI for a range of lags
max_lag = 100
ami = average_mutual_information(data, max_lag)

# Plot AMI
plt.figure(figsize=(10, 4))
plt.plot(range(1, max_lag + 1), ami)
plt.title('Average Mutual Information')
plt.xlabel('Lag')
plt.ylabel('AMI')
plt.show()

# Select the first local minimum of AMI as the time delay
delay = np.argmin(ami) + 1
print(f"Selected time delay: {delay}")

# False Nearest Neighbors for selecting embedding dimension
def false_nearest_neighbours (data, delay, max_dim):
    N = len(data)
    X = np.array ([data[i:N - (max_dim - 1) * delay + i] for i in range (max_dim)]).T
    nbrs = NearestNeighbors(n_neighbors = 2).fit(X)
    distances, indices = nbrs.kneighbors(X)
    false_neighbors = []
    for m in range(1, max_dim):
        X_m = X[:, :m]
        X_m1 = X[:, m+1]
        distances_m = distances[:, 1][:N -(max_dim -m) * delay]
        distances_m1 = np.sqrt(np.sum((X_m1[:, 1:] - X_m1[:, :-1])**2, axis = 1))
        fnn = np.mean(distances_m1 / distances_m > 10)
    return false_neighbors

max_dim = 10
fnn = false_nearest_neighbours(data, delay, max_dim)

# Plot FNN
plt.figure(figsize=(10, 4))
plt.plot(range(1, max_dim), fnn)  # Adjust range to match fnn length
plt.title('False Nearest Neighbors')
plt.xlabel('Embedding Dimension')
plt.ylabel('FNN Ratio')
plt.show()

# Select the embedding dimension where FNN ratio drops below a threshold (e.g., 0.01)
embedding_dim = np.where(np.array(fnn) < 0.01)[0][0] + 1
print(f"Selected embedding dimension: {embedding_dim}")

# Phase space reconstruction
def reconstruct_phase_space(data, delay, embedding_dim):
    N = len(data)
    M = N - (embedding_dim - 1) * delay
    if M <= 0:
        raise ValueError("Time series is too short for the given embedding parameters.")
    phase_space = np.array([data[i * delay : i * delay + M] for i in range(embedding_dim)]).T
    return phase_space

# Calculate the largest Lyapunov exponent
def lyapunov_exponent(data, delay, embedding_dim, epsilon=1e-10):
    phase_space = reconstruct_phase_space(data, delay, embedding_dim)
    N = phase_space.shape[0]
    L = []
    for i in range(N - 1):
        d0 = np.sqrt(np.sum((phase_space[i] - phase_space[i + 1])**2)) + epsilon
        d1 = np.sqrt(np.sum((phase_space[i + 1] - phase_space[(i + 2) % N])**2))
        if d1 > 0:
            L.append(np.log(d1 / d0))
    if len(L) == 0:
        return np.nan
    return np.mean(L)

# Calculate the fractal dimension using box-counting method
def box_counting_dimension(data, max_box_size=None):
    if max_box_size is None:
        max_box_size = len(data) // 2
    box_sizes = np.arange(1, max_box_size + 1)
    counts = np.zeros_like(box_sizes)
    for i, box_size in enumerate(box_sizes):
        counts[i] = np.sum([np.any(data[j:j + box_size]) for j in range(0, len(data), box_size)])
    nonzero = counts > 0
    if not np.any(nonzero):
        return np.nan
    coeffs = np.polyfit(np.log(box_sizes[nonzero]), np.log(counts[nonzero]), 1)
    return -coeffs[0]

# Reconstruct phase space and calculate Lyapunov exponent
lyap_exp = lyapunov_exponent(data, delay, embedding_dim)

print(f"Largest Lyapunov Exponent: {lyap_exp:.4f}")

# Higuchi Fractal Dimension calculation
def higuchi_fd(x, kmax):
    N = len(x)
    Lmk = np.zeros((kmax, kmax))
    
    for k in range(1, kmax + 1):
        for m in range(k):
            Lm = 0
            count = 0
            for i in range(1, (N - m) // k):
                Lm += abs(x[m + i * k] - x[m + (i - 1) * k])
                count += 1
            if count > 0:
                Lm = Lm * (N - 1) / (count * k)
            else:
                Lm = 0
            Lmk[m, k - 1] = Lm
    
    Lk = np.mean(Lmk, axis=0)
    lnLk = np.log(Lk[Lk > 0])
    lnk = np.log(np.arange(1, kmax + 1))[Lk > 0]
    
    coeffs = np.polyfit(lnk, lnLk, 1)
    return coeffs[0]

# Calculate the Higuchi Fractal Dimension
kmax = 10  # Maximum k value
hfd = higuchi_fd(data, kmax)
print(f"Higuchi Fractal Dimension: {hfd:.4f}")

# Plot the Higuchi Fractal Dimension
k_values = np.arange(1, kmax + 1)
Lk = [np.mean(np.abs(data[::k] - np.roll(data[::k], shift=1))) for k in k_values]

plt.figure(figsize=(8, 6))
plt.plot(np.log(k_values), np.log(Lk), 'o', label='Higuchi FD')
plt.xlabel('log(k)')
plt.ylabel('log(L(k))')
plt.title('Higuchi Fractal Dimension')
plt.legend()
plt.show()