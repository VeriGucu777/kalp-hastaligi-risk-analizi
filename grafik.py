import matplotlib.pyplot as plt
import numpy as np

def grafik_ciz(veri, feature_isimleri):

    importance = np.abs(veri[0])

    plt.figure()
    plt.barh(feature_isimleri, importance)
    plt.xlabel("Önem Değeri")
    plt.title("Feature Importance")

    plt.tight_layout()
    plt.savefig("static/feature_importance.png")
    plt.close()