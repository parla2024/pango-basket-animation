# Pango Basket — Sahne 1, ölçülen hareket testi

Bu kaynaklar tek test MP4'ünün düzenlenebilir projesidir. Önceki sürümler korunmuştur. Arka plan, logo, onaylı yazı biçimleri ve gerçek ekran yeniden tasarlanmamıştır.

Bu dizinde `python3 -m http.server 8768` çalıştırıp `http://127.0.0.1:8768` adresini açın. Three.js 0.170.0 yerel olarak dahildir; internet bağlantısı gerekmez. Son kare görüntülenir; tarayıcı konsolunda `await drawFrame(0.35)` ile zamanı değiştirin.

- `phone.js`: bağımsız gerçek 3D geometri ve ekran dokusu.
- `scene.js`: kamera, ışık, bağımsız arka plan / telefon / tipografi canvas katmanları; `window.editableLayers` üzerinden görünürlük.
- `motion.json`: referanstan ölçülmüş kareler, 3D poz uyarlaması ve ara değerlenmiş hareket. Onaylı son konuma uyarlanmış yol. `samples` oynatılan 240 Hz anahtar dizisidir; `keys` ölçüm kayıtlarıdır. `retarget` giriş mesafesini, `anchor_center` son konumu düzenler.
- `timing.json`: kelime başlangıç kareleri ve referansın yazı hareketinden ölçülmüş geçiş profili.
- `screen.png`, `assets/`: değiştirilmemiş ekran ve korunmuş tasarım öğeleri.

Ses testi V13 tam miksinin ilk 3,0667 saniyesini kaydırmadan ve miks işlemi uygulamadan kullanır; ses dosyaları mevcut kaynak pakette korunur. MP4 aynı deponun `output/` dizinindedir.

## Doğrulama sınırları

Görüntü özellikleri takibinin medyan RMS hatası yaklaşık 0,3 px (720×1280 referansta); bu değer, 3D kamera/model eşleşmesinin hatası değildir. 3D poz uyarlamasının medyanı yaklaşık 7 px; onaylı ekranın son konumuna uyarlama yaklaşık 5 px RMS (1080×1920). Referansın arka planı/ekranı kopyalanmadığından yol ve ölçek onaylı sol kompozisyona uyarlanmıştır. İlk iki kare büyük ölçüde kadraj dışında kaldığı için çıkarımla tamamlanır. Ayrı Whip Snap zaman işareti yoktur; önceki kullanıcı onayına göre darbe girişe bağlanır, son yerleşmeye değil. Kelime zamanları konuşma çözümlemesine dayanır. Bu çalışma kesin piksel/kare eşleşmesi onaylanmış nihai reklam değildir.
