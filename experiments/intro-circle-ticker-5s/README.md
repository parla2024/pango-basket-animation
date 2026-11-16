# Pango Basket — yuvarlak giriş ve bağımsız kayan yazı testi

[İki MP4 ve QA raporu](results/REPORT.md)

Yalnızca iki ayrı 5 saniyelik test üretilir. Onaylı 3D telefon/ışık/gölge/kamera, gerçek ekran, logo, kategori ve V13 kaynakları değiştirilmez. Önceden doğrulanmış RGBA telefon önbelleği kullanılır; canlı Three.js çalıştırılmaz. 18 saniyelik alt bant entegrasyonu ve 22 saniyelik ana reklam bu testin dışındadır.

Node.js, FFmpeg, Chromium ve sibling `../remotion-cached-5s` deneyinin hazır `public/phone-cache` katmanı gerekir. Yeni ortamda o deneyin kendi hazırlık/cache komutları bir kez çalıştırılır. Bu deney eksik cache'i otomatik yeniden üretmez.

```sh
npm ci --cache .npm-cache
npm run test:prepare
npm run render:circle
npm run render:ticker
```

Kaynak test başka yerdeyse `PANGO_CACHE_ROOT` ile belirtilir. Hazırlık, mevcut katmanların normal dosya kopyalarını ayrı `public/` klasörüne alır; statik sunucunun dosya symlink'lerini atlamasına bağımlı değildir. Kaynak cache'e veya üretim dosyalarına yazmaz. Bu büyük yerel önbellek Git'e eklenmez.

- `revision-config.json`: yaklaşık1,13sn circle zarfı ve tam kullanıcı metni; kayan yazı takvimi30–540. kare /1–18sn.
- `src/CircleReveal.jsx`: küçükten büyüyen, overshoot/bounce/glow içermeyen mavi-beyaz SVG disk.
- `src/FooterTicker.jsx`: 36px/600 Arial, alt güvenli alanda sağdan sola tek satır; hız gerçek17sn yolculuğa göre hesaplanır.
- `src/PangoTest.jsx`: yuvarlak arka plan ile telefon arasındadır; kategori ve onaylı telefon üst katmanda kalır. Ticker modu yalnızca ayrı alt bant önizlemesidir; orijinal üst logo animasyonu ve arka plan korunur, telefon/kategori bu görsel teste eklenmez.
- `src/motion.mjs`: kare tabanlı eğriler; ticker x konumu lineerdir.
- `scripts/render-tests.cjs`: Remotion PNG akışı + aynı mevcut FFmpeg/V13 hattı; her çıktı150kare/5sn. Başarılı doğrulama sonrası geçici çıktı atomik olarak son ada taşınır.

QA için Python `numpy`, `pillow` gerekir. `qa:effects` orijinal kontrol testinin yerel ham karelerine ihtiyaç duyar (sibling cached testin normal render'ı bunları üretir). `PANGO_SCENE_PATH` gerekirse değişmemiş üretim `scene1` dizinini belirtir. `qa:motion` son render günlüklerindeki gerçek SVG ölçülerini ve kare konumlarını kontrol eder. `qa:playback` dosyaları önceden yükleyip baştan sona oynatır; diğer ağır işler bittikten sonra çalıştırılır.

Yazı önizlemesi yalnızca0–5sn aralığıdır; metin1sn'de başlar. Metnin tamamı5sn'ye sıkıştırılmaz. Tam1–18sn yolculuk matematiksel olarak planlanmıştır; entegrasyon, ana video18sn aşamasına ulaştığında ayrıca yapılacaktır.
