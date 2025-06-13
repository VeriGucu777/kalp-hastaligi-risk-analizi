import os
from dotenv import load_dotenv  # ✅ .env dosyasını okumak için

load_dotenv()  # 📌 `.env` dosyasındaki bilgileri yükler

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # 📌 Proje ana dizini
    DATABASE_PATH = os.path.join(BASE_DIR, "instance", "hospital.db")  # 📌 Tam dosya yolu ile veritabanı

    # ✅ Veritabanı bağlantısı
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"  # 📌 **DOĞRU FORMAT**
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ✅ Güvenlik ayarları
    SECRET_KEY = os.environ.get("SECRET_KEY", "super_guvenli_bir_anahtar")  # 🔐 Rastgele bir anahtar

    # ✅ Oturum yönetimi ayarları
    SESSION_PROTECTION = "strong"  # 📌 Oturum koruma seviyesi
    REMEMBER_COOKIE_DURATION = 2678400  # 📌 Çerez süresi (31 gün)
    SESSION_PERMANENT = True  # 📌 Oturum süresini kalıcı yap

    # ✅ Flask-SQLAlchemy motor ayarları
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}  # 📌 Bağlantı havuzu sorunlarını önleme
