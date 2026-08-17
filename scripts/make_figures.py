import json, os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
plt.rcParams.update({"font.family":"serif","font.serif":["DejaVu Serif"],"font.size":9,
                     "axes.grid":True,"grid.alpha":.3,"axes.edgecolor":"black","savefig.dpi":200})
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); OUT=os.path.join(ROOT,"figures","fig")
R=json.load(open(f"{ROOT}/results/results.json"))
cal=pd.DataFrame(R["cal"])
ORD=["Gaussian","Global","MSCP","CondC","Cond","ACI","Proposed"]
SHORT={"Gaussian":"Gaussian","Global":"Global","MSCP":"MSCP","CondC":"Channel",
       "Cond":"H x C static","ACI":"ACI","Proposed":"Proposed"}
GS=dict(zip(ORD,["0.80","0.68","0.56","0.44","0.32","0.20","0.0"]))

# --- A: audit bars, 7 methods ---
g=cal.groupby("method")[["marginal","worst_cell"]].mean().reindex(ORD)
f,ax=plt.subplots(figsize=(7.4,3.3))
x=np.arange(len(ORD)); w=.36
ax.bar(x-w/2,g["marginal"],w,color="0.78",edgecolor="k",label="marginal coverage")
ax.bar(x+w/2,g["worst_cell"],w,color="0.28",edgecolor="k",label="worst-cell coverage")
ax.axhline(.9,color="k",ls="--",lw=1)
for i,(a,b) in enumerate(zip(g["marginal"],g["worst_cell"])):
    ax.text(i-w/2,a+.005,f"{a:.3f}",ha="center",fontsize=6.5)
    ax.text(i+w/2,b+.005,f"{b:.3f}",ha="center",fontsize=6.5)
ax.set_xticks(x); ax.set_xticklabels([SHORT[m] for m in ORD],fontsize=8)
ax.set_ylim(.65,.98); ax.set_ylabel("coverage"); ax.legend(fontsize=8,loc="lower left")
ax.set_title("Two backbones x 4 datasets x 4 horizons, target 90%",fontsize=9)
f.tight_layout(); f.savefig(f"{OUT}_audit.png",bbox_inches="tight"); plt.close(f)

# --- B: backbone swap ---
b=cal.pivot_table(index="method",columns="backbone",values="worst_cell").reindex(ORD)
f,ax=plt.subplots(figsize=(6.6,3.2))
x=np.arange(len(ORD)); w=.36
ax.bar(x-w/2,b["DLinear"],w,color="0.72",edgecolor="k",label="DLinear backbone")
ax.bar(x+w/2,b["NLinear"],w,color="0.30",edgecolor="k",label="NLinear backbone")
ax.axhline(.9,color="k",ls="--",lw=1)
ax.set_xticks(x); ax.set_xticklabels([SHORT[m] for m in ORD],fontsize=8,rotation=15)
ax.set_ylim(.65,.95); ax.set_ylabel("worst-cell coverage"); ax.legend(fontsize=8)
ax.set_title("Model independence: the ranking is unchanged across backbones",fontsize=9)
f.tight_layout(); f.savefig(f"{OUT}_backbone.png",bbox_inches="tight"); plt.close(f)

# --- C: gate curves ---
cv=R["curves"]; h=np.arange(1,721)
f,ax=plt.subplots(1,2,figsize=(9,3.3))
for m in ORD:
    c=pd.Series(np.array(cv[m]["cov"])).rolling(25,min_periods=1,center=True).mean()
    ax[0].plot(h,c,color=GS[m],lw=1.3,label=SHORT[m])
ax[0].axhline(.9,color="k",ls="--",lw=1); ax[0].set_ylim(.80,1.0)
ax[0].set_xlabel("horizon step h"); ax[0].set_ylabel("empirical coverage")
ax[0].set_title("(a) Coverage across the horizon",fontsize=9); ax[0].legend(fontsize=6.5,ncol=2)
for m in ORD:
    ax[1].plot(h,np.array(cv[m]["width"]),color=GS[m],lw=1.3)
