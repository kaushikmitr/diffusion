import numpy as np, matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, FancyArrowPatch
from style_ck import *

import os
REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# This script writes to two different asset folders.
WORLDLINE_OUT = os.path.join(REPO, "worldline"); os.makedirs(WORLDLINE_OUT, exist_ok=True)
EQUATIONS_OUT = os.path.join(REPO, "equations"); os.makedirs(EQUATIONS_OUT, exist_ok=True)

# ---------------- worldline.png (white, straight line + detour, labels only) ----------------
BG, INK, SUB, RULE, CURV = "#FFFFFF", "#1B2437", "#5B6B82", "#B9C6D6", "#6E86A6"
T_TEAL, T_LAV, T_CORAL = "#2E9C82", "#7A5CD0", "#D2603A"

fig, ax = plt.subplots(figsize=(16, 9.8), dpi=100)
fig.patch.set_facecolor(BG); fig.subplots_adjust(0,0,1,1); ax.set_facecolor(BG)
ax.set_xlim(0, 680); ax.set_ylim(0, 470); strip(ax)
F = lambda y: 470 - y

YLINE = 225
xL, xR = 45, 645
ax.plot([xL, xR-16], [F(YLINE), F(YLINE)], color=CURV, lw=3.6, zorder=2, solid_capstyle="round")
ax.add_patch(FancyArrowPatch((xR-16,F(YLINE)),(xR,F(YLINE)), arrowstyle="-|>",
             mutation_scale=30, color=CURV, lw=3.6, zorder=2))

# detour loop: departs ~x255, dips, rejoins the line at Kac (x=400)
xF, xK, yBot = 328, 400, 355
loop = [(258, F(YLINE)),
        (250, F(YLINE+90)), (258, F(yBot)), (xF, F(yBot)),
        (398, F(yBot)), (xK+10, F(YLINE+90)), (xK, F(YLINE))]
ax.add_patch(PathPatch(Path(loop, [Path.MOVETO]+[Path.CURVE4]*6),
             fill=False, ec=T_LAV, lw=3.2, zorder=1))

def node(x, y, c, r=9): ax.scatter([x],[F(y)], s=r**2*3.14, c=c, zorder=5)

# mainline nodes — single label each, placed ABOVE the line, alternating none needed
# two-line labels: bold year/name on the outer line, contribution on the inner line
def alabel(x, year, who, contrib, c=INK):     # 3 lines above the line
    ax.text(x, F(YLINE)+78, year,    fontsize=14,   color=SUB, ha="center", va="bottom")
    ax.text(x, F(YLINE)+52, who,     fontsize=18,   color=c,   ha="center", weight="bold", va="bottom")
    ax.text(x, F(YLINE)+26, contrib, fontsize=14.5, color=SUB, ha="center", va="bottom")
def blabel(x, year, who, contrib, c=INK):     # 3 lines below the line
    ax.text(x, F(YLINE)-26, year,    fontsize=14,   color=SUB, ha="center", va="top")
    ax.text(x, F(YLINE)-52, who,     fontsize=18,   color=c,   ha="center", weight="bold", va="top")
    ax.text(x, F(YLINE)-78, contrib, fontsize=14.5, color=SUB, ha="center", va="top")

node(80,  YLINE, T_TEAL);  alabel(80,  "1905",      "Einstein",        "Brownian motion")
node(175, YLINE, T_TEAL);  blabel(175, "1914\u201317", "Fokker & Planck", "Fokker\u2013Planck equation")
node(xK,  YLINE, T_LAV);   alabel(xK,  "1947",      "Kac",             "Feynman\u2013Kac theorem")
node(520, YLINE, T_TEAL);  alabel(520, "1982",      "Anderson",        "reverse-time SDE")
node(620, YLINE, T_CORAL); alabel(620, "2015\u201321", "diffusion",       "DDPM \u00b7 DDIM")

# detour node (below, at loop bottom) — 3 lines
node(xF, yBot, T_LAV)
ax.text(xF, F(yBot)-18, "1942\u201348",     fontsize=14, color=SUB,   ha="center", va="top")
ax.text(xF, F(yBot)-42, "Feynman",       fontsize=18, color=T_LAV, ha="center", weight="bold", va="top")
ax.text(xF, F(yBot)-70, "path integrals", fontsize=14.5, color=SUB,  ha="center", va="top")
ax.text(325, 145, "quantum detour", fontsize=12, color=T_LAV, ha="center", va="center", style="italic", alpha=0.9)

fig.savefig(f"{WORLDLINE_OUT}/worldline.png", facecolor=BG); plt.close(fig)

# ---------------- equations.png ----------------
fig = plt.figure(figsize=(16, 9), dpi=100)
ax = fig.add_axes([0,0,1,1]); ax.set_facecolor(PLATE); strip(ax); ax.set_xlim(0,1); ax.set_ylim(0,1)

def compose(y, segments, size=27):
    """Draw math segments left-to-right with per-segment color, centered as a group."""
    r = fig.canvas.get_renderer()
    widths, arts = [], []
    for s, c in segments:
        t = ax.text(0, -10, s, fontsize=size, color=c)
        fig.canvas.draw()
        w = t.get_window_extent(r).width / fig.bbox.width
        widths.append(w); arts.append(t)
    x = 0.5 - sum(widths)/2
    for t, w in zip(arts, widths):
        t.set_position((x, y)); x += w
    return arts

fig.text(0.5, 0.90, "spot the difference", ha="center", fontsize=20, color=DIM)
fig.text(0.5, 0.775, "reverse-time SDE — where DDPM samples (Anderson, 1982)",
         ha="center", fontsize=14.5, color=CHALK)
compose(0.645, [
    (r"$dX \,=\, [\, \mu(X,t) \;-\; \sigma^2(t)\,$", CHALK),
    (r"$\nabla \log p_t(X)$", AMBER),
    (r"$\,]\; dt \;+\; \sigma(t)\, d\bar{W}_t$", CHALK)])
fig.text(0.5, 0.475, "probability-flow ODE — where DDIM samples (Song et al., 2021)",
         ha="center", fontsize=14.5, color=CHALK)
compose(0.345, [
    (r"$dX \,=\, [\, \mu(X,t) \;-\; \frac{1}{2}\, \sigma^2(t)\,$", CHALK),
    (r"$\nabla \log p_t(X)$", AMBER),
    (r"$\,]\; dt$", CHALK)])
fig.text(0.5, 0.19, "same snapshot p_t at every instant; identical destination, no dice",
         ha="center", fontsize=14.5, color=DIM)
fig.text(0.5, 0.115, "the missing half of the score does the work the noise used to do;\n"
         "the amber term is the only thing a neural network learns",
         ha="center", fontsize=12.5, color=DIM)
fig.savefig(f"{EQUATIONS_OUT}/equations_spot_the_difference.png"); plt.close(fig)
print("statics done")
