# Chapter 4 layout guide (input image 1) and mask (image 4) for Painting 4.
# Built only from the original reference's chapter 4 artwork, flat calm fills and the two agreed edge colours.
# Canvas: 729 x 312 reference px at 4 px each = 2916 x 1248 (21:9).
import cv2, numpy as np
P='/tmp/claude-0/-home-user-Eaglesnestresort/83390a2e-e8fd-59f8-9a3b-15014c291845/scratchpad/ch4'
S=4; W,H=729,312
H34=np.array([0xE3,0xD4,0xC0],float)[::-1]   # BGR: mist at the foot of Painting A
H45=np.array([0xE4,0xE3,0xDC],float)[::-1]   # BGR: cloud
ref=cv2.imread('src/ttd/reference.jpg').astype(np.float32)

# 1) source band inside the torn edges, at 4x
y0,y1=1014,1118
src=cv2.resize(ref[y0:y1],(W*S,(y1-y0)*S),interpolation=cv2.INTER_CUBIC)
def R(x0,x1,ya,yb): return (x0*S,(ya-y0)*S,x1*S,(yb-y0)*S)

# the hiker and his outcrop, cut out before cleaning (pasted lower down later)
hx0,hx1,hy0,hy1=0,112,1034,1118
rock=src[(hy0-y0)*S:(hy1-y0)*S, hx0*S:hx1*S].copy()
# keep only the hiker and his rock: dark pixels, and never the paragraph that starts at x 72 above row 1090
lum=cv2.cvtColor(np.clip(rock,0,255).astype(np.uint8),cv2.COLOR_BGR2GRAY)
sil=(lum<105).astype(np.uint8)
sil[:(1090-hy0)*S, 70*S:]=0
n,lab,st,_=cv2.connectedComponentsWithStats(sil)
keep=np.zeros_like(sil)
for i in range(1,n):
    if st[i,cv2.CC_STAT_AREA]>400: keep[lab==i]=1
sil=cv2.morphologyEx(keep,cv2.MORPH_CLOSE,np.ones((15,15),np.uint8))
# backgrounds hold static scenery only: keep the outcrop, drop the hiker and his pole.
# rock = everything from row 1101 down, plus the summit right of x 61 from row 1088 (reference px)
ry=(np.arange(sil.shape[0])[:,None]/S)+hy0; rx=(np.arange(sil.shape[1])[None,:]/S)+hx0
sil=(sil.astype(bool)&((ry>=1101)|((ry>=1088)&(rx>=61)))).astype(np.uint8)

# 2) remove text, photographs, the trail dashes and the hiker's old place
hole=np.zeros(src.shape[:2],np.uint8)
for (a,b,c,d) in [R(0,205,1014,1118),R(203,683,1014,1118)]:
    hole[b:d,a:c]=1
hsv=cv2.cvtColor(np.clip(src,0,255).astype(np.uint8),cv2.COLOR_BGR2HSV)
gold=((hsv[...,0]>=12)&(hsv[...,0]<=28)&(hsv[...,1]>=90)&(hsv[...,2]>=110)).astype(np.uint8)
gold[:, :120*S]=0; gold[:, 260*S:]=0
hole|=cv2.dilate(gold,np.ones((9,9),np.uint8))
# fill holes row by row from the nearest clean pixels on each side, then soften the fill
out=src.copy()
for y in range(src.shape[0]):
    row=hole[y]; xs=np.where(row==0)[0]
    if len(xs)<2: continue
    for c in range(3): out[y,:,c]=np.where(row==1,np.interp(np.arange(src.shape[1]),xs,src[y,xs,c]),src[y,:,c])
soft=cv2.GaussianBlur(out,(0,0),sigmaX=40,sigmaY=26)
m=cv2.GaussianBlur(hole.astype(np.float32),(0,0),28)[...,None]
band=out*(1-m)+soft*m

# 3) canvas: mist top, the band stretched to rows 34-196, cloud below, locked colour bands
cv=np.zeros((H*S,W*S,3),np.float32)
by0,by1=34,196
cv[by0*S:by1*S]=cv2.resize(band,(W*S,(by1-by0)*S),interpolation=cv2.INTER_CUBIC)
top_row=cv[by0*S:by0*S+8].mean((0,1)); bot_row=cv[by1*S-8:by1*S].mean((0,1))
for y in range(0,by0*S):               # mist -> band top
    t=np.clip((y-12*S)/((by0-12)*S),0,1); cv[y]=H34*(1-t)+top_row*t
for y in range(by1*S,H*S):             # band bottom -> sea of cloud -> cloud colour
    t=np.clip((y-by1*S)/((292-by1)*S),0,1); t=t*t*(3-2*t); cv[y]=bot_row*(1-t)+H45*t
# the band emerges gradually from the mist (its first 30 rows blend in from the mist colour)
for i in range(30*S):
    t=i/(30*S); t=t*t*(3-2*t); y=by0*S+i
    cv[y]=cv[y]*t+(H34*(1-t*0.0) if False else cv[by0*S-1])*(1-t)
# soften the joins of the band with the mist above and the cloud below
for (a,b) in [(by0*S-40,by0*S+60),(by1*S-120,by1*S+40)]:
    seg=cv[a:b].copy(); cv[a:b]=cv2.GaussianBlur(seg,(0,0),10)*0.6+seg*0.4

# 4) quiet area behind the heading and text: the band's own pale sky, nothing more
qa=np.zeros((H*S,W*S),np.float32); cv2.rectangle(qa,(30*S,40*S),(214*S,150*S),1,-1)
qa=cv2.GaussianBlur(qa,(0,0),40)[...,None]
sky=cv[44*S:56*S, 30*S:214*S].mean((0,1))
cv=cv*(1-qa*0.85)+sky*qa*0.85

# 5) the outcrop, moved under the text; its top is an empty ledge where the hiker asset will stand
px,py=70,136   # clear of the gold trail, which runs down the margin at x 31-71
hh,hw=rock.shape[:2]
alpha=cv2.GaussianBlur(cv2.dilate(sil,np.ones((7,7),np.uint8)).astype(np.float32),(0,0),3)[...,None]
# the rock's base dissolves into the sea of cloud over its last 12 reference px
fade=np.clip((np.arange(alpha.shape[0])[::-1])/(12*S),0,1)[:,None,None]; alpha=alpha*(fade*fade*(3-2*fade))
yy,xx=py*S,px*S
reg=cv[yy:yy+hh,xx:xx+hw]
cv[yy:yy+hh,xx:xx+hw]=reg*(1-alpha)+rock*alpha

# 6) locked bands, exact colours
cv[:12*S]=H34; cv[292*S:]=H45
guide=np.clip(cv,0,255).astype(np.uint8)
cv2.imwrite(P+'/ch4-image1-layout.png',guide)
cv2.imwrite(P+'/ch4-image1-layout.jpg',guide,[cv2.IMWRITE_JPEG_QUALITY,95])
mask=np.full((H*S,W*S),255,np.uint8); mask[:12*S]=0; mask[292*S:]=0
cv2.imwrite(P+'/ch4-image4-mask.png',mask)
print('guide',guide.shape,'mask white %.1f%%'%(100*(mask>0).mean()))