ax[1].set_xlabel("horizon step h"); ax[1].set_ylabel("mean interval width")
ax[1].set_title("(b) Width across the horizon",fontsize=9)
f.suptitle("S2 decision gate: ETTh1, DLinear, H = 720, target 90%",y=1.02,fontsize=10)
f.tight_layout(); f.savefig(f"{OUT}_gate.png",bbox_inches="tight"); plt.close(f)

# --- D: heatmap ---
ch=["HUFL","HULL","MUFL","MULL","LUFL","LULL","OT"]
f,ax=plt.subplots(1,2,figsize=(8.4,3.0))
for i,m in enumerate(["Global","Proposed"]):
    M=np.array(cv[m]["cell"])
    im=ax[i].imshow(M,cmap="Greys_r",vmin=.60,vmax=1.0,aspect="auto")
    ax[i].set_xticks(range(7)); ax[i].set_xticklabels(ch,fontsize=7,rotation=45)
    ax[i].set_yticks(range(M.shape[0])); ax[i].set_yticklabels([f"b{k+1}" for k in range(M.shape[0])],fontsize=7)
    ax[i].set_title(f"{SHORT[m]}  (worst {M.min():.3f})",fontsize=9); ax[i].set_xlabel("channel"); ax[i].grid(False)
    for a in range(M.shape[0]):
        for bb in range(7):
            ax[i].text(bb,a,f"{M[a,bb]:.2f}",ha="center",va="center",fontsize=6,
                       color="k" if M[a,bb]>.82 else "w")
ax[0].set_ylabel("horizon bucket")
f.colorbar(im,ax=ax,shrink=.85,label="coverage")
f.suptitle("Conditional coverage map, ETTh1 H=720, target 0.90",fontsize=10)
f.savefig(f"{OUT}_heatmap.png",bbox_inches="tight"); plt.close(f)

# --- E: ablations ---
f,ax=plt.subplots(1,2,figsize=(8.6,3.0))
ga=pd.DataFrame(R["gabl"])
ax[0].plot(ga["gamma"],ga["worst"],"o-",color="0.1")
ax[0].axhline(.9,color="k",ls="--",lw=1)
a2=ax[0].twinx(); a2.plot(ga["gamma"],ga["width"],"s--",color="0.55"); a2.set_ylabel("mean width"); a2.grid(False)
ax[0].set_xlabel(r"adaptation step size $\gamma$"); ax[0].set_ylabel("worst-cell coverage")
ax[0].set_title("(a) Adaptation step size",fontsize=9)
ka=pd.DataFrame(R["kabl"])
ax[1].plot(ka["K"],ka["worst"],"o-",color="0.1"); ax[1].axhline(.9,color="k",ls="--",lw=1)
ax[1].set_xlabel("bucket count K"); ax[1].set_ylabel("worst-cell coverage")
ax[1].set_ylim(.80,.92); ax[1].set_xticks([4,6,8,10]); ax[1].set_title("(b) Horizon bucket count",fontsize=9)
f.suptitle("Ablations, ETTh1 H = 720, DLinear",fontsize=10)
f.tight_layout(); f.savefig(f"{OUT}_abl.png",bbox_inches="tight"); plt.close(f)

# --- F: joint ---
j=pd.DataFrame(R["joint"])
f,ax=plt.subplots(1,2,figsize=(8.6,3.0))
for m,s,cc in [("Marginal","o-","0.1"),("MaxScore","s-","0.45"),("Bonferroni","^-","0.65")]:
    d=j[j.method==m].groupby("H")[["joint","width_ratio"]].mean()
    ax[0].plot(d.index,d["joint"],s,color=cc,label=m)
    ax[1].plot(d.index,d["width_ratio"],s,color=cc,label=m)
