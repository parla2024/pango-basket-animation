# Pango Basket — 5 saniyelik önbellekli Remotion testi

[MP4 ve sonuç raporu](results/REPORT.md) · [Performans](results/PERFORMANCE.json) · [Şeffaflık](results/Seffaflik_Kontrolu.jpg)

Üretim kaynakları `../../scene1` altında değişmeden kalır. Telefon baştan yazılmaz. Onaylı Three.js telefon ve gölge katmanı **bir kez** tam çözünürlüklü RGBA/PNG olarak önbelleğe alınır; Remotion bağımsız 2D logo/slogan, kategori ve ses zaman çizelgesini yönetir. Son H.264/AAC birleştirmesi mevcut FFmpeg ile yapılır. 22 saniyelik video üretilmez.

Node.js, npm, FFmpeg ve `/usr/bin/chromium` gerekir. Yalnızca bu deney dizininde:

```sh
npm ci --cache .npm-cache
npm run test:prepare
npm run cache:build
npm run render:cached
```

`cache:build` mevcut geçerli önbellekte 3D çalıştırmaz. PNG cache'i yaklaşık116MiB'dir, `public/phone-cache/` altında tutulur ve Git'e eklenmez. Yeni ortamda bir kez üretilir. Kare SHA'ları ve girdiler `results/phone-cache-manifest.json` dosyasındadır. Render eksik/bozuk/geçersiz cache'te **durur**; gizlice 3D çalıştırmaz. Telefon, ekran, kamera, ışık veya hareket değişirse açıkça yeniden cache üretimi gerekir.

Kategori/metin kodu veya JSON/varlık değişikliği sonrası `npm run render:cached` yeni bundle alır; telefon yine hesaplanmaz. Yalnızca mevcut bileşenlerin parametre/zamanlama revizyonları için:

```sh
node scripts/render-cached.cjs --reuse-bundle
```

Kontrollü +2 kare kategori/slogan performans deneyi: `npm run benchmark:revision`. **Bu komut test MP4'ünün zamanlamasını değiştirerek üzerine yazar; final onaylı teslim değildir.** Onaylı 0-ofset çıktıya dönmek için `npm run render:cached` çalıştırılır. Ölçümde geçici güvenlik kopyası kullanılıp son MP4 orijinal byte'larıyla geri konmuştur; bu ara revizyon videosu teslim edilmez. Logo, telefon ve ses revizyon prop'larından etkilenmez.

- `src/PangoTest.jsx`: Remotion katmanları ve cache PNG okuma; canlı Three.js importu yok.
- `src/CategoryCards.jsx`: kare tabanlı React/SVG kategori maskeleri.
- `scripts/prepare.cjs`: üretim dosyalarından izole test kopyaları; kaynaklara yazmaz.
- `scripts/prepare-typography.cjs`: onaylı maskeleri bağımsız 2D modüle çıkarır.
- `scripts/build-phone-cache.cjs`: onaylı gerçek 3D render; kayıpsız RGBA ve yumuşak gölge.
- `scripts/cache-key.cjs`, `scripts/validate-cache.cjs`: telefon girdileri ve kare SHA/mtime doğrulaması; 2D girdiler cache anahtarından ayrı.
- `scripts/render-cached.cjs`: Remotion PNG kare akışı → aynı sistem FFmpeg; mevcut V13 miksi ilk5 saniye.
- `scripts/render-baseline.cjs`: karşılaştırma için eski üretim yolu; 150 telefon karesini ayrıca cache ile karşılaştırır, QA süresini ayrı kaydeder.

QA için Python `numpy`, `scipy`, `opencv-python-headless`, `pillow` gerekir. `npm run qa`, `npm run qa:alpha`, `npm run qa:revision`, `npm run qa:playback` mevcut çıktıları denetler; playback'i diğer ağır kontroller bittikten sonra çalıştırın. Kaynak farklı yerdeyse `PANGO_SCENE_PATH` ile belirtilir. Hazırlık yalnızca ilk kurulumda kullanılır; deneyde değiştirilmiş 2D veriler üzerine tekrar kaynak kopyalanacağını dikkate alın.

Ana üretim dalına kurulum veya geçiş yapılmadı. Cache/tasarım/katman QA'sı başarısız olursa mevcut yöntem korunur. Sonuçlar yalnızca 5 saniye için geçerlidir; gerçek zamanlı editör hızı veya tam reklam performansı ölçülmedi.
