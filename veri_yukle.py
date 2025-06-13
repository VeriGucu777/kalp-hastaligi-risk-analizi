import numpy as np
import pandas as pd

# Rastgelelik için sabit bir tohum değeri belirleyelim
np.random.seed(42)

# Mevcut veri seti
data = {
    "Yaş": np.random.randint(18, 90, 1000),
    "Cinsiyet": np.random.choice(["Kadın", "Erkek"], 1000),
    "BMI": np.round(np.random.uniform(18.5, 40, 1000), 2),
    "Nabız": np.random.randint(60, 120, 1000),
    "Tansiyon_Sistolik": np.random.randint(90, 180, 1000),
    "Tansiyon_Diastolik": np.random.randint(60, 120, 1000),
    "Oksijen_Doygunluğu": np.random.randint(85, 100, 1000),
    "Kalp_Hastaligi": np.random.choice(["Evet", "Hayır"], 1000),
    "Kanser": np.random.choice(["Evet", "Hayır"], 1000),
    "Tansiyon_Problemi": np.random.choice(["Evet", "Hayır"], 1000),
    "Kolesterol_Sorunu": np.random.choice(["Evet", "Hayır"], 1000),
    "Panik_Atak": np.random.choice(["Evet", "Hayır"], 1000),
    "Son_Ameliyat": np.random.choice(["Evet", "Hayır"], 1000),
    "Kirik": np.random.choice(["Evet", "Hayır"], 1000),
    "Cikik": np.random.choice(["Evet", "Hayır"], 1000),
    "Kalp_Krizi": np.random.choice(["Evet", "Hayır"], 1000),
    "Ic_Kanama": np.random.choice(["Evet", "Hayır"], 1000),
    "Kesik": np.random.choice(["Evet", "Hayır"], 1000),
    "Yaralanma": np.random.choice(["Evet", "Hayır"], 1000),
    "Beyin_Kanamasi": np.random.choice(["Evet", "Hayır"], 1000),
    "Uzuv_Kopmasi": np.random.choice(["Evet", "Hayır"], 1000),
    "Sikisma": np.random.choice(["Evet", "Hayır"], 1000),
    "Omurilik_Zedelenmesi": np.random.choice(["Evet", "Hayır"], 1000),
    "Ağrı_Seviyesi": np.random.randint(1, 11, 1000),
    "Stres_Seviyesi": np.random.randint(1, 11, 1000),
    "Tedaviye_Ulaşma_Süresi": np.random.randint(5, 60, 1000),
    "Sağlık_Ekibi_Kapasitesi": np.random.randint(1, 6, 1000),
    "Ateş": np.round(np.random.uniform(36.0, 41.0, 1000), 1),
    "Bulantı": np.random.choice(["Evet", "Hayır"], 1000),
    "Kusma": np.random.choice(["Evet", "Hayır"], 1000),
    "Bayılma": np.random.choice(["Evet", "Hayır"], 1000),
    "Bilinç_Durumu": np.random.choice(["Normal", "Sersem", "Bilinçsiz"], 1000),
    "Epilepsi": np.random.choice(["Evet", "Hayır"], 1000),
    "KOAH": np.random.choice(["Evet", "Hayır"], 1000),
    "Böbrek_Yetmezliği": np.random.choice(["Evet", "Hayır"], 1000),
    "Yanık": np.random.choice(["1. Derece", "2. Derece", "3. Derece", "Yok"], 1000),
    "Zehirlenme": np.random.choice(["Evet", "Hayır"], 1000),
    "Boğulma": np.random.choice(["Evet", "Hayır"], 1000),
    "Şiddetli_Baş_Ağrısı": np.random.randint(1, 11, 1000),
    "Laboratuvar_Sonuçları": np.random.randint(50, 200, 1000),
    "Kan_Şekeri": np.random.randint(70, 200, 1000),
    "Kalp_Hızı_Değişkenliği": np.round(np.random.uniform(10, 150, 1000), 2),
    "Nefes_Darlığı": np.random.choice(["Evet", "Hayır"], 1000),
    "Hastanın_Medikal_Geçmişi": np.random.choice(
    ["Kalp", "Böbrek", "Akciğer", "Normal", "Kanser", "KOAH", "Diabetes", "Hipertansiyon", "Nörolojik"],
    1000),
    "Şok_Belirtileri": np.random.choice(["Evet", "Hayır"], 1000),
    "Göz_Bebeği_Tepkisi": np.random.choice(["Normal", "Yavaş", "Tepkisiz"], 1000),
    "İshal": np.random.choice(["Evet", "Hayır"], 1000),
    "Ağrı_Konumu": np.random.choice(["Baş", "Karın", "Göğüs", "Sırt", "Bacak", "Kol"], 1000),
    "Göğüs_Ağrısı": np.random.choice(["Evet", "Hayır"], 1000),
    "Vücut_Sıcaklığı_Değişkenliği": np.round(np.random.uniform(35.0, 42.0, 1000), 1),
    "Susuzluk_Belirtileri": np.random.choice(["Evet", "Hayır"], 1000),
    "Son_24_Saatte_Yemek_Yedi": np.random.choice(["Evet", "Hayır"], 1000),
    "Cilt_Kuruluğu": np.random.choice(["Evet", "Hayır"], 1000),
    "Nörolojik_Belirtiler": np.random.choice(["Normal", "Konuşma Bozukluğu", "Uyuşukluk"], 1000),
    "Hasta_Kaç_Saat_Önce_Yaralandı": np.random.randint(0, 24, 1000),
    "Olay_Türü": np.random.choice(["Trafik Kazası", "Ev Kazası", "Spor Yaralanması", "Sanayi Kazası", "Olay Yok"], 1000),
    "İlk_Müdahale_Yapıldı": np.random.choice(["Evet", "Hayır"], 1000),
    "Hastanın_Önceki_Hastane_Ziyaretleri": np.random.randint(0, 11, 1000),
    "Acil_Servise_Geldiği_Saat": np.random.randint(0, 24, 1000),
}
# Veri çerçevesi oluşturma
df = pd.DataFrame(data)

