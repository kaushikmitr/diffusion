# From Pollen to Pixels

**A physics-first story of diffusion models — and the live, reproducible numerics behind every figure.**

This repo accompanies the essay *[From Pollen to Pixels](article/pollen_to_pixels.md)*, which traces a single mathematical worldline from Einstein's 1905 account of Brownian motion, through the Feynman–Kac bridge between random paths and deterministic PDEs, to modern diffusion models (DDPM / DDIM and the probability-flow ODE).

The one claim the essay insists on: **every animation is a numerical integration of the equation printed next to it — not an artist's impression.** The code here is what backs that claim. With the toy datasets used throughout, the score is available in closed form, so the sampling movies run *without any neural network* — pure Einstein-grains-in-reverse.

---

## The story in three acts

| Act | Year | Idea | Figure |
| --- | ---- | ---- | ------ |
| **I** | 1905 | Einstein: randomness at the particle level is determinism at the density level (heat equation). | [`animations/act1_einstein_brownian.mp4`](animations/act1_einstein_brownian.mp4) |
| **II** | 1947 | Feynman–Kac: the dictionary between the SDE (path) view and the Fokker–Planck (density) view. | [`animations/act2_feynman_kac_bridge.mp4`](animations/act2_feynman_kac_bridge.mp4) |
| **III** | 2015–2021 | Diffusion models: run the forward process backward — DDPM on the stochastic side, DDIM on the deterministic side. | [`animations/act3_ddpm_vs_ddim.mp4`](animations/act3_ddpm_vs_ddim.mp4) |
| **Hero** | — | The same reverse process, ~1100 exact Gaussians, drawing a heart. | [`animations/hero_heart.mp4`](animations/hero_heart.mp4) |

Read it as [Markdown](article/pollen_to_pixels.md) or open the self-contained [interactive HTML version](article/pollen_to_pixels.html) in a browser.

---

## Repository layout

```
article/            The essay — Markdown source + standalone interactive HTML
animations/         Rendered .mp4 animations and their final-frame .png stills
equations/          Typeset equation cards used as figures in the article
worldline/          The opening "worldline" plate (1905–2021)
score_training/     Standalone demo: learn a score from samples, compare to closed form
scripts/            Generators for every animation, equation, and static figure
```

## Scripts

Everything visual is generated from code in [`scripts/`](scripts/):

| Script | Produces |
| ------ | -------- |
| [`make_vid1.py`](scripts/make_vid1.py) | Act I — 400 Brownian particles vs. the analytic heat kernel |
| [`make_vid2.py`](scripts/make_vid2.py) | Act II — drifted Brownian motion: paths vs. analytic Fokker–Planck density |
| [`make_vid3.py`](scripts/make_vid3.py) | Act III — DDPM (reverse SDE) vs. DDIM (probability-flow ODE) on a Gaussian mixture |
| [`make_hero_heart.py`](scripts/make_hero_heart.py) | Hero — reverse diffusion onto a heart-shaped distribution |
| [`make_equations.py`](scripts/make_equations.py) | Typeset equation cards |
| [`make_statics.py`](scripts/make_statics.py) | Static plates (worldline, spot-the-difference, etc.) |
| [`style_ck.py`](scripts/style_ck.py) | Shared matplotlib palette and styling |

[`score_training/score_demo.py`](score_training/score_demo.py) is a separate, self-contained teaching demo: it learns the score of drifted Brownian motion from samples alone (denoising score matching) and checks the learned network against the exact closed form `s(x,t) = -(x - X0 - μt) / (σ²t)` — the `1/t` stiffness is never handed to the network; it has to emerge from data.

---

## Reproducing the figures

**Requirements**

- Python 3.9+
- `numpy`, `matplotlib`
- [`ffmpeg`](https://ffmpeg.org/) on your `PATH` (matplotlib uses it to write `.mp4`)
- `torch` — only for [`score_training/score_demo.py`](score_training/score_demo.py)

```bash
python -m pip install numpy matplotlib torch
```

**Render**

The scripts were authored to write to a fixed `OUT` directory (e.g. `/home/claude/assets`) and, for the hero animation, to read heart means from `/tmp/heart_means.npy`. Adjust the `OUT` path (and any `/tmp` inputs) near the top of a script to match your machine, then run it:

```bash
cd scripts
python make_vid1.py      # Act I
python make_vid2.py      # Act II
python make_vid3.py      # Act III
```

Each run performs the actual numerical integration described on that figure's card (scheme, step size, and particle count are all printed in the article), so results are deterministic up to the seeded RNG.

---

## Further reading

Einstein (1905) · Kac (1949) · Anderson (1982, reverse-time diffusion) · Ho, Jain & Abbeel (2020, DDPM) · Song et al. (2021, score-based generative modeling through SDEs) · Song, Meng & Ermon (2021, DDIM). Full citations at the end of the [essay](article/pollen_to_pixels.md).

---

*The neural network occupies one term of one equation. The rest is a century of physics.*
