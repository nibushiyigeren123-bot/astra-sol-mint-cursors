"""Compile existing approved Astra/sol artwork into editable Windows cursors."""
from pathlib import Path
import base64, hashlib, io, json, math, shutil, struct, zipfile
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT if Path(__file__).parent.name == 'source' else ROOT / 'public' / 'astra-sol-mint-cursors'
OLD = Path('E:/cladue缓存/Astra_Sol桌宠_20261009')
SIZES = (32, 48, 64, 128, 256)
ROLES = [
 ('Arrow','正常选择'),('Help','帮助选择'),('AppStarting','后台运行'),
 ('Wait','忙碌'),('Crosshair','精确选择'),('IBeam','文本选择'),
 ('NWPen','手写'),('No','不可用'),('SizeNS','垂直调整'),
 ('SizeWE','水平调整'),('SizeNWSE','对角调整1'),('SizeNESW','对角调整2'),
 ('SizeAll','移动'),('UpArrow','候选选择'),('Hand','链接选择'),
 ('Pin','位置选择'),('Person','人员选择')]
NAMES = {'astra':'Astra 姐姐','sol':'sol 妹妹'}
ACTION_ROWS={'idle':(0,6),'running-right':(1,8),'running-left':(2,8),'waving':(3,4),'jumping':(4,5),'failed':(5,8),'waiting':(6,6),'working':(7,6),'review':(8,6)}
ROLE_ACTION={'Arrow':'idle','Help':'review','AppStarting':'waiting','Wait':'working','Crosshair':'review','IBeam':'working','NWPen':'review','No':'failed','SizeNS':'jumping','SizeWE':'running-right','SizeNWSE':'running-right','SizeNESW':'running-left','SizeAll':'running-right','UpArrow':'jumping','Hand':'waving','Pin':'waiting','Person':'waving'}
ACTION_CACHE={}
INK='#173e35'; WHITE='#f7fff9'; MINT='#78d9b3'; GOLD='#e8c66a'

def save_json(path, value):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(value,ensure_ascii=False,indent=2),encoding='utf-8')

