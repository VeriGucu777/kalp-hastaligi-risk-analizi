from flask import Flask, render_template, request
import os

# Flask uygulamasını başlat ve templates klasör yolunu manuel olarak belirt
app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))

# Debug için çalışma dizinini ve templates içeriğini yazdır
print("Mevcut Klasör:", os.getcwd())
print("Templates Klasörü Yolu:", os.path.join(os.getcwd(), 'templates'))
print("Templates İçeriği:", os.listdir(os.path.join(os.getcwd(), 'templates')))

# Ana Sayfa (Form Sayfası)
@app.route('/')
def index():
    return render_template('form.html')  # form.html, templates klasöründe olmalı

# Form Gönderimi İşlemi
@app.route('/submit', methods=['POST'])
def submit():
    # Formdan gelen verileri al
    yas = request.form.get('yas')
    cinsiyet = request.form.get('cinsiyet')

    # Debug için verileri yazdır
    print(f"Yaş: {yas}, Cinsiyet: {cinsiyet}")

    # Form verilerini işledikten sonra kullanıcıya sonuç göster
    sonuc = f"Girilen Yaş: {yas}, Cinsiyet: {cinsiyet}"  # Basit bir sonuç mesajı
    return render_template('sonuc.html', sonuc=sonuc)  # sonuc.html, templates klasöründe olmalı

# Flask uygulamasını çalıştır
if __name__ == '__main__':
    app.run(debug=True)
