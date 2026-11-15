# Pango Basket — Referans açılış testi

Güncel sahne, 10340.mp4 referansının ilk 2 saniyesindeki telefon ve yazı yerleşimini, girişini ve hareket ritmini kullanır. Eski sol-orta yerleşime uyarlama yapılmaz. Referans arka planı yerine onaylı Pango mavi-beyaz zemin kullanılır. Modern Pro tarzı 3D telefon ve gerçek Pango ekranı korunur; arayüz yeniden çizilmez.

Bu dizinde `python3 -m http.server 8768` çalıştırıp `http://127.0.0.1:8768` adresini açın. Three.js yerel olarak dahildir. Son kare görüntülenir; konsolda `await drawFrame(0.35)` ile zamanı değiştirin.

- `phone.js`: gerçek 3D cihaz ve değişmeyen ekran dokusu.
- `motion.json`: telefon gövdesinin takip edilen izdüşümüne uydurulmuş pozlar ve off-axis kamera; `samples` oynatılan 240 Hz konum/dönüş/lens-shift örnekleridir. Kamera parametreleri tek ve kesin fiziksel kamera çözümü olarak sunulmaz.
- `graphics.json`: orijinal logo yerleşimi ve referanstan ölçülen logo/başlık hareketi ve görünürlükleri.
- `scene.js`: bağımsız telefon ve tipografi katmanları, sabit arka plan, kompozit.
- `timing.json`: test süresi ve başlık giriş karesi.
- `assets/logo.png`: orijinal yüksek çözünürlüklü Pango logosundan şeffaflaştırılmış varlık.
- `assets/headline.png`: referanstaki gerçek ARTIK GİRNE’DE başlığının şeffaf varlığı; farklı font kullanılmaz.

Telefonun 1. karesi optik akışla takip edildi. Kadrajın çoğunlukla dışında kalan 0. kare, devam hareketinden çıkarılıp görünen kenar sınırlarıyla düzeltilmiştir. Telefon modeli değiştiği için kalınlık, kenar ve cam görünümü referansla piksel piksel aynı değildir. Açılış sesi bu testte referansın ilk 2 saniyesinden alınmıştır; önceki V13 zamanlaması kullanılmaz. Çıktı `output/Pango_Basket_Referans_Acilis_Test.mp4` dosyasındadır. Önceki sürümler ve varlıklar silinmemiştir.
