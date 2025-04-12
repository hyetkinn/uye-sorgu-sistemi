from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

def excel_oku():
    try:
        # Excel dosyasını oku
        df = pd.read_excel('uyeler.xlsx')
        # DataFrame'i liste of dict'e çevir
        return df.to_dict('records')
    except Exception as e:
        print(f"Excel okuma hatası: {e}")
        return []

# Excel'den verileri oku
df = excel_oku()

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        isim_input = request.form["isim"].strip().lower()
        soyisim_input = request.form["soyisim"].strip().lower()
        memleket_input = request.form["memleket"].strip().lower()

        # Verileri filtrele
        for member in df:
            if isim_input in str(member["isim"]).lower() and soyisim_input in str(member["soyisim"]).lower() and memleket_input in str(member["memleket"]).lower():
                # GENÇ etiketi ekle
                dogum_yil = int(str(member["dogum"]).split(".")[2])
                genc_etiketi = " (GENÇ)" if dogum_yil >= 1995 else ""
                results.append(f"{member['isim']} {member['soyisim']} – TC: {member['tc']} – İlçe: {member['ilçe']} – Mahalle: {member['mahalle']} – Doğum: {member['dogum']} – Memleket: {member['memleket']} – Baba: {member['baba']} – Anne: {member['anne']} {genc_etiketi}")

        if not results:
            results.append("Sistemde eşleşen kayıt bulunamadı.")

    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
