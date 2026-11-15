import * as T from './three.module.js';
export function roundRect(w,h,r){const s=new T.Shape();s.moveTo(-w/2+r,-h/2);s.lineTo(w/2-r,-h/2);s.quadraticCurveTo(w/2,-h/2,w/2,-h/2+r);s.lineTo(w/2,h/2-r);s.quadraticCurveTo(w/2,h/2,w/2-r,h/2);s.lineTo(-w/2+r,h/2);s.quadraticCurveTo(-w/2,h/2,-w/2,h/2-r);s.lineTo(-w/2,-h/2+r);s.quadraticCurveTo(-w/2,-h/2,-w/2+r,-h/2);return s;}
export async function makeProPhone(renderer){
 const phone=new T.Group();phone.name='Pango custom Pro-style titanium phone';
 const titanium=new T.MeshStandardMaterial({color:0x96938d,metalness:1,roughness:.34});
 const chamfer=new T.MeshStandardMaterial({color:0xbab9b5,metalness:1,roughness:.22});
 const black=new T.MeshPhysicalMaterial({color:0x05070a,metalness:.24,roughness:.13,clearcoat:1,clearcoatRoughness:.10});
 const ceramic=new T.MeshPhysicalMaterial({color:0xc9c6bf,metalness:.10,roughness:.30,clearcoat:.8,clearcoatRoughness:.2});
 function body(w,h,r,d,z,mat,bevel=.008){const g=new T.ExtrudeGeometry(roundRect(w,h,r),{depth:d,steps:1,bevelEnabled:true,bevelThickness:bevel,bevelSize:bevel,bevelSegments:6,curveSegments:32});g.translate(0,0,-d/2);const m=new T.Mesh(g,mat);m.position.z=z;phone.add(m);return m;}
 // Physically separate rear ceramic, machined titanium sidewall and narrow front glass.
 body(2.10,4.52,.308,.232,0,titanium,.012);
 body(2.068,4.486,.296,.014,-.125,ceramic,.007);
 body(2.104,4.524,.310,.010,.122,chamfer,.004);
 body(2.078,4.498,.299,.016,.135,black,.005);
 const tex=await new T.TextureLoader().loadAsync('./screen.png');tex.colorSpace=T.SRGBColorSpace;tex.anisotropy=renderer.capabilities.getMaxAnisotropy();
 const sw=1.997,sh=sw*1536/691;const g=new T.ShapeGeometry(roundRect(sw,sh,.244),48);for(let i=0;i<g.attributes.position.count;i++){g.attributes.uv.setXY(i,g.attributes.position.getX(i)/sw+.5,g.attributes.position.getY(i)/sh+.5);}const display=new T.Mesh(g,new T.MeshBasicMaterial({map:tex,toneMapped:false}));display.position.z=.153;display.name='Unmodified original Pango screenshot';phone.add(display);
 const island=body(.43,.112,.056,.006,.164,black,.002);island.position.y=sh/2-.126;
 const cameraGlass=new T.MeshPhysicalMaterial({color:0x142333,metalness:.65,roughness:.12,clearcoat:1});
 const frontLens=new T.Mesh(new T.CircleGeometry(.022,32),cameraGlass);frontLens.position.set(.149,sh/2-.126,.171);phone.add(frontLens);
 const receiver=body(.25,.008,.004,.002,.163,black,.001);receiver.position.y=2.242;
 function capsule(side,y,len,z=.005){const g=new T.CapsuleGeometry(.026,len-.052,5,12);const m=new T.Mesh(g,titanium);m.scale.z=.8;m.position.set(side*1.062,y,z);phone.add(m);return m;}
 capsule(-1,1.08,.17);capsule(-1,.62,.31);capsule(-1,.17,.31);capsule(1,.60,.56);capsule(1,-.63,.30);
 const band=new T.MeshStandardMaterial({color:0x66625c,roughness:.7});for(const x of [-1.057,1.057])for(const y of [-1.52,1.52]){const m=new T.Mesh(new T.BoxGeometry(.013,.032,.225),band);m.position.set(x,y,0);phone.add(m);}
 // Complete Pro-style triple-lens back: real depth, lens barrels, sapphire surfaces and flash.
 const bump=body(.98,1.04,.235,.065,-.171,ceramic,.014);bump.position.set(-.46,1.54,-.171);
 for(const [x,y] of [[-.67,1.80],[-.25,1.55],[-.67,1.30]]){
  const ring=new T.Mesh(new T.CylinderGeometry(.198,.198,.06,48),chamfer);ring.rotation.x=Math.PI/2;ring.position.set(x,y,-.238);phone.add(ring);
  const barrel=new T.Mesh(new T.CylinderGeometry(.170,.170,.018,48),black);barrel.rotation.x=Math.PI/2;barrel.position.set(x,y,-.273);phone.add(barrel);
  const glass=new T.Mesh(new T.CircleGeometry(.143,48),cameraGlass);glass.rotation.y=Math.PI;glass.position.set(x,y,-.285);phone.add(glass);
  const inner=new T.Mesh(new T.CircleGeometry(.066,32),new T.MeshPhysicalMaterial({color:0x060d16,roughness:.08,metalness:.6,clearcoat:1}));inner.rotation.y=Math.PI;inner.position.set(x,y,-.286);phone.add(inner);
 }
 for(const [x,y,r,c] of [[-.23,1.94,.061,0xe8e0cf],[-.23,1.18,.043,0x151515]]){const m=new T.Mesh(new T.CircleGeometry(r,32),new T.MeshStandardMaterial({color:c,roughness:.4}));m.rotation.y=Math.PI;m.position.set(x,y,-.213);phone.add(m);}
 const port=new T.Mesh(new T.BoxGeometry(.24,.012,.074),black);port.position.set(0,-2.275,0);phone.add(port);for(let i=0;i<5;i++)for(const side of [-1,1]){const m=new T.Mesh(new T.SphereGeometry(.012,12,8),black);m.scale.y=.35;m.position.set(side*(.33+i*.067),-2.272,0);phone.add(m);}
 phone.userData.dimensions={width:2.10,height:4.52,thickness:.256};
 return phone;
}
