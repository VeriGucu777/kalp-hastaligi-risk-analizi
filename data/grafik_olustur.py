import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# 📌 Grafiklerin kaydedileceği klasör
grafik_konumu = "static/raporlar/"

# 📌 Eğer klasör yoksa oluştur
os.makedirs(grafik_konumu, exist_ok=True)

# 📌 Örnek veri seti
np.random.seed(42)
data = pd.DataFrame({
    "Hasta ID": range(1, 101),
    "Kalış Süresi (Gün)": np.random.randint(1, 15, 100)
})

# 📌 1. Hastaların Hastanede Kalış Süreleri Grafiği
plt.figure(figsize=(8,5))
sns.histplot(data["Kalış Süresi (Gün)"], bins=10, kde=True, color="blue")
plt.xlabel("Hastanede Kalış Süresi (Gün)")
plt.ylabel("Hasta Sayısı")
plt.title("Hastaların Hastanede Kalış Süreleri Dağılımı")
plt.grid(True)

# 📌 Grafik kaydediliyor
grafik_yolu = os.path.join(grafik_konumu, "hastanede_kalis_suresi.png")
plt.savefig(grafik_yolu)
plt.close()

print(f"✅ Grafik başarıyla kaydedildi: {grafik_yolu}")
