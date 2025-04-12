from flask import Flask, render_template, request, send_from_directory
import pandas as pd
import traceback
from datetime import datetime
import os
import logging

app = Flask(__name__, static_folder='static')
logging.basicConfig(level=logging.DEBUG)

# Global değişken olarak verileri tut
df = None

def excel_oku():
    global df
    try:
        if df is None:  # Sadece ilk kez oku
            app.logger.info("Excel dosyası okunuyor...")
            df = pd.read_excel('uyeler.xlsx')
            # Sütun isimlerini düzelt
            df.columns = [col.strip().upper() for col in df.columns]
            app.logger.info("Sütun isimleri: %s", df.columns.tolist())
            app.logger.info("Excel dosyası başarıyla okundu. Toplam %d kayıt var.", len(df))
            
            # İlk satırı göster
            if not df.empty:
                app.logger.info("İlk satır örneği:")
                app.logger.info(df.iloc[0])
    except Exception as e:
        app.logger.error("Excel okuma hatası: %s", str(e))
        app.logger.error("Hata detayı: %s", traceback.format_exc())
        df = pd.DataFrame()  # Boş DataFrame oluştur

# Uygulama başladığında Excel'i oku
excel_oku()

def format_dogum_tarihi(gun, ay, yil):
    try:
        # Sayısal değerleri integer'a çevir
        gun = int(float(gun))
        ay = int(float(ay))
        yil = int(float(yil))
        return f"{gun:02d}.{ay:02d}.{yil}"
    except:
        return f"{gun}.{ay}.{yil}"

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/", methods=["GET", "POST"])
def home():
    try:
        app.logger.info("Ana sayfa isteği alındı. Method: %s", request.method)
        results = []
        if request.method == "POST":
            isim_input = request.form["isim"].strip().lower()
            soyisim_input = request.form["soyisim"].strip().lower()
            memleket_input = request.form["memleket"].strip().lower()

            app.logger.info("Arama yapılıyor: %s %s %s", isim_input, soyisim_input, memleket_input)

            if df is not None and not df.empty:
                try:
                    # Pandas ile filtreleme yap
                    mask = (
                        df['İSİM'].str.lower().str.contains(isim_input, na=False) &
                        df['SOYİSİM'].str.lower().str.contains(soyisim_input, na=False) &
                        df['MEMLEKET'].str.lower().str.contains(memleket_input, na=False)
                    )
                    filtered_df = df[mask]
                    app.logger.info("Filtreleme sonucu %d kayıt bulundu", len(filtered_df))

                    for _, row in filtered_df.iterrows():
                        try:
                            # Doğum tarihini kontrol et
                            dogum_yil = int(float(row['YIL']))
                            genc_etiketi = " (GENÇ)" if dogum_yil >= 1995 else ""
                            
                            # Doğum tarihini formatla
                            dogum_tarihi = format_dogum_tarihi(row['GÜN'], row['AY'], row['YIL'])
                            
                            result = (
                                f"{row['İSİM']}{genc_etiketi} {row['SOYİSİM']} – "
                                f"TC: {row['TC KİMLİK']} – "
                                f"İlçe: {row['İLÇE']} – "
                                f"Mahalle: {row['MAHALLE']} – "
                                f"Doğum: {dogum_tarihi} – "
                                f"Memleket: {row['MEMLEKET']} – "
                                f"Baba: {row['BABA ADI']} – "
                                f"Anne: {row['ANNE ADI']}"
                            )
                            results.append(result)
                        except Exception as e:
                            app.logger.error("Satır işleme hatası: %s", str(e))
                            app.logger.error("Hata detayı: %s", traceback.format_exc())
                except Exception as e:
                    app.logger.error("Filtreleme hatası: %s", str(e))
                    app.logger.error("Hata detayı: %s", traceback.format_exc())
                    app.logger.error("Mevcut sütun isimleri: %s", df.columns.tolist())

            if not results:
                results.append("Sistemde eşleşen kayıt bulunamadı.")

        app.logger.info("Şablon render ediliyor...")
        return render_template('index.html', results=results)
    except Exception as e:
        app.logger.error("Genel hata: %s", str(e))
        app.logger.error("Hata detayı: %s", traceback.format_exc())
        return "Bir hata oluştu. Lütfen daha sonra tekrar deneyin.", 500

if __name__ == "__main__":
    app.logger.info("Uygulama başlatılıyor...")
    app.run(debug=True, port=8080, host='127.0.0.1')
