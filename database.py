from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ SQLAlchemy Nesnesi
db = SQLAlchemy()

# ✅ **Veritabanını Başlatan Fonksiyon**
def init_db(app):
    """Flask uygulamasını SQLAlchemy ile başlatır ve bağlar."""
    db.init_app(app)
    with app.app_context():
        db.create_all()  # 📌 Veritabanındaki tabloları oluştur
    print("✅ Veritabanı bağlantısı başarılı ve tablolar oluşturuldu!")

# ✅ **Kullanıcı Modeli**
class Kullanici(db.Model):
    __tablename__ = "kullanici"

    id = db.Column(db.Integer, primary_key=True)
    ad = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)

    def set_password(self, password):
        """📌 Kullanıcı şifresini hash'ler."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """📌 Kullanıcının şifresini doğrular."""
        return check_password_hash(self.password_hash, password)

# ✅ **Hasta Modeli**
class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=False)
    treatment_status = db.Column(db.String(50), nullable=False)
    kayit_tarihi = db.Column(db.DateTime, default=datetime.utcnow)  # 📌 Sütun doğru tanımlandı

    def to_dict(self):
        """📌 Nesneyi JSON formatına çevirir."""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "gender": self.gender,
            "diagnosis": self.diagnosis,
            "treatment_status": self.treatment_status,
            "kayit_tarihi": self.kayit_tarihi.strftime('%Y-%m-%d %H:%M:%S')
        }
