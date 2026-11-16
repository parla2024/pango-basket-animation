# Pango Basket — iki ayrı 5 saniyelik revizyon testi

**Durum: teknik ve görsel kontroller geçti.** Üretim projesi, onaylı iPhone katmanı, gerçek ekran, kamera/hareket verileri, logo varlığı, kategori animasyonları ve V13 kaynağı korunur. Yalnızca ayrı deney dizininde iki çıktı üretildi. Eski proje ve son başarılı videolar değiştirilmedi.

## 1. Yuvarlaklı telefon girişi

[MP4 — Pango_Yuvarlak_Giris_5s.mp4](Pango_Yuvarlak_Giris_5s.mp4)

Mevcut 5 saniyelik telefon sahnesine mavi-beyaz, doğrusal renk geçişli bir SVG disk eklendi. Telefonun önüne gelmez; sıralama **arka plan → yuvarlak → onaylı tipografi → kategori → telefon/gölge** şeklindedir. Disk küçüklükten kontrollü biçimde büyür, overshoot/bounce/elastic veya glow filtresi içermez. Yarıçap72→535px, merkez675/1080; büyüme cubic ease-out, görünürlük smoothstep ile yönetilir.

Zarf 2–36. kareler arasında, yaklaşık **1,13 saniye**; **1,2. saniyede tamamen biter**. Kaybolduktan sonra kaynak sahnenin görünümü korunur. Onaylı telefonun hız, giriş, dönüş, geri çekilme, perspektif, ekran dokusu, ışık/yansıma ve gölgesine yeni işlem uygulanmaz. 3D telefon tekrar render edilmedi; mevcut RGBA cache anahtarı `2243d5b4bbd352fef32e959829ac2c0e8ad011f4c4358e9b08f381d9ec3a381b` değişmedi.

Kontrol karelerinde telefonun opak pikselleri ve üst logo bölgesinde fark0. İlk büyüme karelerinde değişen pikseller yalnızca istenen yuvarlak diskinin içinde kalır; dikdörtgen arka plan oluşmadı. Efekt sonrasındaki kaydedilmiş kontrol kareleri kaynak ham kompozitle birebir eşleşir. Bu ham-kare kontrolüdür; yeni efekt H.264 kodlamasının tahmin zincirini değiştirebileceğinden bütün MP4'ün önceki dosyayla aynı SHA'ya sahip olması beklenmez.

## 2. Bağımsız kayan yazı önizlemesi

[MP4 — Pango_Kayan_Yazi_Onizleme_5s.mp4](Pango_Kayan_Yazi_Onizleme_5s.mp4)

Bu dosya yalnızca alt bandın ayrı görsel testidir: orijinal mavi-beyaz zemin ve üst logo animasyonu korunur. Telefon/kategori görüntüsü bu bağımsız teste eklenmez; **ana telefonlu sahneye ticker henüz bindirilmedi**. Telefon girişte alt alanı kapladığı için bu ayrım, istenen üretim sırasını ve mevcut UI'yi korur. Telefonlu sahnede nihai yerleşim/çakışma kontrolü, ana video18sn aşamasında entegre edilirken yapılmalıdır.

Tam metin değiştirilmeden kullanılır:

> Pango Basket 1 Aralık'ta Girne'de! Marketten yemeğe, yemekten tüpe, giyimden çiçeğe, çiçekten elektroniğe ve ev yaşam ürünlerine kadar aradığın her şey tek uygulamada. Pango Basket çok yakında!

- Planlanan takvim **1–18 saniye**; mevcut önizleme yalnızca **0–5 saniye**. İlk saniyede bant yoktur; ardından metin sağdan sola akar. Tam metin5 saniyeye sıkıştırılmadı.
- Hız sabit: **252.19px/sn**. Gerçek SVG metin genişliği yaklaşık3415px; hız872px görünür alanla birlikte17sn yolculuğa göre hesaplanır. Kare adımı hatası yaklaşık1e-13px; hızlanma/yavaşlama uygulanmaz.
- 36px Arial, ağırlık600; beyaz/saydam ince bant üzerinde Pango mavisi. Bant64/1556 konumunda872×72px; solda64, sağda144, altta292px geometrik boşluk bırakır. Kenar maskesi hafifçe yumuşatılır, metin tek satırdır.
- Kullanıcı metni, render edilen SVG `textContent` ile eşleşti. Canvas/SVG genişlik farkı0,008px altındadır.18sn'de tam çıkış planı matematiksel olarak doğrulandı; **18sn video render'ı yapılmadı**.

## Ortak ses ve kalite kontrolü

İki çıktı da **1080×1920, 30 FPS, 150 kare, görüntü/ses5,000 saniye, H.264/AAC**. V13'ün onaylı ilk5 saniyesi kullanıldı; yeni seslendirme, müzik veya efekt eklenmedi. İki dosyanın AAC paket hash'i, önceki onaylı5 saniyelik dosyayla **birebir aynı**: `SHA256=d5e5254d4d6bdabd1c539e908c95a1d372e35128d741b35e69582a8473eea511`. MP3 ile AAC bit eşitliği iddia edilmez; karşılaştırma önceki onaylı AAC akışınadır.

- Tüm dosyalar baştan sona çözüldü; hata0.
- Ön yüklemeli tarayıcı oynatmasında iki dosya da sona ulaştı:150 kare,0 düşen kare, hata0.
- 150 onaylı RGBA telefon karesinin SHA'ları değişmedi; canlı WebGL/Three.js çağrısı0.
- Telefon ve üst logo ham kontrol kareleri korunur; kategori/slogan geçişleri yuvarlak bittikten sonra kaynakla aynı görünür.
- Bağımsız ticker'ın üst logo karşılaştırması, önizlemede bulunmayan kaynak telefon maskesi dışındaki bölgede yapılır; logo varlığı ve animasyon fazı eşleşir.
- Üretimdeki model, ekran, hareket, logo, arka plan ve V13 kaynak hash'leri yeniden kontrol edildi; değişmedi.

Başarılı render süreleri, paketleme ve kodlama dahil: yuvarlaklı sahne **63.7sn**, bağımsız ticker **45.0sn**. İlk paketleme denemesinde statik symlink dosyaları sunulamadı; izole testte normal dosya kopyalarına geçilerek düzeltildi. Başarısız kurulum denemeleri bu sürelere dahil değildir. Bu bir performans benchmark'ı veya estetik kalite puanı değildir.

[Ham QA raporu](QA_REPORT.json) · [Hareket/kelime ölçümleri](MOTION_QA.json) · [Oynatma kaydı](playback.json)

**22 saniyelik ana video oluşturulmadı. Tam1–18sn kayan yazı entegrasyonu sonraki18sn aşamasına bırakıldı.** Bu teslim yalnızca istenen iki5 saniyelik testtir.
