import json,hashlib,subprocess,os
from pathlib import Path
import numpy as np
from PIL import Image
root=Path(__file__).resolve().parent.parent;p=root/'results';qa=p/'qa';old=Path(os.environ.get('PANGO_CACHE_ROOT',str(root.parent/'remotion-cached-5s')));config=json.loads((root/'revision-config.json').read_text());rows=[]
def probe(file):return json.loads(subprocess.check_output(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(file)]))
def audiohash(file):return subprocess.check_output(['ffmpeg','-v','error','-i',str(file),'-map','0:a:0','-c','copy','-f','hash','-hash','sha256','-']).decode().strip()
reference=old/'results/Pango_Cached_Remotion_5s.mp4';refAudio=audiohash(reference)
methods={}
for mode,name in [('circle','Pango_Yuvarlak_Giris_5s.mp4'),('ticker','Pango_Kayan_Yazi_Onizleme_5s.mp4')]:
 f=p/name;q=probe(f);v=next(s for s in q['streams'] if s['codec_type']=='video');a=next(s for s in q['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],v['nb_frames'])==(1080,1920,'30/1','150');assert float(v['duration'])==5 and float(a['duration'])==5;subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True);h=audiohash(f);assert h==refAudio
 audit=json.loads((p/f'{mode}-audit.json').read_text());u={r['frame']:r for r in audit};assert set(u)==set(range(150));assert all(x['webglCalls']==0 and not x['threeResources'] for x in u.values());methods[mode]={'file':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'dimensions':[1080,1920],'fps':30,'frames':150,'duration':5,'audio_AAC_packets_match_approved':True,'audio_packet_hash':h,'decode_errors':0,'live_3d_calls':0};print(mode,methods[mode],flush=True)
for n in [0,6,9,12,45,75,99,105,124,125,126,144,145,147,149]:
 base=np.array(Image.open(old/'results/qa'/f'cached_composite_{n}.png').convert('RGB'));new=np.array(Image.open(qa/f'circle_{n}.png').convert('RGB'));alpha=np.array(Image.open(root/'public/phone-cache'/f'phone_{n:03d}.png'))[:,:,3];diff=np.any(base!=new,axis=2);opaque=alpha==255;assert not diff[opaque].any();assert not diff[:500].any();r={'frame':n,'opaque_phone_changed_pixels':int(diff[opaque].sum()),'logo_region_changed_pixels':int(diff[:500].sum()),'total_changed_pixels':int(diff.sum())}
 if n==0 or n>=36:assert not diff.any();r['whole_frame_identical_after_effect']=True
 else:
  cc=config['circle'];u=max(0,min(1,(n-cc['startFrame'])/(cc['growthEndFrame']-cc['startFrame'])));radius=cc['radii'][0]+(cc['radii'][1]-cc['radii'][0])*(1-(1-u)**3);yy,xx=np.ogrid[:1920,:1080];outside=(xx-cc['center'][0])**2+(yy-cc['center'][1])**2>(radius+2)**2;assert not diff[outside].any();r['changed_outside_circle_disk']=int(diff[outside].sum());assert r['total_changed_pixels']>0
 rows.append(r)
# Independent footer: exact old upper logo animation, unchanged background outside lane.
bg=np.array(Image.open(root/'public/legacy/assets/background.png').convert('RGB'));l=config['ticker']['lane'];ticker_rows=[]
for f in sorted(qa.glob('ticker_*.png')):
 n=int(f.stem.split('_')[1]);im=np.array(Image.open(f).convert('RGB'));outside=np.ones((1920,1080),bool);outside[:500]=False;outside[l['y']-2:l['y']+l['height']+2,l['x']-2:l['x']+l['width']+2]=False;assert not np.any(im[outside]!=bg[outside]);
 if n<30:assert np.array_equal(im[500:],bg[500:]);
 source=old/'results/qa'/f'cached_composite_{n}.png';logo_verified=False
 if source.exists():
  phone_alpha=np.array(Image.open(root/'public/phone-cache'/f'phone_{n:03d}.png'))[:500,:,3];clear=phone_alpha==0;assert np.array_equal(im[:500][clear],np.array(Image.open(source).convert('RGB'))[:500][clear]);logo_verified=True
 ticker_rows.append({'frame':n,'outside_footer_and_logo_changed_pixels':0,'original_logo_animation_verified':logo_verified})
manifest=json.loads((root/'public/phone-cache/manifest.json').read_text());oldm=json.loads((old/'public/phone-cache/manifest.json').read_text());assert manifest['key']==oldm['key'];assert all(hashlib.sha256((root/'public/phone-cache'/f['file']).read_bytes()).hexdigest()==f['sha256']==oldm['frames'][f['frame']]['sha256'] for f in manifest['frames'])
production=Path(os.environ.get('PANGO_SCENE_PATH',str(root.parent.parent/'scene1')));protected=json.loads((old/'results/QA.json').read_text())['protected_source_hashes'];assert all(hashlib.sha256((production/f).read_bytes()).hexdigest()==h for f,h in protected.items())
report={'protected_production_sources_unchanged':True,'protected_source_hashes':protected,'status':'PASSED','methods':methods,'circle_raw_pixel_checks':rows,'ticker_preview_checks':ticker_rows,'phone_cache_150_frames_unchanged':True,'cacheKey':manifest['key'],'circle_duration_seconds':(config['circle']['endFrame']-config['circle']['startFrame'])/30,'ticker_text_exact':config['ticker']['text'],'ticker_schedule_seconds':[1,18],'preview_rendered_seconds':[0,5],'footer_safe_margins_px':{'left':l['x'],'right':1080-l['x']-l['width'],'bottom':1920-l['y']-l['height']},'scope':'Circle integrated in original 5s; ticker is an independent footer-only visual preview. Full 1–18s integration and 22s main video not rendered.'};(p/'QA_REPORT.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('Raw phone/logo/category/gradient boundaries, footer-only layout and approved audio verified.',flush=True)
