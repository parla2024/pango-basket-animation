const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..');const existing=process.env.PANGO_CACHE_ROOT||path.resolve(root,'../remotion-cached-5s');
if(!fs.existsSync(path.join(existing,'public/phone-cache/manifest.json')))throw Error('Existing approved phone cache required. Prepare/cache:build the sibling remotion-cached-5s test once; this test never starts Three.js.');
fs.mkdirSync(path.join(root,'public'),{recursive:true});
for(const name of ['legacy','phone-cache','typography.js']){const dest=path.join(root,'public',name);if(fs.existsSync(dest)&&fs.lstatSync(dest).isSymbolicLink())fs.unlinkSync(dest);fs.cpSync(path.join(existing,'public',name),dest,{recursive:true,dereference:true});}
console.log('Copied immutable approved assets and RGBA cache to isolated static public directory. No 3D rendering.');
