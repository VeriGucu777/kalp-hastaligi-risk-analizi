document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("tahmin-btn")?.addEventListener("click", function () {
        const form = document.getElementById("tahminForm");
        const formData = new FormData(form);
        let jsonData = {};

        formData.forEach((value, key) => {
            jsonData[key] = value;
        });

        fetch("/tahmin", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(jsonData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.hata) {
                    alert("Tahmin sırasında hata oluştu: " + data.hata);
                } else {
                    document.getElementById("tahmin_sonucu").innerText = "Tahmin Sonucu: " + data.tahmin;
                    document.getElementById("shap_gorseli").innerHTML = data.shap_html;
                }
            })
            .catch(error => console.error("Hata:", error));
    });
});

