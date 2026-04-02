from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

def pdf_olustur(sonuc, risk_orani):

    doc = SimpleDocTemplate("rapor.pdf")
    styles = getSampleStyleSheet()

    icerik = []

    # Başlık
    icerik.append(Paragraph("Hasta Risk Analiz Raporu", styles['Title']))
    icerik.append(Spacer(1, 20))

    # Sonuç
    icerik.append(Paragraph(f"Sonuç: {sonuc}", styles['Normal']))
    icerik.append(Spacer(1, 10))

    # Risk
    icerik.append(Paragraph(f"Risk Oranı: %{risk_orani}", styles['Normal']))
    icerik.append(Spacer(1, 20))

    # Grafik
    try:
        icerik.append(Paragraph("Özellik Önem Grafiği:", styles['Heading2']))
        icerik.append(Spacer(1, 10))
        icerik.append(Image("feature_importance.png", width=400, height=300))
    except:
        pass

    doc.build(icerik)

