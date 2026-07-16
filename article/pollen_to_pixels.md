# From Pollen to Pixels

*Einstein taught us that randomness obeys laws. Feynman and Kac built a bridge between two ways of writing those laws. Diffusion models started on one side of that bridge, and quietly walked across it.*

> Every animation referenced below is a numerical integration of the equation next to it, not an artist's impression. Schemes, step sizes, and particle counts are listed on each figure's card.

![The worldline, 1905–2021](assets/worldline.png)

**Plate 0.** One century, one worldline: Einstein's Brownian motion, Fokker and Planck's law for the density, Feynman's quantum detour, Kac's rotation back to probability, and image and video generation at the end. The shortest path to a video model ran through quantum mechanics.

---

## Act I · 1905 · Einstein: from randomness, law

In 1827 the botanist Robert Brown pointed a microscope at pollen grains suspended in water and watched them jitter for no reason anyone could name. Suspecting he was watching something alive, he swapped the sample: grains of dead pollen jittered too, and so did specks of powdered glass. Whatever drove the motion, it wasn't biology.

It took seventy-eight years and a patent clerk to explain it. Einstein's 1905 argument (published between the paper that won him the Nobel Prize and the one that introduced relativity, which tells you what kind of year he was having) is that each grain is being shoved by an unthinkably large number of water molecules. You cannot track the shoves. You will never predict where *one* grain goes. And then the twist: you don't have to. Ask a different question, "how does the *cloud* of grains evolve?" instead of "where is this grain?", and chaos snaps into clockwork. The mean-squared displacement of a grain grows linearly in time, and the density of grains obeys the heat equation:

$$\langle X_t^2 \rangle = 2Dt, \qquad\qquad \frac{\partial p}{\partial t} = D\,\frac{\partial^2 p}{\partial x^2}$$

Look at what happened there, down to the letters, because they are quietly making the point. On the left, $X_t$ is the position of one pollen grain at time $t$: a random variable, different every time you release a grain and let it wander, and the brackets average over that randomness. On the right, $x$ is not random at all: it is simply a location on the microscope slide, and $p(x,t)$ is the density of grains you would count there at time $t$. One equation per world. The left is a statement about random walkers; the right is a deterministic partial differential equation, the same one that governs how heat spreads through a metal bar, no randomness anywhere in sight. Einstein's discovery is that the two equations describe the same physical situation. Randomness at the level of the individual; complete predictability at the level of the distribution.

Don't take my word for it. The animation below is running the actual process: four hundred independent Brownian particles, released from a point, each taking a fresh random Gaussian kick at every tick of the clock. The histogram underneath is measured from those particles, live. The smooth curve on top of it is the analytic solution of the heat equation. Nobody told the particles about the curve.

🎬 `assets/act1_einstein_brownian.mp4`

**Plate I.** The falsifiable version of "from randomness emerges predictability." Watch the second pass, which follows one grain, and despair: a single trajectory is genuinely lawless. Return to the crowd and the law is sitting right there: the measured histogram hugs the closed-form PDE solution to within Monte-Carlo noise, $O(1/\sqrt{N})$, exactly as advertised.
*Card: N = 400 independent particles · D = 1 · update $X \leftarrow X + \sqrt{2D\Delta t}\,\xi$, $\xi \sim N(0,1)$, $\Delta t = 0.02$; for pure Brownian motion this step is the **exact** transition kernel, not an approximation · overlay: analytic heat kernel $p(x,t) = (4\pi Dt)^{-1/2} e^{-x^2/4Dt}$ · right panel: measured $\langle X_t^2\rangle$ vs. the line $2Dt$.*

This paper did more than explain pollen. Molecules were still controversial in 1905; respectable physicists considered atoms a bookkeeping fiction. Einstein's formula tied the jitter you can see to the size of molecules you can't, and when Jean Perrin measured it and extracted Avogadro's number, the atomic debate ended and Perrin collected a Nobel Prize. The irony deserves a moment, because the rest of this essay lives inside it. *We proved matter has structure by watching structure dissolve into noise.* A century later, the same mathematics would run the dissolution in reverse.

---

## Act II · 1947 · Feynman–Kac: the bridge gets a name

