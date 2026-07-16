import numpy as np, matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from matplotlib.patches import Circle
from style_ck import *
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "animations")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(21)
MEANS = np.array([[-2.2, -1.4], [2.4, -1.0], [0.2, 2.2]])
STD = np.array([0.55, 0.5, 0.6]); W = np.array([0.35, 0.35, 0.30])
MU = np.array([0.35, 0.2]); SIG = 1.2
TF, TEND, NPART, XR, NS = 4.0, 0.1, 220, 8.0, 256

def score(P, t):
    s2 = STD**2 + SIG**2*t                       # (3,)
    c = MEANS + MU*t                             # (3,2)
    d = P[:, None, :] - c[None, :, :]            # (N,3,2)
    q = np.exp(-(d**2).sum(-1)/(2*s2)) * (W/s2)  # (N,3)
    r = q / q.sum(1, keepdims=True)
    return -(r[:, :, None] * d / s2[None, :, None]).sum(1)

comp = rng.choice(3, size=NPART, p=W)
sd = np.sqrt(STD[comp]**2 + SIG**2*TF)[:, None]
seed = MEANS[comp] + MU*TF + sd*rng.standard_normal((NPART, 2))

def integrate(stochastic):
    r2 = np.random.default_rng(99)
    P = seed.copy(); dt = (TF-TEND)/NS
    traj = np.empty((NS+1, NPART, 2)); traj[0] = P
    for s in range(NS):
        t = TF - s*dt; sc = score(P, t)
        if stochastic:
            P = P + (-MU + SIG**2*sc)*dt + SIG*np.sqrt(dt)*r2.standard_normal((NPART, 2))
        else:
            P = P + (-MU + 0.5*SIG**2*sc)*dt
        traj[s+1] = P
    return traj

Tsde = integrate(True); Tode = integrate(False)

def occupancy(P):
    d = ((P[:, None, :] - MEANS[None, :, :])**2).sum(-1)
    c = np.bincount(d.argmin(1), minlength=3)
    return " / ".join(f"{100*v/NPART:.0f}%" for v in c)

fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
gs = fig.add_gridspec(1, 2, left=0.03, right=0.97, top=0.80, bottom=0.115, wspace=0.07)
axs = [fig.add_subplot(gs[0]), fig.add_subplot(gs[1])]
fig.text(0.5, 0.945, "Act III · same noise in, same distribution out, different worlds in between",
         fontsize=16, color=CHALK, weight="bold", ha="center")
fig.text(0.5, 0.905, "220 particles, identical initial seed · the score ∇log p_t is exact (closed-form GMM); no neural net, nothing pre-rendered",
         fontsize=11.5, color=DIM, ha="center")
tlab = fig.text(0.97, 0.945, "", fontsize=13, color=CHALK, ha="right")
occ = [fig.text(0.27, 0.845, "", fontsize=11.5, color=CHALK, ha="center"),
       fig.text(0.73, 0.845, "", fontsize=11.5, color=CHALK, ha="center")]
card(fig, "forward: Plate II's process dX = μ dt + σ dW, μ=(0.35, 0.2), σ=1.2, run to T=4 · "
          "each component stays Gaussian: N(mᵢ+μt, (sᵢ²+σ²t)I), so the score is closed-form · "
          "reverse launched from the exact final-time mixture, one near-Gaussian blob · "
          "DDPM: Euler–Maruyama on the reverse SDE · DDIM: Euler on the probability-flow ODE · "
          "256 steps, t: 4→0.1 · dashed rings: 1σ and 2σ of the true mixture")

titles = [("DDPM · reverse-time SDE (stochastic)", CORAL),
          ("DDIM · probability-flow ODE (deterministic)", TEAL)]

def draw(step):
    for ax, (ttl, col), traj in zip(axs, titles, (Tsde, Tode)):
        ax.cla(); ax.set_facecolor(DEEP)
        ax.set_xlim(-XR, XR); ax.set_ylim(-XR, XR); ax.set_aspect("equal"); strip(ax)
        for m, s in zip(MEANS, STD):
            for k in (1, 2):
                ax.add_patch(Circle(m, k*s, fill=False, ec=DIM, lw=0.8, ls=(0, (4, 5)), alpha=0.6))
        sub = traj[:step+1, ::2, :]
        ax.plot(sub[:, :, 0], sub[:, :, 1], color=col, lw=0.6, alpha=0.16)
        ax.scatter(traj[step, :, 0], traj[step, :, 1], s=7, c=col, alpha=0.95, linewidths=0)
        ax.set_title(ttl, fontsize=12, color=col, loc="left", pad=6)
    tlab.set_text(f"step {step}/{NS}")

writer = FFMpegWriter(fps=30, bitrate=5000)
with writer.saving(fig, f"{OUT}/act3_ddpm_vs_ddim.mp4", dpi=150):
    for step in range(0, NS+1, 2):
        draw(step); writer.grab_frame()
    occ[0].set_text("clusters: " + occupancy(Tsde[-1]) + "   (true 35/35/30)")
    occ[1].set_text("clusters: " + occupancy(Tode[-1]) + "   (true 35/35/30)")
    draw(NS)
    fig.savefig(f"{OUT}/act3_ddpm_vs_ddim_final.png")
    for _ in range(75): writer.grab_frame()
print("vid3 done")
