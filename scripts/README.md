# scripts/

Generators for every figure in the essay *[From Pollen to Pixels](../article/pollen_to_pixels.md)*. Each animation and static plate is a live numerical integration of the equation it illustrates — these scripts are what produce it.

## What each script makes

| Script | Output(s) | Goes to |
| ------ | --------- | ------- |
| [`make_vid1.py`](make_vid1.py) | `act1_einstein_brownian.mp4` + final-frame `.png` — 400 Brownian particles vs. the analytic heat kernel | `../animations/` |
| [`make_vid2.py`](make_vid2.py) | `act2_feynman_kac_bridge.mp4` + `.png` — drifted Brownian motion: simulated paths vs. the analytic Fokker–Planck density | `../animations/` |
| [`make_vid3.py`](make_vid3.py) | `act3_ddpm_vs_ddim.mp4` + `.png` — DDPM (reverse SDE) vs. DDIM (probability-flow ODE) on a 3-component Gaussian mixture | `../animations/` |
| [`make_hero_heart.py`](make_hero_heart.py) | `hero_heart.mp4` + `.png` — reverse diffusion onto a heart-shaped distribution (~1100 exact Gaussians) | `../animations/` |
| [`make_equations.py`](make_equations.py) | the typeset equation cards (`eq1_einstein.png`, `eq2_sde.png`, …) | `../equations/` |
| [`make_statics.py`](make_statics.py) | `worldline.png` → `../worldline/`, `equations_spot_the_difference.png` → `../equations/` | (two folders) |
| [`style_ck.py`](style_ck.py) | shared matplotlib palette + styling helpers — imported by the others, not run directly | — |

## Running

Each script locates the repo relative to itself and writes into the correct folder automatically — no path editing needed. Run from anywhere:

```bash
python scripts/make_vid1.py
python scripts/make_equations.py
```

**Requirements:** `numpy`, `matplotlib`, and [`ffmpeg`](https://ffmpeg.org/) on your `PATH` (matplotlib uses it to write `.mp4`). The equation/static scripts need only matplotlib.

Every run performs the actual integration described on that figure's card in the article (scheme, step size, particle count), so output is deterministic up to the seeded RNG at the top of each script.

## The one extra input

[`make_hero_heart.py`](make_hero_heart.py) needs a precomputed `heart_means.npy` — an array of Gaussian centers sampled over the heart silhouette. It is **not** checked into the repo. Provide one and point the script at it:

```bash
HEART_MEANS=/path/to/heart_means.npy python scripts/make_hero_heart.py
```

It defaults to `scripts/heart_means.npy` if the env var is unset. The other five scripts are self-contained.