First, let's give Einstein's two viewpoints modern clothes. The particle view becomes a *stochastic differential equation*. Note the grammar: no derivatives anywhere, only differentials, small changes responding to small changes. That is forced, not stylistic. Brownian paths are so jagged they have no derivative to write down, so the honest statement is a recipe for increments: a small deliberate step, plus a Gaussian kick, at every instant:

$$dX = \mu(X, t)\,dt + \sigma(t)\,dW$$

Read it term by term. $dX$ is the small change in the particle's position over the next instant $dt$. The drift $\mu(X, t)$ is the deliberate part: the push the particle feels, which may depend on where it is and when. $dW$ is an increment of Brownian motion, the infinitesimal version of Act I's molecular kicks: a fresh Gaussian nudge at every instant, with a typical size that scales as $\sqrt{dt}$, the square-root law from Act I written for a single step. Its coefficient $\sigma(t)$ sets how hard those nudges land. Set $\mu = 0$ and $\sigma = \sqrt{2D}$ and you recover Einstein's pollen exactly. Drift plus diffusion; intention plus jitter. And the distribution view becomes the Fokker–Planck equation, derived by Adriaan Fokker and Max Planck (yes, that Planck) around 1914–1917, the heat equation's grown-up sibling:

$$\frac{\partial p}{\partial t} = -\,\mu\,\frac{\partial p}{\partial x} + \frac{1}{2}\,\sigma^2\,\frac{\partial^2 p}{\partial x^2}, \qquad p(x,0) = \delta(x - X_0)$$

No randomness anywhere: this is a deterministic machine that evolves the density $p_t(x)$ of a swarm of such particles, one term carrying it along the drift, one term spreading it out; set $\mu = 0$, $\sigma = \sqrt{2D}$ and it collapses back to Einstein's heat equation. Every SDE has a twin PDE. Two languages, one reality: you can follow the particles, or you can evolve the density, and you must get the same answer.

The animation below checks the dictionary on the humblest possible case: Brownian motion with a constant drift. This is the SDE from the top of this act, $dX = \mu\,dt + \sigma\,dW$, with $\mu$ and $\sigma$ held to constants. Left panel, the particle language: an ensemble of simulated paths, drift step plus Gaussian kick, pure gambling. Right panel, the density language: the analytic density, the exact solution of this SDE's Fokker–Planck equation,

$$p_t(x) = \mathcal{N}\!\left(x;\; X_0 + \mu t,\; \sigma^2 t\right),$$

a Gaussian whose center marches at speed $\mu$ while its width spreads as $\sigma\sqrt{t}$, drawn as a deterministic curve. The smooth curve is computed from the equation alone, with no reference to the particles; the bars are the particles alone, with no reference to the equation. They agree at every $t$.

🎬 `assets/act2_feynman_kac_bridge.mp4`

**Plate II.** The SDE ↔ PDE dictionary as a laboratory demonstration. The smooth curve is computed from the equation alone, not from the particles. That the bar chart of simulated particles matches it at every instant is the theorem. Note the choice of process is deliberately humble: this is the very SDE displayed above, constants and all. Act III will run this exact process on interesting data and then play it backward. You are looking at the forward half of a diffusion model.
*Card: Brownian motion with drift $dX = \mu\,dt + \sigma\,dW$, $\mu = 0.8$, $\sigma = 0.55$, $X_0 = -1.5$ · left: 2,000 paths, stepped by $X \leftarrow X + \mu\Delta t + \sigma\sqrt{\Delta t}\,\xi$, $\Delta t = 0.0125$ (60 drawn); for constant $\mu, \sigma$ this step is again exact · right: analytic density $N(X_0 + \mu t,\; \sigma^2 t)$, plus the live histogram of the simulated paths.*