ax[0].axhline(.9,color="k",ls="--",lw=1); ax[0].set_ylabel("whole-path coverage")
ax[1].set_ylabel("width relative to marginal")
for a in ax: a.set_xlabel("forecast horizon H"); a.set_xticks([96,192,336,720]); a.legend(fontsize=8)
ax[0].set_title("(a) Joint coverage",fontsize=9); ax[1].set_title("(b) Width price",fontsize=9)
f.suptitle("Marginal versus joint coverage, mean over both backbones",fontsize=10)
f.tight_layout(); f.savefig(f"{OUT}_joint.png",bbox_inches="tight"); plt.close(f)
print("figures regenerated")


# ============================================================
# Static diagrams (architecture, use-case, class) — no data
# ============================================================
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Ellipse

def box(ax, x, y, w, h, t, fs=8, fc="white", r=.02):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.01,rounding_size={r}",
                                fc=fc, ec="black", lw=1.1))
    ax.text(x + w/2, y + h/2, t, ha="center", va="center", fontsize=fs, wrap=True)


def arrow(ax, p, q, style="-|>", ls="-"):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle=style, mutation_scale=11,
                                 lw=1.0, color="black", linestyle=ls,
                                 shrinkA=2, shrinkB=2))



# ---- Fig 10.1 use case ----
f, ax = plt.subplots(figsize=(8.2, 5.2)); ax.set_xlim(0, 10); ax.set_ylim(0, 6.6); ax.axis("off")
ax.add_patch(Rectangle((2.55, .35), 5.0, 5.8, fc="none", ec="black", lw=1.1))
ax.text(5.05, 5.9, "Calibration System", ha="center", fontsize=9, weight="bold")


def stick(ax, x, y, name):
    ax.add_patch(Ellipse((x, y + .52), .26, .3, fc="white", ec="k", lw=1.1))
    ax.plot([x, x], [y + .37, y - .05], "k", lw=1.1)
    ax.plot([x - .22, x + .22], [y + .27, y + .27], "k", lw=1.1)
    ax.plot([x - .18, x, x + .18], [y - .42, y - .05, y - .42], "k", lw=1.1)
    ax.text(x, y - .62, name, ha="center", fontsize=8)


stick(ax, 1.2, 4.3, "Researcher")
stick(ax, 1.2, 1.6, "Energy\noperator")
stick(ax, 8.9, 3.0, "Frozen\nbackbone")
uc = [(5.05, 5.25, "Train and freeze backbone"), (5.05, 4.45, "Build residual tensor"),
      (5.05, 3.65, "Calibrate per bucket x channel"), (5.05, 2.85, "Adapt online (ACI)"),
      (5.05, 2.05, "Emit prediction interval"), (5.05, 1.25, "Report coverage and width"),
      (5.05, .75, "Flag peak-demand decision")]
for x, y, t in uc:
    ax.add_patch(Ellipse((x, y), 4.2, .58, fc="white", ec="k", lw=1.0))
    ax.text(x, y, t, ha="center", va="center", fontsize=7.8)
for y in [5.25, 4.45, 3.65, 2.85]:
    ax.plot([1.45, 2.95], [4.3, y], "k", lw=.7)
for y in [2.05, .75]:
    ax.plot([1.45, 2.95], [1.6, y], "k", lw=.7)
ax.plot([1.45, 2.95], [1.6, 1.25], "k", lw=.7)
ax.plot([8.6, 7.15], [3.0, 4.45], "k", lw=.7)
ax.plot([8.6, 7.15], [3.0, 5.25], "k", lw=.7)
arrow(ax, (5.05, 3.36), (5.05, 3.14), style="-|>", ls="--")
ax.text(5.35, 3.25, "<<include>>", fontsize=6.5)
arrow(ax, (5.05, 2.56), (5.05, 2.34), style="-|>", ls="--")
ax.text(5.35, 2.45, "<<include>>", fontsize=6.5)
f.savefig(f"{OUT}_usecase.png", bbox_inches="tight"); plt.close(f)

# ---- Fig 10.2 class diagram ----
f, ax = plt.subplots(figsize=(8.6, 6.0)); ax.set_xlim(0, 10); ax.set_ylim(0, 8.6); ax.axis("off")