# Güncellenmiş veri çerçevesini oluşturalım
df_final = pd.DataFrame(data)

# CSV olarak kaydedelim
df_final.to_csv("guncellenmis_veri_seti.csv", index=False)

import pandas as pd

# CSV dosyanın adını doğru gir
dosya_yolu = "guncellenmis_veri_seti.csv"

# Veri setini yükle
df = pd.read_csv(dosya_yolu)

# İlk birkaç satırı görüntüle
print("📌 Veri Setinin İlk Satırları:")
print(df.head())

# Sütun isimlerini görüntüle
print("\n📌 Sütun İsimleri:")
print(df.columns)

# Veri türlerini incele
print("\n📌 Veri Türleri:")
print(df.dtypes)

# Eksik değerleri kontrol et
print("\n📌 Eksik Veri Sayısı:")
print(df.isnull().sum())

# Temel istatistiksel özet
print("\n📌 Genel İstatistiksel Özet:")
print(df.describe(include="all"))

import pandas as pd

# CSV dosyanın adını doğru gir
dosya_yolu = "guncellenmis_veri_seti.csv"

# Veri setini tekrar yükle
df = pd.read_csv(dosya_yolu)

# "Evet" → 1, "Hayır" → 0 dönüşümü
evet_hayir_sutunlari = ["Kalp_Hastaligi", "Kanser", "Tansiyon_Problemi", "Kolesterol_Sorunu",
                         "Panik_Atak", "Son_Ameliyat", "Kirik", "Cikik", "Kalp_Krizi",
                         "Ic_Kanama", "Kesik", "Yaralanma", "Beyin_Kanamasi", "Uzuv_Kopmasi",
                         "Sikisma", "Omurilik_Zedelenmesi", "Bulantı", "Kusma", "Bayılma",
                         "Epilepsi", "KOAH", "Böbrek_Yetmezliği", "Zehirlenme", "Boğulma",
                         "Nefes_Darlığı", "Şok_Belirtileri", "İshal", "Göğüs_Ağrısı",
                         "Susuzluk_Belirtileri", "Son_24_Saatte_Yemek_Yedi", "Cilt_Kuruluğu",
                         "İlk_Müdahale_Yapıldı"]

for col in evet_hayir_sutunlari:
    df[col] = df[col].map({"Evet": 1, "Hayır": 0})

# "Kadın" → 0, "Erkek" → 1 dönüşümü
df["Cinsiyet"] = df["Cinsiyet"].map({"Kadın": 0, "Erkek": 1})

# "Normal", "Sersem", "Bilinçsiz" gibi kategorik sütunları sayısal hale getirme
kategorik_sutunlar = ["Bilinç_Durumu", "Yanık", "Olay_Türü", "Göz_Bebeği_Tepkisi", "Nörolojik_Belirtiler"]

df = pd.get_dummies(df, columns=kategorik_sutunlar)

# Dönüştürülmüş veri setini kaydet
df.to_csv("temizlenmis_veri_seti.csv", index=False)

# İşlem tamamlandı mesajı
print("✅ Kategorik veriler başarıyla sayısal hale getirildi ve temizlenmiş veri kaydedildi!")

import pandas as pd

# Temizlenmiş veri setini tekrar yükle
df = pd.read_csv("temizlenmis_veri_seti.csv")

# Veri setinin ilk birkaç satırına bakalım
print("📌 Temizlenmiş Veri Setinin İlk Satırları:")
print(df.head())

# Veri türlerini inceleyelim
print("\n📌 Veri Türleri:")
print(df.dtypes)

# Eksik veri var mı kontrol edelim
print("\n📌 Eksik Veri Sayısı:")
print(df.isnull().sum())

# Genel istatistiksel özet
print("\n📌 Genel İstatistiksel Özet:")
print(df.describe(include="all"))

import pandas as pd

# Temizlenmiş veri setini yükle
df = pd.read_csv("temizlenmis_veri_seti.csv")

# Mevcut sütun isimlerini yazdır
print("📌 Mevcut Sütun İsimleri:")
print(df.columns)

import pandas as pd

# Temizlenmiş veri setini yükle
df = pd.read_csv("temizlenmis_veri_seti.csv")


