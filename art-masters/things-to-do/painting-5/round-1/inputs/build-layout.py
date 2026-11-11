# Chapter 5 layout guide (input image 1) and mask (image 4) for Painting 5. Winter, scenery only.
# Soft colour zones (as in the chapter 4 guide), the reference's own snow-laden spruce at the two edges,
# a pair of track lines for the future snowmobile, and the two agreed edge colours.
# Canvas: 729 x 312 reference px at 4 px each = 2916 x 1248 (21:9). Guide rows = the chapter's own rows.
import cv2, numpy as np
import os
P=os.path.dirname(os.path.abspath(__file__))  
S=4; W,H=729,312
bgr=lambda h: np.array([int(h[5:7],16),int(h[3:5],16),int(h[1:3],16)],np.float32)
H45,H56=bgr('#E4E3DC'),bgr('#3A4763')
ref=cv2.imread('src/ttd/reference.jpg').astype(np.float32)
Y=(np.arange(H*S,dtype=np.float32)/S)[:,None]; X=(np.arange(W*S,dtype=np.float32)/S)[None,:]
ss=lambda e0,e1,v: (lambda t: t*t*(3-2*t))(np.clip((v-e0)/(e1-e0),0,1))
def lay(cv,col,a): a=np.asarray(a,np.float32); a=a[...,None] if a.ndim==2 else a; return cv*(1-a)+col*a

cv=np.zeros((H*S,W*S,3),np.float32)+bgr('#E3E4E1')                 # pale winter sky
# 1) distant snowy ranges across the full width: a soft ridge profile, snow-lit tops, blue-grey flanks
rng=np.random.default_rng(5)
xs=np.linspace(0,W,40); prof=34+9*np.sin(xs/37)+6*np.sin(xs/13+1)+rng.normal(0,2.5,len(xs))
ridge=np.interp(X[0],xs,prof)[None,:]
cv=lay(cv,bgr('#C5CCD2'),ss(ridge-1,ridge+2,Y)*(1-ss(70,86,Y)))      # range body
cv=lay(cv,bgr('#EDE9E3'),ss(ridge-1,ridge+1,Y)*(1-ss(ridge+2,ridge+9,Y))*0.8)  # sunlit snow on the crests
cv=lay(cv,bgr('#F0E4DA'),ss(ridge-1,ridge+1,Y)*(1-ss(ridge+1,ridge+4,Y))*0.5)  # faint rose-gold on the highest snow
# a nearer range in front, a little darker, for depth
prof2=58+6*np.sin(xs/29+2)+4*np.sin(xs/11)+rng.normal(0,2,len(xs)); ridge2=np.interp(X[0],xs,prof2)[None,:]
cv=lay(cv,bgr('#A9B4BD'),ss(ridge2-1,ridge2+2,Y)*(1-ss(74,88,Y)))
cv=lay(cv,bgr('#E4E2DE'),ss(ridge2-1,ridge2+1,Y)*(1-ss(ridge2+2,ridge2+7,Y))*0.6)
# 2) forested slopes and the far shore line of snow-laden spruce
cv=lay(cv,bgr('#8E9BA3'),ss(66,80,Y)*(1-ss(96,104,Y)))
cv=lay(cv,bgr('#5E6B70'),ss(92,98,Y)*(1-ss(102,106,Y))*0.85)
# 3) the frozen lake under snow, middle and right; the open snowfield on the left
# the near shore curves from the far shore at the left down to the bottom at the right of centre:
# snowfield in the lower left, lake in the middle and right
shore=250+170*np.clip((Y-104)/140,0,1)**1.6                        # a gentle curve, steepening toward the bottom
lake=ss(shore-22,shore+22,X)
cv=lay(cv,bgr('#DCDEDC'),ss(102,106,Y)*lake)
cv=lay(cv,bgr('#E7E7E3'),ss(102,106,Y)*(1-lake))
cv=lay(cv,bgr('#D2D8DD'),ss(140,205,Y)*lake*0.7)                   # lake darkens a little toward the near shore
bank=np.exp(-((X-shore-8)/9)**2)*ss(112,140,Y)                     # faint shadow along the snowy bank
cv=lay(cv,bgr('#C3CBD2'),bank*0.3)
# soft blue drifts across the snowfield, kept low and calm
drift=0.5+0.5*np.sin(X/23+Y/9)*np.sin(X/61-Y/17)
cv=lay(cv,bgr('#CFD6DD'),ss(150,190,Y)*(1-lake)*drift*0.35)
# 4) quiet area behind the kicker, heading and paragraph: pale sky and snow only
qa=np.zeros((H*S,W*S),np.float32); cv2.rectangle(qa,(30*S,40*S),(290*S,140*S),1,-1)
qa=cv2.GaussianBlur(qa,(0,0),sigmaX=130,sigmaY=60); qa=qa/qa.max()
cv=lay(cv,bgr('#E6E6E2'),qa*np.where(Y<90,0.62,0.85))   # the ranges stay faintly visible behind the heading
# 5) evening shadow: the snowfield falls into deep blue that becomes the dusk blue of the bottom band
sh=ss(200,262,Y)
cv=lay(cv,bgr('#8D9AAE'),ss(210,236,Y)*0.85)
cv=lay(cv,bgr('#5B6886'),ss(228,252,Y))
cv=lay(cv,H56,ss(246,274,Y))
# 6) two parallel snowmobile tracks, lower left toward the lake (the snowmobile asset will ride along them)
tr=np.zeros((H*S,W*S),np.uint8)
t=np.linspace(0,1,400)
p0,p1,p2,p3=np.array([18,242]),np.array([130,214]),np.array([250,186]),np.array([420,176])
curve=((1-t)**3)[:,None]*p0+(3*(1-t)**2*t)[:,None]*p1+(3*(1-t)*t**2)[:,None]*p2+(t**3)[:,None]*p3
d=np.gradient(curve,axis=0); n=np.stack([-d[:,1],d[:,0]],1); n/=np.linalg.norm(n,axis=1)[:,None]
for off in (-1.6,1.6):
    pts=((curve+n*off)*S).astype(np.int32)
    cv2.polylines(tr,[pts],False,255,max(2,int(0.8*S)),cv2.LINE_AA)
