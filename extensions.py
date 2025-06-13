from flask_migrate import Migrate
from flask_login import LoginManager
from database import db  # ✅ database.py'deki db'yi kullanıyoruz.

# 📌 **Veritabanı Migration (Güncellemeleri Yönetme)**
migrate = Migrate()

# 📌 **Kullanıcı Oturum Yönetimi**
login_manager = LoginManager()
login_manager.login_view = "main.giris"  # 📌 Eğer giriş yapılmazsa yönlendirilecek sayfa