# Aciliyet seviyesi hesaplama fonksiyonu
def hesapla_aciliyet(row):
    # Hayati tehlike oluşturan hastalıklar
    hayati_tehlike = ["Kalp_Krizi", "Ic_Kanama", "Beyin_Kanamasi", "Uzuv_Kopmasi"]

    # Eğer hayati tehlike varsa, doğrudan YÜKSEK RİSK (2)
    if any(row[col] == 1 for col in hayati_tehlike):
        return 2

    # Eğer bilinçsizse veya oksijen seviyesi çok düşükse, YÜKSEK RİSK (2)
    if row["Bilinç_Durumu_Bilinçsiz"] == 1 or row["Oksijen_Doygunluğu"] < 90:
        return 2

    # Eğer ağrı seviyesi 8 ve üstüyse ve stres seviyesi 7+ ise, ORTA RİSK (1)
    if row["Ağrı_Seviyesi"] >= 8 and row["Stres_Seviyesi"] >= 7:
        return 1

    # Eğer tansiyon çok düşük veya çok yüksekse, ORTA RİSK (1)
    if row["Tansiyon_Sistolik"] < 100 or row["Tansiyon_Sistolik"] > 160:
        return 1

    # Eğer herhangi bir kriter sağlanmadıysa, DÜŞÜK RİSK (0)
    return 0


# Aciliyet seviyesini hesaplayıp ekleyelim
df["Aciliyet_Seviyesi"] = df.apply(hesapla_aciliyet, axis=1)

# Yeni veri setini kaydet
df.to_csv("aciliyetli_veri_seti.csv", index=False)

print("✅ Aciliyet Seviyesi başarıyla hesaplandı ve yeni veri seti kaydedildi!")
import pandas as pd

# Temizlenmiş veri setini yükle
df = pd.read_csv("aciliyetli_veri_seti.csv")

# Sayısal olmayan (object türünde) sütunları listele
object_columns = df.select_dtypes(include=["object"]).columns

print("📌 Sayısal Olmayan Sütunlar:")
print(object_columns)

import pandas as pd

# Temizlenmiş veri setini yükle
df = pd.read_csv("aciliyetli_veri_seti.csv")

# One-Hot Encoding uygulayarak sayısal hale getirme
df = pd.get_dummies(df, columns=["Hastanın_Medikal_Geçmişi", "Ağrı_Konumu"])

# Yeni veri setini kaydet
df.to_csv("son_hali_veri_seti.csv", index=False)

print("✅ Metinsel sütunlar sayısallaştırıldı ve yeni veri seti kaydedildi!")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Yeni temizlenmiş veri setini yükle
df = pd.read_csv("son_hali_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y) ayırma
X = df.drop(columns=["Aciliyet_Seviyesi"])  # Model için kullanılacak değişkenler
y = df["Aciliyet_Seviyesi"]  # Modelin tahmin edeceği hedef değişken

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur ve eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli kaydet
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Model başarıyla eğitildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi.")

import pandas as pd
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Veri setini tekrar yükle
df = pd.read_csv("son_hali_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 10 hastayı test edelim
X_sample = X.iloc[:10]
y_sample = y.iloc[:10]

# Model ile tahmin yap
y_pred_sample = model.predict(X_sample)

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 10 Hasta için Tahmin Sonuçları:\n")
for i in range(10):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")

import pandas as pd

# Veri setini yükle
df = pd.read_csv("son_hali_veri_seti.csv")

# Aciliyet seviyelerinin dağılımını inceleyelim
print("📌 Aciliyet Seviyesi Dağılımı:")
print(df["Aciliyet_Seviyesi"].value_counts())

import pandas as pd
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split

# Veri setini yükle
df = pd.read_csv("son_hali_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# SMOTE ile veri dengeleme
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Yeni denge sağlanmış veri setini kaydet
df_resampled = pd.DataFrame(X_resampled, columns=X.columns)
df_resampled["Aciliyet_Seviyesi"] = y_resampled

df_resampled.to_csv("dengelenmis_veri_seti.csv", index=False)

print("✅ Veri dengeleme tamamlandı ve yeni veri seti kaydedildi!")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y) ayırma
X = df.drop(columns=["Aciliyet_Seviyesi"])  # Model için kullanılacak değişkenler
y = df["Aciliyet_Seviyesi"]  # Modelin tahmin edeceği hedef değişken

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur ve eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli kaydet
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Model başarıyla eğitildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi.")

import pandas as pd
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 10 hastayı test edelim
X_sample = X.iloc[:10]
y_sample = y.iloc[:10]

# Model ile tahmin yap
y_pred_sample = model.predict(X_sample)

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 10 Hasta için Tahmin Sonuçları:\n")
for i in range(10):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")
import pandas as pd

# Dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Aciliyet seviyelerinin dağılımını inceleyelim
print("📌 Dengelenmiş Veri Setindeki Aciliyet Seviyesi Dağılımı:")
print(df["Aciliyet_Seviyesi"].value_counts())
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import pickle

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y) ayırma
X = df.drop(columns=["Aciliyet_Seviyesi"])  # Model için kullanılacak değişkenler
y = df["Aciliyet_Seviyesi"]  # Modelin tahmin edeceği hedef değişken

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur ve eğit (Daha az kompleks hale getiriyoruz)
model = RandomForestClassifier(n_estimators=50, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli kaydet
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Yeni model eğitildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi.")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import pickle

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y) ayırma
X = df.drop(columns=["Aciliyet_Seviyesi"])  # Model için kullanılacak değişkenler
y = df["Aciliyet_Seviyesi"]  # Modelin tahmin edeceği hedef değişken

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeli oluştur ve eğit
model = LogisticRegression(max_iter=200, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli kaydet
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Yeni model (Logistic Regression) eğitildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi.")

import pandas as pd
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 10 hastayı test edelim
X_sample = X.iloc[:10]
y_sample = y.iloc[:10]

# Model ile tahmin yap
y_pred_sample = model.predict(X_sample)

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 10 Hasta için Tahmin Sonuçları:\n")
for i in range(10):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score
import pickle

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y) ayırma
X = df.drop(columns=["Aciliyet_Seviyesi"])  # Model için kullanılacak değişkenler
y = df["Aciliyet_Seviyesi"]  # Modelin tahmin edeceği hedef değişken

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost modelini oluştur ve eğit
model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli kaydet
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Yeni model (XGBoost) eğitildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi.")

import pandas as pd
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 10 hastayı test edelim
X_sample = X.iloc[:10]
y_sample = y.iloc[:10]

# Model ile tahmin yap
y_pred_sample = model.predict(X_sample)

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 10 Hasta için Tahmin Sonuçları:\n")
for i in range(10):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y) ayırma
X = df.drop(columns=["Aciliyet_Seviyesi"])  # Model için kullanılacak değişkenler
y = df["Aciliyet_Seviyesi"]  # Modelin tahmin edeceği hedef değişken

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost modelini oluştur ve eğit
model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli JSON formatında kaydet (app.py için uygun format)
model.save_model("trained_model.json")

