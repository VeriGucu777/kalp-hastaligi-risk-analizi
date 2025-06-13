from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from extensions import db  # ✅ Eğer `db` burada tanımlıysa bu kalsın

# 📌 **Kullanıcı Modeli**
class Kullanici(db.Model, UserMixin):
    __tablename__ = "kullanicilar"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kullanici_adi = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    sifre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """📌 Kullanıcı şifresini hash'ler."""
        self.sifre = generate_password_hash(password)

    def check_password(self, password):
        """📌 Kullanıcının şifresini doğrular."""
        return check_password_hash(self.sifre, password)
# 📌 **Hasta Modeli**

# 📌 **Sağlık Verisi Modeli**
class SaglikVerisi(db.Model):
    __tablename__ = "saglik_verisi"

    id = db.Column(db.Integer, primary_key=True)
    hasta_id = db.Column(db.Integer, db.ForeignKey("patients.id"), nullable=False)
    yas = db.Column(db.Integer, nullable=False)
    cinsiyet = db.Column(db.String(10), nullable=False)
    tani = db.Column(db.String(100), nullable=True)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sağlık Verisi Hasta ID: {self.hasta_id} - {self.tani}>"

# 📌 **Mesajlaşma Modeli**
class Mesaj(db.Model):
    __tablename__ = "mesaj"

    id = db.Column(db.Integer, primary_key=True)
    gonderen_id = db.Column(db.Integer, db.ForeignKey("kullanicilar.id", ondelete="CASCADE"), nullable=False)
    alici_id = db.Column(db.Integer, db.ForeignKey("kullanicilar.id", ondelete="CASCADE"), nullable=False)
    icerik = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)
    okundu = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Mesaj {self.gonderen_id} → {self.alici_id}>"

# 📌 **Hatırlatıcı Modeli**
class Hatirlatici(db.Model):
    __tablename__ = "hatirlatici"

    id = db.Column(db.Integer, primary_key=True)
    kullanici_id = db.Column(db.Integer, db.ForeignKey("kullanicilar.id", ondelete="CASCADE"), nullable=False)
    baslik = db.Column(db.String(200), nullable=False)
    aciklama = db.Column(db.Text, nullable=True)
    tarih = db.Column(db.DateTime, nullable=False)
    kritik = db.Column(db.Boolean, default=False)
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Hatırlatıcı {self.baslik} - {self.kullanici_id}>"

# 📌 **Bildirim Modeli**
class Bildirim(db.Model):
    __tablename__ = "bildirim"

    id = db.Column(db.Integer, primary_key=True)
    kullanici_id = db.Column(db.Integer, db.ForeignKey("kullanicilar.id", ondelete="CASCADE"), nullable=True)
    baslik = db.Column(db.String(255), nullable=False)
    mesaj = db.Column(db.Text, nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    okundu = db.Column(db.Boolean, default=False)
    arsivlendi = db.Column(db.Boolean, default=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Bildirim {self.baslik} - {self.kullanici_id}>"

# 📌 **Not Modeli (Kişisel Notlar)**
class Not(db.Model):
    __tablename__ = "notlar"

    id = db.Column(db.Integer, primary_key=True)
    kullanici_email = db.Column(db.String(100), db.ForeignKey("kullanicilar.email"), nullable=False)
    baslik = db.Column(db.String(255), nullable=False)
    icerik = db.Column(db.Text, nullable=False)
    tarih = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Not {self.baslik} - {self.kullanici_email}>"

# 📌 **Acil Durum Çağrısı Modeli**
class EmergencyCall(db.Model):
    __tablename__ = "emergency_calls"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_name = db.Column(db.String(100), nullable=False)
    emergency_level = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<EmergencyCall {self.patient_name} - {self.emergency_level}>"

# 📌 **Genel Bildirim Modeli**
class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="Bilgi")
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

# 📌 **Veritabanını Başlatma Fonksiyonu**
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()  # 📌 Eğer Flask-Migrate kullanıyorsan bu satırı kaldır!
    print("✅ Veritabanı bağlantısı başarılı!")
