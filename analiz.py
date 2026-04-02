import pandas   as pd
df = pd.read_csv("heart.csv")
print(df.head())

df.columns = ["yas", "cinsiyet", "gogus_agrisi", "tansiyon", "kolesterol", "kan_sekeri",
              "ekg", "max_nabiz", "egzersiz_anjina", "st_depresyon", "egim", "damar_sayisi", "thal","hedef"]
print(df.head())

print(df["hedef"].value_counts())
print(df.info())
print(df.describe())
print(df.corr())

import pandas as pd

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

df = pd.read_csv("heart.csv")

plt.figure(figsize=(10,8))


plt.savefig("heatmap.png")

import pandas as pd

import matplotlib
matplotlib.use('Agg')

from sklearn.model_selection import train_test_split

X = df.drop("target", axis=1)
y = df["target"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("Train size:", X_train.shape)
print("Test size:", X_test.shape)

from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000, solver='liblinear')
model.fit(X_train, y_train)

# Tahmin
y_pred = model.predict(X_test)

# Doğruluk oranı
from sklearn.metrics import accuracy_score, confusion_matrix

accuracy = accuracy_score(y_test, y_pred)
print("Model doğruluk oranı:", accuracy)

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Model oluştur (stabil sonuç için random_state ekledik)
rf_model = RandomForestClassifier(random_state=42)

# Eğit
rf_model.fit(X_train, y_train)

# Tahmin
y_pred_rf = rf_model.predict(X_test)

# Accuracy
print("RF doğruluk:", accuracy_score(y_test, y_pred_rf))

# Confusion Matrix
print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred_rf))

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred_rf))

print(df.corr()
["target"].sort_values(ascending=False))

print("Train accuracy:",
rf_model.score(X_train, y_train))
print("Test accuracy:",
rf_model.score(X_test, y_test))


rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    min_samples_split=10,
    random_state=42
)
rf_model.fit(X_train, y_train)
print("Train accuracy:", rf_model.score(X_train, y_train))
print("Test accuracy:", rf_model.score(X_test, y_test))


feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": rf_model.feature_importances_
}).sort_values(by="importance", ascending=False)


import matplotlib
matplotlib.use('Agg')  # ekran yerine dosyaya kaydeder

import matplotlib.pyplot as plt

# Feature importance grafiği
feature_importance.sort_values(by="importance", ascending=True).plot(
    x="feature",
    y="importance",
    kind="barh",
    figsize=(10, 6)
)

plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Features")

# 🔥 Grafik kaydet
plt.savefig("feature_importance.png")

print("Grafik kaydedildi: feature_importance.png")

import pickle
pickle.dump(rf_model, open("model.pkl", "wb"))


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# veri setini yükle
df = pd.read_csv("heart.csv")

# özellikler ve hedef
X = df.drop("target", axis=1)
y = df["target"]

# veriyi böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# modeli oluştur
model = RandomForestClassifier()
model.fit(X_train, y_train)

# modeli kaydet (ESKİ MODELIN ÜZERİNE YAZAR)
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("YENİ MODEL OLUŞTURULDU ✅")

print(X.columns)
print(df["target"].value_counts())

print(X.head())
print(list(zip(X.columns,
model.feature_importances_)))


from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    random_state=42
)

