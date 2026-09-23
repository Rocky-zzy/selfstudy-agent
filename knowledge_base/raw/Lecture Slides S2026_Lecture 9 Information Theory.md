# Lecture Slides S2026\Lecture 9 Information Theory.pdf

## page 1

Basics of Information Theory

[box: ? blob] → [box: Classification networks] → { Tree 90%
 Cat 5%
 dog 5% } ⇒ Tree
(Training a probability model)

⇒ Target: Minimizing the difference between the resulting distribution and "real distribution" ⇒ minimizing cross-entropy loss

---

1. Self Information: Consider a random variable X, with target X probability distribution p(x). The self information when X=x is defined as:

I(X) := −log p(x)

p(x) ↑ self information ↓

[graph: axes log ↗, x →; annotations: p(x)=1, I(x)=0 ; p(x)=0, I(x)=+∞ ; "< log ∈ [0,1]"]

unit of I(x): { 2 as the base of logarithm: bit
 e ·····················: nat

---

2. Entropy: Expectation of Self information.

H(X) = E_X[I(x)] = E_X[−log(p(x))] = −Σ_{x∈X} p(x) log(p(x)) discrete

note: in case p(x)=0 , 0 log 0 := 0 lim_{p→0} p log p = 0

H(X) ↑ , more information (possibility) is contain,

⇒ ① deterministic information: H(X) = 0
 ② uniform distribution: H(X) is maximal.

Example

| p(x₁) | p(x₂) | p(x₃) | Entropy |
|---|---|---|---|
| 1 | 0 | 0 | 0 |
| 1/2 | 1/4 | 1/4 | 3/2 log 2 |
| 1/3 | 1/3 | 1/3 | log 3 (max) |

## page 2

3. Joint Entropy and Conditional Entropy
Consider random variables $X$ and $Y$ with target set $\mathcal{X}$ and $\mathcal{Y}$ respectively.

① Joint Entropy: $H(X, Y) := -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y) \log(p(x, y))$

② Conditional Entropy: $H(X|Y) := -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y) \cdot \log(p(x|y))$
$= -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y) \cdot \log \frac{p(x, y)}{p(y)}$
$= -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y) \log(p(x, y)) - \left( -\sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y) \cdot \log(p(y)) \right)$
$\quad\quad\quad\quad\quad H(X, Y) \quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \sum_{x \in \mathcal{X}} p(x, y) = p(y)$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad -\sum_{y \in \mathcal{Y}} p(y) \log(p(y)) \implies H(Y)$

$H(X|Y) = \boxed{H(X, Y) - H(Y)}$

