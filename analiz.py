import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle

# 📌 Veriyi yükle
df = pd.read_csv("heart.csv")

# 📌 Özellikler ve hedef
X = df.drop("target", axis=1)
y = 1 - df["target"]

# 📌 Train / Test ayır
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 📌 Model oluştur (DÜZGÜN HAL)
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=10,
    min_samples_split=5,
    random_state=42
)

# 📌 Eğit
model.fit(X_train, y_train)

# 📌 Tahmin
y_pred = model.predict(X_test)

# 📌 Sonuçlar
print("Train Accuracy:", model.score(X_train, y_train))
print("Test Accuracy:", model.score(X_test, y_test))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# 📌 Feature Importance
feature_importance = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values(by="importance", ascending=False)

# 📌 Grafik
plt.figure(figsize=(10,6))
feature_importance.sort_values(by="importance").plot(
    x="feature",
    y="importance",
    kind="barh"
)

plt.title("Feature Importance")
plt.xlabel("Importance")
plt.ylabel("Features")
plt.savefig("feature_importance.png")

print("Grafik kaydedildi ✅")

# 📌 Modeli kaydet
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model kaydedildi ✅")