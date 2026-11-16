# Pango Basket — Remotion + mevcut Three.js, 5 saniyelik deney

**Sonuç:** Remotion görsel kaliteyi veya telefonun akıcılığını artırmadı. Kartların bileşen ve parametrelerle revize edilmesini kolaylaştırdı. Bu tek çalıştırmada mevcut yöntem daha hızlıydı. Pango için öneri: onaylı Three.js telefonunu ve V13/FFmpeg ses hattını koruyup, sık revize edilen 2D katmanlarda Remotion'u üst yönetim katmanı olarak değerlendirmek. Mevcut onaylı videoyu sırf kalite/hız beklentisiyle tamamen taşımak gerekçelenmedi.

Üretim kaynağı `86a2c25e641ac652169758c5f9197182aa18b220`. Deney yalnızca ayrı `experiments/remotion-three-5s` dalındadır. `scene1/`, eski MP4'ler, gerçek ekran, logo ve ses kaynağının kontrol edilen dosyalarında değişiklik yoktur; main'e bir geçiş yapılmamıştır.

## Çıktılar

- [Hibrit test MP4](Pango_Remotion_Three_5s.mp4)
- [Mevcut yöntemle aynı 5 saniye](Pango_Baseline_5s.mp4)
- [Gerçek kodlanmış karelerin yan yana karşılaştırması](Karsilastirma.jpg)
- [Sayısal QA](QA.json), [oynatma](playback.json), [revizyon deneyi](revision-probe.json)

İki video da **1080×1920, 30 FPS, 150 kare, görüntü ve ses 5,000 saniye**, H.264/AAC. İlk 5 saniye kullanıldığı için Market, Yemek ve Tüp girişleri bulunur; sonraki kategoriler öne çekilmez. Bu kısa pencere sesin tam bir cümlesi değildir. Orijinal 20,48 saniyelik V13 dosyası değiştirilmez.

## Ölçülen karşılaştırma

| Ölçüt | Mevcut Three.js + Canvas/Playwright | Remotion + mevcut Three.js |
|---|---|---|
| Görsel kalite | Onaylı model/UI/ışık ve kompozisyon | Aynı model/UI/ışık; belirgin kalite artışı yok |
| Akıcılık | 150 kare, 30 FPS, onaylı hareket | Aynı hareket zamanı; ek atlama saptanmadı |
| Ses/kart senkronu | Başlangıç kayması 0 örnek | Başlangıç kayması 0 örnek |
| Revizyon | Canvas fonksiyonları ve JSON işaretleri | React kart bileşeni, props ve ortak kare ekseni; kart revizyonu daha düzenli |
| Toplam işlem süresi | **396.5 sn** | **431.3 sn**, yaklaşık **%8.8 daha yavaş** |

Remotion alt süreleri: önbelleksiz bundle 9.81 sn; composition seçimi 1.15 sn; render/kodlama 420.04 sn; tam süreli son ses birleştirme 0.30 sn. Kurulum ve QA/debug aralıkları dahil değildir; sonradan gerekli olan ses düzeltmesinin ölçülen işlem süresi toplama eklenmiştir. Baseline HTTP/browser başlangıcı, kare render'ı ve kodlamayı içerir. [Ham zamanlar](baseline-timing.json) / [hibrit zamanları](hybrid-timing.json).

Aynı makinede **birer çalıştırma** ve tek sahne işçisi kullanıldı; render'lar paralel çalıştırılmadı. Chromium 156, Three.js r170, Remotion 4.0.544, React 19.2.4; SwiftShader ile yazılımsal WebGL, CPU kotası 2 çekirdek. H.264 CRF17/slow, B-frame0, yuv420p/BT.709, AAC192k/44100 ayarları eşleştirildi. Sistem FFmpeg 7.1.5 ile Remotion'un FFmpeg n7.1 sürümleri ve renk dönüştürme yolları farklıdır. Sonuç genel hız garantisi değildir; kurulum süresi veya istatistiksel çoklu benchmark ölçülmedi.

## Entegrasyon nasıl yapıldı?

Resmi `@remotion/three`, React Three Fiber/ThreeCanvas içindir. Bu deneyde onu kurmak ve telefonu R3F ile yeniden yazmak yerine **mevcut imperatif Three.js motoruna bir bağlantı katmanı** yazıldı. Bu, `@remotion/three` paketinin performans testi değildir.

`useCurrentFrame()/fps` mevcut `drawFrame(t)` yoluna aktarılır. Telefon ve mevcut logo/slogan saydam Canvas katmanları olarak alınır. Kamera, geometriler, malzemeler, ışıklar, gerçek ekran, hareket verileri ve hızla sınırlanan motion blur korunur. Motorun bir kareyi bitirmesi `delayRender/continueRender` ile beklenir. Hazır bir MP4'ü Remotion içine koyup yeniden kodlama yöntemi kullanılmadı.

Kategori kelimeleri `CategoryCards.jsx` içinde React/SVG ile, aynı yerleşim, font, renk ve maske eğrileriyle üretilir. Zamanlar aynı `production.json` tablosundan gelir. Mevcut logo/slogan hâlâ eski Canvas motorundadır; onların React'e taşınmasının revizyon avantajı bu testte ölçülmedi. Telefon modelinde yalnızca test kopyasının doku URL çözümlemesi uyarlanır; geometri değişmez. Orijinal dosyalar salt okunur kaynak olarak kullanılır.

