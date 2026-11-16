const fs=require('fs');const {execFileSync}=require('child_process');const path=require('path');const {bundle}=require('@remotion/bundler');const {selectComposition,renderMedia}=require('@remotion/renderer');
(async()=>{
 const root=path.resolve(__dirname,'..'),results=path.join(root,'results');fs.mkdirSync(results,{recursive:true});
 const start=performance.now();
 const serveUrl=await bundle({entryPoint:path.join(root,'src/index.jsx'),publicDir:path.join(root,'public'),outDir:path.join(root,'build'),enableCaching:false});
 const bundleSeconds=(performance.now()-start)/1000;
 const chromiumOptions={gl:'swangle',enableMultiProcessOnLinux:true,flags:{'enable-unsafe-swiftshader':true}};
 const browserExecutable='/usr/bin/chromium';const common={serveUrl,browserExecutable,chromiumOptions,chromeMode:'chrome-for-testing',timeoutInMilliseconds:120000,logLevel:'warn'};
 const composition=await selectComposition({...common,id:'PangoHybrid5s',inputProps:{cardOffsetFrames:0}});
 const selectionSeconds=(performance.now()-start)/1000-bundleSeconds;
 const frames=[],commands=[];let last=-1;
 const renderStart=performance.now();
 const result=await renderMedia({...common,composition,inputProps:{cardOffsetFrames:0},outputLocation:path.join(results,'Pango_Remotion_Three_5s.mp4'),codec:'h264',crf:17,x264Preset:'slow',pixelFormat:'yuv420p',colorSpace:'bt709',imageFormat:'png',audioCodec:'aac',audioBitrate:'192k',sampleRate:44100,concurrency:1,
 ffmpegOverride:({type,args})=>{let modified=args;if(args.includes('libx264'))modified=[...args.slice(0,-1),'-bf','0',args.at(-1)];commands.push({type,args:modified});return modified;},
 onBrowserLog:log=>{if(log.text.startsWith('PANGO_FRAME ')){try{frames.push(JSON.parse(log.text.slice(12)))}catch(e){console.error(e)}}else if(log.type==='error')console.error(log.text);},
 onProgress:p=>{const n=Math.floor(p.renderedFrames/15);if(n!==last){last=n;console.log('Remotion frames',p.renderedFrames,'encoded',p.encodedFrames);fs.writeFileSync(path.join(results,'hybrid-progress.json'),JSON.stringify(p));}}
 });
 const renderSeconds=(performance.now()-renderStart)/1000;execFileSync(process.execPath,[path.join(root,'scripts/normalize-audio.cjs')],{stdio:'inherit'});const audioFinalizationSeconds=JSON.parse(fs.readFileSync(path.join(results,'audio-finalization.json'),'utf8')).processingSeconds;const totalSeconds=(performance.now()-start)/1000;
 fs.writeFileSync(path.join(results,'hybrid-timing.json'),JSON.stringify({totalSeconds,bundleSeconds,selectionSeconds,renderSeconds,audioFinalizationSeconds,width:1080,height:1920,frames:150,concurrency:1,browser:browserExecutable,gpu:'SwiftShader',remotion:require('remotion/package.json').version,slowestFrames:result.slowestFrames,scope:'One sequential render; dependency installation and QA excluded. Total includes uncached bundling and composition selection. Encoding overlaps frame rendering. Existing FFmpeg path finalizes exact 5-second V13 audio duration without re-encoding video.'},null,2));
 fs.writeFileSync(path.join(results,'hybrid-frame-audit.json'),JSON.stringify(frames,null,2));fs.writeFileSync(path.join(results,'hybrid-ffmpeg-commands.json'),JSON.stringify(commands,null,2));console.log('Hybrid total seconds',totalSeconds);
})().catch(e=>{console.error(e);process.exit(1)});