③ Mutual Information: the uncertainty of one random variable
given another random variable is fixed. $p(x, y) = p(x) \cdot p(y)$
$I(X; Y) = \sum_{x \in \mathcal{X}} \sum_{y \in \mathcal{Y}} p(x, y) \cdot \log \frac{p(x, y)}{p(x) \cdot p(y)} \quad \log \to 0$
$(X, Y \text{ are independent.}$

Another angle: $I(X; Y) = H(X) - H(X|Y)$
$= H(Y) - H(Y|X)$

4. Cross Entropy: the amount of information when using $g(x)$ to
approximate $p(x) \leftarrow \text{(real distribution)}$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \uparrow$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \text{used as approximation}$
$H(p, q) = E_p[-\log(q(x))] = -\sum_x p(x) \log(q(x))$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \uparrow \text{information contains}$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \text{in } q(x).$
$q \text{ and } p \text{ is closer, } H(p, q) \downarrow, \quad p \text{ and } q \text{ is further, } H(p, q) \uparrow$

5. Kullback-Leibler Divergence (KL-Divergence)
$KL(p, q) := H(p, q) - H(p)$
$= -\sum_x p(x) \log(q(x)) + \sum_x p(x) \log(p(x)) = \sum_x p(x) \log \frac{p(x)}{q(x)}$

Statement: $KL(p, q) \ge 0$ and $KL(q, p) = 0$ if $p(x) = q(x)$.

Proof: For $x \in (0, 1]$, one has $\log(x) \le x - 1$, $=$ holds iff $x = 1$
$- KL(p, q) = \sum_x p(x) \log \frac{q(x)}{p(x)} \le \sum_x p(x) \left( \frac{q(x)}{p(x)} - 1 \right) = \sum_x (q(x) - p(x))$

## page 3

= $\sum_x g(x) - \sum_x p(x) = 0 \quad \Rightarrow \quad -KL(p, g) \leq 0 \quad \Rightarrow \quad KL(p, g) \geq 0.$

Note: ① $KL(p, g) = \sum_x p(x) \log \frac{p(x)}{g(x)} = \sum_x p(x) \log(p(x)) - \sum_x p(x) \log(g(x)) \geq 0$
$\Rightarrow \sum_x p(x) \log(p(x)) \geq \sum_x p(x) \log(g(x))$
$\Rightarrow -\sum_x p(x) \log(g(x)) \geq -\sum_x p(x) \log(p(x))$ (Gibbs inequality)

② KL-divergence (relative entropy) characterize the information loss using distribution $g$ to approximate $p$.

③ Similar to cross divergence, $g$ and $p$ is closer, $KL(p, g)$ ({characterize "distance" between $g$ and $p$})
$\llcorner$ NOT a real distance $\begin{cases} \text{symmetric} \\ \text{triangular inequality} \end{cases}$

Exercise: a discrete distribution with three event $x_1, x_2, x_3$
real distribution: $P$:
$P(x_1) = \frac{1}{2} \quad P(x_2) = \frac{3}{10} \quad P(x_3) = \frac{1}{5}.$
A model predict a distribution $Q$
$Q(x_1) = \frac{1}{5} \quad Q(x_2) = \frac{2}{5} \quad Q(x_3) = \frac{2}{5}.$

KL-divergence $KL(P, Q) = \underline{\hspace{3cm}}$ (nat),
$KL(P, Q) = H(P, Q) - H(P)$
$H(P, Q) = -\sum_x p(x) \ln(q(x)) = -(\frac{1}{2} \ln \frac{1}{5} + \frac{3}{10} \ln \frac{2}{5} + \frac{1}{5} \ln \frac{2}{5})$
$H(P) = -\sum_x p(x) \ln(p(x)) = -(\frac{1}{2} \ln \frac{1}{2} + \frac{3}{10} \ln \frac{3}{10} + \frac{1}{5} \ln \frac{1}{5})$

6. Jensen-Shannon Divergence
$JS(p, q) := \frac{1}{2} KL(p, m) + \frac{1}{2} KL(q, m), \text{ with } m = \frac{1}{2}(p+q)$
(a symmetric quantity characterizing similarity between two distribution) $\Rightarrow$ NOT satisfying triangular inequality.

## page 4

Remark: Common drawback of KL and JS divergence
Difficult to to characterize p and q when they have
little or no intersection.

① KL Divergence: $P(x) > 0$, $q(x) = 0$ $\log \frac{p(x)}{q(x)} \to +\infty$
$KL(p, q) \to +\infty$

② JS Divergence:
$JS(p, q) = \frac{1}{2} \sum_x p(x) \log \frac{p(x)}{(p(x)+q(x))/2} + \frac{1}{2} \sum_x q(x) \log \frac{q(x)}{(p(x)+q(x))/2}$
$= \frac{1}{2} \sum_x p(x) \log 2 + \frac{1}{2} \sum_x q(x) \log 2$
$= \log 2.$

7. Wasserstein Distance

Consider distributions $g_1, g_2$, the p-th Wasserstein
distance is
$W_p(g_1, g_2) = \inf_{\gamma(x,y) \in \Gamma(g_1, g_2)} E_\gamma [ d(x,y)^p ]^{\frac{1}{p}}$

$\Rightarrow$ Fulfilling the def of distance thus more
robust during the training process