# Sonuçları ekrana yazdır
print(f"✅ Yeni model (XGBoost) eğitildi ve JSON formatında kaydedildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.json' olarak kaydedildi ve `app.py` dosyasında kullanılabilir.")
import pandas as pd
import numpy as np
import xgboost as xgb

# Modeli JSON formatında yükle
model = xgb.Booster()
model.load_model("trained_model.json")

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 20 hastayı test edelim
X_sample = X.iloc[:20]
y_sample = y.iloc[:20]

# XGBoost için DMatrix formatına çevir
dmatrix = xgb.DMatrix(X_sample)

# Model ile tahmin yap
y_pred_sample = model.predict(dmatrix)
y_pred_sample = np.round(y_pred_sample).astype(int)  # Tahminleri tam sayıya yuvarla ve tamsayıya çevir

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 20 Hasta için Tahmin Sonuçları:\n")
for i in range(20):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")

import pandas as pd
import numpy as np
import xgboost as xgb

# Modeli JSON formatında yükle
model = xgb.Booster()
model.load_model("trained_model.json")

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 20 hastayı test edelim
X_sample = X.iloc[:20]
y_sample = y.iloc[:20]

# XGBoost için DMatrix formatına çevir
dmatrix = xgb.DMatrix(X_sample)

# Model ile tahmin yap
y_pred_sample = model.predict(dmatrix)
y_pred_sample = np.argmax(y_pred_sample, axis=1)  # En yüksek olasılığı alan sınıfı seç

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 20 Hasta için Tahmin Sonuçları:\n")
for i in range(20):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")
import pandas as pd

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Aciliyet seviyesi dağılımını görüntüle
print("📌 Aciliyet Seviyesi Dağılımı:\n")
print(df["Aciliyet_Seviyesi"].value_counts())
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Yeni dengelenmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# Min-Max ölçekleyici ile veriyi normalleştirme
scaler = MinMaxScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Yeni ölçeklenmiş veri setini kaydedelim
df_scaled = pd.concat([X_scaled, y], axis=1)
df_scaled.to_csv("dengelenmis_veri_seti_normalize.csv", index=False)