fade=np.clip((X-300)/120,0,1); trk=cv2.GaussianBlur(tr.astype(np.float32)/255,(0,0),1.2)*(1-fade)
cv=lay(cv,bgr('#97A3B0'),trk*0.9)
# 7) the reference's own snow-laden spruce at both edges (dark trees only, x 0-55, rows 1185-1300)
ry0,ry1,rx1=1194,1290,50
piece=cv2.resize(ref[ry0:ry1,0:rx1],(rx1*S,(ry1-ry0)*S),interpolation=cv2.INTER_CUBIC)
lum=cv2.cvtColor(np.clip(piece,0,255).astype(np.uint8),cv2.COLOR_BGR2GRAY)
sil=(lum<120).astype(np.uint8); sil=cv2.morphologyEx(sil,cv2.MORPH_OPEN,np.ones((3,3),np.uint8))
al=cv2.GaussianBlur(sil.astype(np.float32),(0,0),2.0)[...,None]
fadeb=np.clip(np.arange(al.shape[0])[::-1]/(14*S),0,1)[:,None,None]; al*=fadeb   # bases sink into the shadow
fader=np.clip(np.arange(al.shape[1])[::-1]/(4*S),0,1)[None,:,None]; al*=fader      # no hard cut at the piece's inner side
al*=0.9
for side in ('L','R'):
    pc,a=(piece,al) if side=='L' else (piece[:,::-1],al[:,::-1])
    py=232-(ry1-ry0); px=0 if side=='L' else W-rx1
    reg=cv[py*S:py*S+pc.shape[0], px*S:px*S+pc.shape[1]]
    cv[py*S:py*S+pc.shape[0], px*S:px*S+pc.shape[1]]=reg*(1-a)+pc*a
# small spruce in the evening shadow, right half only (the snowmobile's space in the lower left stays open)
for (sx,base,hgt) in [(352,246,22),(371,250,16),(468,244,26),(489,249,18),(575,247,20),(640,243,28),(662,250,17)]:
    sc=hgt/(ry1-ry0); w_=max(2,int(round(rx1*sc*S))); h_=max(2,int(round((ry1-ry0)*sc*S)))
    pc_=cv2.resize(piece,(w_,h_),interpolation=cv2.INTER_AREA)*0.55+bgr('#2E3A4F')*0.45
    a_=cv2.resize(al,(w_,h_),interpolation=cv2.INTER_AREA)
    a_=a_[...,None] if a_.ndim==2 else a_
    yy_,xx_=int((base-hgt)*S),int(sx*S)
    reg=cv[yy_:yy_+h_,xx_:xx_+w_]; cv[yy_:yy_+h_,xx_:xx_+w_]=reg*(1-a_)+pc_*a_
# 8) locked bands, exact colours
cv[:12*S]=H45; cv[292*S:]=H56
for (a,b) in [(12*S,30*S)]:
    for y in range(a,b): tt=(y-a)/(b-a); tt=tt*tt*(3-2*tt); cv[y]=H45*(1-tt)+cv[y]*tt
guide=np.clip(cv,0,255).astype(np.uint8)
cv2.imwrite(P+'/ch5-image1-layout.png',guide); cv2.imwrite(P+'/ch5-image1-layout.jpg',guide,[cv2.IMWRITE_JPEG_QUALITY,95])
mask=np.full((H*S,W*S),255,np.uint8); mask[:12*S]=0; mask[292*S:]=0
cv2.imwrite(P+'/ch5-image4-mask.png',mask)
cv2.imwrite(P+'/ch5-guide-small.jpg',cv2.resize(guide,(1458,624),interpolation=cv2.INTER_AREA))
print('guide',guide.shape,'mask white %.1f%%'%(100*(mask>0).mean()))
