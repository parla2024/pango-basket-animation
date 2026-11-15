# Pango Basket — Motion revizyonu

3,2 saniye, 1080×1920, 30 FPS. Tek revizyon MP4: `output/Pango_Basket_Motion_Revizyon.mp4`.

Tasarım, arka plan, orijinal logo, gerçek ekran dokusu, telefon modeli ve yazıların son konumları/renkleri değişmez. Büyük ve küçük telefon pozları önceki videodan aynen alınır. Giriş ilk harekette hızlı, sonunda yumuşaktır; geri çekilme sıfır başlangıç/bitiş hızı ve ivmesiyle gerçek 3D derinlikte yapılır. Aşırı dönüş veya konum zıplaması eklenmez.

Logo içindeki Pango/Basket ve slogan kelimeleri aynı orijinal görüntülerden, konuşma vurgularına bağlı prefix maskeleri ve kısa kontrollü yerleşme hareketleriyle açılır. Ekran yeniden çizilmez.

Motion blur, izdüşüm köşelerinin hızından hesaplanır. Hız 350 px/sn altında tek, net örnek alınır; hızlı harekette 4 veya 8 temporal örnek kullanılır. Bekleme pozlarında bulanıklık yoktur.

**V13 ses kurgusu:** Önceki `Pango_Basket_Giris_Geri_Cekilme_Test.mp4` dosyasının AAC ses izi yeniden kodlanmadan kopyalanır. Kaynak, kullanıcının yüklediği `pango reklam müziği.mp3` miksidir; referans sesi kullanılmaz. Ses kaydırma, miks, EQ veya seviye değişikliği yapılmaz.

Bu dizinde `python3 -m http.server 8768` çalıştırıp `http://127.0.0.1:8768` adresini açın. Son kare gösterilir; konsolda `await drawFrame(2.6)` ile zamanı değiştirin. Three.js yerel olarak dahildir.

- `phone.js`, `screen.png`, `assets/`: önceki tasarım ve 3D modelin değiştirilmemiş kaynakları.
- `motion.json`: mevcut videodan korunan büyük/küçük pozlar, giriş ve geri çekilme eğrileri, blur eşikleri.
- `graphics.json`, `timing.json`: konuşma vurgusu kareleri ve maskeli geçiş süreleri.
- `scene.js`: düzenlenebilir bağımsız telefon ve tipografi katmanları.

Önceki test ve proje sürümleri korunur; alternatif video, ZIP veya önizleme dosyası eklenmez.