print("✅ Veri başarıyla normalleştirildi ve kaydedildi: 'dengelenmis_veri_seti_normalize.csv'")

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# XGBoost modelini oluştur ve eğit
model = XGBClassifier(n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli JSON formatında kaydet (app.py için uygun format)
model.save_model("trained_model.json")

# Sonuçları ekrana yazdır
print(f"✅ Yeni model (XGBoost) eğitildi ve JSON formatında kaydedildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.json' olarak kaydedildi ve `app.py` dosyasında kullanılabilir.")

import pandas as pd
import numpy as np
import xgboost as xgb

# Modeli JSON formatında yükle
model = xgb.Booster()
model.load_model("trained_model.json")

# Yeni normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 20 hastayı test edelim
X_sample = X.iloc[:20]
y_sample = y.iloc[:20]

# XGBoost için DMatrix formatına çevir
dmatrix = xgb.DMatrix(X_sample)

# Model ile tahmin yap
y_pred_sample = model.predict(dmatrix)
y_pred_sample = np.argmax(y_pred_sample, axis=1)  # En yüksek olasılığı alan sınıfı seç

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 20 Hasta için Tahmin Sonuçları:\n")
for i in range(20):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")
import pandas as pd
from sklearn.model_selection import train_test_split

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Eğitim ve test verisinde sınıf dağılımı
print("📌 Eğitim Verisindeki Sınıf Dağılımı:")
print(y_train.value_counts())

print("\n📌 Test Verisindeki Sınıf Dağılımı:")
print(y_test.value_counts())

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest modelini oluştur ve eğit
model = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli Pickle formatında kaydet (app.py için uygun format)
import pickle
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Yeni model (RandomForest) eğitildi ve Pickle formatında kaydedildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi ve `app.py` dosyasında kullanılabilir.")
import pandas as pd
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 20 hastayı test edelim
X_sample = X.iloc[:20]
y_sample = y.iloc[:20]

# Model ile tahmin yap
y_pred_sample = model.predict(X_sample)

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 20 Hasta için Tahmin Sonuçları:\n")
for i in range(20):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")
import pandas as pd
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Özellik önemlerini al
feature_importance = pd.DataFrame({"Özellik": X.columns, "Önem": model.feature_importances_})
feature_importance = feature_importance.sort_values(by="Önem", ascending=False)

# İlk 20 özelliği göster
print("📌 Modelin En Önemli 20 Değişkeni:\n")
print(feature_importance.head(20))
import pandas as pd

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Mevcut sütun isimlerini göster
print("📌 Veri Setindeki Mevcut Sütunlar:\n")
print(df.columns.tolist())
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Aşırı baskın değişkenleri çıkaralım (Gerçek sütun isimlerini kullanıyoruz!)
drop_features = ["Kan_Şekeri", "Ağrı_Konumu_Karın", "Uzuv_Kopmasi",
                 "Beyin_Kanamasi", "Kalp_Krizi", "Ic_Kanama"]
X = df.drop(columns=["Aciliyet_Seviyesi"] + drop_features)
y = df["Aciliyet_Seviyesi"]

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Güncellenmiş RandomForest modeli oluştur ve eğit
model = RandomForestClassifier(n_estimators=50, max_depth=3, random_state=42)
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli Pickle formatında kaydet (app.py için uygun format)
import pickle
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Yeni model (RandomForest) eğitildi ve Pickle formatında kaydedildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi ve `app.py` dosyasında kullanılabilir.")
import pandas as pd

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Aciliyet Seviyesi dağılımını incele
print("📌 Veri Setindeki Aciliyet Seviyesi Dağılımı:\n")
print(df["Aciliyet_Seviyesi"].value_counts())
import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# Veriyi eğitim (%80) ve test (%20) olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# LightGBM modelini oluştur
model = lgb.LGBMClassifier(n_estimators=100, learning_rate=0.1, random_state=42)

# Modeli eğit
model.fit(X_train, y_train)

# Test verisiyle tahmin yap ve doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli Pickle formatında kaydet (app.py için uygun format)
with open("trained_model.pkl", "wb") as file:
    pickle.dump(model, file)

# Sonuçları ekrana yazdır
print(f"✅ Yeni model (LightGBM) eğitildi ve Pickle formatında kaydedildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi ve `app.py` dosyasında kullanılabilir.")
import pandas as pd
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# Normalleştirilmiş veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# İlk 20 hastayı test edelim
X_sample = X.iloc[:20]
y_sample = y.iloc[:20]

# Model ile tahmin yap
y_pred_sample = model.predict(X_sample)

# Sonuçları ekrana yazdır
print("✅ Modelin İlk 20 Hasta için Tahmin Sonuçları:\n")
for i in range(20):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_sample.iloc[i]} | Model Tahmini={y_pred_sample[i]}")
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel

# Veri setini yükle
df = pd.read_csv("dengelenmis_veri_seti_normalize.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# Önce RandomForest ile en önemli değişkenleri belirleyelim
selector_model = RandomForestClassifier(n_estimators=100, random_state=42)
selector_model.fit(X, y)

# Önemli değişkenleri seç
selector = SelectFromModel(selector_model, threshold="median", prefit=True)
X_selected = selector.transform(X)

# Seçilen değişken isimlerini al
selected_features = X.columns[selector.get_support()]
print("\n📌 Seçilen En Önemli Değişkenler:\n", selected_features)

# Yeni veri setini oluştur
df_selected = pd.DataFrame(X_selected, columns=selected_features)
df_selected["Aciliyet_Seviyesi"] = y

# Yeni veri setini kaydet
df_selected.to_csv("optimized_data.csv", index=False)

print("\n✅ Veri başarıyla optimize edildi ve yeni veri seti kaydedildi: 'optimized_data.csv'")
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

# Optimize edilmiş veri setini yükle
df = pd.read_csv("optimized_data.csv")

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])
y = df["Aciliyet_Seviyesi"]

# Veriyi eğitim ve test setine ayır
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Yeni model oluştur ve eğit
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Modelin doğruluk oranını hesapla
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# Modeli kaydet
import joblib
joblib.dump(model, "trained_model.pkl")

print(f"\n✅ Yeni model eğitildi! Doğruluk oranı: {accuracy:.4f}")
print("🎯 Model 'trained_model.pkl' olarak kaydedildi ve `app.py` dosyasında kullanılabilir.")

import pandas as pd
import joblib

# Modeli yükle
model = joblib.load("trained_model.pkl")

