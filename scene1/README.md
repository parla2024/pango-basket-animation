# Pango Basket — Büyük giriş ve geri çekilme testi

Telefon önce referanstaki büyük yerleşime gelir, yaklaşık 2,3–2,9 saniyede geri çekilip sağa yerleşir. Önceki 2 saniyelik testte bu bölüm görünmüyordu; güncel test 3,2 saniyedir. Arka plan onaylı Pango mavi-beyaz zemindir; gerçek uygulama ekranı ve modern Pro tarzı 3D model korunur.

Ses kaynağı yalnızca kullanıcının yüklediği **pango reklam müziği.mp3** dosyasıdır. İlk 3,2 saniyesi miks, hız, EQ veya seviye değişikliği yapılmadan kullanılır; referansın sesi kullanılmaz. Dosyanın SHA-256 özeti `timing.json` içindedir. Tam ses dosyası çoğaltılmamıştır; kaynak kullanıcı yüklemesinde korunur.

Kullanıcının seçimine göre başlık onaylı **Çok yakında Girne’de!** biçimindedir. Orijinal onaylı yazı görüntüleri korunur; kelimeler konuşma çözümlemesindeki başlangıç karelerinde maskeli biçimde açılır.

Bu dizinde `python3 -m http.server 8768` çalıştırıp `http://127.0.0.1:8768` adresini açın. Son kare görüntülenir; `await drawFrame(2.6)` ile zamanı değiştirin. Three.js yerel olarak dahildir.

- `phone.js`, `screen.png`: gerçek 3D cihaz ve değişmeyen ekran dokusu.
- `motion.json`: referansın telefon takibinden uydurulan pozlar, derinlik ve off-axis kamera. `samples`, 240 Hz oynatılan anahtar dizisidir. Kamera parametreleri tek fiziksel çözüm olarak sunulmaz.
- `graphics.json`: logo hareketi, onaylı başlık kelimelerinin giriş kareleri ve maskeli hareket eğrisi.
- `scene.js`: bağımsız telefon/tipografi katmanları ve kompozit.
- `timing.json`: süre, ses kaynağı ve kelime zamanları.

Kare 1 optik akışla izlenmiştir. Büyük ölçüde kadraj dışında kalan kare 0 devam hareketinden çıkarılıp görünen kenar sınırlarıyla düzeltilmiştir. Önceki proje ve test dosyaları silinmemiştir. Güncel tek test: `output/Pango_Basket_Giris_Geri_Cekilme_Test.mp4`.
