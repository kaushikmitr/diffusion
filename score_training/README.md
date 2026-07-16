# score_training/

A standalone teaching demo for the one piece of a diffusion model that is actually *learned*: the **score**, $\nabla_x \log p_t(x)$.

Everywhere else in this project the score is written in closed form, so the animations run without a neural network. This demo shows the other half of the story — that the same score can be **recovered from samples alone**, and that the awkward part of it emerges on its own.

## The experiment

The process is the essay's "napkin" example: drifted Brownian motion released from a single point $X_0$,

$$dX = \mu\,dt + \sigma\,dW, \qquad X_0 = -1.5,\ \mu = 0.8,\ \sigma = 0.55.$$

Its exact score is

$$s(x,t) = -\frac{x - X_0 - \mu t}{\sigma^2 t}.$$

A tiny MLP $(x, t) \mapsto \text{score}$ is trained by **denoising score matching**: noise the clean point, regress the network onto the *conditional* score, and weight the loss by $\sigma^2 t$ so the small-$t$ targets don't blow up. The network is never shown the closed form.

**The point of interest is that $1/t$.** The score gets stiff — its slope in $x$ is $-1/(\sigma^2 t)$, steepening without bound as $t \to 0$. That stiffness is never handed to the network; if it appears in the trained model, it was learned from data.

## Running

```bash
pip install numpy torch
python score_training/score_demo.py
```

Prints the training loss, then a comparison table of learned-vs-exact score across several $t$, reporting mean absolute error and the fitted slope against the exact $-1/(\sigma^2 t)$. The slope should get more negative as $t \to 0$ — the $1/t$ law emerging.

**Requirements:** `numpy`, `torch`. No GPU needed; it trains in seconds on CPU.

## Files

- [`score_demo.py`](score_demo.py) — the demo. Seeded (`torch.manual_seed(0)`), so runs are reproducible. Saves the trained weights to `score_net.pt` in the working directory.
- [`score_demo.png`](score_demo.png) — a rendered learned-vs-exact comparison.

Back to the [main README](../README.md) · the [essay](../article/pollen_to_pixels.md).