# Test verisini yükle
df = pd.read_csv("optimized_data.csv")

# İlk 20 hastayı test edelim
X_test = df.drop(columns=["Aciliyet_Seviyesi"]).head(20)
y_real = df["Aciliyet_Seviyesi"].head(20)

# Model tahmini yap
y_pred = model.predict(X_test)

# Tahmin sonuçlarını ekrana yazdır
print("\n✅ Modelin İlk 20 Hasta için Tahmin Sonuçları:\n")
for i in range(20):
    print(f"Hasta {i+1}: Gerçek Aciliyet={y_real.iloc[i]} | Model Tahmini={y_pred[i]}")

print("\n✅ Model tahminleri başarıyla tamamlandı!")
print(f"X_test boyutu: {X_test.shape}")
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Bağımsız değişkenler (X) ve bağımlı değişken (y)
X = df.drop(columns=["Aciliyet_Seviyesi"])  # Hedef değişkeni çıkardık
y = df["Aciliyet_Seviyesi"]  # Hedef değişken

# Veriyi %80 eğitim - %20 test olarak bölelim
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Modeli yeniden eğitelim
model.fit(X_train, y_train)

# Yeni test tahminlerini alalım
y_pred_test = model.predict(X_test)

# Boyutları kontrol edelim
print(f"y_test boyutu: {len(y_test)}")
print(f"y_pred_test boyutu: {len(y_pred_test)}")

# Modelin sınıflandırma performansını gösterelim
print(classification_report(y_test, y_pred_test))
import pickle

# Modeli kaydet
with open("trained_model.pkl", "wb") as f:
    pickle.dump(model, f)
import pickle

# Modeli yükle
with open("trained_model.pkl", "rb") as f:
    model = pickle.load(f)

# Modelin tipini kontrol et
print(type(model))  # Eğer <class 'numpy.ndarray'> olarak çıkarsa, yanlış yüklenmiş demektir.
import pickle

# 1️⃣ Modeli yükle
with open("trained_model.pkl", "rb") as f:
    model = pickle.load(f)

# 2️⃣ Modelin tipini ekrana yazdır
print(f"✅ Model başarıyla yüklendi: {type(model)}")

# 3️⃣ Modelin tahmin yapıp yapmadığını kontrol et
if hasattr(model, "predict"):
    print("✅ Model tahmin yapabiliyor!")
else:
    print("⚠️ Model tahmin yapamıyor, yanlış kaydedilmiş olabilir.")
import numpy as np

# 1️⃣ Örnek bir hasta verisi oluşturalım (Rastgele veri, gerçek verilere uygun olmalı)
sample_patient = np.array([[0.55, 1, 0.8, 0.6, 0.75, 0, 1, 0, 0, 1,
                            1, 0, 0, 1, 0.9, 0.7, 0.3, 0, 1, 0,
                            0.6, 0.4, 0.7, 0.8, 1, 0.5, 0.3, 0, 1, 1,
                            0, 0, 1, 0, 1, 0, 0, 0.5, 1, 0.8,
                            0, 1, 0]])

# 2️⃣ Modelin tahmin yapmasını sağla
prediction = model.predict(sample_patient)

# 3️⃣ Tahmin sonucunu ekrana yazdır
print(f"🚑 Modelin Tahmini: {prediction[0]}")
import pandas as pd

# 1️⃣ Test için bir örnek hasta verisi oluşturalım (sütun isimleriyle birlikte)
columns = ['BMI', 'Nabız', 'Tansiyon_Sistolik', 'Tansiyon_Diastolik', 'Oksijen_Doygunluğu',
           'Kalp_Hastaligi', 'Kanser', 'Kolesterol_Sorunu', 'Kalp_Krizi', 'Ic_Kanama',
           'Kesik', 'Beyin_Kanamasi', 'Uzuv_Kopmasi', 'Omurilik_Zedelenmesi', 'Ağrı_Seviyesi',
           'Stres_Seviyesi', 'Ateş', 'Epilepsi', 'Böbrek_Yetmezliği', 'Şiddetli_Baş_Ağrısı',
           'Laboratuvar_Sonuçları', 'Kan_Şekeri', 'Kalp_Hızı_Değişkenliği', 'Vücut_Sıcaklığı_Değişkenliği',
           'Son_24_Saatte_Yemek_Yedi', 'Hasta_Kaç_Saat_Önce_Yaralandı', 'Hastanın_Önceki_Hastane_Ziyaretleri',
           'Acil_Servise_Geldiği_Saat', 'Bilinç_Durumu_Bilinçsiz', 'Bilinç_Durumu_Normal',
           'Bilinç_Durumu_Sersem', 'Yanık_1. Derece', 'Yanık_2. Derece', 'Yanık_3. Derece',
           'Olay_Türü_Sanayi Kazası', 'Göz_Bebeği_Tepkisi_Tepkisiz', 'Nörolojik_Belirtiler_Uyuşukluk',
           'Hastanın_Medikal_Geçmişi_Böbrek', 'Hastanın_Medikal_Geçmişi_Normal', 'Hastanın_Medikal_Geçmişi_Nörolojik',
           'Ağrı_Konumu_Karın', 'Ağrı_Konumu_Kol', 'Ağrı_Konumu_Sırt']

