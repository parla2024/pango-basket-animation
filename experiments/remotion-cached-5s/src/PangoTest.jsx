import React,{useLayoutEffect,useRef} from 'react';
import {AbsoluteFill,Html5Audio,Img,staticFile,useCurrentFrame,useVideoConfig,delayRender,continueRender,cancelRender} from 'remotion';
import {CategoryCards} from './CategoryCards';
import production from '../public/legacy/production.json';
import manifest from '../public/phone-cache/manifest.json';
if(!window.__PANGO_CACHE_INSTRUMENTED){window.__PANGO_CACHE_INSTRUMENTED=true;window.__PANGO_WEBGL_CALLS=0;const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(kind,...args){if(['webgl','webgl2','experimental-webgl'].includes(kind))window.__PANGO_WEBGL_CALLS++;return original.call(this,kind,...args);};}
export const PangoTest=({cardOffsetFrames=0,typographyOffsetFrames=0})=>{
 const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();const typography=useRef(null),controller=useRef(null);
 useLayoutEffect(()=>{const handle=delayRender(`2D typography ${frame}`);if(!controller.current)controller.current=import(/* webpackIgnore: true */ staticFile('typography.js')).then(m=>m.createTypography(typography.current));controller.current.then(t=>{t.draw(frame/fps,typographyOffsetFrames);const card=production.categories.find(c=>frame-cardOffsetFrames>=c.start_frame&&frame-cardOffsetFrames<c.end_frame);const resources=performance.getEntriesByType('resource').map(x=>x.name);const audit={frame,cacheFrame:frame,cacheKey:manifest.key,webglCalls:window.__PANGO_WEBGL_CALLS,threeResources:resources.filter(u=>/\/engine\/|three\.module\.js|\/phone\.js/.test(u)),category:card?.label||null,cardOffsetFrames,typographyOffsetFrames};window.__PANGO_QA=audit;console.log('PANGO_FRAME '+JSON.stringify(audit));continueRender(handle);}).catch(cancelRender);},[frame,fps,typographyOffsetFrames,cardOffsetFrames]);
 const style={position:'absolute',inset:0,width,height};
 return <AbsoluteFill style={{backgroundColor:'white'}}>
  <Img src={staticFile('legacy/assets/background.png')} style={style}/>
  <canvas ref={typography} width={width} height={height} style={style}/>
  <CategoryCards production={production} offsetFrames={cardOffsetFrames}/>
  <Img src={staticFile(`phone-cache/phone_${String(frame).padStart(3,'0')}.png`)} style={style}/>
  <Html5Audio src={staticFile('legacy/assets/V13_Onayli_Miks.mp3')} volume={1}/>
 </AbsoluteFill>;
};
