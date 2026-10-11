"""Editable cursor demo, rendered from the same distributed PNG frames."""
from pathlib import Path
import json,math,subprocess,importlib.util
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1]
R=ROOT if Path(__file__).parent.name=='source' else ROOT/'public'/'astra-sol-mint-cursors'
V=ROOT/'source'/'video' if R==ROOT else ROOT/'video';V.mkdir(exist_ok=True)
FONT='C:/Windows/Fonts/msyh.ttc'
F={n:ImageFont.truetype(FONT,n) for n in (20,24,28,32,40,48,60)}
characters={c:Image.open(R/'source'/'characters'/f'{c}.png').convert('RGBA') for c in ('astra','sol')}
cache={}
manifest=json.loads((R/'source'/'cursor_manifest.json').read_text(encoding='utf-8'))
states=[e for e in manifest if e['character']=='astra' and e['size']==64]
BY_ROLE={e['role']:e for e in states}
DURATION=75.2
spec=importlib.util.spec_from_file_location('cursor_builder',R/'source'/'build_cursors.py')
builder=importlib.util.module_from_spec(spec);spec.loader.exec_module(builder)
def cursor(c,role='Arrow',size=64,frame=0):
 key=c,role,size,frame%BY_ROLE[role]['frames']
 if key not in cache:cache[key]=Image.open(R/'source'/'frames'/c/str(size)/f'{role}-{key[3]:02}.png').convert('RGBA')
 return cache[key]
def text(d,pos,value,n=32,fill='#dffaea'):d.text(pos,value,font=F[n],fill=fill)
def character(im,c,box):
 asset=characters[c].copy();asset.thumbnail((box[2],box[3]),Image.Resampling.LANCZOS);im.paste(asset,(box[0],box[1]),asset)