def cls(ax, x, y, w, name, attrs, ops, hh=.42):
    h = hh + .2 * (len(attrs) + len(ops)) + .18
    ax.add_patch(Rectangle((x, y - h), w, h, fc="white", ec="k", lw=1.1))
    ax.add_patch(Rectangle((x, y - hh), w, hh, fc="0.9", ec="k", lw=1.1))
    ax.text(x + w/2, y - hh/2, name, ha="center", va="center", fontsize=8, weight="bold")
    yy = y - hh - .16
    for a in attrs:
        ax.text(x + .08, yy, a, fontsize=6.8, va="center"); yy -= .2
    ax.plot([x, x + w], [yy + .1, yy + .1], "k", lw=1.0)
    yy -= .06
    for o in ops:
        ax.text(x + .08, yy, o, fontsize=6.8, va="center"); yy -= .2
    return h


cls(ax, .2, 8.4, 3.0, "DatasetLoader", ["- path : str", "- split : (tr,va,te)", "- scaler : mu, sd"],
    ["+ load() : array", "+ windows(H, stride)"])
cls(ax, 3.6, 8.4, 3.0, "DLinearBackbone", ["- seq_len = 336", "- kernel = 25", "- W : (2L+1, H)"],
    ["+ decompose(x)", "+ fit(train)", "+ predict(X) : Y_hat"])
cls(ax, 7.0, 8.4, 2.9, "ResidualTensor", ["- R : (n, H, C)", "- scale : (C,)"],
    ["+ score() : |r|/scale", "+ split(cal, test)"])
cls(ax, .2, 5.2, 3.1, "CalibrationLayer  <<abstract>>", ["# alpha : float"],
    ["+ fit(scores)", "+ half_width(h, c)"])
cls(ax, .2, 2.9, 2.3, "GlobalSplitCP", ["- q : float"], ["+ fit()", "+ half_width()"])
cls(ax, 2.75, 2.9, 2.3, "MSCP", ["- q : (H,)"], ["+ fit()", "+ half_width()"])
cls(ax, 5.3, 2.9, 4.6, "CondAdaptiveCP  (proposed)",
    ["- K : int = 6", "- bucket_id : (H,)", "- q : (K, C)", "- alpha_t : (K, C)", "- gamma : float"],
    ["+ fit(cal_scores)", "+ half_width(h, c)", "+ update(covered)"])
cls(ax, 5.9, 1.05, 4.0, "Evaluator", ["- target : float"],
    ["+ marginal()", "+ worst_cell()", "+ joint()", "+ width()"])
for x in [1.75, 3.9, 7.6]:
    ax.plot([x, x], [4.05, 3.55], "k", lw=.9)
ax.plot([1.75, 7.6], [3.55, 3.55], "k", lw=.9)
ax.plot([1.75, 1.75], [3.55, 3.4], "k", lw=.9)
arrow(ax, (1.75, 4.05), (1.75, 4.28), style="-|>")
arrow(ax, (1.7, 7.0), (1.7, 6.5))
arrow(ax, (5.1, 7.0), (5.1, 6.5))
arrow(ax, (8.45, 7.0), (8.45, 6.5))
arrow(ax, (7.9, 2.2), (7.9, 1.95))
ax.text(1.85, 4.15, "generalisation", fontsize=6.5)
ax.text(5.2, 6.7, "uses", fontsize=6.5)
ax.text(8.0, 2.05, "reports to", fontsize=6.5)
f.savefig(f"{OUT}_class.png", bbox_inches="tight"); plt.close(f)

print("diagrams done")

# ---- architecture (corrected spacing) ----
def arch_box(ax,x,y,w,h,t,fs=8,fc="white"):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.01,rounding_size=0.03",
                                fc=fc,ec="black",lw=1.1))
    ax.text(x+w/2,y+h/2,t,ha="center",va="center",fontsize=fs)
def arch_arrow(ax,p,q):
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle="-|>",mutation_scale=12,lw=1.1,
                                 color="black",shrinkA=1,shrinkB=1))

