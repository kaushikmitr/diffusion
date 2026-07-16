import numpy as np, matplotlib.pyplot as plt
from matplotlib.animation import FFMpegWriter
from style_ck import *
import os

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "animations")
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)
N, D, DT, TMAX, L, BINS = 400, 1.0, 0.02, 6.0, 8.0, 61
STEPS = int(TMAX/DT)  # 300
S = np.sqrt(2*D*DT)

# precompute two passes of positions (crowd pass, follow pass)
def run():
    x = np.zeros((STEPS+1, N)); y = np.zeros((STEPS+1, N))
    for s in range(1, STEPS+1):
        x[s] = x[s-1] + S*rng.standard_normal(N)
        y[s] = y[s-1] + S*rng.standard_normal(N)
    return x, y
X1, Y1 = run(); X2, Y2 = run()

fig = plt.figure(figsize=(12.8, 7.2), dpi=150)
gs = fig.add_gridspec(2, 2, width_ratios=[1.45, 1], height_ratios=[1, 1],
                      left=0.045, right=0.975, top=0.86, bottom=0.10, wspace=0.16, hspace=0.28)
axc = fig.add_subplot(gs[:, 0]); axh = fig.add_subplot(gs[0, 1]); axm = fig.add_subplot(gs[1, 1])
fig.text(0.045, 0.945, "Act I · Einstein, 1905", fontsize=17, color=CHALK, weight="bold")
fig.text(0.045, 0.905, "one grain is lawless; the crowd obeys the heat equation", fontsize=12, color=DIM)
tlab = fig.text(0.975, 0.945, "", fontsize=13, color=CHALK, ha="right")
plab = fig.text(0.975, 0.905, "", fontsize=12, color=CORAL, ha="right")
card(fig, "N = 400 independent Brownian particles · X ← X + √(2DΔt)·ξ, ξ~N(0,1); the exact transition kernel · "
          "white curve: analytic heat kernel (4πDt)^-½ e^(−x²/4Dt), computed from the equation, not from the particles")

xs_grid = np.linspace(-L, L, 240)
edges = np.linspace(-L, L, BINS+1); bw = edges[1]-edges[0]

def draw(frame, X, Y, follow):
    s = min(frame, STEPS)
    t = max(s*DT, 1e-6)
    axc.cla(); axc.set_facecolor(DEEP); axc.set_xlim(-L, L); axc.set_ylim(-L, L); strip(axc)
    axc.axhline(0, color=DIM, lw=0.4, alpha=0.3); axc.axvline(0, color=DIM, lw=0.4, alpha=0.3)
    a = 0.25 if follow else 0.85
    axc.scatter(X[s], Y[s], s=4, c=CHALK, alpha=a, linewidths=0)
    if follow:
        k0 = max(0, s-380)
        axc.plot(X[k0:s+1, 0], Y[k0:s+1, 0], color=CORAL, lw=1.0)
        axc.scatter([X[s, 0]], [Y[s, 0]], s=26, c=CORAL, zorder=5)
    axc.set_title("the ensemble" + ("  ·  one grain highlighted" if follow else ""),
                  fontsize=11, color=DIM, loc="left", pad=6)

    axh.cla(); axh.set_facecolor(DEEP); axh.set_xlim(-L, L); axh.set_ylim(0, 0.62); strip(axh, True)
    cnt, _ = np.histogram(X[s], bins=edges)
    axh.bar(edges[:-1], cnt/(N*bw), width=bw*0.92, align="edge", color=TEAL, alpha=0.6, linewidth=0)
    anl = np.exp(-xs_grid**2/(4*D*t))/np.sqrt(4*np.pi*D*t)
    axh.plot(xs_grid, np.clip(anl, 0, 0.62), color=CHALK, lw=1.8)
    axh.set_title("measured histogram of x  vs  analytic PDE solution", fontsize=11, color=DIM, loc="left", pad=6)

    axm.cla(); axm.set_facecolor(DEEP); axm.set_xlim(0, TMAX); axm.set_ylim(0, 2*D*TMAX*1.15); strip(axm, True)
    ts = np.arange(s+1)*DT
    axm.plot([0, TMAX], [0, 2*D*TMAX], color=DIM, lw=1.2, ls=(0, (4, 4)))
    axm.plot(ts, (X[:s+1]**2).mean(axis=1), color=TEAL, lw=1.8)
    axm.set_title(r"$\langle X_t^2 \rangle$ measured (teal)  vs  2Dt (dashed)", fontsize=11, color=DIM, loc="left", pad=6)
    tlab.set_text(f"t = {s*DT:4.2f} / {TMAX:.0f}")
    plab.set_text("pass 2: follow one grain" if follow else "pass 1: watch the crowd")

writer = FFMpegWriter(fps=30, bitrate=4500)
with writer.saving(fig, f"{OUT}/act1_einstein_brownian.mp4", dpi=150):
    for f in range(0, STEPS+1, 2):
        draw(f, X1, Y1, False); writer.grab_frame()
    for _ in range(20): writer.grab_frame()          # hold 0.66 s
    for f in range(0, STEPS+1, 2):
        draw(f, X2, Y2, True); writer.grab_frame()
    fig.savefig(f"{OUT}/act1_einstein_final.png")
    for _ in range(30): writer.grab_frame()          # hold 1 s
print("vid1 done")
