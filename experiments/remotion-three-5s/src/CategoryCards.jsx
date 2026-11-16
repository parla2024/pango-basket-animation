import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
const ease=(n)=>1-Math.pow(1-Math.max(0,Math.min(1,n)),3);
let measurement;
const Word=({label,x,y,start,size=64,exit=1,frame,id})=>{
 if(frame<start||exit<=0)return null;
 measurement??=document.createElement('canvas').getContext('2d');
 measurement.font=`500 ${size}px Arial`;
 const width=measurement.measureText(label).width;
 const p=ease((frame-start+1)/4);
 return <g><defs><clipPath id={id}><rect x={x} y={y-size-8} width={width*p*exit+2} height={size+18}/></clipPath></defs><text clipPath={`url(#${id})`} x={x+12*(1-p)} y={y+5*(1-p)} fill="#006ee6" fontFamily="Arial" fontWeight="500" fontSize={size}>{label}</text></g>;
};
export const CategoryCards=({production,offsetFrames=0})=>{
 const frame=useCurrentFrame()-offsetFrames;
 const {width,height}=useVideoConfig();
 const card=production.categories.find(c=>frame>=c.start_frame&&frame<c.end_frame);
 let words=[];
 if(card){const exit=Math.min(1,(card.end_frame-frame)/3);words=card.words?card.words.map((w,i)=>({label:w.label,x:i===1?140:80,y:i===2?1127:1050,start:w.frame,size:[38,60,64][i],exit})): [{label:card.label,x:80,y:1076,start:card.start_frame,size:64,exit}];}
 return <svg width={width} height={height} viewBox={`0 0 ${width} ${height}`} style={{position:'absolute',inset:0}}>{words.map((word,i)=><Word key={word.label} {...word} frame={frame} id={`word-mask-${i}`}/>)}</svg>;
};
