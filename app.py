from flask import Flask, render_template, request

app = Flask(__name__)

# Örnek veriler (gerçek verilerle değiştirilmeli)
df = [
    {"isim": "Hüseyin Yetkin", "soyisim": "Türkmen", "tc": "123456789", "ilçe": "Mamak", "mahalle": "Yenimahalle", "dogum": "12.03.1995", "memleket": "Ankara", "baba": "Ali Yetkin", "anne": "Zeynep Yetkin"},
    # Diğer üyeleri burada ekleyebilirsin.
]

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        isim_input = request.form["isim"].strip().lower()
        soyisim_input = request.form["soyisim"].strip().lower()
        memleket_input = request.form["memleket"].strip().lower()

        # Verileri filtrele
        for member in df:
            if isim_input in member["isim"].lower() and soyisim_input in member["soyisim"].lower() and memleket_input in member["memleket"].lower():
                # GENÇ etiketi ekle
                dogum_yil = int(member["dogum"].split(".")[2])
                genc_etiketi = " (GENÇ)" if dogum_yil >= 1995 else ""
                results.append(f"{member['isim']} {member['soyisim']} – TC: {member['tc']} – İlçe: {member['ilçe']} – Mahalle: {member['mahalle']} – Doğum: {member['dogum']} – Memleket: {member['memleket']} – Baba: {member['baba']} – Anne: {member['anne']} {genc_etiketi}")

        if not results:
            results.append("Sistemde eşleşen kayıt bulunamadı.")

    return render_template('index.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
