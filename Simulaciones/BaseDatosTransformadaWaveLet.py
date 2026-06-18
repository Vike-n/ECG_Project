import wfdb
import pywt
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# Cargar ECG
# =====================================================

record = wfdb.rdrecord('rec_1')

ecg = record.p_signal[:, 0]
fs = record.fs

t = np.arange(len(ecg)) / fs

print(f"Frecuencia: {fs} Hz")
print(f"Muestras: {len(ecg)}")

# =====================================================
# Wavelet
# =====================================================

wavelet_name = 'db4'
level = 10

coeffs = pywt.wavedec(
    ecg,
    wavelet_name,
    level=level
)

# =====================================================
# Energia por banda
# =====================================================

print("\nEnergia por banda:\n")

energy = np.sum(coeffs[0]**2)
print(f"A10  {energy:.3f}")

for i in range(1, len(coeffs)):

    level_num = 11 - i

    energy = np.sum(coeffs[i]**2)

    print(
        f"D{level_num:<2}  "
        f"{energy:.3f}"
    )

# =====================================================
# Ganancias manuales
# =====================================================

gains = {
    "A10": 0.1,
    "D10": 0.1,
    "D9":  0.5,
    "D8":  1.0,
    "D7":  1.0,
    "D6":  1.0,
    "D5":  1.0,
    "D4":  1.0,
    "D3":  0.3,
    "D2":  0.0,
    "D1":  0.0
}

# =====================================================
# Aplicar ganancias
# =====================================================

coeffs_mod = []

coeffs_mod.append(
    coeffs[0] * gains["A10"]
)

for i in range(1, len(coeffs)):

    level_num = 11 - i

    coeffs_mod.append(
        coeffs[i] *
        gains[f"D{level_num}"]
    )

# =====================================================
# Reconstruccion
# =====================================================

filtered = pywt.waverec(
    coeffs_mod,
    wavelet_name
)

filtered = filtered[:len(ecg)]

# =====================================================
# Graficar
# =====================================================

plt.figure(figsize=(14, 6))

plt.plot(
    t,
    ecg,
    label="Original",
    linewidth=1
)

plt.plot(
    t,
    filtered,
    label="Filtrada",
    linewidth=1
)

plt.xlim(3.5, 5.8)

plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.title(
    f"Wavelet={wavelet_name} "
    f"Nivel={level}"
)

plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