V13, Remotion `Html5Audio` ile aynı kompozisyonda test edildi: ilk yerel çıktıda ses başlangıcı kayması 0, korelasyon 0,999667 idi. Ancak ses izi 5,015011 saniyeye uzadı. Son teslimde mevcut FFmpeg yöntemiyle orijinal MP3'ün ilk 5 saniyesi bir kez AAC kodlanarak birleştirildi. **Video akışı yeniden kodlanmadı; önce/sonra SHA256 aynı.** Son görüntü ve ses süreleri 5,000 saniye. [Ses sonlandırma kaydı](audio-finalization.json), [yerel ses ölçümü](native-audio-check.json). Bu nedenle önerilen hibrit altyapı son ses mux aşamasında mevcut FFmpeg hattını korur.

## QA ve somut bulgular

- Her iki dosya tamamen çözüldü; hata yok. Son oynatma testinde 150/150 kare ve **0 düşen kare**; iki dosya da sona ulaştı.
- Tüm 150 kodlanmış karede yöntemler arası SSIM: ortalama **0.997873**, minimum **0.996631**. Bu bir estetik puanı değil, benzerlik ölçümüdür. SVG rasterizasyonu, kompozit ve codec/renk dönüşüm farkları nedeniyle bit/piksel eşitliği iddia edilmez.
- Kaynak ekranın en-boy oranı ve doku dosyası değişmedi. 0,4 / 1,5 / 2,5 / 3,5 / 4,2 / 4,9 saniyede gerçek MP4 ekranları ters perspektifle kaynak UI'ye karşılaştırıldı. Hibrit SSIM yaklaşık 0,966–0,970; baseline yaklaşık 0,968–0,972. Hibrit daha net bir ekran üretmedi. Kaynak 691×1536 çözünürlüktedir; girişte telefonun kadraj dışına çıkması korunur.
- Kategoriler ilk kez **Market 99 / Yemek 125 / Tüp 145. karelerde** görünür. Yemek ve Tüp'ten önceki geçiş kareleri 124 ve 144'te kategori alanında mavi yazı pikseli 0'dır; sonraki kart erken görünmez. Bunlar 3,300 / 4,1667 / 4,8333 saniyedir; sözcük başlangıçlarından önce değildir. Diğer kategoriler 5 saniyelik kapsamın dışındadır.
- Final sesin orijinal 5 saniyeye korelasyonu iki yöntemde de **0,998962**, kayma **0 örnek**. AAC kodlaması nedeniyle kaynak MP3 ile bit eşitliği iddia edilmez.
- Revizyon deneyi: yalnızca `cardOffsetFrames: 0 → 2` değiştirilip 125. kare iki kez render edildi. **2186 piksel değişti; kategori alanı dışında değişen piksel 0.** Telefon/logo/arka plan etkilenmedi. Deney MP4'ü onaylı 0 ofsettedir. Remotion API'sinde yeni props için composition metadata'sı da yeniden seçildi. Bu test insanın düzenleme süresini veya uzun dönem ekip verimliliğini ölçmez.
- Gerçek UI, logo, arka plan, hareket JSON'u, model ve V13 kaynak hash'leri QA dosyasında yer alır; orijinaller değişmedi.

## Hangisi avantajlı?

**Bu onaylı sahnenin tek seferlik üretimi:** mevcut yöntem daha az bağımlılığa sahip ve bu testte daha hızlı; kalite ve akıcılık bakımından geride kalmadı.

**Sık kategori/kelime zamanlaması, farklı reklam süreleri ve tekrar kullanılabilir 2D bileşenler:** Remotion üst katmanı daha avantajlı. Deneyde tek prop değişikliği yalnızca ilgili kategori katmanını etkiledi. Telefonun Three.js'te kalması, onaylı hareket ve gerçek UI'nin korunmasını sağlar. Geçişi yalnızca bu katmanlarla sınırlamak mantıklı; bütün projeyi yeniden yazmak için bu deney bir gerekçe sunmuyor.

Remotion doğru sözcük başlangıçlarını kendiliğinden belirlemez; aynı cue tablosu ve ses/görüntü QA'sı gerekir. Studio/Player üzerinden editör kullanımı, gerçek zamanlı önizleme FPS'i, tüm 20,48 saniyelik miks ve altı kategorinin tamamı bu deneyde ölçülmedi. Üretim altyapısı otomatik olarak taşınmadı.

## Resmi araştırma kaynakları

- [Three entegrasyonu](https://www.remotion.dev/docs/three) / [GitHub doküman kaynağı](https://github.com/remotion-dev/remotion/blob/main/packages/docs/docs/three.mdx)
- [ThreeCanvas ve kareye bağlı animasyon](https://www.remotion.dev/docs/three-canvas)
- [Asenkron render bekleme](https://www.remotion.dev/docs/delay-render)
- [Html5Audio](https://www.remotion.dev/docs/html5-audio)
- [renderMedia seçenekleri](https://www.remotion.dev/docs/renderer/render-media)

Resmi web sitesi bu ortamda HTTP403 verdi; aynı dokümanların resmi `remotion-dev/remotion` GitHub kaynakları ve kurulan 4.0.544 API/type dosyaları incelendi.
