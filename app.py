from flask import Flask, render_template, request
import pandas as pd
import traceback
from datetime import datetime

app = Flask(__name__)

# Global değişken olarak verileri tut
df = None

def excel_oku():
    global df
    try:
        if df is None:  # Sadece ilk kez oku
            print("Excel dosyası okunuyor...")
            df = pd.read_excel('uyeler.xlsx')
            # Sütun isimlerini düzelt
            df.columns = [col.strip().upper() for col in df.columns]
            print("Sütun isimleri:", df.columns.tolist())
            print(f"Excel dosyası başarıyla okundu. Toplam {len(df)} kayıt var.")
            
            # İlk satırı göster
            if not df.empty:
                print("İlk satır örneği:")
                print(df.iloc[0])
    except Exception as e:
        print(f"Excel okuma hatası: {e}")
        print("Hata detayı:", traceback.format_exc())
        df = pd.DataFrame()  # Boş DataFrame oluştur

# Uygulama başladığında Excel'i oku
excel_oku()

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        results = []
        if request.method == "POST":
            isim_input = request.form["isim"].strip().lower()
            soyisim_input = request.form["soyisim"].strip().lower()
            memleket_input = request.form["memleket"].strip().lower()

            print(f"Arama yapılıyor: {isim_input} {soyisim_input} {memleket_input}")

            if df is not None and not df.empty:
                try:
                    # Pandas ile filtreleme yap
                    mask = (
                        df['İSİM'].str.lower().str.contains(isim_input, na=False) &
                        df['SOYİSİM'].str.lower().str.contains(soyisim_input, na=False) &
                        df['MEMLEKET'].str.lower().str.contains(memleket_input, na=False)
                    )
                    filtered_df = df[mask]

                    for _, row in filtered_df.iterrows():
                        try:
                            # Doğum tarihini birleştir
                            dogum_yil = int(row['YIL'])
                            genc_etiketi = " (GENÇ)" if dogum_yil >= 1995 else ""
                            
                            result = (
                                f"{row['İSİM']} {row['SOYİSİM']} – "
                                f"TC: {row['TC KİMLİK']} – "
                                f"İlçe: {row['İLÇE']} – "
                                f"Mahalle: {row['MAHALLE']} – "
                                f"Doğum: {row['GÜN']}.{row['AY']}.{row['YIL']} – "
                                f"Memleket: {row['MEMLEKET']} – "
                                f"Baba: {row['BABA ADI']} – "
                                f"Anne: {row['ANNE ADI']}"
                                f"{genc_etiketi}"
                            )
                            results.append(result)
                        except Exception as e:
                            print(f"Satır işleme hatası: {e}")
                            print("Hata detayı:", traceback.format_exc())
                except Exception as e:
                    print(f"Filtreleme hatası: {e}")
                    print("Hata detayı:", traceback.format_exc())
                    print("Mevcut sütun isimleri:", df.columns.tolist())

            if not results:
                results.append("Sistemde eşleşen kayıt bulunamadı.")

        return render_template('index.html', results=results)
    except Exception as e:
        print(f"Genel hata: {e}")
        print("Hata detayı:", traceback.format_exc())
        return "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", 500

if __name__ == "__main__":
    app.run(debug=True)
