from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)
df = pd.read_excel("uyeler.xlsx")

@app.route("/", methods=["GET", "POST"])
def home():
    results = []
    if request.method == "POST":
        isim_input = request.form["isim"].strip()
        soyisim_input = request.form["soyisim"].strip()
        memleket_input = request.form["memleket"].strip()

        def normalize(val):
            if pd.isna(val):
                return ""
            return str(val).lower()\
                .replace("ç", "c").replace("ğ", "g").replace("ı", "i")\
                .replace("ö", "o").replace("ş", "s").replace("ü", "u")\
                .strip()

        def contains_all_parts(cell_value, search_input):
            if not search_input:
                return True
            normalized_cell = normalize(cell_value)
            normalized_input = normalize(search_input)
            return all(part in normalized_cell for part in normalized_input.split())

        filtered_df = df.copy()

        if isim_input:
            filtered_df = filtered_df[filtered_df["İSİM"].apply(lambda x: contains_all_parts(x, isim_input))]
        if soyisim_input:
            filtered_df = filtered_df[filtered_df["SOYİSİM"].apply(lambda x: contains_all_parts(x, soyisim_input))]
        if memleket_input:
            filtered_df = filtered_df[filtered_df["MEMLEKET"].apply(lambda x: contains_all_parts(x, memleket_input))]

        if not filtered_df.empty:
            for _, row in filtered_df.iterrows():
                gun = int(row['GÜN']) if not pd.isna(row['GÜN']) else "--"
                ay = int(row['AY']) if not pd.isna(row['AY']) else "--"
                yil = int(row['YIL']) if not pd.isna(row['YIL']) else "--"

                dogum_tarihi = f"{gun}.{ay}.{yil}"
                genc_etiketi = " (GENÇ)" if not pd.isna(row['YIL']) and int(row['YIL']) > 1994 else ""

                result = (
                    f"{row['İSİM']} {row['SOYİSİM']} – "
                    f"TC: {row['TC KİMLİK']} – "
                    f"İlçe: {row['İLÇE']} – Mahalle: {row['MAHALLE']} – "
                    f"Doğum: {dogum_tarihi}{genc_etiketi} – "
                    f"Memleket: {row['MEMLEKET']} – "
                    f"Baba: {row['BABA ADI']} – Anne: {row['ANNE ADI']}"
                )
                results.append(result)
        else:
            results = ["Sistemde eşleşen kayıt bulunamadı."]
    return render_template("index.html", results=results)

if __name__ == '__main__':
    app.run(debug=True)
