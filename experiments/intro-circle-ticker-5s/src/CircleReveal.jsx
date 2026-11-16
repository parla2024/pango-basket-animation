import React from 'react';
import {useCurrentFrame} from 'remotion';
import config from '../revision-config.json';
import {circleState} from './motion.mjs';
export const CircleReveal=()=>{const s=circleState(config.circle,useCurrentFrame());if(s.opacity<=0)return null;return <svg width="1080" height="1920" viewBox="0 0 1080 1920" style={{position:'absolute',inset:0}} aria-label="Pango blue white circle"><defs><linearGradient id="pango-entry-circle" x1="0%" y1="65%" x2="100%" y2="35%"><stop offset="0%" stopColor="#006EE6"/><stop offset="34%" stopColor="#006EE6"/><stop offset="68%" stopColor="#8EC6FF"/><stop offset="100%" stopColor="#FFFFFF"/></linearGradient></defs><circle cx={s.cx} cy={s.cy} r={s.radius} fill="url(#pango-entry-circle)" opacity={s.opacity}/></svg>};
