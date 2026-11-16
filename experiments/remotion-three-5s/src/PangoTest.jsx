import React,{useLayoutEffect,useRef} from 'react';
import {AbsoluteFill,Html5Audio,Img,staticFile,useCurrentFrame,useVideoConfig,delayRender,continueRender,cancelRender} from 'remotion';
import {CategoryCards} from './CategoryCards';
import production from '../public/legacy/production.json';
let scenePromise;
const getScene=()=>{
 if(!scenePromise)scenePromise=import(/* webpackIgnore: true */ staticFile('engine/scene.js')).then(m=>m.createScene(document.createElement('canvas')));
 return scenePromise;
};
export const PangoTest=({cardOffsetFrames=0})=>{
 const frame=useCurrentFrame();const {fps,width,height}=useVideoConfig();
 const typography=useRef(null),phone=useRef(null);
 useLayoutEffect(()=>{
  const handle=delayRender(`Approved Three.js frame ${frame}`,{timeoutInMilliseconds:120000});
  getScene().then(async engine=>{
   const result=await engine.render(frame/fps);
   for(const [ref,layer] of [[typography,engine.layers.typography],[phone,engine.layers.phone]]){
    const ctx=ref.current.getContext('2d');ctx.clearRect(0,0,width,height);ctx.drawImage(layer.canvas,0,0);
   }
   const audit={frame,time:frame/fps,sourceTime:frame/fps,phone:result.motion,card:result.card};
   window.__PANGO_QA=audit;console.log('PANGO_FRAME '+JSON.stringify(audit));continueRender(handle);
  }).catch(cancelRender);
 },[frame,fps,width,height]);
 const style={position:'absolute',inset:0,width,height};
 return <AbsoluteFill style={{backgroundColor:'white'}}>
  <Img src={staticFile('legacy/assets/background.png')} style={style}/>
  <canvas ref={typography} width={width} height={height} style={style}/>
  <CategoryCards production={production} offsetFrames={cardOffsetFrames}/>
  <canvas ref={phone} width={width} height={height} style={style}/>
  <Html5Audio src={staticFile('legacy/assets/V13_Onayli_Miks.mp3')} volume={1}/>
 </AbsoluteFill>;
};
