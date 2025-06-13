import os
import json
from flask import session, redirect, url_for, flash
from functools import wraps

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

# 📌 **Kullanıcı giriş yapmış mı kontrol eden dekoratör**
def login_required(f):
    """ Kullanıcının giriş yapıp yapmadığını kontrol eden dekoratör."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("logged_in", False):
            flash("Bu sayfaya erişmek için giriş yapmalısınız!", "warning")
            return redirect(url_for("main.giris"))
        return f(*args, **kwargs)
    return decorated_function

# 📌 **Kullanıcının belirli bir role sahip olup olmadığını kontrol eden dekoratör**
def role_required(role):
    """ Kullanıcının belirli bir role sahip olup olmadığını kontrol eden dekoratör."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get("role") != role:
                flash(f"Bu sayfaya erişmek için '{role}' olarak giriş yapmalısınız!", "danger")
                return redirect(url_for("main.giris"))
            return f(*args, **kwargs)
        return decorated_function
    return decorator