# 2️⃣ Veriyi pandas DataFrame formatına çevirelim
sample_patient_df = pd.DataFrame([sample_patient[0]], columns=columns)

# 3️⃣ Modelin tahmin yapmasını sağlayalım
prediction = model.predict(sample_patient_df)

# 4️⃣ Tahmin sonucunu ekrana yazdıralım
print(f"🚑 Modelin Tahmini (Düzeltildi): {prediction[0]}")
import pickle
import numpy as np

# 📌 Modeli yükle
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

print(f"✅ Model başarıyla yüklendi: {type(model)}")

# 📌 Örnek bir hasta verisi (Sıralama: Seçtiğin özelliklere göre olmalı!)
sample_patient = np.array([[35, 1, 24.5, 80, 120, 80, 98, 1, 0, 0, 1, 0, 0, 0, 1, 0, 8, 7, 38.2, 0, 120, 5.5, 36.5, 1, 2, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0]])

# 📌 Tahmin yap
prediction = model.predict(sample_patient)

print(f"🚑 Modelin Tahmini: {prediction[0]}")

import pickle
import pandas as pd
import numpy as np

# 📌 Modeli yükleyelim
with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

# 📌 Modelin beklediği özellikleri al
expected_features = model.feature_names_in_

# 📌 Yeni hasta verisi (örnek)
sample_patient = {
    "BMI": 22.5,
    "Nabız": 80,
    "Tansiyon_Sistolik": 120,
    "Tansiyon_Diastolik": 80,
    "Oksijen_Doygunluğu": 98,
    "Kalp_Hastaligi": 0,
    "Kanser": 0,
    "Kolesterol_Sorunu": 1,
    "Kalp_Krizi": 0,
    "Ic_Kanama": 0,
    "Kesik": 1,
    "Beyin_Kanamasi": 0,
    "Uzuv_Kopmasi": 0,
    "Omurilik_Zedelenmesi": 0,
    "Ağrı_Seviyesi": 5,
    "Stres_Seviyesi": 3,
    "Ateş": 37.2,
    "Epilepsi": 0,
    "Böbrek_Yetmezliği": 0,
    "Şiddetli_Baş_Ağrısı": 1,
    "Laboratuvar_Sonuçları": 1,
    "Kan_Şekeri": 90,
    "Kalp_Hızı_Değişkenliği": 75,
    "Vücut_Sıcaklığı_Değişkenliği": 0.5,
    "Son_24_Saatte_Yemek_Yedi": 1,
    "Hasta_Kaç_Saat_Önce_Yaralandı": 2,
    "Hastanın_Önceki_Hastane_Ziyaretleri": 0,
    "Acil_Servise_Geldiği_Saat": 12,
    "Bilinç_Durumu_Bilinçsiz": 0,
    "Bilinç_Durumu_Normal": 1,
    "Bilinç_Durumu_Sersem": 0,
    "Yanık_1. Derece": 0,
    "Yanık_2. Derece": 0,
    "Yanık_3. Derece": 0,
    "Olay_Türü_Sanayi Kazası": 0,
    "Göz_Bebeği_Tepkisi_Tepkisiz": 0,
    "Nörolojik_Belirtiler_Uyuşukluk": 0,
    "Hastanın_Medikal_Geçmişi_Böbrek": 0,
    "Hastanın_Medikal_Geçmişi_Normal": 1,
    "Hastanın_Medikal_Geçmişi_Nörolojik": 0,
    "Ağrı_Konumu_Karın": 1,
    "Ağrı_Konumu_Kol": 0,
    "Ağrı_Konumu_Sırt": 0
}

# 📌 Hasta verisini DataFrame formatına çevirelim
patient_df = pd.DataFrame([sample_patient])

# 📌 **Eksik veya fazla sütunları düzeltelim**
for feature in expected_features:
    if feature not in patient_df.columns:
        patient_df[feature] = 0  # Eksik sütunları 0 ile doldur

# 📌 Fazla sütunları temizleyelim
patient_df = patient_df[expected_features]

# 📌 Model ile tahmin yapalım
prediction = model.predict(patient_df)[0]

print(f"🚑 Modelin Tahmini (Düzeltilmiş): {prediction}")

import joblib

# Modelin değişkeni 'model' olmalıdır. Eğer farklıysa uygun olanı yaz.
joblib.dump(model, "trained_model_final.pkl")

print("✅ Model başarıyla kaydedildi: trained_model_final.pkl")
import joblib

# Modeli yükle
model = joblib.load("trained_model_final.pkl")

print("✅ Model başarıyla yüklendi:", type(model))
from sklearn.metrics import classification_report, accuracy_score

# Daha önce ayrılmış test verilerini kullan
y_pred_test = model.predict(X_test)

# Modelin doğruluğunu ölçelim
accuracy = accuracy_score(y_test, y_pred_test)
print(f"🎯 Modelin Test Doğruluk Oranı: {accuracy:.4f}")

# Sınıflandırma raporunu yazdıralım
print("📌 Sınıflandırma Raporu:\n", classification_report(y_test, y_pred_test))

import numpy as np
import pandas as pd

