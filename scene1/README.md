# Pango Basket — Üst logo, solda slogan

Tek güncel MP4: `output/Pango_Basket_Ust_Logo_Revizyon.mp4` — 3,2 saniye, 1080×1920, 30 FPS.

Kullanıcı önceki telefon hareketini tercih ettiği için referanstan ölçülen eski yola dönülmüştür. Büyük giriş yaklaşık 0,6 saniyede tamamlanır. Yaklaşık 0,15 saniyelik tek kısa duraklamanın ardından 0,75–1,4 saniye arasında geri çekilip sağdaki küçük yerleşime geçer. Uzun ara bekleme kaldırılmıştır. Son poz, sesli sloganın okunması için tutulur.

Logo kullanıcının isteğiyle yeniden üst bölüme alınır (yaklaşık x=80, y=150). Boyutu, çizimi ve animasyon zamanları korunur. **Çok yakında Girne’de!** sloganı telefonun sol yanında kalır. Telefonun kısa duruşu ve geri çekilmesi, gerçek UI, mavi-beyaz zemin ve V13 sesi değişmez. Sabit telefon karesi tekrar kullanılarak yalnızca yeni yazı konumları kompozit edilir; `invalidatePhoneCache()` ile önbellek temizlenebilir.

V13 AAC ses izi kullanıcının yüklediği `Pango_Basket_Motion_Revizyon.mp4` dosyasından yeniden kodlanmadan kopyalanır. Miks, seviye, EQ veya zaman kayması yapılmaz. Eski MP4 ve proje sürümleri silinmemiştir.

Bu dizinde `python3 -m http.server 8768` çalıştırıp `http://127.0.0.1:8768` adresini açın. Son kare görünür; konsolda `await drawFrame(1.1)` ile zamanı değiştirin. Three.js yerel olarak dahildir.

- `motion.json`: önceki ölçülmüş yol, kısa duruş ve geri çekilme zaman eşlemesi.
- `graphics.json`: soldaki grup yerleşimi, orijinal logo dönüşümü ve kelime maskeleri.
- `scene.js`: bağımsız telefon/tipografi katmanları, 3D telefon, hızla sınırlanan blur.
- `phone.js`, `screen.png`, `assets/`: korunmuş model, gerçek ekran ve tasarım varlıkları.
