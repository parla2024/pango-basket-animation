from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent.parent;p=root/'results';load=lambda f:json.loads((p/f).read_text());b=load('baseline-timing.json');c=load('cache-generation.json');first=load('cached-approved-timing.json');repeat=load('cached-revision-timing.json');qa=load('QA.json');alpha=load('alpha-QA.json');play=load('playback.json');probes=load('revision-pixel-check.json');restored=load('revision-output-check.json')
assert qa['status']=='technical_gates_passed' and qa['methods']['baseline']['sha256']==qa['methods']['cached']['sha256'];assert alpha['exact_source_png_hash_matches']==150 and all(x['pass'] for x in probes);assert all(x['ended'] and x['duration']==5 and x['droppedVideoFrames']==0 for x in play);assert repeat['cacheFilesUnchanged'] and repeat['threeRenderCalls']==0 and restored['approved_video_restored_byte_for_byte']
for label in ['approved','revision']:
 a=load('cached-'+label+'-audit.json');frames={x['frame']:x for x in a};assert set(frames)==set(range(150));assert all(x['cacheFrame']==x['frame'] and x['webglCalls']==0 and not x['threeResources'] for x in frames.values())
manifest=json.loads((root/'public/phone-cache/manifest.json').read_text());summary={'status':'PASSED_5_SECOND_CACHE_TEST','production_modified':False,'full_length_rendered':False,'duration':5,'fps':30,'frames':150,'size':[1080,1920],'phone_cache_generation_seconds':c['elapsedSeconds'],'phone_cache_bytes':c['bytes'],'cache_key':c['key'],'existing_render_wall_seconds':b['seconds'],'existing_extra_qa_seconds':b['qaExtraSeconds'],'existing_seconds_excluding_extra_qa_estimate':b['secondsExcludingQa'],'cached_first_composite_seconds':first['totalSeconds'],'cached_revision_seconds':repeat['totalSeconds'],'repeat_speedup_using_qa_excluded_estimate':b['secondsExcludingQa']/repeat['totalSeconds'],'cold_total_seconds':c['elapsedSeconds']+first['totalSeconds'],'cached_phone_re_render_calls':0,'all_phone_png_source_hashes_match':150,'output_sha256':qa['methods']['cached']['sha256'],'cached_and_existing_mp4_byte_identical':True,'decoded_mp4_ssim':1,'audio_lag_samples':0,'revision_isolation':probes,'playback':play,'scope':'Single machine and one measured pass per path. Existing path includes extra validation whose elapsed time is separately reported; subtraction is an estimate because encoding overlaps. Cached revision uses existing bundle and only changes 2D props. Full project and 22-second ad are not migrated.'};(p/'PERFORMANCE.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
text=f'''# Pango Basket — önbellekli Remotion + Three.js / 5 saniye

**Sonuç: test geçti.** 3D telefon bir kez şeffaf, kayıpsız RGBA/PNG katmanı olarak üretildi. Remotion telefon karelerini okuyup bağımsız logo/slogan, kategori ve ses zaman çizelgesiyle birleştiriyor. Tekrar render'da telefon yeniden hesaplanmıyor. Bu testin son MP4'ü mevcut yöntemle üretilen MP4 ile **dosya düzeyinde birebir aynı**: SHA-256 `{qa['methods']['cached']['sha256']}`; tüm 150 karede SSIM 1,000000.

**Üretim projesi değiştirilmedi.** Çalışma yalnızca `experiments/remotion-cached-5s` deney dalındadır. Onaylı hareket, gerçek ekran, orijinal logo, ışık/yansıma/gölge, mavi-beyaz zemin ve V13 kaynağı korunur. Telefon modeli yeniden yazılmadı. **22 saniyelik ana videoya geçilmedi.** Kaynak üretim commit'i: `86a2c25e641ac652169758c5f9197182aa18b220`; önceki doğrulanmış yedek etiketi: `backup/pango-before-remotion-production-20261116`.

## Teslim

- [5 saniyelik önbellekli MP4](Pango_Cached_Remotion_5s.mp4): 1080×1920, 30 FPS, 150 kare, 5,000 s H.264/AAC.
- [Mevcut / önbellekli gerçek kodlanmış kareler](Karsilastirma.jpg)
- [Kaynak / önbellek şeffaflık kontrolü](Seffaflik_Kontrolu.jpg): gerçek RGBA katmanları dama ve koyu zeminde.
- [Performans ve son durum](PERFORMANCE.json), [görüntü/ses QA](QA.json), [alfa QA](alpha-QA.json), [oynatma](playback.json).

Yeni ölçümdeki baseline MP4, önceki deneydeki [baseline dosyasıyla](https://raw.githubusercontent.com/parla2024/pango-basket-animation/7d3fc14/experiments/remotion-three-5s/results/Pango_Baseline_5s.mp4) aynı SHA'ya sahiptir. Aynı videonun gereksiz ikinci kopyası bu deney dalına eklenmedi.

## Ölçülen süreler

| İşlem | Süre | 3D telefon yeniden render? |
|---|---:|---|
| Mevcut yöntem, yeni tekrar çalıştırma | **{b['seconds']:.1f} sn** | Evet, 150 kare |
| Bu çalıştırmadaki ek telefon/alfa doğrulama süresi | {b['qaExtraSeconds']:.1f} sn | Yukarıdaki süreye dahil |
| Mevcut yöntem, ek kontrol çıkarılmış yaklaşık süre | **{b['secondsExcludingQa']:.1f} sn** | Evet |
| Telefon katmanının tek seferlik oluşturulması | **{c['elapsedSeconds']:.1f} sn** | Evet, yalnızca önbellek hazırlanırken |
| Önbellekten ilk birleştirme, yeni bundle dahil | **{first['totalSeconds']:.1f} sn** | **Hayır** |
| Yazı/kategori zamanlama revizyonu, mevcut bundle | **{repeat['totalSeconds']:.1f} sn** | **Hayır** |

Bu ölçümde tekrar render yaklaşık **{b['secondsExcludingQa']/repeat['totalSeconds']:.1f} kat** daha kısa sürdü. Bunun ilk 3D önbellek oluşturma maliyetini dışarıda bıraktığı özellikle belirtilmelidir. Soğuk başlangıçta telefon üretimi + ilk birleştirme yaklaşık **{c['elapsedSeconds']+first['totalSeconds']:.1f} sn**; tek seferlik videoda ilk işlem mevcut yöntemden daha uzun olabilir. Kazanç, sonraki 2D revizyonlardadır. Bu koşullarda ikinci toplam render civarında ön hazırlık maliyeti karşılanır; farklı sahne/hardware için garanti değildir.

Mevcut yöntemin 420,8 saniyesi, 150 telefon karesini ayrıca PNG'ye alıp karşılaştıran 12,7 saniyelik QA'yı da içerir. 408,1 saniye bu gözlenen QA aralığının çıkarılmasıyla elde edilen yaklaşık değerdir; encoder paralel çalıştığı için kusursuz bir saf-render benchmark'ı sayılmaz. Önceki kontrolsüz-ek-QA ölçümü 396,5 saniyeydi. Remotion ilk birleştirmesi önbellek doğrulaması, önbelleksiz bundle, composition seçimi, 150 kare yakalama ve aynı sistem FFmpeg ile H.264/AAC kodlamayı içerir. Tekrar testi bundle'ı tekrar derlemez; prop/zamanlama revizyonunu ölçer. Kod veya metin içeriği değiştiğinde yeniden bundle gerekir; telefon yine render edilmez. Kurulum, hata ayıklama ve son QA süreleri kıyasa dahil değildir. İşler sırayla çalıştırıldı; render'lar paralel değildi.

Ortam: Chromium 156, Remotion 4.0.544, Three.js r170, Node24; 2 CPU çekirdeği kotası ve SwiftShader. Tek sahne işçisi; aynı 1080×1920/30 FPS; **iki yolda da aynı sistem FFmpeg**, H.264 CRF17/slow, B-frame0, yuv420p/BT.709, AAC192k/44100. Birer ölçülen çalıştırma vardır; istatistiksel çoklu benchmark veya gerçek zamanlı editör FPS testi yapılmadı.

## Önbelleğin içeriği ve geçersizleştirme

PNG'ler tam çözünürlükte **RGBA**, sıkıştırma kayıpsızdır; arka plan/logo/metin telefon katmanına gömülmez. Mevcut `editableLayers.phone` çıktısı alınır; metal/cam malzemeleri, ortam ışığı, yansımalar, kameranın ölçülmüş perspektifi, orijinal hareket, hızlı hareketlerdeki kontrollü blur ve yumuşak gölge aynı motor tarafından üretilir. Sonradan telefonun arkasına bir dikdörtgen boyanmaz; MP4 üzerinden ekran/maske tahmin edilmez.

Anahtar; telefon geometrisi/malzemeleri, `motion.json`, gerçek `screen.png`, Three.js sürümü, 3D kurulum/kamera/render geçişi ve 1080×1920/30 FPS/150 kare özelliklerini kapsar. **Logo, arka plan, tipografi, kategori JSON'u ve ses zamanlaması anahtara dahil değildir.** Dolayısıyla 2D revizyonlar telefonu geçersizleştirmez. Gerçek bir 3D/ekran değişikliğinde render komutu durur ve açıkça önbelleği yeniden üretmek gerekir; render sırasında gizli bir Three.js yeniden hesaplaması başlatılmaz.

Üretilmiş katman `{c['bytes']:,}` bayt (yaklaşık {c['bytes']/1024**2:.1f} MiB) ve 150 PNG'dir; test ortamında `public/phone-cache/` altında tekrar kullanılmak üzere saklanır. [Önbellek manifesti](phone-cache-manifest.json) anahtar ve kare SHA'larını içerir. Büyük PNG paketi veya ZIP GitHub'a eklenmedi. Yeni bir ortamda `cache:build` yalnızca bir kez çalıştırılır; mevcut test ortamında tekrar çağrı 0,31 saniyede cache hit verdi ve 3D çalıştırmadı. Cache, git deposundan bağımsız bir üretim önbelleğidir.

## Remotion katmanları ve ses

Katman sırası aynen korunur: arka plan → logo/slogan → kategori → şeffaf telefon ve gölgesi. Onaylı logo/slogan maske mantığı bağımsız bir **2D** modüle çıkarıldı; bunun Three.js bağımlılığı yoktur. Kategoriler Remotion kare numarasıyla yönetilen React/SVG bileşenidir. Telefon yalnızca ilgili PNG karesini yükler. Tarayıcı ölçümünde 150 karenin her birinde WebGL context isteği **0**, canlı Three.js/model kaynağı isteği **0**. Önbellek dosyalarının SHA ve değiştirilme zamanları ilk render ve revizyon sonrasında aynıdır.

V13, Remotion `Html5Audio` ile 0. kareden, volume1 / playbackRate1 olarak kompozisyona kayıtlıdır. İlk ve son medya kareleri sırasıyla 0 ve149'dur; timeline kaydı [ses zaman çizelgesi](audio-timeline.json) dosyasındadır. Son görüntü/ses birleştirmesi mevcut FFmpeg hattıyla, aynı zaman ekseninde orijinal miksin ilk 5 saniyesi kullanılarak yapılır. Miks/EQ/seviye/konuşma/efektler yeniden tasarlanmaz; AAC formatına bir kez kodlanır. Kaynak MP3 değişmez. Bu kısa pencere, tam reklam veya tam bir seslendirme cümlesi değildir; sonraki kategoriler öne çekilmez.

## Kalite kontrolü

1. **150/150 şeffaf telefon PNG'si**, yeni baştan çalıştırılan mevcut 3D telefonun PNG çıktısıyla SHA düzeyinde eşleşti. Kamera, UI, malzeme/ışık/yansıma ve motion blur korunmuştur. Seçilmiş 15 kaynak/önbellek RGBA görüntüsü de piksel düzeyinde karşılaştırıldı; fark 0.
2. PNG'lerde alfa gerçekten vardır; dış köşeler saydamdır. Dama/koyu zeminlerde halo, arka plan dikdörtgeni, beyaz kalıntı veya kırpma artefaktı saptanmadı. Orijinal yumuşak gölge katmanın içindedir.
3. 15 ham kompozit karesinde telefonun hem opak alanında hem yarı şeffaf kenar/gölgesinde RGB farkı **0**. Telefonun üstte olduğu katman sırası korunur.
4. Son **MP4 dosyaları birebir aynı SHA**; tüm 150 kodlanmış karede SSIM **1,000000**. Bu yalnızca mevcut 5 saniyelik testin sonucudur; gelecekteki her düzenlemenin otomatik olarak bit eşitliği sağlayacağı iddiası değildir. Nihai MP4 H.264 olduğu için kayıplı bir formattır; kayıpsız olan ara telefon PNG katmanıdır.
5. Kategorilerin ilk görünür kareleri değişmedi: Market99 / Yemek125 / Tüp145. 124 ve144. geçiş karelerinde sonraki kategori erken görünmez. Sonraki üç kategori bu testin dışında kalır.
6. Final V13 ses başlangıcı kayması **0 örnek**; kaynak ilk5 saniyeye korelasyon 0,998962. MP3 ile AAC'nin bit eşitliği iddia edilmez; mevcut ve önbellekli MP4'lerin sesleri ise aynı son dosyanın parçasıdır.
7. Tipografi ve kategori ayrı prop testlerinde 2 kare kaydırıldı. Kategori testinde 2.186, slogan testinde 8.391 piksel değişti; metin alanı dışında ve logo alanında değişen piksel **0**. Telefon cache'i değişmedi. Tam 5 saniyelik revizyon render'ında da 3D çağrısı0. Bu kontrollü iç testin değiştirilmiş MP4'ü teslim edilmez; son teslim orijinal onaylı 0-ofsetli dosyadır ve güvenlik kopyasından byte-for-byte doğrulanarak geri konmuştur.
8. İki son MP4 tamamen çözüldü ve tarayıcıda baştan sona oynatıldı: 150/150 kare, 0 düşen kare, hata0; ses ve görüntü5,000 s.
9. Üretim `scene1/`, eski MP4'ler, gerçek ekran, logo ve V13 kaynak hash'leri değişmedi. Eski yöntem main dalında korunuyor; otomatik üretim göçü yapılmadı.

## Karar

**5 saniyelik tekrar revizyonları için önbellekli yöntem avantajlı:** bu testte aynı görüntü ve ses, yaklaşık 9 kat daha kısa tekrar render; telefon yeniden yazılmadan ve yeniden render edilmeden tipografi/kategoriler düzenlenebiliyor. Telefon hareketi/ışığı/ekranı değişecekse yeniden önbellek üretimi gerekir. Bu maliyet ile yaklaşık116MiB cache depolama ihtiyacı karşılığında 2D revizyonlar hızlanır.

Bu bir estetik veya “ajans kalitesi” puanı değildir; onaylı görüntü kalitesinin korunmasını ve iş akışının hızını ölçer. Sonraki üretim kararı ayrıca alınmalıdır; **22 saniyelik ana video üretilmedi**. Herhangi bir ileriki alfa/katman/kalite kontrolü başarısız olursa çalışan eski yöntem korunmalıdır.
'''
(p/'REPORT.md').write_text(text);(p/'phone-cache-manifest.json').write_text(json.dumps(manifest,indent=2));print('Final report passed and written.')
