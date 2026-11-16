# Pango Basket — production brief revizyonu

Güncel tek kontrollü çıktı: [`output/Pango_Basket_Production_Kontrol.mp4`](../output/Pango_Basket_Production_Kontrol.mp4), 1080×1920, 30 FPS, H.264/AAC, 20,5 saniye. Onaylı V13 miksin 20,48 saniyelik tamamı korunur; müzik, seslendirme ve efektler kesilmez veya hızlandırılmaz. Önceki MP4’ler silinmemiştir.

Kullanıcı, hareket kilidi için **10340.mp4’teki orijinal hareketi** seçti. Önceki 0,15 saniyelik duruş / erken geri çekilme eşlemesi kaldırılmıştır. Kaynak videonun 155 karesinden ölçülen gövde ve kamera perspektifi aynı zaman ekseninde kullanılır. İlk, büyük ölçüde kadraj dışı poz kestirilmiştir. Kaynak 5,1667 saniyede bittiğinden sonraki bölümde son telefon pozu tutulur; diğer sahneler üretilmez.

## Düzeltilen üç problem

- **Ekran:** Gerçek 691×1536 JPG’nin çözülmüş pikselleri `screen.png` ile birebir aynıdır. Ekran, özgün en-boy oranıyla fiziksel cam içinde, açık merkezli 3D çerçeve dudağının altında yer alır. Kamera adası uygulamanın üzerine binmez. MP4 üzerine sabit görüntü yapıştırılmaz. Kısmen kadraj dışında kalan girişte telefonun ekranı da doğal olarak kadraj dışında kalabilir.
- **Kart senkronu:** Onaylı sesin gerçek sözcük başlangıçları kullanılır. Market: kare 99; Yemek: 125; Tüp: 145; Su: 160; Çiçek: 176. “ve / daha / fazlası”: 189 / 195 / 204. İlk görünür piksel sözcükten önce başlamaz; geçişte bir karelik boşluk eski kartın yeni sözcüğe taşmasını engeller. Kartlar bağımsız, saydam metin katmanıdır; sahte ikon veya uygulama arayüzü değildir.
- **Arka plan:** Orijinal logo mavisi `#006EE6`; arka plan varlığında yaklaşık %59,64 beyaz, %35 canlı mavi, %5,36 çok açık ton. Yeni dekor eklenmez. Logo varlığı, üst yerleşimi ve soldaki sloganın mevcut konumları korunur.

## Katmanlar ve tekrar üretim

`window.editableLayers`: telefon, tipografi, kategoriler. `window.editablePhone`: gerçek Three.js geometrisi. `motion.json`: orijinal zaman eksenindeki ölçülmüş 3D yol; `graphics.json`: korunmuş logo/slogan yerleşimi; `production.json`: kartların ses/kare eşlemesi; `phone.js`: fiziksel cihaz ve özgün ekran yüzeyi.

Statik inceleme: bu dizinde `python3 -m http.server 8768`; `http://127.0.0.1:8768` son pozu gösterir. Konsolda `await drawFrame(3.5)` belirli zamanı gösterir. Three.js yerel olarak dahildir.

Render için Node.js, FFmpeg ve Chromium gerekir: `npm install`, ardından `npm run render`. Chromium yolu gerekiyorsa `CHROMIUM_PATH` ile verilir. Render, aynı tek çıktı adına yazar; eski teslimleri silmez. Ses kaynağı `assets/V13_Onayli_Miks.mp3` onaylı yüklemenin aynısıdır. MP4 standardı için bir kez AAC kodlanır; miks/zaman/seviye değişikliği yapılmaz. MP3 ve AAC bit düzeyinde aynı dosya değildir.

## Kalite kontrolü

[`QA_REPORT.json`](qa/QA_REPORT.json) ölçümleri ve sınırlarını içerir. [`QA_Karsilastirma.jpg`](qa/QA_Karsilastirma.jpg) istenen 0,4 / 1,5 / 2,5 / 3,5 / 4,2 / 5,3 saniye anlarında gerçek referansı, **kodlanmış MP4’ten alınan** karelerle yan yana gösterir. Kaynakta olmayan 5,3 saniye karesi açıkça işaretlenir; son kaynak kare tekrar edilmez.

Kontroller: her referans karesinde ekran/gövde kapsaması, kaynak ekran oranı ve piksel doğrulaması, ters perspektifle ekran karşılaştırması, ilk görünür kart kareleri, tüm dosyanın hatasız video/ses çözülmesi, baştan sona tarayıcıda oynatma, tam V13 sesinin süre/korelasyon/zaman kayması karşılaştırması. Ekran benzerliği geometrik/örnekleme doğrulamasıdır; cihazın fiziksel tasarımının veya reklam estetiğinin referansla birebir olduğu iddiası değildir. Kaynak ekranın 691×1536 çözünürlük sınırı korunur.
