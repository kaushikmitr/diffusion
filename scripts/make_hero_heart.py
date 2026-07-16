import numpy as np, matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from style_ck import strip

OUT = "/home/claude/assets"
M = np.load('/tmp/heart_means.npy'); K = len(M)
S0, MU, SIG, TF = 0.075, np.array([0.,0.]), 1.35, 4.0
NP, NS, XR = 3000, 200, 4.2          # 1500 -> 3000 points (doubled)

# palette: white bg, black text, red points
BG   = "#FFFFFF"
INK  = "#111111"
RED  = "#E23B3B"       # DDPM (left)
BLUE = "#2C6FE0"       # DDIM (right)

def score(P, t):
    s2 = S0**2 + SIG**2*t; c = M + MU*t
    d = P[:,None,:] - c[None,:,:]
    q = -(d**2).sum(-1)/(2*s2); q -= q.max(1, keepdims=True)
    w = np.exp(q); w /= w.sum(1, keepdims=True)
    return -(w[:,:,None]*d/s2).sum(1)

def sample_pT(r):
    comp = r.integers(0, K, size=NP)
    return M[comp] + MU*TF + np.sqrt(S0**2+SIG**2*TF)*r.standard_normal((NP,2))

def trajectory(stochastic, seed):
    r = np.random.default_rng(seed); P = sample_pT(r); dt=(TF-0.012)/NS
    T = np.empty((NS+1, NP, 2)); T[0]=P
    for s in range(NS):
        t = TF - s*dt; sc = score(P,t)
        if stochastic: P = P + (-MU+SIG**2*sc)*dt + SIG*np.sqrt(dt)*r.standard_normal((NP,2))
        else:          P = P + (-MU+0.5*SIG**2*sc)*dt
        T[s+1]=P
    return T

SEED = 7
Tp = trajectory(True, SEED)
To = trajectory(False, SEED)

fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
fig.patch.set_facecolor(BG)
gs = fig.add_gridspec(1, 2, left=0.02, right=0.98, top=0.90, bottom=0.06, wspace=0.04)
axs = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
# no heading; description bigger (13 -> 19)
fig.text(0.5, 0.945, "the same noise, walked two ways, arrives at the same heart",
         fontsize=19, color=INK, ha="center", style="italic")
titles = [("DDPM · stochastic", RED), ("DDIM · deterministic", BLUE)]

def draw(step):
    for ax,(ttl,col),T in zip(axs, titles, (Tp,To)):
        ax.cla(); ax.set_facecolor(BG)
        ax.set_xlim(-XR,XR); ax.set_ylim(-XR*0.60,XR*0.66); ax.set_aspect("equal"); strip(ax)
        tail = T[max(0,step-7):step+1]
        if len(tail)>1:
            ax.plot(tail[:,::5,0], tail[:,::5,1], color=col, lw=0.4, alpha=0.07)
        prog = step/NS
        ax.scatter(T[step,:,0], T[step,:,1], s=13, c=col,          # s 7 -> 13 (bigger points)
                   alpha=0.45+0.5*prog, linewidths=0)
        ax.set_title(ttl, fontsize=15, color=INK, loc="center", pad=4)

writer = FFMpegWriter(fps=30, bitrate=6000)
with writer.saving(fig, f"{OUT}/hero_heart.mp4", dpi=150):
    for step in range(NS+1):                 # noise -> heart
        draw(step); writer.grab_frame()
    for _ in range(60): writer.grab_frame()  # hold the finished heart
    draw(NS); fig.savefig(f"{OUT}/hero_heart_final.png")
print("hero done")