def cursor_bytes(image, hotspot):
 """32-bit bottom-up BGRA DIB plus DWORD-aligned 1-bit AND mask."""
 w,h=image.size; assert 1 <= w <= 256 and 1 <= h <= 256
 rgba=image.tobytes(); pixels=bytearray(); stride=((w+31)//32)*4
 mask=bytearray(stride*h)
 for out_y,y in enumerate(range(h-1,-1,-1)):
  for x in range(w):
   r,g,b,a=rgba[(y*w+x)*4:(y*w+x+1)*4]
   pixels.extend((b,g,r,a))
   if a==0:mask[out_y*stride+x//8] |= 1 << (7-x%8)
 dib=struct.pack('<IiiHHIIiiII',40,w,h*2,1,32,0,len(pixels),0,0,0,0)+pixels+mask
 return struct.pack('<HHH',0,2,1)+struct.pack('<BBBBHHII',w % 256,h % 256,0,0,*hotspot,len(dib),22)+dib

def chunk(kind,data):
 return kind+struct.pack('<I',len(data))+data+(b'\0' if len(data)%2 else b'')

def ani_bytes(images,hotspot,jiffies=8):
 frames=b''.join(chunk(b'icon',cursor_bytes(im,hotspot)) for im in images)
 header=struct.pack('<9I',36,len(images),len(images),0,0,32,1,jiffies,1)
 body=b'ACON'+chunk(b'anih',header)+chunk(b'LIST',b'fram'+frames)
 return b'RIFF'+struct.pack('<I',len(body))+body

def symbol(role, frame):
 """Draw symbol at 4x, in a 64-unit design space."""
 k=4; im=Image.new('RGBA',(256,256)); d=ImageDraw.Draw(im)
 def pts(p):return [(round(x*k),round(y*k)) for x,y in p]
 def line(p,fill=WHITE,width=2.5):
  d.line(pts(p),fill=INK,width=round((width+2)*k),joint='curve')
  d.line(pts(p),fill=fill,width=round(width*k),joint='curve')
 def poly(p,fill=WHITE):
  d.polygon(pts(p),fill=fill);d.line(pts(p+[p[0]]),fill=INK,width=6,joint='curve')
 def ellipse(box,fill=WHITE):
  d.ellipse(tuple(round(a*k) for a in box),fill=fill,outline=INK,width=6)
 def arrow(p):poly(p,MINT)
 hs=(4,4)
 if role in ('Arrow','Help','AppStarting'):
  poly([(4,4),(5,31),(12,24),(19,37),(25,33),(18,21),(29,20)])
  if role=='Help':
   ellipse((27,3,45,21),MINT)
   f=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',15*k)
   d.text((32*k,2*k),'?',font=f,fill=INK)
  if role=='AppStarting':
   ellipse((28,5,46,23),WHITE)
   for i in range(8):
    a=2*math.pi*(i+frame)/8; x=37+6*math.cos(a);y=14+6*math.sin(a)
    d.ellipse(((x-1.8)*k,(y-1.8)*k,(x+1.8)*k,(y+1.8)*k),fill=MINT if i<4 else INK)
 elif role=='Wait':
  hs=(19,19);ellipse((5,5,33,33),WHITE)
  a=2*math.pi*frame/8
  line([(19,19),(19+10*math.sin(a),19-10*math.cos(a))],MINT,3)
  line([(19,19),(12,16)],GOLD,2)
 elif role=='Crosshair':
  hs=(19,19);line([(19,3),(19,35)]);line([(3,19),(35,19)])
  ellipse((15,15,23,23),MINT)
 elif role=='IBeam':
  hs=(16,20);line([(16,4),(16,36)],MINT)
  line([(8,4),(24,4)]);line([(8,36),(24,36)])
 elif role=='NWPen':
  hs=(5,34);poly([(5,34),(9,23),(28,4),(35,11),(16,30)],MINT)
  poly([(5,34),(9,23),(16,30)],WHITE)
 elif role=='No':
  hs=(19,19);ellipse((4,4,34,34),WHITE);line([(9,9),(29,29)],'#ed8991',4)
 elif role.startswith('Size'):
  hs=(19,19)
  dirs={'SizeNS':[(0,-1),(0,1)],'SizeWE':[(-1,0),(1,0)],
   'SizeNWSE':[(-.707,-.707),(.707,.707)],'SizeNESW':[(.707,-.707),(-.707,.707)],
   'SizeAll':[(0,-1),(0,1),(-1,0),(1,0)]}[role]
  for dx,dy in dirs:
   tx=19+16*dx;ty=19+16*dy;nx=-dy;ny=dx
   line([(19,19),(tx,ty)],MINT,3)
   arrow([(tx,ty),(tx-7*dx+5*nx,ty-7*dy+5*ny),(tx-7*dx-5*nx,ty-7*dy-5*ny)])
 elif role=='UpArrow':
  hs=(19,4);poly([(19,4),(6,18),(14,18),(14,35),(24,35),(24,18),(32,18)],MINT)
 elif role=='Hand':
  hs=(14,4)
  poly([(10,31),(5,22),(6,18),(10,18),(12,22),(12,6),(14,4),(17,5),
   (18,17),(21,13),(24,14),(26,15),(30,15),(32,18),(34,20),(34,30),(29,37),(16,37)],WHITE)
  line([(21,17),(21,26)],MINT,1.2);line([(27,18),(27,26)],MINT,1.2)
 elif role=='Pin':
  hs=(19,35);ellipse((7,4,31,28),MINT)
  poly([(9,20),(19,35),(29,20)],MINT);ellipse((14,10,24,20),WHITE)
 elif role=='Person':
  hs=(19,10);ellipse((12,4,26,18),MINT)
  poly([(6,34),(8,26),(13,22),(25,22),(30,26),(32,34)],WHITE)
 return im,hs

def frame_count(role):
 return 8 if role in ('AppStarting','Wait') else ACTION_ROWS[ROLE_ACTION[role]][1]

def action_frame(character,role,frame):
 if character not in ACTION_CACHE:
  atlas=Image.open(REPO/'source'/'characters'/f'{character}-actions.png').convert('RGBA')
  assert atlas.size==(1536,1872)
  actions={}
  for name,(row,count) in ACTION_ROWS.items():
   group=[atlas.crop((i*192,row*208,(i+1)*192,(row+1)*208)) for i in range(count)]
   # A shared action bounds includes every frame, preserving animation movement.
   bounds=[im.getbbox() for im in group]
   bbox=(min(b[0] for b in bounds),min(b[1] for b in bounds),max(b[2] for b in bounds),max(b[3] for b in bounds))
   normalized=[]
   for im in group:
    source=im.crop(bbox)
    factor=min(240/source.width,240/source.height)
    source=source.resize((round(source.width*factor),round(source.height*factor)),Image.Resampling.LANCZOS)
    normalized.append(source)
   actions[name]=normalized
  ACTION_CACHE[character]=actions
 return ACTION_CACHE[character][ROLE_ACTION[role]][frame % ACTION_ROWS[ROLE_ACTION[role]][1]]

def compile_frame(character,role,size,frame=0):
 canvas=Image.new('RGBA',(256,256))
 # Full-body character dominates all five canvas sizes; no opaque pixels cropped.
 source=action_frame(character,role,frame)
 canvas.alpha_composite(source,((256-source.width)//2,248-source.height))
 icon,hs=symbol(role,frame)
 box=icon.getbbox();badge=icon.crop(box)
 factor=66/max(badge.size)
 badge=badge.resize((round(badge.width*factor),round(badge.height*factor)),Image.Resampling.LANCZOS)
 canvas.alpha_composite(badge,(3,3))
 result=canvas.resize((size,size),Image.Resampling.LANCZOS)
 hs=tuple(max(0,min(size-1,round(((value*4-box[axis])*factor+3)*size/256))) for axis,value in enumerate(hs))
 return result,hs

def main():
 REPO.mkdir(parents=True,exist_ok=True)
 source_dir=REPO/'source'/'characters';source_dir.mkdir(parents=True,exist_ok=True)
 origins={}
 for c in NAMES:
  dst=source_dir/f'{c}.png'
  src=OLD/f'{c}_Q版透明.png' if REPO!=ROOT else dst
  if src!=dst:shutil.copy2(src,dst)
  origins[c]={'source':str(src.resolve()),'sha256':hashlib.sha256(src.read_bytes()).hexdigest()}
  atlas=source_dir/f'{c}-actions.png'
  if REPO!=ROOT:
   atlas_src=OLD/c/'spritesheet.png';shutil.copy2(atlas_src,atlas)
   origins[c]['action_atlas']={'source':str(atlas_src.resolve()),'sha256':hashlib.sha256(atlas_src.read_bytes()).hexdigest()}
 if Path(__file__).resolve()!= (REPO/'source'/'build_cursors.py').resolve():
  shutil.copy2(Path(__file__),REPO/'source'/'build_cursors.py')
 entries=[]
 previous=REPO/'source'/'cursor_manifest.json'
 if previous.exists():
  for old_entry in json.loads(previous.read_text(encoding='utf-8')):
   old_path=(REPO/old_entry['file']).resolve();old_path.relative_to(REPO.resolve())
   if old_path.exists():old_path.unlink()
 for c in NAMES:
  for size in SIZES:
   target=REPO/'cursors'/c/str(size);target.mkdir(parents=True,exist_ok=True)
   for role,label in ROLES:
    animated=True
    frames=[]
    for f in range(frame_count(role)):
     im,hs=compile_frame(c,role,size,f);frames.append(im)
     png=REPO/'source'/'frames'/c/str(size)/f'{role}-{f:02}.png'
     png.parent.mkdir(parents=True,exist_ok=True);im.save(png)
    ext='ani' if animated else 'cur';path=target/f'{role}.{ext}'
    jiffies=12 if role=='Arrow' else 6 if role in ('AppStarting','Wait') else 8
    path.write_bytes(ani_bytes(frames,hs,jiffies))
    entries.append({'character':c,'size':size,'role':role,'label':label,'file':path.relative_to(REPO).as_posix(),'hotspot':hs,'frames':len(frames),'jiffies':jiffies,'frame_ms':jiffies*1000/60,'action':ROLE_ACTION[role]})
 save_json(REPO/'source'/'cursor_manifest.json',entries)
 if REPO!=ROOT:save_json(ROOT/'provenance.json',origins)
 previews=REPO/'previews';previews.mkdir(exist_ok=True)
 font=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',22)
 small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',15)
 sheet=Image.new('RGB',(1440,880),'#152721');d=ImageDraw.Draw(sheet)
 d.text((45,25),'薄荷绿 GPT 姐妹 · Windows 指针',font=font,fill='#daf9e8')
 d.text((45,64),'Astra 姐姐 / sol 妹妹     17 种状态 × 32 / 48 / 64 / 128 / 256 px',font=small,fill='#90bbaa')
 for ci,c in enumerate(NAMES):
  y0=120+ci*365;d.text((45,y0),NAMES[c],font=font,fill='#b4f4d4')
  for i,(role,label) in enumerate(ROLES):
   col=i%9;row=i//9;x=40+col*154;y=y0+45+row*146
   d.rounded_rectangle((x,y,x+142,y+128),12,fill='#eff8f2')
   im,hs=compile_frame(c,role,64)
   sheet.paste(im,(x+37,y+10),im)
   d.text((x+8,y+91),label,font=small,fill='#174438')
 sheet.save(previews/'cursor-overview.png')
 # Actual native-size comparisons on light and dark backgrounds.
 comp=Image.new('RGB',(1920,900),'#152721');cd=ImageDraw.Draw(comp)
 cd.text((40,20),'实际尺寸对照：32 / 48 / 64 / 128 / 256 px · 每个指针均为原生像素',font=font,fill='#d7f9e7')
 for ci,c in enumerate(NAMES):
  y=115+ci*385;cd.text((40,y-42),NAMES[c],font=font,fill='#b4f4d4')
  for si,size in enumerate(SIZES):
   x=40+si*374
   cd.rounded_rectangle((x,y,x+350,y+335),12,fill='#f2f8f4')
   im,_=compile_frame(c,'Arrow',size);comp.paste(im,(x+(350-size)//2,y+18+(256-size)//2),im)
   cd.text((x+125,y+289),f'{size} px',font=font,fill='#214a3e')
 comp.save(previews/'actual-sizes.png')
 gifs=[]
 for f in range(24):
  card=Image.new('RGB',(680,220),'#152721');dc=ImageDraw.Draw(card)
  for i,c in enumerate(NAMES):
   dc.text((25+i*340,20),NAMES[c],font=font,fill='#c8f7df')
   for j,role in enumerate(('Arrow','Hand','Wait')):
    im,_=compile_frame(c,role,64,f);im=im.resize((96,96),Image.Resampling.NEAREST)
    card.paste(im,(20+i*340+j*102,77),im)
  gifs.append(card)
 gifs[0].save(previews/'busy-animation.gif',save_all=True,append_images=gifs[1:],duration=100,loop=0,disposal=2)
 print(json.dumps({'root':str(REPO),'cursor_files':len(entries),'animated_files':sum(e['frames']>1 for e in entries),'roles':len(ROLES)},ensure_ascii=False))

if __name__=='__main__':main()
