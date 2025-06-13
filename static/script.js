document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("tahminForm");

    if (!form) {
        console.error("❌ tahminForm bulunamadı!");
        return;
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();  // Sayfanın yenilenmesini engeller
        console.log("✅ Form gönderildi, tahmin işlemi başlıyor!");

        const formData = new FormData(form);
        let jsonData = {};

        formData.forEach((value, key) => {
            let num = parseFloat(value);
            jsonData[key] = isNaN(num) ? value : num;
        });

        console.log("📤 JSON olarak gönderilen veri:", jsonData);

        try {
            const response = await fetch("/tahmin", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(jsonData)
            });

            const result = await response.json();
            console.log("📥 Tahmin sonucu alındı:", result);

            if (result.tahmin !== undefined) {
                document.getElementById("tahminSonuc").textContent = "Tahmin Sonucu: " + result.tahmin;
                document.getElementById("shapSonuc").innerHTML = result.shap_html || "SHAP görseli bulunamadı.";
            } else if (result.hata) {
                alert("⚠️ Tahmin hatası: " + result.hata);
            } else {
                alert("⚠️ Beklenmeyen yanıt formatı!");
            }

        } catch (error) {
            console.error("❌ Tahmin sırasında hata:", error);
            alert("❌ Sunucuya bağlanılamadı veya hata oluştu.");
        }
    });
});

