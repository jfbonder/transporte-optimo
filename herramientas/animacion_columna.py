import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from PIL import Image

W,H,DPI = 720,368,100
CYAN,MAG,RED = "#029BDF","#E2017B","#A8000C"
TINTA,GRIS,LINEA,FONDO,TUBO = "#1d1d1f","#5b5b60","#dcdce0","#ffffff","#fafaf8"
COLS=[CYAN,MAG,RED]
V=[0.56,0.40,0.305]; A=[0.26,0.34,0.40]
T0,T1,NF = 0.18, 4.35, 96
x=np.linspace(-0.01,1.01,460); td=np.linspace(0,T1,900)
sig=lambda t: np.sqrt(0.00040+0.0021*np.maximum(t,0.0))
def conc(i,t):  return A[i]*np.exp(-0.5*((x-V[i]*t)/sig(t))**2)/(sig(t)*np.sqrt(2*np.pi))
def senal(i,ts):
    s=sig(ts); return A[i]*V[i]*np.exp(-0.5*((1-V[i]*ts)/s)**2)/(s*np.sqrt(2*np.pi))
cmax=max(conc(i,T0).max() for i in range(3))
det=[senal(i,td) for i in range(3)]; tot=sum(det); ymax=tot.max()*1.15
YB,YT = 0.30,0.80
ALTO = (YT-YB)*0.88

def cuadro(k):
    t=T0+(T1-T0)*k/(NF-1)
    fig=plt.figure(figsize=(W/DPI,H/DPI),dpi=DPI); fig.patch.set_facecolor(FONDO)
    ax=fig.add_axes([0.055,0.58,0.90,0.33]); ax.set_facecolor(FONDO)
    ax.set_xlim(-0.03,1.05); ax.set_ylim(0,1); ax.axis("off")
    caja=FancyBboxPatch((0,YB),1,YT-YB,boxstyle="round,pad=0,rounding_size=0.12",
                        linewidth=1.1,edgecolor=LINEA,facecolor=TUBO)
    ax.add_patch(caja)
    for i in range(3):
        c=conc(i,t)
        if c.max()/cmax < 0.02: continue      # ya salió: no dibujar una banda plana
        y=YB+0.025+ALTO*c/cmax
        f=ax.fill_between(x,YB+0.025,np.minimum(y,YT-0.015),where=(c/cmax>0.004),
                          interpolate=True,color=COLS[i],alpha=0.72,linewidth=0)
        f.set_clip_path(caja)
    ax.plot([1.0,1.0],[YB-0.05,YT+0.05],color=GRIS,lw=1.2)
    ax.text(0,YT+0.11,"inyección",color=GRIS,fontsize=8.5,ha="left")
    ax.text(1.02,YT+0.11,"detector",color=GRIS,fontsize=8.5,ha="right")

    bx=fig.add_axes([0.055,0.13,0.90,0.38]); bx.set_facecolor(FONDO)
    bx.set_xlim(0,T1); bx.set_ylim(0,ymax)
    for s in ("top","right"): bx.spines[s].set_visible(False)
    bx.spines["left"].set_color(LINEA); bx.spines["bottom"].set_color(LINEA)
    bx.set_xticks([]); bx.set_yticks([])
    m=td<=t
    if m.sum()>1:
        bx.plot(td[m],tot[m],color=TINTA,lw=2.2)
        for i in range(3): bx.plot(td[m],det[i][m],color=COLS[i],lw=1.7,alpha=0.92)
    bx.text(0,-0.14,"tiempo de retención",color=GRIS,fontsize=8.5,ha="left",transform=bx.transAxes)
    bx.text(1,-0.14,"lo que mide el detector",color=GRIS,fontsize=8.5,ha="right",transform=bx.transAxes)
    fig.canvas.draw()
    im=np.asarray(fig.canvas.buffer_rgba())[:,:,:3].copy(); plt.close(fig); return im

ims=[Image.fromarray(cuadro(k)) for k in range(NF)]
ims[40].save("medio.png"); ims[NF-1].save("fin.png")
ims+=[ims[-1]]*10
# paleta chica: el dibujo usa pocos colores y el GIF baja mucho de tamaño
pal=ims[len(ims)//2].convert("P",palette=Image.ADAPTIVE,colors=48)
ims=[im.quantize(palette=pal,dither=Image.NONE) for im in ims]
ims[0].save("columna.gif",save_all=True,append_images=ims[1:],duration=75,loop=0,
            optimize=True,disposal=2)
print("listo",NF+10,"cuadros")
