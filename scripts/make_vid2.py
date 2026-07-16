import numpy as np, matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from style_ck import *
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "animations")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(2)
MU, SIG, X0, T = 0.8, 0.55, -1.5, 3.0
NP, STEPS, NDRAW, BINS, XR = 2000, 240, 60, 51, 4.0
DT = T/STEPS; SQ = SIG*np.sqrt(DT)

paths = np.zeros((STEPS+1, NP)); paths[0] = X0
for s in range(1, STEPS+1):
    paths[s] = paths[s-1] + MU*DT + SQ*rng.standard_normal(NP)

edges = np.linspace(-XR, XR, BINS+1); bw = edges[1]-edges[0]
xg = np.linspace(-XR, XR, 240)
mean = lambda t: X0 + MU*t
var = lambda t: max(SIG**2*t, 1e-4)
PK = 1.35

fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
gs = fig.add_gridspec(1, 2, width_ratios=[1.8, 1], left=0.045, right=0.975,
                      top=0.84, bottom=0.11, wspace=0.10)
axp = fig.add_subplot(gs[0]); axd = fig.add_subplot(gs[1])
fig.text(0.045, 0.945, "Act II · the SDE ↔ PDE dictionary", fontsize=17, color=CHALK, weight="bold")
fig.text(0.045, 0.905, "left: random paths (SDE) · right: deterministic density (PDE) · they must agree, and do",
         fontsize=12, color=DIM)
tlab = fig.text(0.975, 0.945, "", fontsize=13, color=CHALK, ha="right")
card(fig, "Brownian motion with drift dX = μ dt + σ dW, μ=0.8, σ=0.55, X₀=−1.5 · left: 2,000 paths, X ← X + μΔt + σ√Δt·ξ (exact for constant μ, σ), Δt=0.0125 (60 drawn) · "
          "right: closed-form analytic density N(X₀ + μt, σ²t) + histogram of the simulated paths")

def draw(idx):
    t = idx*DT
    axp.cla(); axp.set_facecolor(DEEP); axp.set_xlim(0, T); axp.set_ylim(-XR, XR); strip(axp, True)
    axp.axhline(0, color=DIM, lw=0.4, alpha=0.35)
    ts = np.arange(idx+1)*DT
    for k in range(1, NDRAW):
        axp.plot(ts, paths[:idx+1, k], color=CHALK, lw=0.55, alpha=0.14)
    axp.plot(ts, paths[:idx+1, 0], color=CHALK, lw=1.4, alpha=0.95)
    axp.axvline(t, color=DIM, lw=0.9, ls=(0, (3, 4)))
    axp.set_title("SDE side: an ensemble of particle paths", fontsize=11, color=DIM, loc="left", pad=6)

    axd.cla(); axd.set_facecolor(DEEP); axd.set_xlim(0, 1.02); axd.set_ylim(-XR, XR); strip(axd, True)
    cnt, _ = np.histogram(paths[idx], bins=edges)
    dens = cnt/(NP*bw)
    axd.barh(edges[:-1], np.clip(dens/PK, 0, 1), height=bw*0.9, align="edge",
             color=TEAL, alpha=0.55, linewidth=0)
    m, v = mean(t), var(t)
    anl = np.exp(-(xg-m)**2/(2*v))/np.sqrt(2*np.pi*v)
    axd.plot(np.clip(anl/PK, 0, 1.02), xg, color=CHALK, lw=1.8)
    axd.set_title("PDE side: analytic p(x,t)", fontsize=11, color=DIM, loc="left", pad=6)
    tlab.set_text(f"t = {t:4.2f} / {T:.0f}")

writer = FFMpegWriter(fps=30, bitrate=4500)
with writer.saving(fig, f"{OUT}/act2_feynman_kac_bridge.mp4", dpi=150):
    for idx in range(0, STEPS+1):
        draw(idx); writer.grab_frame()
    fig.savefig(f"{OUT}/act2_bridge_final.png")
    for _ in range(45): writer.grab_frame()   # hold 1.5 s
print("vid2 done")