# Modelin eğitildiği sütun isimlerini al
feature_names = X_test.columns  # Eğer X_test yoksa, eğitildiği veri kümesindeki sütunları kullan

# Rastgele bir hasta oluştur
sample_patient = np.random.rand(1, len(feature_names))  # Rastgele değerler oluştur
sample_patient_df = pd.DataFrame(sample_patient, columns=feature_names)  # Veriyi DataFrame'e çevir

# Model tahminini yap
prediction = model.predict(sample_patient_df)[0]
print(f"🚑 Modelin Tahmini (Rastgele Hasta): {prediction}")

import numpy as np

# Her sınıf için 3 örnek hasta alalım
for urgency_level in [0, 1, 2]:
    print(f"\n🩺 Aciliyet Seviyesi: {urgency_level} için test ediliyor...")

    # O sınıfa ait rastgele 3 hasta seç
    sample_patients = X_test[y_test == urgency_level].sample(3, random_state=42)

    # Model tahminleri yap
    predictions = model.predict(sample_patients)

    # Sonuçları göster
    for i, pred in enumerate(predictions, 1):
        print(f"🔹 Hasta {i}: Gerçek={urgency_level} | Model Tahmini={pred}")
import joblib

# Modeli kaydet
joblib.dump(model, "trained_model_final.pkl")

# Özellik isimlerini kaydet (modelin doğru çalışması için gerekli!)
feature_names = list(X_test.columns)
joblib.dump(feature_names, "model_features.pkl")

print("✅ Model ve özellikler başarıyla kaydedildi!")

import pickle

with open("trained_model.pkl", "rb") as file:
    model = pickle.load(file)

print(model.feature_names_in_)  # Modelin beklediği sütunları listeler

print("✅ Modelin beklediği sütunlar:", model.feature_names_in_)

import joblib

# Modeli kaydet
joblib.dump(model, "trained_model_final.pkl")

# Modelin özellik isimlerini kaydet
feature_names = list(X_train.columns)  # Eğitimde kullanılan sütunlar
joblib.dump(feature_names, "model_features.pkl")

print("✅ Model ve özellikler başarıyla kaydedildi!")



import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
# Mevcut veri setini DataFrame'e çeviriyoruz
df = pd.DataFrame(data)

# 1. "Evet" - "Hayır" sütunlarını 0-1 olarak çeviriyoruz
evet_hayir_kolonlari = [
    "Kalp_Hastaligi", "Kanser", "Tansiyon_Problemi", "Panik_Atak", "Son_Ameliyat",
    "Kirik", "Cikik", "Kalp_Krizi", "Ic_Kanama", "Kesik", "Yaralanma", "Beyin_Kanamasi",
    "Uzuv_Kopmasi", "Sikisma", "Omurilik_Zedelenmesi", "Bulantı", "Kusma", "Bayılma",
    "Epilepsi", "KOAH", "Böbrek_Yetmezliği", "Zehirlenme", "Boğulma", "Nefes_Darlığı",
    "Şok_Belirtileri", "İshal", "Göğüs_Ağrısı", "Susuzluk_Belirtileri", "Son_24_Saatte_Yemek_Yedi", "Cilt_Kuruluğu"
]
for kolon in evet_hayir_kolonlari:
    df[kolon] = df[kolon].map({"Evet": 1, "Hayır": 0})

# 🔥 Bunu ekliyoruz
df = df.replace({"Evet": 1, "Hayır": 0})

# 2. Kategorik değişkenleri one-hot encoding ile dönüştürüyoruz
one_hot_kolonlar = [
    "Cinsiyet", "Bilinç_Durumu", "Yanık", "Hastanın_Medikal_Geçmişi",
    "Göz_Bebeği_Tepkisi", "Nörolojik_Belirtiler", "Olay_Türü", "Ağrı_Konumu"
]
df = pd.get_dummies(df, columns=one_hot_kolonlar)

# 3. Hedef değişkeni (etiket)
df["Aciliyet_Seviyesi"] = np.random.choice([0, 1, 2], size=len(df))  # 0=Normal, 1=Acil, 2=Kritik

# 4. Özellikler ve hedef ayrımı
X = df.drop("Aciliyet_Seviyesi", axis=1)
y = df["Aciliyet_Seviyesi"]

# 5. Eğitim ve test seti
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 6. Model eğitimi
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("✅ Model yeniden başarıyla eğitildi!")
import joblib

# Eğittiğimiz yeni modeli kaydediyoruz
joblib.dump(model, "model_yeni.pkl")  # İSİMİ FARKLI YAPTIK ✅

# Modelin beklediği sütunları da kaydediyoruz
joblib.dump(list(X.columns), "model_yeni_sutunlar.pkl")  # İSİMİ FARKLI YAPTIK ✅

print("✅ Yeni model ve özellikler başarıyla kaydedildi! (model_yeni.pkl)")
import joblib

# 🔹 Yeni eğittiğimiz modeli kaydediyoruz
joblib.dump(model, "trained_model_yeni.pkl")
joblib.dump(X_train.columns.tolist(), "model_features_yeni.pkl")

print("✅ Yeni model ve özellikler başarıyla 'trained_model_yeni.pkl' ve 'model_features_yeni.pkl' olarak kaydedildi!")
