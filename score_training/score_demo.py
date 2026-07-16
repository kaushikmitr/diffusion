"""
Toy: learn the score of drifted Brownian motion released from a point X0,
using ONLY samples (denoising score matching). Then compare the learned
network against the exact closed form  s(x,t) = -(x - X0 - mu t)/(sigma^2 t).
The 1/t stiffness is never given to the network — it must emerge from data.
"""
import numpy as np, torch, torch.nn as nn
torch.manual_seed(0); np.random.seed(0)

# --- the napkin process ---
X0, MU, SIG, T = -1.5, 0.8, 0.55, 3.0
def exact_score(x, t):                       # the answer we're NOT allowed to use in training
    return -(x - X0 - MU*t) / (SIG**2 * t)

# --- tiny MLP: (x, t) -> scalar score ---
class ScoreNet(nn.Module):
    def __init__(s, h=128):
        super().__init__()
        s.net = nn.Sequential(
            nn.Linear(2, h), nn.SiLU(),
            nn.Linear(h, h), nn.SiLU(),
            nn.Linear(h, h), nn.SiLU(),
            nn.Linear(h, 1))
    def forward(s, x, t):
        return s.net(torch.stack([x, t], -1)).squeeze(-1)

net = ScoreNet(); opt = torch.optim.Adam(net.parameters(), lr=2e-3)

# --- denoising score matching training loop ---
# For each step: pick t, noise the clean point x0=X0, and regress the network
# onto the CONDITIONAL score -(x_t - x0 - mu t)/(sigma^2 t) = -eps/sqrt(sigma^2 t).
# We weight the loss by (sigma^2 t) so the 1/t-scaled target doesn't explode near t=0.
N, STEPS = 4096, 6000
tmin = 0.05
for step in range(STEPS):
    t   = torch.rand(N) * (T - tmin) + tmin        # t ~ U(tmin, T)
    eps = torch.randn(N)
    std = (SIG**2 * t).sqrt()
    x_t = X0 + MU*t + std*eps                       # noised sample (the ONLY data)
    target = -eps / std                             # conditional score = -(x_t - X0 - mu t)/(sig^2 t)
    pred = net(x_t, t)
    # variance-weighted loss (standard trick): multiply by std^2 so small-t targets don't dominate
    loss = ((pred - target)**2 * std**2).mean()
    opt.zero_grad(); loss.backward(); opt.step()
    if step % 1000 == 0:
        print(f"step {step:5d}  loss {loss.item():.4f}")

# --- evaluation: learned vs exact, across x and t ---
net.eval()
print("\n--- learned score vs exact (does the 1/t emerge?) ---")
with torch.no_grad():
    for t in [0.1, 0.3, 1.0, 2.5]:
        xs = torch.linspace(X0+MU*t-3, X0+MU*t+3, 7)
        learned = net(xs, torch.full_like(xs, t))
        exact   = torch.tensor([exact_score(x.item(), t) for x in xs])
        err = (learned - exact).abs().mean().item()
        print(f"t={t:4.2f}  mean|err|={err:.3f}   "
              f"slope learned={ (learned[-1]-learned[0])/(xs[-1]-xs[0]) :.3f}  "
              f"exact slope=-1/(sig^2 t)={-1/(SIG**2*t):.3f}")

# The key test: the score is linear in x with slope -1/(sigma^2 t).
# If the net learned the 1/t law, its slope should track -1/(sig^2 t) as t shrinks.
torch.save(net.state_dict(), "score_net.pt")
print("\nsaved. slope should get steeper (more negative) as t->0, tracking -1/(sig^2 t).")
