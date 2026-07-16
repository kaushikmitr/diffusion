import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PLATE = "#0B2545"; DEEP = "#081B33"; CHALK = "#DCE8F5"; DIM = "#8FA9C7"
TEAL = "#6FD3B8"; CORAL = "#F0997B"; AMBER = "#E8A33D"; LAV = "#B7A9F5"

plt.rcParams.update({
    "font.family": "DejaVu Sans Mono",
    "figure.facecolor": PLATE,
    "axes.facecolor": DEEP,
    "axes.edgecolor": DIM,
    "axes.labelcolor": CHALK,
    "xtick.color": DIM, "ytick.color": DIM,
    "text.color": CHALK,
    "axes.linewidth": 0.6,
    "mathtext.fontset": "dejavusans",
})

def strip(ax, keep_spines=False):
    ax.set_xticks([]); ax.set_yticks([])
    if not keep_spines:
        for s in ax.spines.values():
            s.set_visible(False)

def card(fig, text, y=0.012):
    parts = text.split(" \u00b7 ")
    lines, cur = [], ""
    for p in parts:
        cand = (cur + " \u00b7 " + p) if cur else p
        if len(cand) > 132 and cur:
            lines.append(cur); cur = p
        else:
            cur = cand
    lines.append(cur)
    for i, ln in enumerate(reversed(lines[:3])):
        fig.text(0.5, y + i*0.031, ln, ha="center", va="bottom", fontsize=10, color=DIM)
