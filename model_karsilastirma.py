from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
# Veri setini yükle
df = pd.read_csv("heart.csv")

X = df.drop("target", axis=1)
y = df["target"]

# Veriyi böl
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Modeller
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Random Forest": RandomForestClassifier(),
    "Decision Tree": DecisionTreeClassifier()
}

# Sonuçları tut
results = {}

for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    results[name] = acc
    cm = confusion_matrix(y_test, y_pred)
    print("f{name} Confusion Matrix:")
    print(cm)
    print("---------------")
# Sonuçları yazdır
for model, acc in results.items():
    print(f"{model}: {acc:.2f}")

from sklearn.model_selection import cross_val_score
print("\nCross Validation Sonuçları:")
for name, model in models.items():
    scores = cross_val_score(model, X, y,cv=5)
    print(f"{name}: {scores.mean():.2f}")





