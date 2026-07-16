import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.transforms as mt
from style_ck import *
import os

OUT = "/home/claude/assets"; os.makedirs(OUT, exist_ok=True)
INK, EDGE, AMBER_DARK = "#1B2437", "#0B2545", "#B8770A"


def eq_card_light(fname, eq, size=38):
    """Single-color equation in a white rounded box, tight-cropped."""
    fig = plt.figure(figsize=(12, 2.6), dpi=100)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.text(0.5, 0.5, eq, ha="center", va="center", fontsize=size, color=INK,
            bbox=dict(boxstyle="round,pad=0.55", facecolor="white",
                      edgecolor=EDGE, linewidth=1.8))
    fig.savefig(f"{OUT}/{fname}", facecolor="white",
                bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


def eq_card_light_seg(fname, segments, size=32):
    """Multi-color equation (e.g. amber score term) in the same white boxed style."""
    fig = plt.figure(figsize=(12, 2.6), dpi=100)
    fig.patch.set_facecolor("white")
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_axis_off()
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    r = fig.canvas.get_renderer(); widths, arts = [], []
    for seg, col in segments:
        t = ax.text(0, -10, seg, fontsize=size, color=col, zorder=3)
        fig.canvas.draw()
        widths.append(t.get_window_extent(r).width / fig.bbox.width); arts.append(t)
    x = 0.5 - sum(widths) / 2
    for t, w in zip(arts, widths):
        t.set_position((x, 0.5)); x += w
    fig.canvas.draw()
    union = mt.Bbox.union([t.get_window_extent(r) for t in arts]).transformed(fig.transFigure.inverted())
    pad = 0.035
    ax.add_patch(FancyBboxPatch((union.x0 - pad, union.y0 - pad * 3.2),
                 union.width + 2 * pad, union.height + pad * 4.2,
                 boxstyle="round,pad=0.012,rounding_size=0.035",
                 facecolor="white", edgecolor=EDGE, linewidth=1.8,
                 transform=ax.transAxes, zorder=1))
    fig.savefig(f"{OUT}/{fname}", facecolor="white",
                bbox_inches="tight", pad_inches=0.22)
    plt.close(fig)


SCORE = r"$\nabla \log p_t(X)$"

eq_card_light("eq1_einstein.png",
    r"$\langle X_t^2 \rangle \;=\; 2Dt \qquad\qquad \frac{\partial p}{\partial t} \;=\; D\,\frac{\partial^2 p}{\partial x^2}$")

eq_card_light("eq2_sde.png",
    r"$dX \,=\, \mu(X, t)\, dt \;+\; \sigma(t)\, dW$", size=34)

eq_card_light("eq2c_analytic_density.png",
    r"$p_t(x) \;=\; \mathcal{N}\!\left(x;\; X_0 + \mu t,\; \sigma^2 t\right)$",
    size=36)

eq_card_light("eq2b_fokker_planck.png",
    r"$\dfrac{\partial p}{\partial t} \;=\; -\,\mu\,\dfrac{\partial p}{\partial x} \;+\; \dfrac{1}{2}\,\sigma^2\,\dfrac{\partial^2 p}{\partial x^2}, \qquad p(x,0) = \delta(x - X_0)$",
    size=28)

eq_card_light("eq3b_backward_kolmogorov.png",
    r"$\dfrac{\partial u}{\partial t} \;=\; -\,\mu\,\dfrac{\partial u}{\partial x} \;-\; \dfrac{1}{2}\,\sigma^2\,\dfrac{\partial^2 u}{\partial x^2}, \qquad u(x,T) = f(x)$",
    size=28)

eq_card_light("eq3_feynman_kac.png",
    r"$u(x,t) \,=\, \mathbb{E}\left[\, f(X_T) \;\mid\; X_t = x \,\right]$", size=32)

eq_card_light("eq3c_napkin_reversal.png",
    r"$dX \;=\; \left[\, -\mu \;-\; \dfrac{X - X_0 - \mu t}{t} \,\right] d\tau \;+\; \sigma\, d\bar{W}_{\!\tau}$",
    size=30)

eq_card_light_seg("eq4_reverse_sde.png",
    [(r"$dX \,=\, [\, \mu(X,t) \;-\; \sigma^2(t)\,$", INK),
     (SCORE, AMBER_DARK),
     (r"$\,]\; dt \;+\; \sigma(t)\, d\bar{W}_t$", INK)], size=30)

eq_card_light_seg("eq5_prob_flow_ode.png",
    [(r"$dX \,=\, [\, \mu(X,t) \;-\; \frac{1}{2}\, \sigma^2(t)\,$", INK),
     (SCORE, AMBER_DARK),
     (r"$\,]\; dt$", INK)], size=32)

print("all cards rendered")