f,ax=plt.subplots(figsize=(8.4,7.0)); ax.set_xlim(0,10); ax.set_ylim(0,11.6); ax.axis("off")
ax.text(5,11.3,"Horizon and Channel Conditional Adaptive Conformal Calibration",
        ha="center",fontsize=10.5,weight="bold")

# bands: (bottom, height, label, shade)
bands=[(9.35,1.55,"DATA LAYER","0.94"),(7.45,1.55,"FROZEN BACKBONE LAYER  (trained once, then frozen)","0.94"),
       (5.55,1.55,"RESIDUAL LAYER","0.94"),(2.75,2.45,"CALIBRATION LAYER   <<contribution>>","0.86"),
       (0.85,1.55,"EVALUATION LAYER","0.94")]
for y,h,t,c in bands:
    ax.add_patch(Rectangle((.2,y),9.6,h,fc=c,ec="0.4",lw=.8,zorder=0))
    ax.text(.38,y+h-.22,t,fontsize=7.6,weight="bold",va="center",zorder=3)

arch_box(ax,.55,9.55,2.6,.75,"ETT h1 h2 m1 m2\n7 channels each")
arch_box(ax,3.45,9.55,2.9,.75,"Sequential split\n12 / 4 / 4 months")
arch_box(ax,6.6,9.55,2.85,.75,"Train-only scaling\ndrop_last disabled")
arch_box(ax,.55,7.65,2.9,.75,"Series decomposition\nmoving average k = 25")
arch_box(ax,3.75,7.65,2.6,.75,"DLinear map\nseasonal + trend")
arch_box(ax,6.6,7.65,2.85,.75,"Closed-form least\nsquares fit")
arch_box(ax,.55,5.75,2.9,.75,"Strided calibration\nwindows, stride = 1 day")
arch_box(ax,3.75,5.75,2.6,.75,"Residual tensor\nH x C x t")
arch_box(ax,6.6,5.75,2.85,.75,"Scale-normalised score\ns = |r| / MAD")
arch_box(ax,.55,3.85,2.55,.8,"Horizon buckets\nK log-spaced",fc="0.99")
arch_box(ax,3.35,3.85,2.3,.8,"Channel index\nc = 1 .. C",fc="0.99")
arch_box(ax,5.9,3.85,3.55,.8,"Per-cell conformal quantile\nq(k, c) at level 1 - alpha",fc="0.99")
arch_box(ax,1.5,2.9,3.1,.72,"ACI online update\nalpha(k,c) += g (alpha - err)",fc="0.99")
arch_box(ax,5.1,2.9,4.35,.72,"Interval:  y_hat  +/-  q(k,c) x scale(c)",fc="0.99")
arch_box(ax,.55,1.05,2.15,.75,"Marginal and\nworst-cell coverage")
arch_box(ax,2.95,1.05,2.15,.75,"Interval width\nWinkler score")
arch_box(ax,5.35,1.05,2.05,.75,"Joint whole-path\ncoverage")
arch_box(ax,7.65,1.05,1.8,.75,"Decision cost\n(stage S5)")

for a,b in [((5,9.55),(5,8.45)),((5,7.65),(5,6.55)),((5,5.75),(5,4.72)),
            ((3.05,3.85),(3.05,3.65)),((7.3,3.85),(7.3,3.65)),((5,2.9),(5,1.85))]:
    arch_arrow(ax,a,b)
arch_arrow(ax,(4.6,3.26),(5.1,3.26))
# feedback loop
ax.add_patch(FancyArrowPatch((1.5,3.26),(.42,3.26),arrowstyle="-",lw=1.0,color="black"))
ax.add_patch(FancyArrowPatch((.42,3.26),(.42,5.55),arrowstyle="-|>",mutation_scale=12,lw=1.0,color="black"))
ax.text(.15,4.45,"realised coverage feedback",rotation=90,fontsize=6.8,va="center")
f.savefig(f"{OUT}_arch.png",bbox_inches="tight"); print("ok")

print("arch done")
