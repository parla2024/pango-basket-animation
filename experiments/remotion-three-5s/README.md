# Pango Basket — izole 5 saniyelik Remotion deneyi

[Sonuç ve karşılaştırma raporu](results/REPORT.md) · [Hibrit MP4](results/Pango_Remotion_Three_5s.mp4) · [Baseline MP4](results/Pango_Baseline_5s.mp4)

Üretim kaynakları bu deney dalındaki değişmemiş `../../scene1` dizininden alınır. Kurulum, üretilen `public/` ve render'lar bu deney dizinindedir. `scene1` veya eski teslimler üzerine yazılmaz. Remotion 4.0.544 kullanılır; `@remotion/three`/R3F kurulmaz. Mevcut Three.js motoru kare tabanlı bir köprüyle kullanılır.

Gereksinimler: Node.js, npm, FFmpeg, `/usr/bin/chromium`. Bu deney dizininde:

```sh
npm ci --cache .npm-cache
npm run test:prepare
npm run render:baseline
npm run render:hybrid
```

Kaynak başka yerdeyse `PANGO_SCENE_PATH` ile belirtilir. Hazırlık yalnızca test kopyalarını oluşturur; test çıktılarının aynı iki dosya adına yazılması beklenir. `render:hybrid`, Remotion render'ından sonra video akışını koruyup mevcut FFmpeg hattıyla V13'ün ilk 5 saniyesini kesin süreyle birleştirir. Kurulum ve QA, benchmark süresine dahil edilmez.

- `src/PangoTest.jsx`: Remotion kare ekseni, Three.js köprüsü, korunmuş logo/slogan katmanı ve ses.
- `src/CategoryCards.jsx`: bağımsız React/SVG kartları; aynı kaynak zamanlama/maske eğrileri.
- `scripts/prepare.cjs`: değişmemiş üretim kaynaklarından izole test ve modül uyarlaması.
- `scripts/render-*.cjs`: iki üretim yolu ve süre kayıtları.
- `scripts/normalize-audio.cjs`: 5 saniyelik son V13 ses birleştirmesi; video SHA256 değişmez.
- `scripts/qa.py`, `scripts/playback.cjs`, `scripts/revision-probe.cjs`: gerçek çıktı doğrulamaları.

Sayısal QA için `requirements-qa.txt` içindeki Python paketleri gerekir. `npm run qa`, ardından `npm run qa:playback`; `npm run qa:revision` yalnızca iç kontrol kareleri üretir. Remotion props değiştiğinde composition metadata'sı da yeni props ile seçilmelidir. MP4'te varsayılan kart ofseti 0'dır.

Remotion Studio/Player iş akışı veya tam proje göçü bu deneyin kapsamı değildir. Onaylı hareket/UI/logo korunur; yeni reklam konsepti üretilmez.