That "must" deserves to be a theorem, and the theorem arrived from the strangest possible direction. In the 1940s at Cornell, Richard Feynman was giving seminars on his path-integral formulation of quantum mechanics: to get the amplitude for a particle going from point A to point B, sum a phase over *every possible path*, including the ridiculous ones (a detour to Mars and back counts). In the audience sat the probabilist Mark Kac. Two decades earlier, Norbert Wiener had made Brownian motion rigorous by assigning probabilities to entire wiggly paths, so that a quantity could be averaged over all Brownian paths at once; the technique is called Wiener integration, and it was Kac's home turf. Kac later wrote that he understood one thing immediately: Feynman's sum over paths, with time $t$ rotated to the imaginary axis $t \to -i\tau$, stopped being quantum mechanics and became exactly such an average over Brownian paths. Feynman had reinvented Wiener integration with an $i$ in it. Kac took the $i$ back out and got a theorem of classical probability. Here is its cleanest version, and it starts from an equation we have already seen. Take the Fokker–Planck equation from a moment ago, keep its operator exactly, but change the question. Instead of releasing a spike at the start and asking where the density flows, pin a chosen function at the *end* and ask what must have led to it:

$$\frac{\partial u}{\partial t} = -\,\mu\,\frac{\partial u}{\partial x} - \frac{1}{2}\,\sigma^2\,\frac{\partial^2 u}{\partial x^2}, \qquad u(x,T) = f(x)$$

Same operator as Fokker–Planck, opposite sign on the diffusion term, and a condition at the end rather than the start. That flipped sign is the whole difference between running time forward and backward. And the object it solves for is no longer a density but an expectation: $u$ is not how much stuff sits at $x$, but the average of a future measurement. This is a perfectly deterministic problem. The unknown $u$ is pinned at the final time: at $t = T$ it must equal a chosen function, $u(x,T) = f(x)$. The equation then asks what $u$ must have been at earlier times, and there is not a random symbol in sight. The Feynman–Kac recipe for solving it: to find $u$ at position $x$ and time $t$, release a wanderer there, let the SDE carry it to time $T$, record $f$ wherever it lands, and average over all Brownian paths:

$$u(x,t) = \mathbb{E}\big[\, f(X_T) \mid X_t = x \,\big]$$

The conditioning bar is the launch: position $x$, time $t$. And $f(X_T)$ is the measurement collected where the path ends; pick $f(y) = 1$ inside some target region and $0$ outside, and $u(x,t)$ is the probability that the wanderer finishes in the target. The randomness averages out, leaving an ordinary, non-random function of the launch point, and the theorem is that this function solves the equation above exactly. A deterministic PDE, solved by gambling.

Careful with these two functions, because they are easy to conflate: $u$ is not a density. Put the two displayed PDEs side by side. The density $p_t(x)$ is pinned at the start, a spike at the release point, and Fokker–Planck pushes it forward: released back then, how much of the swarm sits here now? The expectation $u(x,t)$ is pinned at the end, $u(x,T) = f(x)$, and its equation pulls it backward: standing here now, what will the measurement average out to at time $T$? One function carries the past forward; the other carries the future backward. Forward and reverse gears of the same dictionary.

