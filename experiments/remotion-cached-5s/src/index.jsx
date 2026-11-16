import React from 'react';import {registerRoot,Composition} from 'remotion';import {PangoTest} from './PangoTest';
const Root=()=> <Composition id="PangoCached5s" component={PangoTest} width={1080} height={1920} fps={30} durationInFrames={150} defaultProps={{cardOffsetFrames:0,typographyOffsetFrames:0}}/>;registerRoot(Root);
