from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import timedelta
from functools import wraps
import os
import json
from dotenv import load_dotenv
# 📌 **Gerekli Modülleri Dahil Et**
import os
from datetime import timedelta
from flask import Flask, session, redirect, url_for, flash
from flask_login import LoginManager, current_user
from flask_migrate import Migrate
from functools import wraps
from dotenv import load_dotenv
from extensions import db, migrate, login_manager  # ✅ Gerekli bileşenleri extensions.py'den alıyoruz
from models import init_db  # ✅ Döngü sorunu olmadan import ettik
import matplotlib
matplotlib.use('Agg')  # ✅ Grafik çiziminde ekran yerine dosyaya kaydetmeye zorlar
import matplotlib.pyplot as plt  # Bunu da ekleyelim
from flask import request, redirect, url_for, flash
from datetime import datetime
# ✅ Acil Durum Çağrısı Oluşturma Rotası
from flask import request, flash, redirect, url_for
from utils import translate  # Çeviri fonksiyonunu içe aktardık
from flask import Flask
from extensions import db, migrate, login_manager  # ✅ Gerekli bileşenleri içe aktardık
from models import init_db  # ✅ Veritabanı modellerini içe aktardık
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from extensions import db, migrate, login_manager  # 📌 Genişletilmiş modülleri ekledik.
from models import Kullanici, init_db  # 📌 Modelleri ve veritabanı başlatma fonksiyonunu ekledik.
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import Kullanici, db
from extensions import migrate
from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify, send_file
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from extensions import migrate
from datetime import datetime, timedelta
import time
import csv
import os
from fpdf import FPDF
from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate  # 📌 Flask-Migrate eklendi
from database import db, init_db, Patient, Kullanici  # ✅ Tek seferde import ettik
from database import db, Patient  # 📌 `database.py` içindeki `db` ve `Patient` modelini al
from flask_cors import CORS
import matplotlib
matplotlib.use('Agg')  # SHAP grafiğini backend'de oluşturabilmek için
import shap
import io
import base64
from matplotlib import pyplot as plt
# --- Küçük yardımcı fonksiyonlar ---

def convert_evet_hayir(value):
    """'Evet' veya 'Hayır' değerlerini 1.0 veya 0.0'a çevirir."""
    if isinstance(value, str):
        value = value.strip().lower()
        if value == "evet":
            return 1.0
        elif value == "hayır":
            return 0.0
    return value

def one_hot_encode(data, field_name, possible_values):
    """One-hot encoding uygular. Önce tüm seçenekleri 0 yapar, sonra seçili olanı 1 yapar."""
    for option in possible_values:
        data[option] = 0.0

    selected_value = data.get(field_name)
    if selected_value:
        ohe_key = f"{field_name}_{selected_value}"
        if ohe_key in possible_values:
            data[ohe_key] = 1.0

    # Asıl alanı kaldır
    data.pop(field_name, None)

    return data

def prepare_features(data, required_columns):
    """Eksik sütunları tamamlar, sıralamayı modelin istediği hale getirir."""
    prepared = {}
    for col in required_columns:
        prepared[col] = float(data.get(col, 0.0))  # Eksikse 0.0 koy
    return prepared

# 📌 **Flask Uygulamasını Başlat**
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospital.db"
app.config["SECRET_KEY"] = "super_guvenli_bir_anahtar"
app.config["SESSION_PERMANENT"] = True

# 📌 **Veritabanı ve Migration Bağlantısı**
db.init_app(app)
migrate = Migrate(app, db)  # 📌 migrate nesnesi oluşturuldu

# 📌 **LoginManager Tanımlama**
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "giris"  # 📌 Kullanıcı giriş yapmamışsa yönlendirilecek sayfa

# 📌 **Dil dosyalarının bulunduğu klasör**
LANGUAGES_FOLDER = os.path.join(os.path.dirname(__file__), "templates/languages")
DEFAULT_LANGUAGE = "tr"
AVAILABLE_LANGUAGES = ["tr", "en", "de", "fr", "es", "it", "jp", "zh"]

