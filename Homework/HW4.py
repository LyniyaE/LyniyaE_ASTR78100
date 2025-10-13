import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

# loading the file
filename = "Downloads/cm_tess_file.fits"
hdul = fits.open(filename)
times = hdul[1].data['times']
fluxes = hdul[1].data['fluxes']
ferrs = hdul[1].data['ferrs']

# seeing what the data looks like
plt.plot(times, fluxes, '.')
plt.xlabel('Time')
plt.ylabel('Flux')
plt.title('all the data')
plt.show()

print(np.min(times), np.max(times))

# choosing one chunk of data to look at
# from the plot I can see times around 2250-2500 have lots of points
start = 2250
end = 2500

# getting only the data in that range
indices = (times >= start) & (times <= end)
t = times[indices]
flux = fluxes[indices]

print(len(t), "data points")

# plotting just this part
plt.figure()
plt.plot(t, flux, '.')
plt.xlabel('Time')
plt.ylabel('Flux')
plt.title('my epoch')
plt.show()

# subtracting mean for fourier transform
flux_mean = np.mean(flux)
flux_norm = flux - flux_mean

print("mean:", flux_mean)

# fft
fft_result = np.fft.fft(flux_norm)

# power
pwr = np.abs(fft_result)**2

# frequencies
n = len(t)
dt = np.median(np.diff(t))
freqs = np.fft.fftfreq(n, dt)

# only positive freqs
pos_freqs = freqs[:n//2]
pos_pwr = pwr[:n//2]

# plotting power spectrum
plt.figure()
plt.plot(pos_freqs, pos_pwr)
plt.xlabel('Frequency')
plt.ylabel('Power')
plt.title('power spectrum')
plt.xlim(0, 5)
plt.show()

# finding the peak
# skipping the first point because thats just the mean
idx = np.argmax(pos_pwr[1:]) + 1
peak_freq = pos_freqs[idx]
period = 1.0 / peak_freq

print("frequency:", peak_freq)
print("period:", period, "days")

# trying to reconstruct with fewer coefficients
# starting with 10
num_coeff = 10

fft_copy = fft_result.copy()
magnitudes = np.abs(fft_copy)

# keeping only the biggest ones
sorted_mag = np.sort(magnitudes)
cutoff = sorted_mag[-num_coeff]
fft_copy[magnitudes < cutoff] = 0

# inverse transform
reconstructed = np.fft.ifft(fft_copy)
reconstructed = np.real(reconstructed) + flux_mean

# plotting
plt.figure()
plt.plot(t, flux, '.', label='data')
plt.plot(t, reconstructed, 'r-', label='10 coeff')
plt.title('reconstruction test')
plt.legend()
plt.show()

# trying more numbers to see what works
# making subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 5))

coeffs_to_try = [5, 10, 20, 50]

for i in range(4):
    num = coeffs_to_try[i]
    
    fft_temp = fft_result.copy()
    mags = np.abs(fft_temp)
    sorted_mags = np.sort(mags)
    threshold = sorted_mags[-num]
    fft_temp[mags < threshold] = 0
    
    recon = np.fft.ifft(fft_temp)
    recon = np.real(recon) + flux_mean
    
    row = i // 2
    col = i % 2
    
    axes[row, col].plot(t, flux, '.', alpha=0.4)
    axes[row, col].plot(t, recon, 'r-')
    axes[row, col].set_title(str(num) + ' coefficients')
    axes[row, col].set_xlabel('Time')
    axes[row, col].set_ylabel('Flux')

plt.tight_layout()
plt.show()

# looks like even 5 or 10 captures most of it

# checking for missing data
gaps = np.diff(t)
median_gap = np.median(gaps)

print("median gap:", median_gap)

# seeing where there are bigger gaps
big_gaps = gaps > median_gap * 1.5
print("number of gaps:", np.sum(big_gaps))

# trying to fill in the gaps - this part was confusing
if np.sum(big_gaps) > 0:
    t_new = []
    f_new = []
    
    # going through each point
    for i in range(len(t)):
        t_new.append(t[i])
        f_new.append(flux[i])
        
        # check if theres a gap after this point
        if i < len(t) - 1:
            gap = t[i+1] - t[i]
            if gap > median_gap * 1.5:
                # gap detected
                # how many points should be here
                n_missing = int(gap / median_gap) - 1
                
                # adding the missing points
                for j in range(1, n_missing + 1):
                    # time 
                    new_time = t[i] + j * median_gap
                    
                    # flux using linear interpolation
                    # this took forever to figure out
                    w = j / (n_missing + 1)
                    new_f = flux[i] * (1 - w) + flux[i+1] * w
                    
                    t_new.append(new_time)
                    f_new.append(new_f)
    
    t_new = np.array(t_new)
    f_new = np.array(f_new)
    
    print("before:", len(t))
    print("after:", len(t_new))
    
    # plot comparison
    plt.figure(figsize=(10,4))
    
    plt.subplot(1,2,1)
    plt.plot(t, flux, '.')
    plt.title('original')
    plt.xlabel('Time')
    plt.ylabel('Flux')
    
    plt.subplot(1,2,2)
    plt.plot(t_new, f_new, '.')
    plt.title('filled')
    plt.xlabel('Time')
    plt.ylabel('Flux')
    
    plt.show()
    