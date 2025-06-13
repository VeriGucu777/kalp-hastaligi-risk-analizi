import tkinter as tk
from PIL import Image, ImageTk
graphic_path = [("Yaş Dağılımı", "../data/yas_dagilimi.jpg"),
("Yaralanma Türü Dağılımı", "../data/yaralanma_turu_dagilimi.jpg"),
("Ağrı Seviyesi ve Aciliyet İlişkisi", "../data/agri_aciliyet_iliskisi.jpg"),
("Aciliyet Seviyesi", "../data/aciliyet_seviyesi.jpg"),
("Tedaviye Ulaşma Süresi", "../data/tedaviye_ulasma_suresi.jpg"),
("Sağlık Ekibi Kapasitesi", "../data/saglik_ekibi_kapasitesi.jpg"),
("Oksijen ve Aciliyet İlişkisi", "../data/oksijen_aciliyet_iliskisi.jpg")]

root = tk.Tk()
root.title("Grafik Görüntüleme Arayüzü")
root.geometry("800x600")

img_label = tk.Label(root)
img_label.pack(pady=20)

def show_graphic(graphic_path):
    image = Image.open(graphic_path)
    image = image.resize((600, 400))
    photo = ImageTk.PhotoImage(image)
    img_label.config(image=photo)
for title, path in graphic_paths:
    btn = tk.Button(root, text=title, command=lambda p=path:
show_graphic(p))
    btn.pack()
root.mainloop()


