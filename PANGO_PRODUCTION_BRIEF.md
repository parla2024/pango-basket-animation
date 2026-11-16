# Pango Basket — Onaylı Açılış Sahnesi: Üretim ve Kalite Şartnamesi

**Durum:** V13 ses ve orijinal referans hareketi onaylı. V14 **reddedildi**. Bu belge yeni bir konsept izni vermez.

## Kaynaklar — değiştirme
- `10340.mp4` / WhatsApp referans videosu: telefonun hareketi, kamera ritmi, kategori geçişlerinin görsel dili için kaynak; içindeki ESKİ arayüz ve eski metinler kullanılmayacak.
- `17266.jpg`: kullanıcının gönderdiği **güncel ve gerçek Pango ana ekranı**. Ekran elemanları yeniden tasarlanmayacak.
- `pango reklam müziği.mp3` veya `Pango_Basket_V13_TAM_MIKS.mp3`: son onaylı **V13** miks. Müzik, konuşma ve efektler değiştirilmez.
- Pango orijinal logo görseli: logonun biçimi ve marka mavisi için kaynak.

Dosya adları çalışma alanında farklıysa kaynakların kendisini bul; asla var olmayan dosyalar üretildiğini iddia etme.

## Kullanıcının kesin beklentisi
Referansın **telefon giriş/dönüş hareketi ve tipografi hareketinin** mümkün olduğunca aynısı; tek fark **güncel Pango ekranı**, metin **“Pango Basket, çok yakında Girne'de!”**, **temiz beyaz + belirgin Pango mavisi** kurumsal arka plan ve onaylı V13 müzik/ses. Teknoloji ürünü afişi, sarı dekor, dalga/halkalar, sahte ikonlar, yeni konsept, yeniden çizilmiş UI YASAK.

## KRİTİK TEKNİK HATA: KAYNAK MP4 TEK KATMANLI
Eski telefona yeni JPG'yi düz resim/perspektif overlay ile yapıştırmak artefakt/yamulma oluşturdu. Arka plan, ekran, başlık bir tek MP4'ün içine gömülüyse alanların üzerine boyama ve sabit perspektif uygulaması YAPMA.
- Önce gerçek telefon maskesini/rotoskopunu **her karede** çıkar ve incele; arka planı telefonla birlikte hareket ettirme.
- Gerçek ekranı yalnızca telefonun cam iç yüzeyine, çerçevenin **altında**, zamanla değişen dört noktalı yüzey takibi (corner pin/homography) veya takip edilmiş 3D geometri üzerinden bağla.
- Telefon hızlı döndüğünde ekranın geometrisini sağlayamıyorsan **eski arayüzü görünür bırakıp final diye sunma**. Sorunu açıkça raporla.
- Telefonun kenarında halo/yuvarlak maske izleri/dikdörtgen resim kalıntısı/görüntü bozulması/yağlanma olmamalı.
- Kaynaktaki hareketi yeni bir kaba slide veya keyframe hareketine dönüştürme.

## SES/KART SENKRONU
Onaylı miksin gerçek kelime başlangıçlarından tek tek işaretle; aşağıdaki zamanlar yalnızca başlangıç aralıklarıdır ve son ses dosyasından **kare hassasiyetinde doğrulanmalıdır**:
- Market ~3.36 s
- Yemek ~4.14 s
- Tüp ~4.83 s
- Su ~5.30 s
- Çiçek ~5.92 s
- “ve daha fazlası” ~6.85 s
**Kural:** Kart, kelimenin duyulmasından ÖNCE görünemez. “Market” söylenirken “Yemek” kartı sahneye girmeyecek. İlgili kartların bütün girişleri kendi sözcükleriyle eşleşir. İlk 5.17 saniyelik referansın süresini uzatmadan altı kategorinin tamamını içine sıkıştırma. Onaylı sesi hızlandırma, kesme veya yeniden üretme.

## ARKA PLAN
- Beyaz ağırlıklı (%55–60) ve markanın orijinal **canlı mavi** tonları (%30–35).
- Açık mavi yalnızca çok düşük miktarda; tertemiz ve ferah. Sarı dekor, halka, manzara, parıltı, metin altı çizgisi ve mavi blokla yazı kapatma YOK.
- Altın kural: Orijinal telefon animasyonu ve tipografi okunabilir, arka plan hareketin önüne geçmez.

## HAREKET/TİPOGRAFİ
- Referanstaki hız, yerleşme, dönüş, geri çekilme ve metin maskelerinin kare kare ölçümlerini kullan.
- Ekran metni: “Pango Basket” + “Çok yakında Girne'de!”; eski “Artık Girne'de” olmayacak.
- Orijinal logo bozulmayacak. Sans-serif tipografi, yumuşak fakat enerjik maskeli reveal; ucuz fade, aşırı büyük/kaba font, sürüklenme ve rastgele bounce YOK.

## TESLİM PLANI — TEK KONTROLLÜ ÇIKTI
1. Önce 0.4 s, 1.5 s, 2.5 s, 3.5 s, 4.2 s, 5.3 s anlarından gerçek ekran görüntüsü al, kaynak ve revizyonu **yan yana** karşılaştır.
2. Telefon ekranı bozulmadan değişmiş; arka plan Pango mavi-beyaz; hiçbir kart kelimeden erken başlamıyorsa **tek kısa MP4** hazırla.
3. V13 ses aynen korunmalı; 1080x1920, 30 FPS, H.264/AAC.
4. QA geçmeyen çalışmayı “hazır”, “9/10”, “ajans kalitesi” diye sunma. Hangi koşulun sağlanmadığını açıkça bildir.
5. Çalışan dosyaları/son başarılı sürümü ve onaylı kaynakları bozma; V14 üzerine yazma; gereksiz ZIP ve çok sayıda versiyon oluşturma.

## Bu belgenin amacı
Üretimdeki tekrar eden üç hatayı önlemek: **(1) erken kategori kartları (2) yamulan telefon UI'si (3) marka kimliği taşımayan arka plan**. Hareket korunacak; sadece bu üç problem düzeltilmeli.