def render(t):
 im=Image.new('RGB',(1920,1080),'#11231e');d=ImageDraw.Draw(im)
 d.rounded_rectangle((40,40,1880,1040),36,outline='#315648',width=2)
 text(d,(95,74),'MINT SISTERS',24,'#72d6ab')
 text(d,(95,117),'薄荷绿 GPT 姐妹 · Windows 鼠标指针',48)
 text(d,(96,189),'Astra 姐姐  /  sol 妹妹',28,'#a1cdb6')
 d.line((95,249,1825,249),fill='#2b5140',width=2)
 if t<4:
  character(im,'astra',(210,310,360,535));character(im,'sol',(1310,345,300,460))
  text(d,(710,335),'把薄荷绿带到光标旁',40)
  for i,s in enumerate(['姐妹各一套 · 17 种动态状态','待机 / 挥手 / 跑动 / 工作','32 / 48 / 64 / 128 / 256 px 五档','透明 ANI + 安装器 + 编辑源']):text(d,(755,435+i*74),s,28,'#b5dcc7')
 elif t<65.2:
  c='astra' if t<34.6 else 'sol';local=t-(4 if c=='astra' else 34.6)
  index=min(16,int(local/1.8));entry=states[index];role=entry['role'];phase=local-index*1.8
  anim_frame=int(phase*1000/entry['frame_ms'])%entry['frames']
  name='Astra 姐姐' if c=='astra' else 'sol 妹妹'
  text(d,(105,295),name,40,'#baf3d4')
  pose=builder.action_frame(c,role,anim_frame).resize((320,400),Image.Resampling.LANCZOS)
  im.paste(pose,(110,390),pose)
  d.rounded_rectangle((545,300,1805,847),24,fill='#edf7f0')
  text(d,(588,333),'工作台的一点薄荷绿',32,'#245342')
  d.rounded_rectangle((600,420,1200,510),14,fill='#d3eadc')
  text(d,(625,448),'输入今天想完成的小事',28,'#3b6553')
  d.rounded_rectangle((600,570,865,650),14,fill='#368465')
  text(d,(630,590),'打开分享页面',28,'#f5fff8')
  d.rounded_rectangle((930,570,1195,650),14,fill='#cedbd3')
  text(d,(963,590),'暂不可用',28,'#8ca095')
  text(d,(600,725),'位置 ●    人员 ●    帮助 ?',24,'#48715c')
  dx=int(40*math.sin(phase*math.pi)) if role=='SizeAll' else 0
  dy=int(20*math.sin(phase*math.pi)) if role=='SizeAll' else 0
  dw=int(45*math.sin(phase*math.pi)) if role in ('SizeWE','SizeNWSE','SizeNESW') else 0
  dh=int(35*math.sin(phase*math.pi)) if role in ('SizeNS','SizeNWSE','SizeNESW') else 0
  x1,y1,x2,y2=1270+dx,435+dy,1690+dx+dw,720+dy+dh
  d.rounded_rectangle((x1,y1,x2,y2),18,outline='#769d88',width=3)
  text(d,(x1+36,y1+30),'可调整的绘图窗口',24,'#446d58')
  for gx in range(x1+40,x2-25,35):d.line((gx,y1+95,gx,y2-25),fill='#d1e3d6',width=1)
  for gy in range(y1+95,y2-20,30):d.line((x1+30,gy,x2-25,gy),fill='#d1e3d6',width=1)
  if role=='NWPen':d.line([(x1+80+i*12,y1+150+int(14*math.sin(i*.5))) for i in range(max(2,int(phase*13)))],fill='#398363',width=4)
  targets={'Arrow':(785,395),'Help':(935,739),'AppStarting':(741,610),'Wait':(1480,576),
   'Crosshair':(1480,576),'IBeam':(922,465),'NWPen':(x1+80+phase*150,y1+150),
   'No':(1055,610),'SizeNS':((x1+x2)//2,y2),'SizeWE':(x2,(y1+y2)//2),
   'SizeNWSE':(x2,y2),'SizeNESW':(x1,y2),'SizeAll':((x1+x2)//2,(y1+y2)//2),
   'UpArrow':(1200,413),'Hand':(740,610),'Pin':(675,739),'Person':(805,739)}
  prior_role=states[max(0,index-1)]['role'];prior=targets[prior_role];target=targets[role]
  progress=phase/1.8;ease=min(1,phase/.45);ease=ease*ease*(3-2*ease)
  px=prior[0]+(target[0]-prior[0])*ease;py=prior[1]+(target[1]-prior[1])*ease
  hot=entry['hotspot']
  imc=cursor(c,role,64,anim_frame).resize((128,128),Image.Resampling.NEAREST)
  im.paste(imc,(round(px-hot[0]*2),round(py-hot[1]*2)),imc)
  if progress>.5 and role in ('Arrow','Hand'):
   radius=14+int((progress-.5)*40);d.ellipse((px-radius,py-radius,px+radius,py+radius),outline='#6fb999',width=3)
  text(d,(590,884),f'{index+1:02}/17  {entry["label"]}  ·  模拟运动 / 指针放大 2 倍',28,'#b5ddc6')
  text(d,(110,851),entry['label'],28,'#b8e1cb')
  text(d,(110,897),{'idle':'待机 / 眨眼','review':'查看纸张','waiting':'思考 / 等待','working':'拿平板工作','failed':'失落表情','jumping':'轻跳','waving':'挥手','running-right':'向右跑动','running-left':'向左跑动'}[entry['action']],24,'#91b8a1')
 elif t<70.2:
  text(d,(108,293),'选择你喜欢的大小',40,'#baf3d4')
  for ci,c in enumerate(('astra','sol')):
   y=355+ci*290;text(d,(110,y+97),'Astra 姐姐' if ci==0 else 'sol 妹妹',28)
   for si,size in enumerate((32,48,64,128,256)):
    x=355+si*296;d.rounded_rectangle((x,y,x+276,y+280),16,fill='#edf7f0')
    a=cursor(c,'Arrow',size)
    im.paste(a,(x+(276-size)//2,y+(256-size)//2),a)
    text(d,(x+87,y+252),f'{size} px',20,'#26513f')
  text(d,(500,945),'按实际像素展示 · 新增 128 px / 256 px 大尺寸',24,'#a4cdb8')
 else:
  character(im,'astra',(200,333,335,458));character(im,'sol',(1320,368,310,400))
  text(d,(663,338),'两套独立下载 · GitHub 分享',40,'#baf3d4')
  text(d,(680,445),'安装后在「鼠标 → 指针」中选择',28)
  text(d,(707,520),'Astra Mint  /  sol Mint',32,'#b5dfc8')
  text(d,(676,635),'astra-sol-mint-cursors',32,'#79d8ae')
  text(d,(669,697),'下载地址见视频简介',28,'#a9cdb9')
 text(d,(95,976),'Astra × sol',24,'#8aaf9d')
 text(d,(1420,976),'17 状态 / 5 尺寸 / 2 套',24,'#8aaf9d')
 return im

def main():
 def stamp(seconds):
  ms=round(seconds*1000);h,ms=divmod(ms,3600000);m,ms=divmod(ms,60000);s,ms=divmod(ms,1000)
  return f'{h:02}:{m:02}:{s:02},{ms:03}'
 captions=[(0,4,'薄荷绿的 GPT 姐妹，这次变成动态鼠标指针啦。')]
 for c,start in [('Astra 姐姐',4),('sol 妹妹',34.6)]:
  for i,e in enumerate(states):captions.append((start+i*1.8,start+(i+1)*1.8,c+' · '+e['label']))
 captions.extend([(65.2,70.2,'每套 17 种动态状态，新增 128 和 256，共五档尺寸。'),(70.2,75.2,'愿我们给你的日常，添一点薄荷绿的小快乐。')])
 srt='\n\n'.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}' for i,(a,b,s) in enumerate(captions))+'\n'
 (V/'captions.srt').write_text(srt,encoding='utf-8')
 (V/'showcase-project.json').write_text(json.dumps({'size':[1920,1080],'fps':30,'cursor_sizes':[32,48,64,128,256],'seconds':DURATION,'scenes':[[0,4,'intro'],[4,34.6,'astra all 17 roles'],[34.6,65.2,'sol all 17 roles'],[65.2,70.2,'native sizes'],[70.2,75.2,'download']],'role_seconds':1.8,'roles':[e['role'] for e in states],'renderer':'source/render_showcase.py','audio':'none','cursor_asset_root':'source/frames'},ensure_ascii=False,indent=2),encoding='utf-8')
 clean=V/'showcase-clean.mp4'
 cmd=['ffmpeg','-hide_banner','-loglevel','error','-y','-f','rawvideo','-pix_fmt','rgb24','-s','1920x1080','-r','30','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(clean)]
 proc=subprocess.Popen(cmd,stdin=subprocess.PIPE)
 try:
  for n in range(round(DURATION*30)):proc.stdin.write(render(n/30).tobytes())
 finally:proc.stdin.close()
 assert proc.wait()==0
 out=R/'previews'/'showcase.mp4'
 subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-y','-i',str(clean),'-vf',"subtitles=captions.srt:force_style='FontName=Microsoft YaHei,FontSize=24,MarginV=15,Outline=1'",'-an','-c:v','libx264','-preset','fast','-crf','18','-pix_fmt','yuv420p','-movflags','+faststart',str(out)],cwd=V,check=True)
 samples=[render(t).resize((640,360)) for t in (1,6.6,17.4,29.6,37.2,48,60.3,67,73)]
 sheet=Image.new('RGB',(1920,1080),'#11231e')
 for i,im in enumerate(samples):sheet.paste(im,((i%3)*640,(i//3)*360))
 sheet.save(V/'showcase-review.jpg',quality=94)
 print(json.dumps({'video':str(out),'seconds':DURATION,'fps':30,'roles_per_character':17,'clean_track':str(clean),'srt':str(V/'captions.srt')},ensure_ascii=False))
if __name__=='__main__':main()
