from database import db
from models import HealthData

def hasta_bilgilerini_getir():
    hastalar = HealthData.query.all()  # Tüm hastaları getir
    for hasta in hastalar:
        print(f"Hasta ID: {hasta.id}, Yaş: {hasta.yas}, Cinsiyet: {hasta.cinsiyet}")

# 📌 Flask uygulaması çalışırken bu fonksiyonu kullanabiliriz.
if __name__ == "__main__":
    print("✅ Hasta bilgileri getiriliyor...")
    hasta_bilgilerini_getir()
