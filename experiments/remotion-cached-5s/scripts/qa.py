import json,subprocess,re,hashlib,sys,os
from pathlib import Path
import numpy as np
from scipy.signal import correlate,correlation_lags
from PIL import Image,ImageDraw,ImageFont
import cv2
from scipy.spatial.transform import Rotation
root=Path(__file__).resolve().parent.parent;p=root/'results';qa=p/'qa';qa.mkdir(exist_ok=True)
original=Path(os.environ.get('PANGO_SCENE_PATH',str(root/'../../scene1'))).resolve()
files={'baseline':p/'Pango_Baseline_5s.mp4','cached':p/'Pango_Cached_Remotion_5s.mp4'}
def capture(args):return subprocess.check_output(args)
def ffprobe(f):return json.loads(capture(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(f)]))
def pcm(f,limit=True):
 args=['ffmpeg','-v','error','-i',str(f),'-map','0:a:0']
 if limit:args+=['-t','5']
 return np.frombuffer(capture(args+['-ac','2','-ar','44100','-f','f32le','-']),np.float32).reshape(-1,2)
source=pcm(root/'public/legacy/assets/V13_Onayli_Miks.mp3');assert len(source)==220500
reports={}
for method,f in files.items():
 probe=ffprobe(f);(qa/f'{method}-ffprobe.json').write_text(json.dumps(probe,indent=2));v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio');assert (v['width'],v['height'],v['r_frame_rate'],int(v['nb_frames']))==(1080,1920,'30/1',150);assert abs(float(v['duration'])-5)<.001;assert v['codec_name']=='h264' and a['codec_name']=='aac';assert abs(float(a['duration'])-5)<.001
 subprocess.run(['ffmpeg','-v','error','-i',str(f),'-f','null','-'],check=True)
 sound=pcm(f);n=min(len(source),len(sound));x=source[:n].mean(1);y=sound[:n].mean(1);cc=correlate(y,x,method='fft');lag=int(correlation_lags(len(y),len(x))[np.argmax(cc)]);corr=float(np.corrcoef(source[:n].ravel(),sound[:n].ravel())[0,1]);gain=float(np.sum(source[:n]*sound[:n])/np.sum(source[:n]**2));assert corr>.99 and abs(lag)<=1
 raw=capture(['ffmpeg','-v','error','-i',str(f),'-vf','select=between(n\\,98\\,149),crop=424:180:56:970','-vsync','0','-pix_fmt','rgb24','-f','rawvideo','-']);arr=np.frombuffer(raw,np.uint8).reshape(-1,180,424,3);assert len(arr)==52;counts={i+98:int(np.sum((fr[:,:,2]>150)&(fr[:,:,0]<80)&(fr[:,:,1]>60)&(fr[:,:,1]<170))) for i,fr in enumerate(arr)};first={str(n):counts[n] for n in [99,125,145]};guards={str(n):counts[n] for n in [124,144]};assert all(x>10 for x in first.values()) and all(x<5 for x in guards.values())
 reports[method]={'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'video_duration':v['duration'],'audio_duration':a['duration'],'fps':v['r_frame_rate'],'frames':v['nb_frames'],'decoded_audio_samples':len(sound),'source_excerpt_samples':len(source),'audio_correlation':corr,'audio_lag_samples':lag,'estimated_audio_gain':gain,'first_category_pixels':first,'blank_guard_pixels':guards,'full_decode_errors':0}
 print(method,reports[method],flush=True)
# Full-frame match on all 150 encoded frames; no cherry-picked quality sample.
stats=qa/'full-frame-ssim.txt';subprocess.run(['ffmpeg','-v','error','-i',str(files['baseline']),'-i',str(files['cached']),'-lavfi',f'ssim=stats_file={stats}','-an','-f','null','-'],check=True)
vals=[float(x) for x in re.findall(r'All:([0-9.]+)',stats.read_text())];assert len(vals)==150
quality={'frame_count':len(vals),'mean_ssim':float(np.mean(vals)),'min_ssim':min(vals),'worst_frame':int(np.argmin(vals)),'scope':'Decoded whole-frame SSIM between two pipelines, including compression and rasterization differences. Does not rate aesthetic quality.'};print('quality',quality,flush=True)
# Inspect 6 representative actual decoded frames, not browser preview substitutes.
frames=[12,45,75,105,126,147]
for method,f in files.items():
 expr='+'.join(f'eq(n\\,{n})' for n in frames);subprocess.run(['ffmpeg','-v','error','-y','-i',str(f),'-vf','select='+expr,'-vsync','0',str(qa/(method+'_%02d.png'))],check=True)
motion=json.loads((root/'public/legacy/motion.json').read_text());screen=json.loads((original/'qa/QA_REPORT.json').read_text())['category_first_visible_pixels']['screen']
def viewport(n):
 s=motion['samples'][n*8];R=Rotation.from_quat(s[4:8]).as_matrix();pos=np.array(s[1:4]);w,h,iy,z=screen['width'],screen['height'],screen['centerY'],screen['z'];local=np.array([[-w/2,iy+h/2,z],[w/2,iy+h/2,z],[w/2,iy-h/2,z],[-w/2,iy-h/2,z]])-np.array([0,0,.122]);v=local@R.T+pos;f=motion['focal_ref_px']*1.5;fit=motion['initial_visibility_fit_px'];u=max(0,1-(n/30)/fit['duration']);cx=s[8]*1.5+fit['dx']*u;cy=s[9]*1.5+fit['dy']*u;return np.float32(np.c_[f*v[:,0]/-v[:,2]+cx,cy-f*v[:,1]/-v[:,2]])
reference=cv2.imread(str(root/'public/legacy/screen.png'));W=346;H=round(W*1536/691);ref=cv2.resize(reference,(W,H),interpolation=cv2.INTER_AREA)
def ssim(a,b):
 a=a.astype(float);b=b.astype(float);m1=cv2.GaussianBlur(a,(7,7),1.5);m2=cv2.GaussianBlur(b,(7,7),1.5);v1=cv2.GaussianBlur(a*a,(7,7),1.5)-m1*m1;v2=cv2.GaussianBlur(b*b,(7,7),1.5)-m2*m2;c=cv2.GaussianBlur(a*b,(7,7),1.5)-m1*m2;return float(np.mean(((2*m1*m2+6.5025)*(2*c+58.5225))/((m1*m1+m2*m2+6.5025)*(v1+v2+58.5225))))
screens=[]
for i,n in enumerate(frames,1):
 quad=viewport(n);M=cv2.getPerspectiveTransform(quad,np.float32([[0,0],[W,0],[W,H],[0,H]]));row={'frame':n,'time':n/30}
 for method in files:
  im=cv2.imread(str(qa/f'{method}_{i:02d}.png'));flat=cv2.warpPerspective(im,M,(W,H));row[method+'_ui_ssim']=ssim(ref[8:-8,8:-8],flat[8:-8,8:-8]);assert row[method+'_ui_ssim']>.95
 screens.append(row)
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',21);sheet=Image.new('RGB',(1080,1002*6),'#ddd');d=ImageDraw.Draw(sheet)
for i,n in enumerate(frames,1):
 y=(i-1)*1002;d.text((12,y+8),f'Mevcut sistem / {n/30:.2f} s',fill='black',font=font);d.text((550,y+8),f'Onbellekli Remotion / {n/30:.2f} s',fill='black',font=font)
 for k,method in enumerate(files):sheet.paste(Image.open(qa/f'{method}_{i:02d}.png').convert('RGB').resize((540,960)),(540*k,y+42))
sheet.save(p/'Karsilastirma.jpg',quality=90)
audit=json.loads((p/'cached-approved-audit.json').read_text());unique={r['frame']:r for r in audit};assert set(unique)==set(range(150));assert all(r['cacheFrame']==r['frame'] and r['webglCalls']==0 and not r['threeResources'] for r in unique.values());assert unique[99]['category']=='Market' and unique[125]['category']=='Yemek' and unique[145]['category']=='Tüp'
protected=original.parent;before=json.loads((p/'source-hashes-before.json').read_text());after={f:hashlib.sha256((protected/f).read_bytes()).hexdigest() for f in before};assert before==after
hashes={f:hashlib.sha256((original/f).read_bytes()).hexdigest() for f in ['phone.js','motion.json','screen.png','graphics.json','assets/logo.png','assets/background.png','assets/V13_Onayli_Miks.mp3']};assert all((original/f).read_bytes()==(root/'public/legacy'/f).read_bytes() for f in hashes)
raw=[]
for n in [0,6,9,12,45,75,99,105,124,125,126,144,145,147,149]:
 a=np.array(Image.open(qa/f'original_{n}.png').convert('RGB'));bb=np.array(Image.open(qa/f'cached_composite_{n}.png').convert('RGB'));alpha=np.array(Image.open(root/'public/phone-cache'/f'phone_{n:03d}.png'))[:,:,3];d=np.abs(a.astype(np.int16)-bb.astype(np.int16));opaque=alpha==255;edge=(alpha>0)&(alpha<255);raw.append({'frame':n,'opaque_rgb_max_delta':int(d[opaque].max()) if opaque.any() else 0,'opaque_rgb_mae':float(d[opaque].mean()) if opaque.any() else 0,'alpha_edge_max_delta':int(d[edge].max()) if edge.any() else 0,'alpha_edge_mae':float(d[edge].mean()) if edge.any() else 0})
(p/'cache-raw-quality.json').write_text(json.dumps(raw,indent=2));assert all(r['opaque_rgb_max_delta']==0 and r['alpha_edge_max_delta']==0 for r in raw);source_phone=json.loads((p/'source-phone-checks.json').read_text());assert len(source_phone)==150
report={'raw_phone_quality':raw,'source_phone_exact_png_matches':sum(x['exact_png_match'] for x in source_phone),'status':'technical_gates_passed' if quality['min_ssim']>.98 and quality['mean_ssim']>.99 else 'visual_difference_requires_review','methods':reports,'quality':quality,'screen_checks':screens,'cached_unique_frames':len(unique),'original_files_unchanged':before==after,'protected_source_hashes':hashes,'category_frames':{'Market':99,'Yemek':125,'Tüp':145},'scope':'5-second excerpt only; later categories and full-length migration not tested. Technical similarity is not a claim of improved aesthetic quality.'};(p/'QA.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print('QA report',report['status'],flush=True)