Read the formula right to left and it says *simulate particles, average, and you have solved a PDE*. Read it left to right and it says *any average over random paths can be computed without simulating a single path: solve the PDE instead*. It is the SDE ↔ PDE dictionary, certified. (Kac's full theorem carries one more passenger: a potential $V(x)$ charged as a toll along the path, entering the average as $e^{-\int V}$, the imaginary-time shadow of Feynman's quantum phase. Same idea, more luggage.) One loose end, acknowledged and set down: the same rotation $t \to -i\tau$ also connects quantum mechanics to thermodynamics, with imaginary time playing the role of inverse temperature. That connection is deep, it deserves its own essay, and nothing in this one depends on it. (Schrödinger, incidentally, had poked at this correspondence from the other side back in 1931; his "bridge" problem is now a diffusion-model subfield of its own, but that's another essay.)

---

## Act III · 2015–2021 · Diffusion models: crossing the bridge in reverse

Here is the entire scheme of a diffusion model, in Einstein's vocabulary. Take your data (images, molecules, audio) and treat every sample as a pollen grain. Let it undergo Plate II's process, verbatim: Brownian motion with a constant drift, until, after enough time, every trace of the original structure has dissolved and the swarm is, to a very good approximation, a single featureless Gaussian blob. (Production models bend the drift into a restoring pull toward the origin, which makes the endpoint exactly $N(0, I)$ whatever the data. Nothing else in the story changes; we keep the humble version.) That's the forward process, and it is 1905 physics, verbatim. The heresy is the next question: *can you run it backwards?* Can you start from noise and un-dissolve?

Remarkably, yes, and you do not need the general theory to taste it. Take the process you can already watch, Plate II's drifted Brownian motion, and ask what law the movie obeys when played in reverse. The answer fits on a napkin:

$$dX = \Big[ -\mu \;-\; \frac{X - X_0 - \mu t}{t} \Big]\, d\tau \;+\; \sigma\, d\bar{W}_\tau$$

with $\tau$ running backward, from $T$ toward $0$. Two terms, two jobs. The first, $-\mu$, undoes the march. The second is a leash pulling each particle back toward the release point, with a stiffness that grows like $1/t$: gentle far from the start, ferocious near it, herding every reverse path onto exactly $X_0$ at exactly $t = 0$ and un-spreading everything diffusion spread. Reversing the drift undoes the march; the leash undoes the entropy. (Set $\mu = 0$ and this is the textbook Brownian bridge.) And the leash is not an ad hoc invention. Take Plate II's density, $p_t = N(X_0 + \mu t,\, \sigma^2 t)$, and compute the gradient of its logarithm: you get exactly the leash, divided by $\sigma^2$. The reversal knew about the density.

This is not special to Gaussians. In 1982 Brian Anderson proved that reversing *any* diffusion gives another diffusion, with an explicit formula. One note on notation: the literature writes the sample as a lowercase $x$ and the coefficients as $f$ and $g$. We keep our own letters instead: capital $X$ for the random wanderer, lowercase $x$ reserved for map coordinates, as Act I taught, and Act II's $\mu$ and $\sigma$, with the one restriction the theorem wants, that $\sigma$ may vary with time but not with position:

$$dX = \Big[ \mu(X,t) - \sigma^2(t)\, \nabla \log p_t(X) \Big]\,dt + \sigma(t)\, d\bar{W}_t$$

This is the reverse-time SDE, and everything in it is known from the forward process you chose, except the term in the middle. That term is a field: a quantity defined at every point of space, like wind on a weather map, which the equation reads off wherever the wanderer currently stands. The field is $\nabla_x \log p_t(x)$, the *score*: the uphill direction on the log of $p_t$. And $p_t$ is an old friend, not a new character: Act II's forward density, the snapshot of the dissolving swarm at time $t$. There is one such field per moment of the dissolution, and each is the general form of the napkin's leash: it points from wherever you are toward wherever the data is.

If you had the score, you could reverse entropy on demand. You don't: for real data $p_t$ is unknowable. This is the single point in the whole story where deep learning enters: train a neural network $s_\theta(x,t) \approx \nabla_x \log p_t(x)$. One learned function. Everything else, the forward SDE, the reversal formula, the sampling procedure, is Einstein and Anderson.

DDPM, the 2020 model that ignited the field, lives entirely on the particle side of the SDE ↔ PDE dictionary. Sampling is a stochastic simulation: a thousand small steps, each one drift-plus-fresh-noise, a genuine Brownian path wandering home to the data distribution. Run it twice from the same starting noise and you get two different images. Beautiful; also slow, and about as reproducible as an actual pollen grain.

Then Song and colleagues asked the dictionary's standing question: this reverse SDE describes a swarm of particles; what does the *density* say? Writing down the Fokker–Planck equation of the reverse process and factoring it, they found something lovely: there is a completely deterministic ODE whose flow pushes the density through *exactly the same sequence of distributions*:

$$dX = \Big[ \mu(X,t) - \tfrac{1}{2}\, \sigma^2(t)\, \nabla \log p_t(X) \Big]\,dt$$

![Spot the difference](assets/equations_spot_the_difference.png)

This is the probability-flow ODE, and the name is literal: it is the deterministic flow that carries probability. Play spot-the-difference with Anderson's equation above. The noise term is gone, and the score's coefficient dropped by half: the missing half of the score is doing precisely the work the noise used to do, herding probability mass outward in expectation. Same snapshot $p_t$ at every instant; radically different character. No dice. Given the starting point, the trajectory is fixed, and so is the image at the end of it. And DDIM, published as a clever re-derivation of DDPM's math with the stochasticity dialed to zero, turns out to be a discretization of exactly this ODE. The field's migration from DDPM to DDIM and its descendants is, on our worldline, the walk across Kac's bridge: from Einstein's language to the deterministic one.

Why walk across? Because determinism pays. A smooth trajectory is easy to follow in big steps, so 20 to 50 steps replace DDPM's thousand. Because nothing is random, the same starting noise always gives the same image. And the route can be driven in both directions: push a real image forward into its noise, nudge that noise, and come back, which is where a whole genre of image editing lives. The deterministic view is also the doorway to flow matching and consistency models, which is where the field went next.

The animation below shows all of this. Because the toy data is a mixture of three Gaussians, the score can be written down exactly: no neural network, no pre-rendered frames, nothing up the sleeves. What you are watching is the real mathematics running. And for this mixture the exact score is easy to read: three copies of the napkin's leash, one per cluster (each bump of a distribution is called a mode), blended by how plausibly each cluster explains where you currently stand. Watch the deterministic streamlines split into three families as that vote sharpens.

🎬 `assets/act3_ddpm_vs_ddim.mp4`

**Plate III.** DDPM on the left: jittery stochastic paths, every run a fresh Brownian excursion. DDIM on the right: laminar streamlines, the same initial noise landing on the same sample, every time, and both started from the *identical* 220-particle seed. At high step counts both reproduce the cluster weights of the true mixture, which is the whole claim: *the same sequence of snapshots, traveled by entirely different paths.* (Drop DDIM to 8 steps in the interactive version and watch samples cut corners and smear between clusters; few-step sampling is a discretization bargain, not magic.)
*Card: data = 3-component Gaussian mixture (weights .35/.35/.30) · forward: Plate II's process, $dX = \mu\,dt + \sigma\,dW$ with $\mu = (0.35, 0.2)$, $\sigma = 1.2$, run to $T = 4$; each component stays Gaussian, $N(m_i + \mu t,\, (s_i^2 + \sigma^2 t)\,I)$, so $p_t$ and $\nabla \log p_t$ are exact closed-form expressions · reverse launched from the exact $p_T$, one near-Gaussian blob · DDPM: Euler–Maruyama on the reverse SDE · DDIM: Euler on the probability-flow ODE · 256 steps, $t: 4 \to 0.1$ · in production models the exact score is replaced by a learned network $s_\theta(x,t)$; every other object on screen is unchanged.*

---

## Epilogue: how much of this was actually new?

Strip the story to one sentence per act. Einstein discovered that randomness, viewed at the level of distributions, is deterministic, and handed us the forward process. Feynman and Kac (with an accidental detour through quantum mechanics) certified the dictionary between the path view and the density view. Diffusion models learned the one function nature wouldn't give us, the score, and then used the dictionary in both directions: DDPM samples on Einstein's side of the bridge, DDIM on the deterministic side, and the snapshots can't tell the difference.

I find the accounting here genuinely humbling. Of everything running inside a modern image or video generator's sampler, the neural network occupies one term of one equation. The rest is a 1905 argument about pollen, a 1947 theorem born when a probabilist recognized his own subject inside a quantum lecture, and a 1982 reversal formula that waited forty years for its moment. We didn't invent a new mathematics of generation. We learned to estimate a single gradient, and a century of physics did the generating.

> The next time a diffusion model draws you a picture, remember what the machinery is: pollen grains, running backwards, across a bridge built by a physicist who was trying to do something else entirely.

---

**Further reading:** Einstein (1905), *Über die von der molekularkinetischen Theorie…* · Kac (1949), *On distributions of certain Wiener functionals* · Anderson (1982), *Reverse-time diffusion equation models* · Ho, Jain & Abbeel (2020), *Denoising Diffusion Probabilistic Models* · Song et al. (2021), *Score-Based Generative Modeling through SDEs* · Song, Meng & Ermon (2021), *Denoising Diffusion Implicit Models*.

*All animations are live numerical integrations of the stated equations; generation scripts (Python/matplotlib) and an interactive HTML version accompany this article.*
