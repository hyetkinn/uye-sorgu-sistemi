from flask import Flask, render_template, request
import pandas as pd
import traceback

app = Flask(__name__)

def excel_oku():
    try:
        # Excel dosyasını oku
        df = pd.read_excel('uyeler.xlsx')
        print("Excel dosyası başarıyla okundu")
        print(f"Okunan veri sayısı: {len(df)}")
        print("Sütun isimleri:", df.columns.tolist())
        # DataFrame'i liste of dict'e çevir
        return df.to_dict('records')
    except Exception as e:
        print(f"Excel okuma hatası: {e}")
        print("Hata detayı:", traceback.format_exc())
        return []

# Excel'den verileri oku
df = excel_oku()
print(f"Toplam {len(df)} kayıt yüklendi")

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        results = []
        if request.method == "POST":
            isim_input = request.form["isim"].strip().lower()
            soyisim_input = request.form["soyisim"].strip().lower()
            memleket_input = request.form["memleket"].strip().lower()

            print(f"Arama yapılıyor: {isim_input} {soyisim_input} {memleket_input}")

            # Verileri filtrele
            for member in df:
                try:
                    if isim_input in str(member["isim"]).lower() and soyisim_input in str(member["soyisim"]).lower() and memleket_input in str(member["memleket"]).lower():
                        # GENÇ etiketi ekle
                        dogum_yil = int(str(member["dogum"]).split(".")[2])
                        genc_etiketi = " (GENÇ)" if dogum_yil >= 1995 else ""
                        results.append(f"{member['isim']} {member['soyisim']} – TC: {member['tc']} – İlçe: {member['ilçe']} – Mahalle: {member['mahalle']} – Doğum: {member['dogum']} – Memleket: {member['memleket']} – Baba: {member['baba']} – Anne: {member['anne']} {genc_etiketi}")
                except Exception as e:
                    print(f"Üye işleme hatası: {e}")
                    print("Hata detayı:", traceback.format_exc())

            if not results:
                results.append("Sistemde eşleşen kayıt bulunamadı.")

        return render_template('index.html', results=results)
    except Exception as e:
        print(f"Genel hata: {e}")
        print("Hata detayı:", traceback.format_exc())
        return "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", 500

if __name__ == "__main__":
    app.run(debug=True)
