console.log("JavaScript dosyası başarıyla yüklendi.");

// Dinamik Alanları Gösterme
function turAlanlariniGoster() {
    const tur = document.getElementById("hatirlaticiTuru").value;

    document.getElementById("ilacAlanlari").style.display = tur === "ilac" ? "block" : "none";
    document.getElementById("randevuAlanlari").style.display = tur === "randevu" ? "block" : "none";
    document.getElementById("igneAlanlari").style.display = tur === "igne" ? "block" : "none";
    document.getElementById("notAlanlari").style.display = tur === "not" ? "block" : "none";
}

// Hatırlatıcıları Listeye Ekleme
function hatirlaticiEkle() {
    const tur = document.getElementById("hatirlaticiTuru").value;
    let hatirlatici = {};

    if (tur === "ilac") {
        const ilacAdi = document.getElementById("ilacAdi").value;
        const ilacSaati = document.getElementById("ilacSaati").value;

        if (!ilacAdi || !ilacSaati) {
            alert("Lütfen tüm alanları doldurun!");
            return;
        }

        hatirlatici = {
            tur: "İlaç",
            ad: ilacAdi,
            saat: ilacSaati
        };
    } else if (tur === "randevu") {
        const randevuTarihi = document.getElementById("randevuTarihi").value;
        const doktorAdi = document.getElementById("doktorAdi").value;

        if (!randevuTarihi || !doktorAdi) {
            alert("Lütfen tüm alanları doldurun!");
            return;
        }

        hatirlatici = {
            tur: "Randevu",
            tarih: randevuTarihi,
            doktor: doktorAdi
        };
    } else if (tur === "igne") {
        const igneSaati = document.getElementById("igneSaati").value;

        if (!igneSaati) {
            alert("Lütfen tüm alanları doldurun!");
            return;
        }

        hatirlatici = {
            tur: "İğne",
            saat: igneSaati
        };
    } else if (tur === "not") {
        const genelNot = document.getElementById("genelNot").value;

        if (!genelNot) {
            alert("Lütfen bir not yazın!");
            return;
        }

        hatirlatici = {
            tur: "Genel Not",
            not: genelNot
        };
    }

    // Hatırlatıcıyı localStorage'a Kaydet
    const hatirlaticilar = JSON.parse(localStorage.getItem("hatirlaticilar")) || [];
    hatirlaticilar.push(hatirlatici);
    localStorage.setItem("hatirlaticilar", JSON.stringify(hatirlaticilar));

    // Listeye Ekle
    const liste = document.getElementById("hatirlaticiListesi");
    const item = document.createElement("div");
    item.className = "list-item";
    item.innerHTML = `
        <span><strong>${hatirlatici.tur}</strong> - ${hatirlatici.ad || hatirlatici.not || hatirlatici.doktor || ""} 
        ${hatirlatici.saat || hatirlatici.tarih || ""}</span>
        <button class="delete-btn" onclick="this.parentElement.remove()">Sil</button>
    `;
    liste.appendChild(item);

    alert("Hatırlatıcı başarıyla eklendi!");
}