# 📌 **Dil dosyalarını yükleyen fonksiyon**
def load_language(lang_code):
    """Seçilen dili JSON dosyasından yükler."""
    lang_file = os.path.join(LANGUAGES_FOLDER, f"{lang_code}.json")
    if os.path.exists(lang_file):
        try:
            with open(lang_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            print(f"❌ JSON Format Hatası: {e}")
            return {}
    print(f"❌ JSON Dosyası Bulunamadı: {lang_file}")
    return {}

# 📌 **Çeviri Fonksiyonu**
def translate(key):
    """JSON dosyasından çeviri yapar, bulunamazsa anahtar kelimeyi döndürür."""
    lang_code = session.get("language", DEFAULT_LANGUAGE)
    translations = load_language(lang_code)
    return translations.get(key, key)

# 📌 **Flask'e `translate` fonksiyonunu tanıt**
app.jinja_env.globals.update(translate=translate)

# 📌 **Flask Şablonlarına Çeviri Fonksiyonunu Tanıt**
@app.context_processor
def inject_translate():
    return dict(translate=translate)

# 📌 **Oturum Süresini Güncelleme**
@app.before_request
def refresh_session():
    session.permanent = True
    session.modified = True
    session.permanent_session_lifetime = timedelta(minutes=30)

# 📌 **Yetkilendirme Dekoratörü**
def role_required(role):
    def decorator(f):
        @login_required
        def decorated_function(*args, **kwargs):
            if session.get("role") != role:
                flash("⚠️ Bu sayfaya erişim izniniz yok!", "danger")
                return redirect(url_for("anasayfa"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
from models import Kullanici  # 📌 Kullanıcı modelini import ettik
from models import Kullanici  # 📌 Kullanıcı modelini import ettik
from models import Kullanici  # 📌 Kullanıcı modelini import ettik
@login_manager.user_loader
def load_user(user_id):
    """📌 Kullanıcıyı ID'ye göre veritabanından yükler."""
    from models import Kullanici  # Döngüsel import hatasını önlemek için içeride çağırıldı
    return Kullanici.query.get(int(user_id))  # Kullanıcıyı veritabanından al
# 📌 **Ana Yönlendirme Sayfası**
# 📌 **Ana Yönlendirme Sayfası**
@app.route("/")
def index():
    # 📌 Kullanıcı giriş yapmış mı?
    if session.get("logged_in"):
        role = session.get("role")

        # 📌 Eğer giriş yapılmışsa, ama önce giriş sayfasına yönlendir
        return redirect(url_for("giris"))

    return render_template("giris.html")  # Eğer giriş yapmamışsa giriş sayfasını göster

def load_users():
    users = Kullanici.query.all()
    print("📌 Veritabanındaki Kullanıcılar:")
    for user in users:
        print(
            f"ID: {user.id}, Ad: {user.kullanici_adi}, Email: {user.email}, Şifre: {user.sifre}, Rol: {user.rol}")  # 📌 Debugging için

    return [
        {
            "id": user.id,
            "ad": user.kullanici_adi,
            "email": user.email,
            "password": user.sifre,  # 📌 Burada sorun olabilir!
            "role": user.rol
        }
        for user in users
    ]

@login_manager.user_loader
def load_user(user_id):
    """📌 Kullanıcıyı ID'ye göre yükler."""
    from models import Kullanici
    return Kullanici.query.get(int(user_id))
from werkzeug.security import check_password_hash
@app.route("/")
def home():
    """ Kullanıcı giriş yapmamışsa giriş sayfasına yönlendir. """
    if not session.get("logged_in"):
        flash("Lütfen giriş yapın!", "warning")
        return redirect(url_for("giris"))

    role = session.get("role", "guest")

    if role == "hasta":
        return redirect(url_for("ana_sayfa"))  # **Hasta giriş yaptıysa, hasta sayfasına gitsin!**
    elif role == "saglik_calisani":
        return redirect(url_for("saglik_calisani"))  # **Sağlık çalışanı giriş yaptıysa, sağlık çalışanı sayfasına gitsin!**

    flash("Rol belirlenemedi, lütfen tekrar giriş yapın.", "danger")
    return render_template("giris.html")
from flask import request, redirect, url_for, flash, session, render_template
from werkzeug.security import check_password_hash
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required
from models import Kullanici  # Kullanıcı modeli
@app.route("/giris", methods=["GET", "POST"])
def giris():
    error = None
    users = load_users()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        selected_role = request.form.get("role", "").strip().lower().replace("ı", "i")

        print(f"🛠 Giriş yapan kullanıcı: {email}, Seçilen Rol: {selected_role}")

        # 📌 **Eşleşen kullanıcıları bul**
        matched_users = [u for u in users if u["email"] == email]

        if not matched_users:
            error = "❌ Hatalı giriş bilgileri! Lütfen tekrar deneyin."
            return render_template("giris.html", error=error)

        # 📌 **Şifre kontrolü ve rol doğrulaması**
        user = next((u for u in matched_users if check_password_hash(u["password"], password)), None)

        if not user:
            error = "❌ Yanlış şifre! Lütfen tekrar deneyin."
            print(f"❌ Yanlış giriş! Eposta: {email}")
            return render_template("giris.html", error=error)

        # 📌 **Rol doğrulama**
        user_roles = user["role"].split(",")

        if selected_role not in user_roles:
            error = "❌ Yanlış rol seçildi! Lütfen doğru rolü seçin."
            print(f"❌ Yanlış rol seçildi! Eposta: {email}, Seçilen Rol: {selected_role}, Kullanıcı Rolleri: {user_roles}")
            return render_template("giris.html", error=error)

        # 📌 **Başarılı giriş: Kullanıcıyı oturuma kaydet**
        session['logged_in'] = True
        session['email'] = user["email"]
        session['role'] = selected_role
        session['ad'] = user["ad"]

        print(f"✅ Başarılı giriş: {email}, Seçilen Rol: {selected_role}")
        print("🛠 Oturum Durumu:", session)  # ✅ **Oturum değişkenlerini kontrol et**

        # 📌 **Giriş sonrası yönlendirme**
        if selected_role == "hasta":
            return redirect(url_for("ana_sayfa"))
        elif selected_role == "saglik_calisani":
            return redirect(url_for("saglik_calisani"))

    return render_template("giris.html", error=error)

@app.route("/logout")
@login_required
def logout():
    """📌 Kullanıcı çıkış işlemi."""
    logout_user()
    session.clear()
    return redirect(url_for("giris"))
# 📌 **Şifremi Unuttum**
@app.route("/sifremi_unuttum", methods=["GET", "POST"])
def sifremi_unuttum():
    if request.method == "POST":
        email = request.form.get("email")
        kullanici = Kullanici.query.filter_by(email=email).first()
        if kullanici:
            flash("✅ Şifre sıfırlama talimatları e-posta adresinize gönderildi.", "success")
        else:
            flash("❌ Bu e-posta adresi sistemde kayıtlı değil!", "danger")
    return render_template("sifremi_unuttum.html")

# 📌 **Anasayfa**
@app.route("/anasayfa")
@login_required
def anasayfa():
    return render_template("ana_sayfa.html")

# 📌 **Hatırlatıcı Ekleme**
@app.route("/hatirlatici_ekle", methods=["POST"])
@login_required
def hatirlatici_ekle():
    data = request.get_json()
    baslik = data.get("baslik")
    tarih_str = data.get("tarih")

    if not baslik or not tarih_str:
        return jsonify({"error": "🚨 Başlık ve tarih zorunludur!"}), 400

    tarih = datetime.strptime(tarih_str, "%Y-%m-%dT%H:%M")
    yeni_hatirlatici = Hatirlatici(kullanici_id=current_user.id, baslik=baslik, tarih=tarih)

    db.session.add(yeni_hatirlatici)
    db.session.commit()
    return jsonify({"success": "✅ Hatırlatıcı başarıyla eklendi!"}), 201

# 📌 **Hatırlatıcı Listeleme**
@app.route("/hatirlatici_listele")
@login_required
def hatirlatici_listele():
    hatirlaticilar = Hatirlatici.query.filter_by(kullanici_id=current_user.id).all()
    liste = [{"id": h.id, "baslik": h.baslik, "tarih": h.tarih.strftime("%Y-%m-%d %H:%M")} for h in hatirlaticilar]
    return jsonify({"hatirlaticilar": liste})

# 📌 **Bildirimleri Arşivleme**
@app.route("/bildirim_arsivle/<int:notification_id>", methods=["POST"])
def bildirim_arsivle(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_archived = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

# 📌 **Acil Durum Çağrısı**
@app.route("/acil_durum_cagri", methods=["POST"])
def acil_durum_cagri():
    patient_name = request.form.get("patient_name")
    emergency_level = request.form.get("emergency_level")
    description = request.form.get("description")

    if not patient_name or not emergency_level or not description:
        flash("⚠️ Lütfen tüm alanları doldurun!", "warning")
        return redirect(url_for("anasayfa"))

    new_call = EmergencyCall(patient_name=patient_name, emergency_level=emergency_level, description=description)
    db.session.add(new_call)
    db.session.commit()

    flash("✅ Acil durum çağrısı başarıyla oluşturuldu!", "success")
    return redirect(url_for("anasayfa"))
# 📌 **Kayıt Ol (Üye Ol) Sayfası**
@app.route("/kayit_ol", methods=["GET", "POST"])
def kayit_ol():
    if request.method == "POST":
        email = request.form.get("email")
        sifre = request.form.get("sifre")
        isim = request.form.get("isim")

        # 📌 Kullanıcı zaten var mı?
        mevcut_kullanici = Kullanici.query.filter_by(email=email).first()
        if mevcut_kullanici:
            flash("❌ Bu e-posta adresi zaten kayıtlı!", "danger")
            return redirect(url_for("kayit_ol"))

        # 📌 Yeni kullanıcı oluştur
        yeni_kullanici = Kullanici(email=email, isim=isim)
        yeni_kullanici.set_password(sifre)

        db.session.add(yeni_kullanici)
        db.session.commit()

        flash("✅ Kayıt başarılı! Şimdi giriş yapabilirsiniz.", "success")
        return redirect(url_for("giris"))

    return render_template("kayit_ol.html")
@app.route("/ana_sayfa")
@login_required
def ana_sayfa():
    if session.get("role") != "hasta":
        flash("Bu sayfaya erişmek için hasta olarak giriş yapmalısınız!", "danger")
        return redirect(url_for("giris"))

    # 📌 Günlük sağlık önerileri listesi
    health_tips = [
        "Günde en az 2 litre su içmelisiniz.",
        "Her gün en az 30 dakika yürüyüş yapın.",
        "Uyku düzeninize dikkat edin, en az 7 saat uyuyun.",
        "Sağlıklı beslenmeye özen gösterin, fast food tüketimini azaltın.",
        "Düzenli egzersiz yaparak kaslarınızı güçlendirin.",
        "Meyve ve sebze tüketimini artırın.",
        "Şeker ve tuz tüketimini azaltın.",
        "Stresten uzak durmaya çalışın, meditasyon yapabilirsiniz.",
        "Gün içinde kısa molalar vererek dinlenin.",
        "Göz sağlığınız için uzun süre ekran karşısında kalmamaya özen gösterin."
    ]

    return render_template("ana_sayfa.html", ad=session.get("ad", "Ziyaretçi"), health_tips=health_tips)

from flask import Flask, current_app

@app.context_processor
def inject_notifications():
    """📌 Bildirimleri şablonlara otomatik olarak iletmek için kullanılır."""
    try:
        with app.app_context():  # ✅ Flask uygulama bağlamı içinde çalıştır
            from models import Notification  # ✅ Döngüsel import hatasını önledik!
            unread_count = Notification.query.filter_by(is_read=False).count()
    except Exception as e:
        print(f"⚠️ Bildirim yükleme hatası: {e}")  # 📌 Hata ayıklamak için
        unread_count = 0
    return dict(unread_count=unread_count)
# 📌 Hatırlatıcı Silme
@app.route('/hatirlatici_sil/<int:hatir_id>', methods=['DELETE'])
@login_required
def hatirlatici_sil(hatir_id):
    """📌 Kullanıcının belirli bir hatırlatıcısını siler."""
    try:
        # 📌 Kullanıcı giriş yapmamışsa yönlendir
        if not current_user.is_authenticated:
            return redirect(url_for('giris'))

        # 📌 Silinecek hatırlatıcıyı getir
        hatirlatici = Hatirlatici.query.get_or_404(hatir_id)

        # 📌 Kullanıcıya ait olup olmadığını kontrol et
        if hatirlatici.kullanici_id != current_user.id:
            return jsonify({'success': False, 'error': '🚫 Yetkisiz işlem!'}), 403

        # 📌 Hatırlatıcıyı veritabanından sil
        db.session.delete(hatirlatici)
        db.session.commit()

        return jsonify({'success': True, 'message': '✅ Hatırlatıcı başarıyla silindi!'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': f'❌ Hata oluştu: {str(e)}'}), 500
from models import Hatirlatici, Not  # ✅ Gerekli modelleri içe aktardık

# 📌 Önceki çakışmayı önlemek için rota varsa siliyoruz
if 'saglikci_hatirlaticilar' in app.view_functions:
    del app.view_functions['saglikci_hatirlaticilar']
# 📌 Kullanıcının Hatırlatıcılarını Getir
from models import Hatirlatici  # ✅ Modeli içe aktardık
from datetime import datetime
from flask import jsonify
# 📌 Eğer `hatirlatici_listele` fonksiyonu zaten tanımlıysa, yeniden ekleme!
if 'hatirlatici_listele' in app.view_functions:
    del app.view_functions['hatirlatici_listele']

@app.route("/hatirlatici_listele")
@login_required
def hatirlatici_listele():
    """📌 Kullanıcının tüm hatırlatıcılarını getirir."""
    try:
        hatirlaticilar = (
            Hatirlatici.query
            .filter_by(kullanici_id=current_user.id)
            .order_by(Hatirlatici.tarih.asc())
            .all()
        )

        liste = [
            {
                "id": hatir.id,
                "baslik": hatir.baslik,
                "aciklama": hatir.aciklama,
                "tarih": hatir.tarih.strftime("%Y-%m-%dT%H:%M"),
                "kritik": (hatir.tarih - datetime.now()).total_seconds() < 3600
            }
            for hatir in hatirlaticilar
        ]
        return jsonify({"success": True, "hatirlaticilar": liste}), 200

    except Exception as e:
        return jsonify({"error": f"❌ Hata oluştu: {str(e)}"}), 500

# 📌 **Yetki Gerektiren Sayfalar İçin Dekoratör**
def role_required(role):
    """📌 Kullanıcının belirli bir role sahip olup olmadığını kontrol eden dekoratör."""
    def decorator(f):
        @login_required
        def decorated_function(*args, **kwargs):
            if session.get("role") != role:
                flash("⚠️ Bu sayfaya erişim izniniz yok!", "danger")
                return redirect(url_for("main.anasayfa"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# 📌 **Eğer önceden `hatirlatici_ekle` varsa kaldır**
if "hatirlatici_ekle" in app.view_functions:
    del app.view_functions["hatirlatici_ekle"]

# 📌 **Hatırlatıcı Ekleme Rotası**
@app.route("/hatirlatici_ekle", methods=["POST"])
@login_required
def hatirlatici_ekle():
    """📌 Kullanıcının yeni bir hatırlatıcı eklemesini sağlar."""
    try:
        data = request.get_json()
        baslik = data.get("baslik")
        aciklama = data.get("aciklama", "")
        tarih_str = data.get("tarih")

        if not baslik or not tarih_str:
            return jsonify({"error": "🚨 Başlık ve tarih zorunludur!"}), 400

        tarih = datetime.strptime(tarih_str, "%Y-%m-%dT%H:%M")

        yeni_hatirlatici = Hatirlatici(
            kullanici_id=current_user.id,
            baslik=baslik,
            aciklama=aciklama,
            tarih=tarih
        )
        db.session.add(yeni_hatirlatici)
        db.session.commit()
        return jsonify({"success": "✅ Hatırlatıcı başarıyla eklendi!"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"❌ Hata oluştu: {str(e)}"}), 500

# 📌 **Önceden Tanımlanmış Route'ları Kaldır (Çakışmaları Önlemek İçin)**
for route in ["hatirlatici_listele", "hatirlatici_sil"]:
    if route in app.view_functions:
        del app.view_functions[route]

# 📌 **Hatırlatıcı Listeleme Rotası**
@app.route("/hatirlatici_listele")
@login_required
def hatirlatici_listele():
    """📌 Kullanıcının tüm hatırlatıcılarını getirir."""
    try:
        hatirlaticilar = (
            Hatirlatici.query
            .filter_by(kullanici_id=current_user.id)
            .order_by(Hatirlatici.tarih.asc())
            .all()
        )

        su_an = datetime.now()
        liste = [
            {
                "id": hatir.id,
                "baslik": hatir.baslik,
                "aciklama": hatir.aciklama,
                "tarih": hatir.tarih.strftime("%Y-%m-%dT%H:%M"),
                "kritik": (hatir.tarih - su_an).total_seconds() < 3600
            } for hatir in hatirlaticilar
        ]
        return jsonify({"success": True, "hatirlaticilar": liste}), 200

    except Exception as e:
        return jsonify({"error": f"❌ Hata oluştu: {str(e)}"}), 500

# 📌 **Hatırlatıcı Silme Rotası**
@app.route("/hatirlatici_sil/<int:hatir_id>", methods=["POST"])
@login_required
def hatirlatici_sil(hatir_id):
    """📌 Kullanıcının hatırlatıcısını silmesini sağlar."""
    try:
        hatirlatici = Hatirlatici.query.get(hatir_id)
        if not hatirlatici or hatirlatici.kullanici_id != current_user.id:
            return jsonify({"error": "🚫 Yetkisiz işlem veya hatırlatıcı bulunamadı!"}), 403

        db.session.delete(hatirlatici)
        db.session.commit()
        return jsonify({"success": "✅ Hatırlatıcı başarıyla silindi!"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"❌ Hata oluştu: {str(e)}"}), 500

# 📌 **Okunmamış Bildirimleri Sayfaya Ekler**
@app.context_processor
def inject_notifications():
    """📌 Sayfalara okunmamış bildirim sayısını ekler."""
    try:
        unread_count = Notification.query.filter_by(is_read=False).count()
    except Exception as e:
        print(f"⚠️ Bildirim yükleme hatası: {e}")  # Hata ayıklama için
        unread_count = 0
    return dict(unread_notifications_count=unread_count)
import os
from flask import send_file, current_app
from fpdf import FPDF

# 📌 Önceden tanımlanmış `hasta_raporu_pdf` varsa kaldırarak çakışmayı önleyelim.
if "hasta_raporu_pdf" in app.view_functions:
    del app.view_functions["hasta_raporu_pdf"]

@app.route('/hasta_raporu_pdf/<int:hasta_id>')
def hasta_raporu_pdf(hasta_id):
    """📄 Seçilen hastanın detaylı raporunu PDF olarak oluştur ve indir."""

    # 📌 Hasta ID’ye göre veritabanından hasta bilgisini al
    hasta = Patient.query.get(hasta_id)
    if not hasta:
        return "Hata: Hasta bulunamadı!", 404

    # 📌 PDF oluştur
    pdf = FPDF()
    pdf.add_page()

    # 📌 Türkçe destekli fontu ekleyelim
    FONT_PATH = os.path.join(current_app.root_path, "static", "fonts", "DejaVuSans.ttf")  # 📌 Font dosya yolu
    try:
        if os.path.exists(FONT_PATH):
            pdf.add_font("DejaVuSans", "", FONT_PATH, uni=True)  # ✅ Türkçe desteği için font yüklendi.
            pdf.set_font("DejaVuSans", size=12)
            print("✅ Font başarıyla yüklendi: DejaVuSans")
        else:
            raise FileNotFoundError("⚠️ Uyarı: DejaVuSans.ttf bulunamadı, Arial fontu kullanılacak.")
    except Exception as e:
        print(f"❌ Font yükleme hatası: {e}")
        pdf.set_font("Arial", size=12)

    # 📌 PDF Başlık
    pdf.cell(200, 10, "Hasta Raporu", ln=True, align='C')
    pdf.ln(10)  # Satır boşluğu bırak

    # 📌 Hasta bilgilerini ekleyelim
    pdf.cell(200, 10, f"Ad: {hasta.name}", ln=True)
    pdf.cell(200, 10, f"Yaş: {hasta.age}", ln=True)
    pdf.cell(200, 10, f"Cinsiyet: {hasta.gender}", ln=True)
    pdf.cell(200, 10, f"Teşhis: {hasta.diagnosis}", ln=True)
    pdf.cell(200, 10, f"Tedavi Durumu: {hasta.treatment_status}", ln=True)
    pdf.cell(200, 10, f"Kayıt Tarihi: {hasta.kayit_tarihi.strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
    pdf.ln(10)  # Boşluk bırak

    pdf.set_font("Arial", size=12)

    # 📌 Grafiklerin tam yolunu belirleyelim
    grafik_konumu = os.path.join(current_app.root_path, "static", "raporlar")
    os.makedirs(grafik_konumu, exist_ok=True)  # Eğer yoksa dizini oluştur

    grafik_dosyalar = [
        "grafik_1.png",
        "grafik_2.png",
        "grafik_3.png",
        "grafik_4.png",
        "grafik_5.png"
    ]

    # 📌 Grafikleri PDF'ye ekleyelim
    for grafik in grafik_dosyalar:
        grafik_yolu = os.path.join(grafik_konumu, grafik)

        if os.path.exists(grafik_yolu):  # Grafik dosyası varsa ekle
            try:
                pdf.image(grafik_yolu, x=10, w=180)  # Grafiği PDF'ye ekle
                pdf.ln(10)  # Grafikler arasında boşluk bırak
                print(f"✅ {grafik} PDF'ye eklendi!")  # Terminal için log
            except Exception as e:
                print(f"⚠️ Grafik ekleme hatası: {grafik} - {e}")
                pdf.cell(200, 10, f"⚠️ {grafik} yüklenemedi!", ln=True)
        else:
            print(f"⚠️ Grafik bulunamadı: {grafik_yolu}")  # Hata ayıklamak için
            pdf.cell(200, 10, f"⚠️ {grafik} bulunamadı!", ln=True)

    # 📌 PDF dosyasını kaydet
    pdf_folder = os.path.join(current_app.root_path, "static", "raporlar")
    os.makedirs(pdf_folder, exist_ok=True)  # 📌 Eğer klasör yoksa oluştur
    pdf_path = os.path.join(pdf_folder, f"hasta_raporu_{hasta_id}.pdf")

    try:
        pdf.output(pdf_path)
        print(f"📄 PDF başarıyla oluşturuldu: {pdf_path}")
    except Exception as e:
        print(f"❌ PDF oluşturma hatası: {e}")
        return f"Hata: PDF oluşturulamadı! Hata Detayı: {str(e)}", 500

    # 📌 Eğer buraya kadar geldiysek, dosyanın var olup olmadığını kontrol edelim
    if not os.path.exists(pdf_path):
        print(f"❌ Hata: PDF dosyası oluşturulamadı! Dosya yolu: {pdf_path}")
        return f"Hata: PDF dosyası bulunamadı! {pdf_path}", 500

    # 📌 Son olarak dosyayı göndermeden önce yazdıralım
    print(f"✅ PDF Dosyası Hazır, Gönderiliyor: {pdf_path}")

    return send_file(pdf_path, as_attachment=True, mimetype="application/pdf")

@app.route('/raporlar')
def raporlar():
    return render_template('raporlar.html')

@app.route('/yeni_rapor')
def yeni_rapor():
    return render_template('yeni_rapor.html')

@app.route('/rapor_kaydet', methods=['POST'])
def rapor_kaydet():
    baslik = request.form.get('baslik')
    icerik = request.form.get('icerik')

    # 📌 Burada veritabanına kaydedebilirsiniz
    print(f"Yeni Rapor Kaydedildi: {baslik}")

    return redirect(url_for('raporlar'))

@app.route('/mesajlar')
def mesajlar():
    return render_template('mesajlar.html')

@app.route('/aktif_tedavi')
def aktif_tedavi():
    return render_template('aktif_tedavi.html')

@app.route('/bekleyen_raporlar')
def bekleyen_raporlar():
    return render_template('bekleyen_raporlar.html')

# 📌 Hasta Düzenleme Sayfası
@app.route('/edit_patient/<int:patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)

    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.gender = request.form['gender']
        patient.diagnosis = request.form['diagnosis']
        patient.treatment_status = request.form['treatment_status']
        patient.raporlar = request.form.get('raporlar', '')  # Eğer formda boş olabilir ise get() kullan
        patient.randevular = request.form.get('randevular', '')
        patient.tedaviler = request.form.get('tedaviler', '')
        patient.operasyonlar = request.form.get('operasyonlar', '')
        patient.alerjiler = request.form.get('alerjiler', '')
        patient.ilaclar = request.form.get('ilaclar', '')

        db.session.commit()
        flash("Hasta bilgileri başarıyla güncellendi!", "success")
        return redirect(url_for('hasta_detay', hasta_id=patient.id))

    return render_template('edit_patient.html', patient=patient)
@app.route('/hasta_tahmin/<int:patient_id>', methods=['POST'])
def hasta_tahmin(patient_id):
    # 📌 Hastayı veritabanından al
    patient = Patient.query.get_or_404(patient_id)

    # 📌 Hastanın tahmin için gerekli özelliklerini modele gönderelim
    hasta_verisi = [
        patient.age,
        1 if patient.gender == "Erkek" else 0,  # Cinsiyeti sayıya çeviriyoruz
        patient.treatment_status == "Devam Ediyor",
        len(patient.diagnosis)  # Teşhis uzunluğu bir faktör olabilir
    ]

    # 📌 Model tahmini yap
    tahmin = model.predict([hasta_verisi])[0]  # İlk sonucu alıyoruz

    # 📌 Tahmini kullanıcıya göster
    flash(f"📊 Model Tahmini: {tahmin}", "info")

    return redirect(url_for('hasta_takip'))
# 📌 📂 Bildirimi Arşivleme
  # 🔹 Modeli içe aktaralım
from flask import jsonify, render_template

from models import Notification
if 'bildirim_arsivle' in app.view_functions:
    del app.view_functions['bildirim_arsivle']

@app.route('/bildirim_arsivle/<int:notification_id>', methods=['POST'])
def bildirim_arsivle(notification_id):
    """📌 Bildirimi arşivler."""
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_archived = True
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 404

# 📌 Eğer önceki arsivlenen_bildirimler fonksiyonu zaten kayıtlıysa kaldır
if 'arsivlenen_bildirimler' in app.view_functions:
    del app.view_functions['arsivlenen_bildirimler']

@app.route('/arsivlenen_bildirimler')
def arsivlenen_bildirimler():
    """📌 Arşivlenen bildirimleri getirir ve ekranda gösterir."""
    archived_notifications = Notification.query.filter_by(is_archived=True).all()
    return render_template('arsivlenen_bildirimler.html', notifications=archived_notifications)

# 📌 Eğer önceki bildirim_ekle fonksiyonu zaten tanımlıysa kaldır
if 'bildirim_ekle' in globals():
    del bildirim_ekle

def bildirim_ekle(title, message, category="Bilgi"):
    """📌 Yeni bir bildirim oluşturur ve veritabanına ekler."""
    try:
        yeni_bildirim = Notification(
            title=title,
            message=message,
            category=category
        )
        db.session.add(yeni_bildirim)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"❌ Bildirim eklenirken hata oluştu: {e}")

# 📌 Eğer önceki inject_notifications fonksiyonu zaten tanımlıysa kaldır
if 'inject_notifications' in app.template_context_processors[None]:
    del app.template_context_processors[None]['inject_notifications']

@app.context_processor
def inject_notifications():
    """📌 Sayfadaki bildirim ikonuna okunmamış bildirim sayısını ekler."""
    unread_count = Notification.query.filter_by(is_read=False).count()
    return dict(unread_notifications_count=unread_count)

# 📌 Eğer önceki bildirimler fonksiyonu zaten tanımlıysa kaldır
if 'bildirimler' in app.view_functions:
    del app.view_functions['bildirimler']

@app.route('/bildirimler')
def bildirimler():
    """📌 Tüm bildirimleri sıralayarak gösterir."""
    try:
        notifications = Notification.query.order_by(Notification.timestamp.desc()).all()
        return render_template('bildirimler.html', notifications=notifications)
    except Exception as e:
        print(f"❌ Bildirimler yüklenirken hata oluştu: {e}")
        return render_template('bildirimler.html', notifications=[])

# 📌 Eğer önceki bildirim_sil fonksiyonu zaten tanımlıysa kaldır
if 'bildirim_sil' in app.view_functions:
    del app.view_functions['bildirim_sil']

@app.route('/bildirim_sil/<int:notification_id>', methods=['POST'])
def bildirim_sil(notification_id):
    """📌 Belirtilen bildirimi siler."""
    try:
        notification = db.session.get(Notification, notification_id)  # ✅ SQLAlchemy 2.0 uygun hale getirildi

        if not notification:
            return jsonify({'success': False, 'message': '❌ Bildirim bulunamadı!'}), 404

        db.session.delete(notification)
        db.session.commit()
        return jsonify({'success': True, 'message': '✅ Bildirim başarıyla silindi!'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'❌ Hata oluştu: {str(e)}'}), 500
# 📌 Hızlı Erişim Sayfası Rotası
if 'hizli_erisim' in app.view_functions:
    del app.view_functions['hizli_erisim']

@app.route('/hizli_erisim')
def hizli_erisim():
    """📌 Hızlı Erişim Sayfası"""
    return render_template('hizli_erisim.html')
# Eğer rota tanımlıysa önce sil
if 'acil_durum_mudahale' in app.view_functions:
    del app.view_functions['acil_durum_mudahale']

@app.route('/acil_durum_mudahale')
def acil_durum_mudahale():
    return render_template("acil_durum_mudahale.html")  # ✅ HTML sayfasını çağırıyor

# 📌 Eğer önceki bos_yogun_bakim fonksiyonu zaten tanımlıysa kaldır
if 'bos_yogun_bakim' in app.view_functions:
    del app.view_functions['bos_yogun_bakim']

@app.route('/bos_yogun_bakim')
def bos_yogun_bakim():
    """📌 Boş yoğun bakım yataklarını listeleyen sayfayı döndürür."""
    try:
        return render_template('bos_yogun_bakim.html')
    except Exception as e:
        print(f"❌ Boş yoğun bakım sayfası yüklenirken hata oluştu: {e}")
        return render_template('error.html', message="Boş yoğun bakım sayfası yüklenirken hata oluştu.")

# 📌 Önce mevcut rotaların tanımlı olup olmadığını kontrol edelim ve varsa kaldıralım
routes_to_remove = [
    "acil_durum_istatistikleri",
    "acil_raporlar",
    "bekleyen_tedaviler",
    "tamamlanan_tedaviler"
]

for route in routes_to_remove:
    if route in app.view_functions:
        del app.view_functions[route]

# 📌 Acil Durum İstatistikleri Sayfası
@app.route('/acil_durum_istatistikleri')
def acil_durum_istatistikleri():
    """📌 Acil durumlara ait istatistiklerin gösterildiği sayfa"""
    try:
        return render_template('acil_durum_istatistikleri.html')
    except Exception as e:
        print(f"❌ Acil durum istatistikleri sayfası yüklenirken hata oluştu: {e}")
        return render_template('error.html', message="Acil durum istatistikleri sayfası yüklenirken hata oluştu.")

# 📌 Acil Raporlar Sayfası
@app.route('/acil_raporlar')
def acil_raporlar():
    """📌 Acil durumlarla ilgili raporların gösterildiği sayfa"""
    try:
        return render_template('acil_raporlar.html')
    except Exception as e:
        print(f"❌ Acil raporlar sayfası yüklenirken hata oluştu: {e}")
        return render_template('error.html', message="Acil raporlar sayfası yüklenirken hata oluştu.")

# 📌 Bekleyen Tedaviler Sayfası
@app.route('/bekleyen_tedaviler')
def bekleyen_tedaviler():
    """📌 Bekleyen tedavilerin listelendiği sayfa"""
    try:
        return render_template('bekleyen_tedaviler.html')
    except Exception as e:
        print(f"❌ Bekleyen tedaviler sayfası yüklenirken hata oluştu: {e}")
        return render_template('error.html', message="Bekleyen tedaviler sayfası yüklenirken hata oluştu.")

# 📌 Tamamlanan Tedaviler Sayfası
@app.route('/tamamlanan_tedaviler')
def tamamlanan_tedaviler():
    """📌 Tamamlanan tedavilerin gösterildiği sayfa"""
    try:
        return render_template('tamamlanan_tedaviler.html')
    except Exception as e:
        print(f"❌ Tamamlanan tedaviler sayfası yüklenirken hata oluştu: {e}")
        return render_template('error.html', message="Tamamlanan tedaviler sayfası yüklenirken hata oluştu.")
# 📌 Önce bu rota tanımlı mı kontrol edelim ve varsa kaldıralım
if "acil_durum_cagri" in app.view_functions:
    del app.view_functions["acil_durum_cagri"]

@app.route('/acil_durum_cagri', methods=['GET', 'POST'])
def acil_durum_cagri():
    """📌 Yeni bir acil çağrı oluşturur ve kaydeder."""
    try:
        patient_name = request.form.get('patient_name')
        emergency_level = request.form.get('emergency_level')
        description = request.form.get('description')

        if not patient_name or not emergency_level or not description:
            flash("⚠️ Lütfen tüm alanları doldurun!", "warning")
            return redirect(url_for('acil_durum_mudahale'))

        # 📌 Yeni acil çağrı oluştur ve veritabanına ekle
        new_call = EmergencyCall(
            patient_name=patient_name.strip(),
            emergency_level=emergency_level.strip(),
            description=description.strip()
        )
        db.session.add(new_call)
        db.session.commit()

        flash("✅ Acil durum çağrısı başarıyla oluşturuldu!", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"❌ Hata oluştu: {str(e)}", "danger")

    finally:
        db.session.remove()  # 📌 Bağlantıyı güvenli bir şekilde kapatıyoruz

    return redirect(url_for('acil_durum_mudahale'))
from flask import request, send_file
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# 📌 Eğer önceki hastane_ici_acil fonksiyonu varsa, önce kaldır
if 'hastane_ici_acil' in app.view_functions:
    del app.view_functions['hastane_ici_acil']

@app.route('/hastane_ici_acil')
def hastane_ici_acil():
    """🏥 Hastane içi acil çağrıyı bildirir."""
    return "🏥 Hastane içi acil çağrı bildirildi!"

# 📌 Eğer önceki dis_acil fonksiyonu varsa, önce kaldır
if 'dis_acil' in app.view_functions:
    del app.view_functions['dis_acil']

@app.route('/dis_acil')
def dis_acil():
    """📞 112 veya en yakın hastaneye acil çağrı yapar."""
    return "📞 112 veya en yakın hastane çağrısı yapıldı!"

# 📌 Eğer önceki en_yakin_hastane fonksiyonu varsa, önce kaldır
if 'en_yakin_hastane' in app.view_functions:
    del app.view_functions['en_yakin_hastane']

@app.route('/en_yakin_hastane')
def en_yakin_hastane():
    """📍 En yakın hastaneye yönlendirme yapar."""
    lat = request.args.get('lat')  # 📌 Enlem (Latitude)
    lon = request.args.get('lon')  # 📌 Boylam (Longitude)

    if lat and lon:
        return f"📍 En Yakın Hastane için Yönlendirme Yapılıyor... (Konum: {lat}, {lon})"
    else:
        return "🚨 Konum bilgisi alınamadı!"

# 📌 Eğer önceki acil_durum_istatistikleri_pdf fonksiyonu varsa, önce kaldır
if 'acil_durum_istatistikleri_pdf' in app.view_functions:
    del app.view_functions['acil_durum_istatistikleri_pdf']

@app.route('/acil_durum_istatistikleri/pdf')
def acil_durum_istatistikleri_pdf():
    """📌 Acil Durum İstatistikleri PDF Olarak İndirilir"""

    try:
        # 📌 Grafiklerin olduğu bir PDF oluştur
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(200, height - 50, "📊 Acil Durum İstatistikleri")

        # 📌 Örnek grafik (Gerçek grafikleri buraya ekleyelim)
        plt.figure(figsize=(6, 4))
        labels = ["Acil Servis", "Yoğun Bakım", "Genel Servis"]
        values = [7, 3, 5]  # Örnek acil hasta sayıları
        plt.bar(labels, values, color=["red", "blue", "green"])
        plt.title("Hastane Acil Hasta Dağılımı")
        plt.xlabel("Bölüm")
        plt.ylabel("Hasta Sayısı")

        img_buffer = BytesIO()
        plt.savefig(img_buffer, format="png")
        img_buffer.seek(0)
        plt.close()

        # 📌 PDF'e resmi ekleyelim
        pdf.drawInlineImage(img_buffer, 100, height - 300, width=400, height=200)

        pdf.save()
        buffer.seek(0)

        return send_file(
            buffer,
            as_attachment=True,
            download_name="acil_durum_istatistikleri.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        print(f"❌ PDF oluşturulurken hata oluştu: {e}")
        return "❌ PDF oluşturulurken bir hata oluştu!", 500
import os
from flask import send_from_directory, render_template

# 📌 Önceden tanımlı route fonksiyonları varsa kaldırarak çakışmayı önleyelim
routes_to_remove = [
    'get_yatak_durumu',
    'get_sehir_yatak_durumu',
    'sehir_yogun_bakim',
    'get_tamamlanan_tedaviler',
    'get_bekleyen_tedaviler',
    'static_files'
]

for route in routes_to_remove:
    if route in app.view_functions:
        del app.view_functions[route]

# 📌 JSON dosyalarını API olarak sunan rotalar
@app.route('/data/yatak_durumu.json')
def get_yatak_durumu():
    """📌 Yatak durumu verisini JSON formatında döndürür"""
    return send_from_directory(os.path.join(app.root_path, 'data'), 'yatak_durumu.json')

@app.route('/data/sehir_yatak_durumu.json')
def get_sehir_yatak_durumu():
    """📌 Şehir bazlı yatak durumu verisini JSON formatında döndürür"""
    return send_from_directory(os.path.join(app.root_path, 'data'), 'sehir_yatak_durumu.json')

# 📌 Şehir bazlı yoğun bakım sayfasını render eden route
@app.route('/sehir_yogun_bakim')
def sehir_yogun_bakim():
    """📌 Şehir bazlı yoğun bakım durumu sayfasını döndürür"""
    return render_template('sehir_yogun_bakim.html')

# 📌 Tamamlanan tedaviler JSON verisini döndüren API
@app.route('/data/tamamlanan_tedaviler.json')
def get_tamamlanan_tedaviler():
    """📌 Tamamlanan tedavileri JSON formatında döndürür"""
    return send_from_directory(os.path.join(app.root_path, 'data'), 'tamamlanan_tedaviler.json')

# 📌 Bekleyen tedaviler JSON verisini döndüren API
@app.route('/data/bekleyen_tedaviler.json')
def get_bekleyen_tedaviler():
    """📌 Bekleyen tedavileri JSON formatında döndürür"""
    return send_from_directory(os.path.join(app.root_path, 'data'), 'bekleyen_tedaviler.json')

# 📌 Statik dosyaları sunan route
@app.route('/static/<path:filename>')
def static_files(filename):
    """📌 Statik dosyaları (CSS, JS, resimler) sunar"""
    return send_from_directory('static', filename)

from flask import request, jsonify, render_template
from flask_login import login_required, current_user
from models import Mesaj, Kullanici  # ✅ Modelleri içe aktardık

# 📌 Önceden tanımlı route fonksiyonları varsa kaldırarak çakışmayı önleyelim
routes_to_remove = [
    'hasta_verileri',
    'guvenlik_yasal'
]

for route in routes_to_remove:
    if route in app.view_functions:
        del app.view_functions[route]

# 📌 Hasta verileri sayfası
@app.route('/hasta-verileri')
def hasta_verileri():
    """📌 Hasta verilerini görüntüleyen sayfa"""
    return render_template("hasta_verileri.html")  # ✅ HTML dosya adının doğru yazıldığından emin ol

# 📌 Güvenlik ve yasal uyumluluk sayfası
@app.route('/guvenlik-ve-yasal-uyumluluk')
def guvenlik_yasal():
    """📌 Güvenlik ve yasal uyumluluk bilgilerini içeren sayfa"""
    return render_template('guvenlik_yasal_uyumluluk.html')  # ✅ HTML dosya adı doğru olmalı
from flask import request, jsonify
from flask_login import login_required, current_user
from app import app, db  # ✅ Flask uygulaması ve veritabanını içe aktardık
from models import Mesaj  # ✅ Modeli içe aktardık

# 📌 Önceden tanımlı mesaj_gonder route'u varsa kaldırarak çakışmayı önleyelim
if 'mesaj_gonder' in app.view_functions:
    del app.view_functions['mesaj_gonder']

# 📌 Mesaj Gönderme
@app.route('/mesaj_gonder', methods=['POST'])
@login_required
def mesaj_gonder():
    """📌 Kullanıcılar arasında mesaj gönderme işlemi"""
    try:
        data = request.get_json()

        alici_id = data.get('alici_id')
        icerik = data.get('icerik')

        # 📌 Verilerin eksik olup olmadığını kontrol edelim
        if not alici_id or not icerik:
            return jsonify({'error': '❌ Alıcı ve içerik zorunludur'}), 400

        # 📌 Yeni mesaj oluştur
        yeni_mesaj = Mesaj(
            gonderen_id=current_user.id,
            alici_id=int(alici_id),  # ✅ ID’nin integer olduğundan emin ol
            icerik=icerik.strip()  # ✅ Fazladan boşlukları temizle
        )

        # 📌 Mesajı veritabanına ekleyelim
        db.session.add(yeni_mesaj)
        db.session.commit()

        return jsonify({'success': '✅ Mesaj başarıyla gönderildi'}), 201

    except Exception as e:
        db.session.rollback()  # ✅ Hata olursa işlemi geri al
        return jsonify({'error': f'❌ Hata oluştu: {str(e)}'}), 500

# 📌 Önceden tanımlı route'lar varsa çakışmayı önlemek için kaldırıyoruz
for route in ['cevrimici_mesajlasma', 'mesaj_kutusu', 'mesaj_okundu']:
    if route in app.view_functions:
        del app.view_functions[route]

# 📌 Çevrimiçi Mesajlaşma Sayfası
@app.route('/cevrimici-mesajlasma')
def cevrimici_mesajlasma():
    """📌 Çevrimiçi mesajlaşma sayfasını yükler."""
    return render_template("cevrimici_mesajlasma.html")

# 📌 Mesaj Kutusu Sayfası
@app.route('/mesaj_kutusu')
@login_required
def mesaj_kutusu():
    """📌 Kullanıcının mesaj kutusunu gösterir."""
    return render_template("mesaj_kutusu.html")

# 📌 Mesajı Okundu Olarak İşaretleme
@app.route('/mesaj_okundu/<int:mesaj_id>', methods=['PUT'])
@login_required
def mesaj_okundu(mesaj_id):
    """📌 Belirtilen mesajı 'okundu' olarak işaretler."""
    try:
        mesaj = Mesaj.query.get(mesaj_id)

        # 📌 Mesajın mevcut olup olmadığını ve yetkisiz erişimi kontrol et
        if not mesaj or mesaj.alici_id != current_user.id:
            return jsonify({'error': '❌ Mesaj bulunamadı veya yetkisiz erişim'}), 404

        # 📌 Mesajı okundu olarak işaretle
        mesaj.okundu = True
        db.session.commit()

        return jsonify({'success': '✅ Mesaj okundu olarak işaretlendi'}), 200

    except Exception as e:
        db.session.rollback()  # ✅ Hata olursa işlemi geri al
        return jsonify({'error': f'❌ Hata oluştu: {str(e)}'}), 500

# 📌 Mevcut tüm rotaları listeleyelim
existing_routes = [rule.endpoint for rule in app.url_map.iter_rules()]
# 📌 Mevcut rotaları kontrol edip kaldıran güvenli bir fonksiyon
def remove_existing_route(route_name):
    if route_name in app.view_functions:
        del app.view_functions[route_name]
        print(f"⚠️ Uyarı: '/{route_name}' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")

# 📌 Eski sağlık çalışanı rotasını kaldırıp yenisini ekliyoruz
remove_existing_route("saglik_calisani")
# 📌 Eğer `/saglik_calisani` rotası daha önce tanımlanmışsa kaldır
# 📌 Eğer `/saglik_calisani` rotası zaten tanımlıysa, eskiyi kaldır
if "saglik_calisani" in app.view_functions:
    print("⚠️ Uyarı: '/saglik_calisani' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    del app.view_functions["saglik_calisani"]

# 📌 Yeni Sağlık Çalışanı Rotası
@app.route("/saglik_calisani")
def saglik_calisani():
    return render_template("saglik_calisani.html")  # Sağlık çalışanı sayfasını yükler

# Eğer eski form_sayfasi tanımlıysa kaldır
if "form_sayfasi" in app.view_functions:
    del app.view_functions["form_sayfasi"]
    print("⚠️ Uyarı: '/form_sayfasi' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")
@app.route("/form_sayfasi")
def form_sayfasi():
    return render_template("form_sayfasi.html")  # 📌 İlgili sayfayı yükler
# 📌 Önce mevcut 'kayit_tarihi' rotasını kaldırıyoruz (varsa)
# 📌 Eğer 'kayit_tarihi' rotası zaten varsa, eski tanımları kaldırıyoruz
if "kayit_tarihi" in app.view_functions:
    print("⚠️ Uyarı: '/kayit_tarihi' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    app.view_functions.pop("kayit_tarihi")

# 📌 Yeni 'kayit_tarihi' rotasını tanımlıyoruz
@app.route("/kayit_tarihi")
def kayit_tarihi():
    # 📌 Hasta kayıt tarihlerini veritabanından al
    hastalar = Patient.query.with_entities(Patient.name, Patient.kayit_tarihi).all()

    if not hastalar:
        print("⚠️ Hiç hasta kaydı bulunamadı!")

    return render_template("kayit_tarihi.html", hastalar=hastalar)

# 📌 Önce mevcut 'saglikci_hatirlaticilar' rotasını kaldırıyoruz (varsa)
if "saglikci_hatirlaticilar" in app.view_functions:
    print("⚠️ Uyarı: '/saglikci_hatirlaticilar' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    app.view_functions.pop("saglikci_hatirlaticilar")

# 📌 Yeni 'saglikci_hatirlaticilar' rotasını tanımlıyoruz
@app.route("/saglikci_hatirlaticilar")
def saglikci_hatirlaticilar():
    # 📌 Veritabanından sağlık çalışanı için hatırlatıcıları alalım
    hatirlaticilar = Hatirlatici.query.all()

    if not hatirlaticilar:
        print("⚠️ Hiç hatırlatıcı kaydı bulunamadı!")

    return render_template("saglikci_hatirlaticilar.html", hatirlaticilar=hatirlaticilar)
for route in ["hasta_takip", "hasta_ekle", "form_sayfasi", "hizli_erisim", "kayit_tarihi", "saglikci_hatirlaticilar"]:
    if route in app.view_functions:
        app.view_functions.pop(route)

# 📌 Form Sayfası
@app.route("/form_sayfasi")
def form_sayfasi():
    return render_template("form_sayfasi.html")

# 📌 Hızlı Erişim Paneli
@app.route("/hizli_erisim")
def hizli_erisim():
    return render_template("hizli_erisim.html")

# 📌 Hasta Kayıt Tarihleri
@app.route("/kayit_tarihi")
def kayit_tarihi():
    return render_template("kayit_tarihi.html")

# 📌 Sağlıkçı Hatırlatıcıları
@app.route("/saglikci_hatirlaticilar")
def saglikci_hatirlaticilar():
    return render_template("saglikci_hatirlaticilar.html")

# 📌 Daha önce var olan geri_bildirim rotasını kaldırıyoruz
if "geri_bildirim" in app.view_functions:
    app.view_functions.pop("geri_bildirim")

@app.route("/geri_bildirim")
def geri_bildirim():
    return render_template("geri_bildirim.html")

# 📌 Daha önce var olan ayarlar rotasını kaldırıyoruz
if "ayarlar" in app.view_functions:
    app.view_functions.pop("ayarlar")

@app.route("/ayarlar")
def ayarlar():
    return render_template("ayarlar.html")
# 📌 Daha önce var olan egitim rotasını kaldırıyoruz
if "egitim" in app.view_functions:
    app.view_functions.pop("egitim")

@app.route("/egitim")
def egitim():
    return render_template("egitim.html")
if "verimlilik" in app.view_functions:
    app.view_functions.pop("verimlilik")

@app.route("/verimlilik")
def verimlilik():
    return render_template("verimlilik.html")

# 📌 Daha önce var olan hasta_verileri_analiz rotasını kaldırıyoruz
if "hasta_verileri_analiz" in app.view_functions:
    app.view_functions.pop("hasta_verileri_analiz")

@app.route("/hasta_verileri_analiz")
def hasta_verileri_analiz():
    return render_template("hasta_verileri_analiz.html")
# 📌 Daha önce var olan saglikci_hatirlaticilar rotasını kaldırıyoruz
if "saglikci_hatirlaticilar" in app.view_functions:
    app.view_functions.pop("saglikci_hatirlaticilar")

@app.route("/saglikci_hatirlaticilar")
def saglikci_hatirlaticilar():
    return render_template("saglikci_hatirlaticilar.html")
# 📌 Daha önce var olan hakkimizda rotasını kaldırıyoruz
if "hakkimizda" in app.view_functions:
    app.view_functions.pop("hakkimizda")

@app.route("/hakkimizda")
def hakkimizda():
    return render_template("hakkimizda.html")
# 📌 Daha önce var olan form_sayfasi rotasını kaldırıyoruz
# 📌 Daha önce var olan form_sayfasi rotasını kaldırıyoruz
# 📌 Daha önce var olan form_sayfasi rotasını kaldırıyoruz
# 📌 Daha önce tanımlanmışsa kaldır
if "form_sayfasi" in app.view_functions:
    app.view_functions.pop("form_sayfasi")

# ✅ POST ve GET destekleyen rota tanımı
@app.route("/form_sayfasi", methods=["GET", "POST"])
def form_sayfasi():
    if request.method == "POST":
        # Burada gelen form verilerini işleyebilirsin
        form_data = request.form.to_dict()
        print("📩 Formdan gelen veriler:", form_data)
        return "Form başarıyla alındı!"  # İstersen başka bir sayfaya yönlendirme de yapılabilir

    return render_template("form.html")
# 📌 Eğer daha önce tanımlandıysa kaldır
if "saglikci_hatirlaticilar" in app.view_functions:
    app.view_functions.pop("saglikci_hatirlaticilar")

@app.route("/saglikci_hatirlaticilar")
def saglikci_hatirlaticilar():
    return render_template("hatirlaticilar.html")  # örnek içerik

if "raporlama" in app.view_functions:
    app.view_functions.pop("raporlama")

@app.route("/raporlama")
def raporlama():
    return render_template("yeni_rapor.html")  # ✅ Doğru dosya adı
# 📌 Daha önce var olan geri_bildirim rotasını kaldırıyoruz
# 📌 Daha önce var olan geri_bildirim rotasını kaldırıyoruz
# 📌 Daha önce var olan geri_bildirim_saglikci rotasını kaldırıyoruz
# Önce varsa eski rotayı kaldırıyoruz
# Eğer önceki `geri_bildirim_saglikci` rotası tanımlıysa kaldır
if "geri_bildirim_saglikci" in app.view_functions:
    del app.view_functions["geri_bildirim_saglikci"]
    print("⚠️ Uyarı: '/geri_bildirim_saglikci' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")
# Eğer eski `akilli_not_defteri` rotası tanımlıysa kaldır
# Eğer eski `akilli_not_defteri` rotası tanımlıysa kaldır
if "akilli_not_defteri" in app.view_functions:
    del app.view_functions["akilli_not_defteri"]
    print("⚠️ Uyarı: '/akilli_not_defteri' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")

# Yeni rota tanımlanıyor
@app.route("/akilli_not_defteri")
def akilli_not_defteri():
    return render_template("akilli_not_defteri.html")
# Eğer eski `geri_bildirim_saglikci` rotası tanımlıysa kaldır
if "geri_bildirim_saglikci" in app.view_functions:
    del app.view_functions["geri_bildirim_saglikci"]
    print("⚠️ Uyarı: '/geri_bildirim_saglikci' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")

# Yeni rota tanımlama
@app.route("/geri_bildirim_saglikci")
def geri_bildirim_saglikci():
    return render_template("geri_bildirim_saglikci.html")  # HTML dosya adınızı doğrulayın!
# Eğer eski `zaman_yonetimi` rotası tanımlıysa kaldır
if "zaman_yonetimi" in app.view_functions:
    del app.view_functions["zaman_yonetimi"]
    print("⚠️ Uyarı: '/zaman_yonetimi' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")

# Yeni rota tanımlama
@app.route("/zaman_yonetimi")
def zaman_yonetimi():
    return render_template("zaman_yonetimi.html")  # Dosya adını doğrulayın!
# Eğer eski `hastane_yonetimi` rotası tanımlıysa kaldır
if "hastane_yonetimi" in app.view_functions:
    del app.view_functions["hastane_yonetimi"]
    print("⚠️ Uyarı: '/hastane_yonetimi' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")

# Yeni `hastane_yonetimi` rotasını tanımlıyoruz
@app.route("/hastane_yonetimi")
def hastane_yonetimi():
    return render_template("hastane_yonetimi.html")  # HTML dosya adı doğru mu kontrol et!
# Eğer eski `dashboard` rotası tanımlıysa kaldır
if "dashboard" in app.view_functions:
    del app.view_functions["dashboard"]
    print("⚠️ Uyarı: '/dashboard' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")

# Yeni `dashboard` rotasını tanımlıyoruz
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")  # Eğer bu HTML dosyası yoksa, oluşturulmalı!
# 📌 Hasta Ekleme Rotası
# 📌 Hasta Ekleme Rotası (Hata ayıklama eklenmiş versiyon)
@app.route("/hasta_ekle", methods=["GET", "POST"])
def hasta_ekle():
    if request.method == "POST":
        try:
            # 📌 FORM'DAN VERİLERİ DOĞRU İSİMLERLE AL
            hasta_ad = request.form.get("name")  # Eskiden "ad" idi, şimdi "name"
            hasta_yas = request.form.get("age")  # Eskiden "yas" idi, şimdi "age"
            hasta_cinsiyeti = request.form.get("gender")  # Eskiden "cinsiyet" idi, şimdi "gender"
            hasta_tani = request.form.get("diagnosis")  # Eskiden "tani" idi, şimdi "diagnosis"
            hasta_tedavi_durumu = request.form.get("treatment_status")  # Eskiden "tedavi_durumu" idi, şimdi "treatment_status"

            # 📌 EKSİK ALAN VARSA UYARI GÖSTER
            if not (hasta_ad and hasta_yas and hasta_cinsiyeti and hasta_tani and hasta_tedavi_durumu):
                flash("⚠️ Tüm alanları doldurun!", "danger")
                return redirect(url_for("hasta_ekle"))

            # 📌 HASTA EKLE
            yeni_hasta = Patient(
                name=hasta_ad,
                age=int(hasta_yas),
                gender=hasta_cinsiyeti,
                diagnosis=hasta_tani,
                treatment_status=hasta_tedavi_durumu
            )
            db.session.add(yeni_hasta)
            db.session.commit()

            flash("✅ Hasta başarıyla eklendi!", "success")
            return redirect(url_for("hasta_takip"))

        except Exception as e:
            flash(f"❌ Hata oluştu: {str(e)}", "danger")
            db.session.rollback()

    return render_template("hasta_ekle.html")

# 📌 Eğer 'hasta_guncelle' rotası varsa eskiyi kaldır
# Eğer hasta_guncelle rotası daha önce tanımlandıysa, eski tanımı kaldır
if "hasta_guncelle" in app.view_functions:
    print("⚠️ Uyarı: '/hasta_guncelle' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    app.view_functions.pop("hasta_guncelle")
# Eğer hasta_guncelle rotası daha önce tanımlandıysa, eski tanımı kaldır
if "hasta_guncelle" in app.view_functions:
    print("⚠️ Uyarı: '/hasta_guncelle' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    app.view_functions.pop("hasta_guncelle")

# 📌 Hasta Güncelleme Rotası (HTML ile Tam Uyumlu)
@app.route("/hasta_guncelle/<int:patient_id>", methods=["GET", "POST"])
def hasta_guncelle(patient_id):
    patient = db.session.get(Patient, patient_id)  # 🔹 Hasta bilgilerini veritabanından al

    if not patient:
        flash("⚠️ Hasta bulunamadı!", "danger")
        return redirect(url_for("hasta_takip"))

    if request.method == "POST":
        # 🔹 Formdan gelen verilerle güncelleme yap
        patient.name = request.form.get("name")
        patient.age = int(request.form.get("age"))
        patient.gender = request.form.get("gender")
        patient.diagnosis = request.form.get("diagnosis")
        patient.treatment_status = request.form.get("treatment_status")

        db.session.commit()
        flash("✅ Hasta bilgileri başarıyla güncellendi!", "success")
        return redirect(url_for("hasta_takip"))

    return render_template("hasta_guncelle.html", patient=patient)  # 🔹 `patient` değişkeni şablona gönderildi

# 📌 Eğer 'hasta_sil' rotası zaten tanımlıysa eskiyi kaldır
if "hasta_sil" in app.view_functions:
    print("⚠️ Uyarı: '/hasta_sil' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    app.view_functions.pop("hasta_sil")


# 📌 Hasta Silme Rotası (Doğru Değişken İsmi: `patient_id`)
@app.route("/hasta_sil/<int:patient_id>", methods=["POST"])
def hasta_sil(patient_id):
    hasta = db.session.get(Patient, patient_id)  # 🔹 `hasta_id` yerine `patient_id` kullanıldı

    if not hasta:
        flash("⚠️ Hasta bulunamadı!", "danger")
        return redirect(url_for("hasta_takip"))

    db.session.delete(hasta)
    db.session.commit()

    flash("✅ Hasta başarıyla silindi!", "success")
    return redirect(url_for("hasta_takip"))

# 📌 Eğer 'hasta_detay' rotası zaten tanımlıysa eskiyi kaldır
# Eğer hasta_detay rotası zaten tanımlandıysa, eski tanımı kaldır
if "hasta_detay" in app.view_functions:
    print("⚠️ Uyarı: '/hasta_detay' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    app.view_functions.pop("hasta_detay")

# 📌 Hasta Detayları Gösterme Rotası
@app.route("/hasta_detay/<int:hasta_id>")
def hasta_detay(hasta_id):
    patient = db.session.get(Patient, hasta_id)  # 🔹 `hasta_id` ile hasta çekiliyor

    if not patient:
        flash("⚠️ Hasta bulunamadı!", "danger")
        return redirect(url_for("hasta_takip"))

    return render_template("hasta_detay.html", patient=patient)  # 🔹 `patient` gönderildi
from flask_login import login_required, current_user
# 📌 Hasta Takip Sayfası (Yeniden Tanımlama)
@app.route("/hasta_takip", methods=["GET"])
def hasta_takip():
    patients = db.session.query(Patient).all()  # 📌 Veritabanından tüm hastaları al
    return render_template("hasta_takip.html", patients=patients)  # Değişken ismi düzeltildi!

# Eğer saglik_calisani rotası daha önce tanımlandıysa, eski tanımı kaldır
if "saglik_calisani" in app.view_functions:
    print("⚠️ Uyarı: '/saglik_calisani' rotası zaten tanımlanmış! Eski tanımları kaldırıyoruz...")
    app.view_functions.pop("saglik_calisani")

# 📌 Sağlık Çalışanı Sayfası
@app.route("/saglik_calisani")
def saglik_calisani():
    return render_template("saglik_calisani.html")  # Sağlık çalışanı sayfasını yükler
import matplotlib.pyplot as plt
import os
from flask import render_template, url_for

# 📌 Grafiklerin kaydedileceği klasör
OUTPUT_FOLDER = "static/raporlar/"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 📌 Grafiklerin açıklamaları ve verileri
grafikler = [
    {
        "filename": "grafik_1.png",
        "title": "Cinsiyete Göre Hasta Dağılımı",
        "data": (["Kadın", "Erkek"], [150, 120]),
        "type": "bar"
    },
    {
        "filename": "grafik_2.png",
        "title": "Hastalık Türlerine Göre Dağılım",
        "data": (["Diyabet", "Hipertansiyon", "Diğer"], [30, 50, 20]),
        "type": "pie"
    },
    {
        "filename": "grafik_3.png",
        "title": "Tedavi Süreleri",
        "data": ([1, 2, 3, 4, 5], [20, 35, 30, 35, 27]),
        "type": "line"
    },
    {
        "filename": "grafik_4.png",
        "title": "Yaş Gruplarına Göre Hasta Sayısı",
        "data": (["0-18", "19-35", "36-50", "51+"], [50, 80, 60, 40]),
        "type": "bar"
    },
    {
        "filename": "grafik_5.png",
        "title": "Hastaların Tedaviye Yanıt Süresi",
        "data": ([1, 2, 3, 4, 5], [10, 15, 25, 30, 35]),
        "type": "line"
    }
]

# 📌 Grafikleri oluştur ve kaydet
def generate_graphs():
    for grafik in grafikler:
        fig, ax = plt.subplots()

        if grafik["type"] == "bar":
            ax.bar(grafik["data"][0], grafik["data"][1])
        elif grafik["type"] == "pie":
            ax.pie(grafik["data"][1], labels=grafik["data"][0], autopct="%1.1f%%")
        elif grafik["type"] == "line":
            ax.plot(grafik["data"][0], grafik["data"][1], marker="o")

        ax.set_title(grafik["title"])

        grafik_path = os.path.join(OUTPUT_FOLDER, grafik["filename"])
        plt.savefig(grafik_path)
        plt.close()

        print(f"✅ Kaydedildi: {grafik_path}")

    print("🚀 Tüm grafikler başarıyla oluşturuldu!")
from flask import render_template
# Eğer "akilli_notlar" rotası daha önce tanımlandıysa, eski tanımı kaldır
# Eğer "akilli_not_defteri" rotası daha önce tanımlandıysa, eski tanımı kaldır
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

# 📌 Notları saklamak için geçici liste
notlar = [
    {"id": 1, "baslik": "Örnek Not 1", "icerik": "Bu bir test notudur.", "tarih": datetime.now()},
    {"id": 2, "baslik": "Örnek Not 2", "icerik": "İkinci test notu.", "tarih": datetime.now()},
]

# 📌 **Mevcut rotaları kaldırma fonksiyonu**
def remove_route(endpoint_name):
    """Eğer bir route tanımlıysa, önce kaldırır."""
    if endpoint_name in app.view_functions:
        del app.view_functions[endpoint_name]
        print(f"⚠️ Uyarı: '{endpoint_name}' rotası zaten tanımlanmış! Eski tanımı kaldırıyoruz...")

# 📌 **Rotaları kaldır ve yeniden tanımla**
remove_route("akilli_not_defteri")

@app.route("/akilli_not_defteri", methods=["GET", "POST"])
def akilli_not_defteri():
    if request.method == "POST":
        baslik = request.form.get("baslik", "").strip()
        icerik = request.form.get("icerik", "").strip()

        # 📌 Girişlerin boş olup olmadığını kontrol et
        if not baslik or not icerik:
            return render_template("akilli_not_defteri.html", notlar=notlar, hata="Başlık ve içerik boş olamaz!")

        # 📌 Yeni not için en yüksek ID değerini bul ve 1 artır
        yeni_id = max(notlar, key=lambda x: x["id"], default={"id": 0})["id"] + 1

        yeni_not = {
            "id": yeni_id,
            "baslik": baslik,
            "icerik": icerik,
            "tarih": datetime.now(),
        }
        notlar.append(yeni_not)

        return redirect(url_for("akilli_not_defteri"))  # Sayfayı yenile

    return render_template("akilli_not_defteri.html", notlar=notlar)

# 📌 **Rotaları kaldır ve yeniden tanımla**
remove_route("not_sil")

@app.route("/not_sil/<int:not_id>", methods=["POST", "GET"])
def not_sil(not_id):
    global notlar
    notlar = [not_kayit for not_kayit in notlar if not_kayit["id"] != not_id]
    return redirect(url_for("akilli_not_defteri"))
# 📌 Eğer rota zaten tanımlıysa önce siliyoruz
if "planlayici" in app.view_functions:
    del app.view_functions["planlayici"]

# 📌 Rota tanımlama
@app.route("/planlayici")
def planlayici():
    return render_template("planlayici.html")
# 📌 Eğer "takvim" rotası tanımlıysa önce kaldır
if "takvim" in app.view_functions:
    del app.view_functions["takvim"]

# 📌 Takvim sayfası rotası
@app.route("/takvim")
def takvim():
    return render_template("takvim.html")
# 📌 Eğer "zamanlayici" rotası tanımlıysa önce kaldır
if "zamanlayici" in app.view_functions:
    del app.view_functions["zamanlayici"]

# 📌 Zamanlayıcı sayfası rotası
@app.route("/zamanlayici")
def zamanlayici():
    return render_template("zamanlayici.html")
# Eğer '/hasta_bilgi' rotası zaten tanımlanmışsa, önce kaldır
for rule in list(app.url_map.iter_rules()):
    if rule.endpoint == "hasta_bilgi":
        app.view_functions.pop("hasta_bilgi", None)
        break

@app.route("/hasta_bilgi")
def hasta_bilgi():
    return render_template("hasta_bilgi.html")  # Eğer HTML dosyası yoksa oluştur.
# 📌 Eğer rota zaten tanımlıysa kaldır
existing_routes = [rule.endpoint for rule in app.url_map.iter_rules()]
if "randevu_takibi" in existing_routes:
    app.view_functions.pop("randevu_takibi")

# 📌 Yeni rotayı ekle
@app.route("/randevu_takibi")
def randevu_takibi():
    return render_template("randevu_takibi.html")  # Eğer dosya yoksa oluştur

# 📌 **✅ Eğer rota varsa sil, yoksa oluştur**
if "randevu_ekle" in [rule.endpoint for rule in app.url_map.iter_rules()]:
    app.view_functions.pop("randevu_ekle")

@app.route("/randevu_ekle", methods=["POST"])
def randevu_ekle():
    hasta_adi = request.form.get("hasta_adi")
    randevu_tarihi = request.form.get("randevu_tarihi")

    if hasta_adi and randevu_tarihi:  # Boş kontrolü
        yeni_id = max([r["id"] for r in randevular], default=0) + 1
        randevular.append({"id": yeni_id, "hasta_adi": hasta_adi, "randevu_tarihi": randevu_tarihi})

    return redirect(url_for("randevu_takibi"))
    # Eğer daha önce tanımlandıysa kaldır

if "raporlari_goster" in app.view_functions:
    app.view_functions.pop("raporlari_goster")
@app.route("/raporlari_goster")
def raporlari_goster():
    raporlar = [
        {"id": 1, "ad": "Hasta Tedavi Raporu"},
        {"id": 2, "ad": "Aylık Hasta İstatistikleri"},
        {"id": 3, "ad": "Genel Sağlık Verileri"},
    ]
    return render_template("raporlari_goster.html", raporlar=raporlar)
# Eğer rota zaten varsa, önce kaldır
if "rapor_detay" in app.view_functions:
    app.view_functions.pop("rapor_detay")

@app.route("/rapor_detay/<int:rapor_id>")
def rapor_detay(rapor_id):
    # Örnek rapor listesi (Verileri veritabanından çekmek daha iyidir)
    raporlar = [
        {"id": 1, "ad": "Hasta Tedavi Raporu", "icerik": "Bu rapor hasta tedavi süreçlerini içerir."},
        {"id": 2, "ad": "Aylık Hasta İstatistikleri", "icerik": "Aylık hasta istatistik verileri."},
        {"id": 3, "ad": "Genel Sağlık Verileri", "icerik": "Genel sağlık istatistikleri raporu."},
    ]

    # İlgili raporu bul
    rapor = next((r for r in raporlar if r["id"] == rapor_id), None)

    # Eğer rapor yoksa hata döndür
    if rapor is None:
        return "Rapor bulunamadı!", 404

    return render_template("rapor_detay.html", rapor=rapor)

# Eğer "rapor_sil" rotası zaten varsa, önce kaldır
if "rapor_sil" in app.view_functions:
    app.view_functions.pop("rapor_sil")

@app.route("/rapor_sil/<int:rapor_id>", methods=["POST", "GET"])
def rapor_sil(rapor_id):
    global raporlar  # Rapor listesine erişim sağla

    # Belirtilen ID'ye sahip raporu listeden kaldır
    raporlar = [rapor for rapor in raporlar if rapor["id"] != rapor_id]

    # Raporları göster sayfasına yönlendir
    return redirect(url_for("raporlari_goster"))

# 📌 Geçici Rapor Listesi (İleride Veritabanına Geçilebilir)
hasta_tedavi_raporlari = [
    {"id": 1, "hasta_adi": "Ali Yılmaz", "tarih": "2025-03-14", "icerik": "Hasta ameliyat sonrası kontrole alındı."},
    {"id": 2, "hasta_adi": "Zeynep Demir", "tarih": "2025-03-12", "icerik": "Kan tahlilleri yapıldı, sonuçlar değerlendiriliyor."}
]

# 📌 Eğer rota daha önce tanımlandıysa kaldır
if "hasta_tedavi_raporlari_sayfasi" in app.view_functions:
    app.view_functions.pop("hasta_tedavi_raporlari_sayfasi")


# 📌 Hasta Tedavi Raporları Sayfası (Listeleme ve Yeni Rapor Ekleme)
@app.route("/hasta_tedavi_raporlari", methods=["GET", "POST"])
def hasta_tedavi_raporlari_sayfasi():
    if request.method == "POST":
        hasta_adi = request.form.get("hasta_adi", "").strip()
        icerik = request.form.get("icerik", "").strip()

        if hasta_adi and icerik:  # Boş veri eklenmemesi için kontrol
            yeni_rapor = {
                "id": len(hasta_tedavi_raporlari) + 1,
                "hasta_adi": hasta_adi,
                "tarih": datetime.today().strftime("%Y-%m-%d"),  # Bugünün tarihini otomatik ekler
                "icerik": icerik
            }
            hasta_tedavi_raporlari.append(yeni_rapor)

        return redirect(url_for("hasta_tedavi_raporlari_sayfasi"))

    return render_template("hasta_tedavi_raporlari.html", raporlar=hasta_tedavi_raporlari)

# 📌 Eğer rota daha önce tanımlandıysa kaldır
if "hasta_tedavi_goruntule" in app.view_functions:
    app.view_functions.pop("hasta_tedavi_goruntule")

@app.route("/hasta_tedavi_goruntule/<int:rapor_id>")
def hasta_tedavi_goruntule(rapor_id):
    # Mevcut rapor listesinden ilgili raporu bul
    rapor = next((r for r in hasta_tedavi_raporlari if r["id"] == rapor_id), None)

    # Eğer rapor bulunamazsa hata mesajı döndür
    if rapor is None:
        return "❌ Rapor bulunamadı!", 404

    return render_template("hasta_tedavi_raporu.html", rapor=rapor)

# 📌 Eğer rota daha önce tanımlandıysa kaldır
if "rapor_indir" in app.view_functions:
    app.view_functions.pop("rapor_indir")

# 📌 Rapor İndirme Rotası (Yoksa Oluştur)
@app.route("/rapor_indir/<int:rapor_id>")
def rapor_indir(rapor_id):
    rapor = next((r for r in hasta_tedavi_raporlari if r["id"] == rapor_id), None)
    if rapor is None:
        return "Rapor bulunamadı!", 404

    # PDF oluşturma işlemleri burada yapılabilir
    return "PDF indirme özelliği yakında eklenecek."
# 📌 Eğer rota daha önce tanımlandıysa kaldır
if "aylik_hasta_istatistikleri" in app.view_functions:
    app.view_functions.pop("aylik_hasta_istatistikleri")

# 📌 Aylık Hasta İstatistikleri Rotası (Yoksa Oluştur)
@app.route("/aylik_hasta_istatistikleri")
def aylik_hasta_istatistikleri():
    # Örnek İstatistik Verileri (İleride Veritabanına Geçilebilir)
    istatistikler = [
        {"ay": "Ocak", "toplam_hasta": 120, "acil_hasta": 30, "poliklinik_hasta": 90},
        {"ay": "Şubat", "toplam_hasta": 150, "acil_hasta": 45, "poliklinik_hasta": 105},
        {"ay": "Mart", "toplam_hasta": 200, "acil_hasta": 60, "poliklinik_hasta": 140},
        {"ay": "Nisan", "toplam_hasta": 180, "acil_hasta": 50, "poliklinik_hasta": 130},
    ]

    print("DEBUG: İstatistikler verisi -->", istatistikler)  # ✅ Terminale veriyi yazdır
    return render_template("aylik_hasta_istatistikleri.html", istatistikler=istatistikler)
# 📌 Eğer rota daha önce tanımlandıysa kaldır
# 📌 Eğer ilgili rota daha önce tanımlandıysa kaldır
for route in ["egitim", "ilk_yardim_egitimi", "hastane_prosedurleri", "acil_mudahale", "hasta_veri_yonetimi"]:
    if route in app.view_functions:
        app.view_functions.pop(route)

# 📌 Eğitim Modülü Ana Sayfa
@app.route("/egitim")
def egitim():
    return render_template("egitim.html")

# 📌 Ders Detay Sayfaları
@app.route("/ilk_yardim_egitimi")
def ilk_yardim_egitimi():
    return render_template("ilk_yardim_egitimi.html")

@app.route("/hastane_prosedurleri")
def hastane_prosedurleri():
    return render_template("hastane_prosedurleri.html")

@app.route("/acil_mudahale")
def acil_mudahale():
    return render_template("acil_mudahale.html")

@app.route("/hasta_veri_yonetimi")
def hasta_veri_yonetimi():
    return render_template("hasta_veri_yonetimi.html")
# 📌 Eğer rota daha önce tanımlandıysa kaldır
for route_name in ["hasta_kayit", "muayene_teshis", "tedavi_recete", "hastane_yatis_taburcu"]:
    if route_name in app.view_functions:
        app.view_functions.pop(route_name)

# 📌 Hasta Kayıt İşlemi Sayfası
@app.route("/hasta_kayit")
def hasta_kayit():
    return render_template("hasta_kayit.html")

# 📌 Muayene ve Teşhis Sayfası
@app.route("/muayene_teshis")
def muayene_teshis():
    return render_template("muayene_teshis.html")

# 📌 Tedavi ve Reçete Yazımı Sayfası
@app.route("/tedavi_recete")
def tedavi_recete():
    return render_template("tedavi_recete.html")

# 📌 Hastaneye Yatış ve Taburcu Süreci Sayfası
@app.route("/hastane_yatis_taburcu")
def hastane_yatis_taburcu():
    return render_template("hastane_yatis_taburcu.html")

# Mevcut rota varsa kaldır
if 'acil_mudahale_teknikleri' in app.view_functions:
    app.view_functions.pop('acil_mudahale_teknikleri')

# Yeni rota tanımla
@app.route('/acil_mudahale_teknikleri')
def acil_mudahale_teknikleri():
    return render_template("acil_mudahale_teknikleri.html")

# Önce var olan rotayı kaldır
if 'hasta_veri_yonetimi' in app.view_functions:
    del app.view_functions['hasta_veri_yonetimi']

# Yeni rota oluştur
@app.route('/hasta_veri_yonetimi')
def hasta_veri_yonetimi():
    return render_template("hasta_veri_yonetimi.html")
# 📌 Eğer rota daha önce tanımlandıysa kaldır
if "hastane_yonetimi_entegrasyonu" in app.view_functions:
    app.view_functions.pop("hastane_yonetimi_entegrasyonu")

# 📌 Hastane Yönetimi Entegrasyonu Rotası (Yoksa Oluştur)
@app.route("/hastane_yonetimi_entegrasyonu")
def hastane_yonetimi_entegrasyonu():
    return render_template("hastane_yonetimi_entegrasyonu.html")

# 📌 Geçici Log Listesi (İleride Veritabanına Geçilebilir)

# 📌 **Geçici Log Listesi**
sistem_loglari = [
    {"id": 1, "tarih": "2025-03-16", "kullanici": "Admin", "islem": "Sistem başlatıldı", "durum": "Bilgi"},
    {"id": 2, "tarih": "2025-03-16", "kullanici": "Admin", "islem": "Yüksek CPU kullanımı", "durum": "Uyarı"},
    {"id": 3, "tarih": "2025-03-16", "kullanici": "Admin", "islem": "Veritabanı bağlantı hatası", "durum": "Hata"},
]

# 📌 Eğer rota daha önce tanımlandıysa kaldır
if "sistem_loglari_sayfasi" in app.view_functions:
    app.view_functions.pop("sistem_loglari_sayfasi")


# 📌 **Hata Analizi Fonksiyonu**
def hata_analizini_hesapla():
    hata_turleri = ["Bilgi", "Uyarı", "Hata"]
    hata_sayilari = [0, 0, 0]

    for log in sistem_loglari:
        if log["durum"] == "Bilgi":
            hata_sayilari[0] += 1
        elif log["durum"] == "Uyarı":
            hata_sayilari[1] += 1
        elif log["durum"] == "Hata":
            hata_sayilari[2] += 1

    return hata_turleri, hata_sayilari


# 📌 **Sistem Logları Sayfası (Listeleme)**
@app.route("/sistem-loglari")
def sistem_loglari_sayfasi():
    hata_turleri, hata_sayilari = hata_analizini_hesapla()
    return render_template(
        "sistem_loglari.html",
        loglar=sistem_loglari,
        hata_turleri=hata_turleri,
        hata_sayilari=hata_sayilari
    )


# 📌 Eğer `log_ekle` rotası zaten tanımlandıysa kaldır
if "log_ekle" in app.view_functions:
    app.view_functions.pop("log_ekle")


# 📌 **Yeni Log Ekleme API**
@app.route("/log-ekle", methods=["POST"])
def log_ekle():
    veri = request.get_json()
    yeni_log = {
        "id": len(sistem_loglari) + 1,
        "tarih": datetime.datetime.now().strftime("%Y-%m-%d"),
        "kullanici": veri.get("kullanici", "Bilinmiyor"),
        "islem": veri.get("islem", "Bilinmiyor"),
        "durum": veri.get("durum", "Bilinmiyor"),
    }
    sistem_loglari.append(yeni_log)
    return jsonify({"mesaj": "Log başarıyla eklendi", "log": yeni_log})


# 📌 Eğer `loglari_indir` rotası zaten tanımlandıysa kaldır
if "loglari_indir" in app.view_functions:
    app.view_functions.pop("loglari_indir")


# 📌 **Logları CSV olarak indir**
@app.route("/loglari-indir/<format>")
def loglari_indir(format):
    dosya_adi = f"sistem_loglari.{format}"

    if format == "csv":
        with open(dosya_adi, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Tarih", "Kullanıcı", "İşlem", "Durum"])
            for log in sistem_loglari:
                writer.writerow([log["id"], log["tarih"], log["kullanici"], log["islem"], log["durum"]])

    elif format == "pdf":
        return jsonify({"hata": "PDF oluşturma şu anda desteklenmiyor"})

    return send_file(dosya_adi, as_attachment=True)
# 📌 Flask Rotaları Listede Var mı Kontrol Et
# Eğer rota daha önce tanımlandıysa kaldır
# 📌 Kullanıcı ve Hata Verileri (Eğer veritabanı yoksa geçici olarak kullanılıyor)
kullanici_verileri = [
    {"rol": "Hasta", "sayi": 120},
    {"rol": "Sağlık Çalışanı", "sayi": 80},
    {"rol": "Yönetici", "sayi": 10}
]

hata_verileri = [
    {"tur": "Veritabanı Hatası", "sayi": 5},
    {"tur": "Yetkilendirme Hatası", "sayi": 3},
    {"tur": "Bağlantı Hatası", "sayi": 7}
]

# 📌 Eğer rota daha önce tanımlandıysa kaldır
if "istatistik_raporlama" in app.view_functions:
    app.view_functions.pop("istatistik_raporlama")

# 📌 **İstatistik ve Raporlama Sayfası**
@app.route("/istatistik")  # 🔴 Önceden /istatistik_raporlama idi, şimdi düzeltildi
def istatistik_raporlama():
    gunluk_giris_sayisi = 50
    toplam_kullanici = sum([k["sayi"] for k in kullanici_verileri])
    en_populer_modul = "Hasta Takip Sistemi"

    kullanici_turleri = [k["rol"] for k in kullanici_verileri]
    kullanici_sayilari = [k["sayi"] for k in kullanici_verileri]

    hata_turleri = [h["tur"] for h in hata_verileri]
    hata_sayilari = [h["sayi"] for h in hata_verileri]

    return render_template(
        "istatistik_raporlama.html",
        gunluk_giris_sayisi=gunluk_giris_sayisi,
        toplam_kullanici=toplam_kullanici,
        en_populer_modul=en_populer_modul,
        kullanici_turleri=kullanici_turleri,
        kullanici_sayilari=kullanici_sayilari,
        hata_turleri=hata_turleri,
        hata_sayilari=hata_sayilari
    )
# 📌 Eğer rota daha önce tanımlandıysa kaldır
import csv
import pandas as pd
from fpdf import FPDF
from flask import send_file, jsonify

# Eğer "rapor_indir" daha önce tanımlandıysa, kaldır
if "rapor_indir" in app.view_functions:
    app.view_functions.pop("rapor_indir")

# 📌 **Raporları CSV, PDF veya Excel olarak indir**
@app.route("/rapor_indir/<format>")
def rapor_indir(format):
    dosya_adi = f"istatistik_raporu.{format}"

    if format == "csv":
        with open(dosya_adi, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Kategori", "Değer"])
            writer.writerow(["📅 Günlük Giriş Sayısı", 50])
            writer.writerow(["👥 Toplam Kullanıcı", sum([k["sayi"] for k in kullanici_verileri])])
            writer.writerow(["📂 En Popüler Modül", "Hasta Takip Sistemi"])

    elif format == "xlsx":
        df = pd.DataFrame([
            {"Kategori": "📅 Günlük Giriş Sayısı", "Değer": 50},
            {"Kategori": "👥 Toplam Kullanıcı", "Değer": sum([k["sayi"] for k in kullanici_verileri])},
            {"Kategori": "📂 En Popüler Modül", "Değer": "Hasta Takip Sistemi"}
        ])
        df.to_excel(dosya_adi, index=False)

    elif format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 16)
        pdf.cell(200, 10, "📊 İstatistik Raporu", ln=True, align="C")
        pdf.ln(10)

        pdf.set_font("Arial", "", 12)
        pdf.cell(200, 10, f"📅 Günlük Giriş Sayısı: 50", ln=True)
        pdf.cell(200, 10, f"👥 Toplam Kullanıcı Sayısı: {sum([k['sayi'] for k in kullanici_verileri])}", ln=True)
        pdf.cell(200, 10, f"📂 En Popüler Modül: Hasta Takip Sistemi", ln=True)

        pdf.output(dosya_adi)

    else:
        return jsonify({"hata": f"'{format}' formatı desteklenmiyor."})

    return send_file(dosya_adi, as_attachment=True)


def rota_sil(rota):
    """Belirtilen rota varsa siler"""
    rule_list = list(app.url_map.iter_rules())
    for rule in rule_list:
        if rule.rule == rota:
            app.view_functions.pop(rule.endpoint, None)

# Eğer rota zaten varsa sil
rota_sil('/sosyal-medya')

# Rotayı yeniden oluştur
@app.route('/sosyal-medya')
def sosyal_medya():
    return render_template('sosyal_medya.html')
from flask import Flask, render_template, request

# Örnek Hasta Verileri (Gerçek veri tabanı ile değiştirebilirsin)
hastalar = [
    {"id": 1, "adi": "Ahmet Yılmaz", "aciliyet": 2},  # 2: Kritik
    {"id": 2, "adi": "Mehmet Kaya", "aciliyet": 1},  # 1: Acil
    {"id": 3, "adi": "Zeynep Demir", "aciliyet": 0}  # 0: Normal
]

def rota_sil(rota):
    """Belirtilen rota varsa siler"""
    with app.app_context():
        rule_list = list(app.url_map.iter_rules())
        for rule in rule_list:
            if rule.rule == rota:
                if rule.endpoint in app.view_functions:
                    app.view_functions.pop(rule.endpoint, None)

# Eğer `/oncelik-karsilastirma` rotası zaten varsa, önce silelim.
rota_sil('/oncelik-karsilastirma')

# Yeni Hasta Öncelik Karşılaştırma Rotası
@app.route('/oncelik-karsilastirma', methods=['GET', 'POST'])
def oncelik_karsilastirma():
    sonuc = None
    if request.method == 'POST':
        hasta1_id = int(request.form['hasta1'])
        hasta2_id = int(request.form['hasta2'])

        # Seçilen hastaları bul
        hasta1 = next((hasta for hasta in hastalar if hasta["id"] == hasta1_id), None)
        hasta2 = next((hasta for hasta in hastalar if hasta["id"] == hasta2_id), None)

        if hasta1 and hasta2:
            if hasta1["aciliyet"] > hasta2["aciliyet"]:
                sonuc = f"{hasta1['adi']} daha öncelikli!"
            elif hasta1["aciliyet"] < hasta2["aciliyet"]:
                sonuc = f"{hasta2['adi']} daha öncelikli!"
            else:
                sonuc = "Her iki hasta da aynı öncelik seviyesinde."

    return render_template("oncelik_karsilastirma.html", hastalar=hastalar, sonuc=sonuc)

# 📌 Eğer 'acil_durum_sayfasi' rotası varsa önce siliyoruz
if "acil_durum_sayfasi" in app.view_functions:
    del app.view_functions["acil_durum_sayfasi"]

# 📌 Rotayı güvenli bir şekilde ekleme
@app.route("/acil_durum_sayfasi")
def acil_durum_sayfasi():
    return render_template("acil_durum.html")

# 📌 **Mevcut rotaları kontrol et ve varsa kaldır**
existing_routes = [rule.endpoint for rule in app.url_map.iter_rules()]
if "hatirlaticilar" in existing_routes:
    app.view_functions.pop("hatirlaticilar")  # Mevcut rotayı kaldır
    print("⚠️ 'hatirlaticilar' rotası zaten tanımlıydı, kaldırıldı ve yeniden tanımlanıyor...")

# 📌 **Yeni rota tanımla**
@app.route("/hatirlaticilar")
@login_required
def hatirlaticilar():
    return render_template("hatirlaticilar.html")  # Eğer böyle bir HTML dosyan varsa
# 📌 **"Grafikler" Rotası Kontrol Et, Varsa Sil, Yoksa Ekle**
existing_routes = [rule.endpoint for rule in app.url_map.iter_rules()]
if "grafikler" in existing_routes:
    app.view_functions.pop("grafikler")
    print("⚠️ 'grafikler' rotası zaten tanımlıydı, kaldırıldı ve yeniden tanımlanıyor...")

# 📌 **Yeni rota tanımla**
@app.route("/grafikler")
@login_required
def grafikler():
    return render_template("grafikler.html")  # Eğer böyle bir HTML dosyan varsa
# 📌 **"Sağlık Önerileri" Rotası Kontrol Et, Varsa Sil, Yoksa Ekle**
existing_routes = [rule.endpoint for rule in app.url_map.iter_rules()]
if "saglik_onerileri" in existing_routes:
    app.view_functions.pop("saglik_onerileri")
    print("⚠️ 'saglik_onerileri' rotası zaten tanımlıydı, kaldırıldı ve yeniden tanımlanıyor...")

# 📌 **Yeni rota tanımla**
@app.route("/saglik_onerileri")
@login_required
def saglik_onerileri():
    return render_template("saglik_onerileri.html")  # Eğer böyle bir HTML dosyan varsa
# 📌 **Profil Rotası - Varsa Sil, Yoksa Ekle**
existing_routes = [rule.endpoint for rule in app.url_map.iter_rules()]
if "profil" in existing_routes:
    app.view_functions.pop("profil")
    print("⚠️ 'profil' rotası zaten tanımlıydı, kaldırıldı ve yeniden tanımlanıyor...")

@app.route("/profil")
@login_required
def profil():
    return render_template("profil.html")  # Eğer böyle bir HTML dosyan varsa
# 📌 **Hasta Paneli Rotası - Varsa Sil, Yoksa Ekle**
existing_routes = [rule.endpoint for rule in app.url_map.iter_rules()]
if "hasta_paneli" in existing_routes:
    app.view_functions.pop("hasta_paneli")
    print("⚠️ 'hasta_paneli' rotası zaten tanımlıydı, kaldırıldı ve yeniden tanımlanıyor...")

@app.route("/hasta_paneli")
@login_required
def hasta_paneli():
    return render_template("hasta_paneli.html")  # Eğer böyle bir HTML dosyan varsa
# 📌 Önce aynı rota tanımlı mı kontrol edelim, varsa silelim
route_name = "/acil_durum_sayfasi"
existing_routes = [rule.rule for rule in app.url_map.iter_rules()]

if route_name in existing_routes:
    del app.view_functions["acil_durum_sayfasi"]  # Mevcut rotayı kaldır

# 📌 **Yeni rota oluştur**
@app.route("/acil_durum_sayfasi")
@login_required
def acil_durum_sayfasi():
    return render_template("acil_durum_sayfasi.html")  # ✅ Doğru dosya adı

import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify, render_template
# ✅ Modeli ve özellik isimlerini yükle
model = joblib.load(r"C:\Users\ummug\OneDrive\Masaüstü\TedaviOnceligiProjesi\tedavi_onceligi\trained_model_yeni.pkl")
feature_names = joblib.load(r"C:\Users\ummug\OneDrive\Masaüstü\TedaviOnceligiProjesi\tedavi_onceligi\model_features_yeni.pkl")

# 🔹 Modelin yüklenip yüklenmediğini test et
print("✅ Yeni model başarıyla yüklendi:", type(model))
print("✅ Yeni modelin beklediği sütunlar:", feature_names)

# Eğer "/tahmin" rotası zaten varsa, önce silelim
if "tahmin" in [rule.endpoint for rule in app.url_map.iter_rules()]:
    app.view_functions.pop("tahmin")

import shap
import matplotlib.pyplot as plt
import io
import base64
@app.route('/tahmin', methods=['POST'])
def tahmin():
    print("🚀 /tahmin rotası çalıştı!")

    try:
        if not request.is_json:
            return jsonify({"hata": "İstek JSON formatında değil!"}), 400

        data = request.get_json()
        print("📩 Gelen JSON Veri:", data)

        if not data or not isinstance(data, dict):
            return jsonify({"hata": "Geçersiz veri!"}), 400

        # ✅ 'Evet'/'Hayır' dönüşümü
        for k in list(data.keys()):
            data[k] = convert_evet_hayir(data[k])

        # ✅ One-hot encoding alanları
        one_hot_fields = {
            "Bilinç_Durumu": ["Bilinç_Durumu_Bilinçsiz", "Bilinç_Durumu_Normal", "Bilinç_Durumu_Sersem"],
            "Yanık": ["Yanık_1. Derece", "Yanık_2. Derece", "Yanık_3. Derece"],
            "Olay_Türü": ["Olay_Türü_Sanayi Kazası"],
            "Göz_Bebeği_Tepkisi": ["Göz_Bebeği_Tepkisi_Tepkisiz"],
            "Nörolojik_Belirtiler": ["Nörolojik_Belirtiler_Uyuşukluk"],
            "Hastanın_Medikal_Geçmişi": [
                "Hastanın_Medikal_Geçmişi_Böbrek",
                "Hastanın_Medikal_Geçmişi_Normal",
                "Hastanın_Medikal_Geçmişi_Nörolojik"
            ],
            "Ağrı_Konumu": ["Ağrı_Konumu_Karın", "Ağrı_Konumu_Kol", "Ağrı_Konumu_Sırt"]
        }

        # 🔵 One-hot encoding uygula
        for field, options in one_hot_fields.items():
            if field in data:
                data = one_hot_encode(data, field, options)

        # ✅ Modelin beklediği sıraya göre düzenleme
        input_features = prepare_features(data, feature_names)

        # ✅ DataFrame oluştur
        df = pd.DataFrame([input_features], columns=feature_names)
        print("📊 Veri çerçevesi oluşturuldu.")

        # ✅ Tahmin
        prediction = int(model.predict(df)[0])
        print(f"🔮 Tahmin sonucu: {prediction}")

        # ✅ SHAP Açıklaması
        explainer = shap.Explainer(model)
        shap_values = explainer(df)

        # Sınıfa özel SHAP gösterimi
        shap_for_class = shap.Explanation(
            values=shap_values.values[0][prediction],
            base_values=shap_values.base_values[0][prediction],
            data=shap_values.data[0],
            feature_names=shap_values.feature_names
        )

        # Grafik oluştur
        plt.figure(figsize=(10, 4))
        shap.plots.waterfall(shap_for_class, show=False)
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        image_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close()

        shap_html = f'''
            <img src="data:image/png;base64,{image_base64}" 
                 style="max-width:100%; height:auto; border:1px solid #ccc; 
                        border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1);" />
        '''

        return jsonify({
            "tahmin": prediction,
            "shap_html": shap_html
        })

    except Exception as e:
        print(f"❌ Sunucu Hatası: {str(e)}")
        return jsonify({"hata": f"Sunucu hatası: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)
