from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
import numpy as np,json
root=Path(__file__).resolve().parent.parent;p=root/'results';cache=root/'public/phone-cache';manifest=json.loads((cache/'manifest.json').read_text());rows=[]
for f in manifest['frames']:
 a=np.array(Image.open(cache/f['file']));assert a.shape==(1920,1080,4);alpha=a[:,:,3];assert all(alpha[y,x]==0 for x,y in [(0,0),(1079,0),(0,1919)]);rows.append({'frame':f['frame'],'transparent_pixels':int((alpha==0).sum()),'partial_alpha_pixels':int(((alpha>0)&(alpha<255)).sum()),'opaque_pixels':int((alpha==255).sum()),'corner_alpha':[int(alpha[y,x]) for x,y in [(0,0),(1079,0),(0,1919)]]})
checks=json.loads((p/'source-phone-checks.json').read_text());decoded=[]
for n in [0,6,9,12,45,75,99,105,124,125,126,144,145,147,149]:
 source=np.array(Image.open(p/'qa'/f'uncached_phone_{n}.png').convert('RGBA'));cached=np.array(Image.open(cache/f'phone_{n:03d}.png').convert('RGBA'));decoded.append({'frame':n,'rgba_changed_values':int(np.count_nonzero(source!=cached)),'max_rgba_delta':int(np.max(abs(source.astype(np.int16)-cached.astype(np.int16))))})
assert all(r['rgba_changed_values']==0 for r in decoded)
# Genuine raw baseline and cached phone, compared on checkerboard and dark matte.
frames=[6,12,45,75,126,147];font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',20);sheet=Image.new('RGB',(1080,1002*6),'#ddd');d=ImageDraw.Draw(sheet)
for i,n in enumerate(frames):
 for k,name in enumerate(['source','cached']):
  im=Image.open(p/'qa'/f'uncached_phone_{n}.png' if k==0 else cache/f'phone_{n:03d}.png').convert('RGBA');bg=Image.new('RGBA',im.size,'#15283f');bd=ImageDraw.Draw(bg)
  if i%2==0:
   for y in range(0,1920,80):
    for x in range(0,1080,80):bd.rectangle((x,y,x+79,y+79),fill=('#b9b9b9' if (x//80+y//80)%2 else '#ececec'))
  bg=Image.alpha_composite(bg,im).convert('RGB').resize((540,960));sheet.paste(bg,(k*540,i*1002+42));d.text((k*540+12,i*1002+8),f'{"Kaynak 3D" if k==0 else "Onbellek RGBA"} / {n/30:.2f} s',font=font,fill='black')
sheet.save(p/'Seffaflik_Kontrolu.jpg',quality=90)
report={'status':'passed','frame_count':150,'exact_source_png_hash_matches':sum(c['exact_png_match'] for c in checks),'selected_decoded_rgba_comparisons':decoded,'all_frame_alpha_checks':rows,'scope':'Original approved phone layer including soft shadow. Straight RGBA PNG; no background or text baked into phone. Source is freshly re-rendered baseline, not a guessed matte.'};assert report['exact_source_png_hash_matches']==150;(p/'alpha-QA.json').write_text(json.dumps(report,indent=2));print('All 150 phone PNGs exactly match fresh source; selected RGBA pixel comparisons and alpha/matte checks passed.')
