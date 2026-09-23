# Lecture Slides S2026\Lecture 8 Probability and Distribution.pdf

## page 1

Lecture 8. Probability and Distribution
Roughly speaking: the key insight for a sequence generative model
(e.g. Large Language model) is to output the next word
(given the previous output) with the highest probability

0. Basic concepts for Probability and Random variable.

(1) Basic concepts

① Sample space $\Omega$: The set of all possible outcome the experiment.

② Event space $\mathcal{A}$: The set of all subsets of $\Omega$. The space of
potential results of the experiment. $A \in \mathcal{A}$ with $A \subseteq \Omega$

③ Probability P: $P(A)$ the probability of $A \in \mathcal{A}$, which is a number
in $[0, 1]$, measures the probability or degree of belief that an
event $A \in \mathcal{A}$ will occur.

④ Target space: denote by $T$, associated with a mapping
$X: \Omega \longrightarrow T$ that maps event to a value in $T$

⑤ Random variable: the function $X$ associated with $T$

⑥ Probability distribution: $P_X$, the law or distribution of random
variable $X$.

⑦ Probability Space $(\Omega, \mathcal{A}, P)$

(2) Discrete and Continuous probability : see section 6.2

1. Sum & product rule for probability.

Consider $\vec{x}$ and $\vec{y}$ are vectors of random variables

① $p(\vec{x}, \vec{y})$: denotes the joint distribution of $\vec{x}, \vec{y}$. (probability for
(a small neighbourhood around) the point $(\vec{x}, \vec{y})$).

## page 2

(Borel σ-algebra)

② $p(\vec{y}|\vec{x})$: condition probability of $\vec{y}$ given $\vec{x}$ (given $\vec{x}$, how possible a $\vec{y}$ can be selected)

(1) Product rule: $p(\vec{x}, \vec{y}) = P(\vec{y}|\vec{x}) \cdot p(\vec{x}) = p(\vec{x}|\vec{y}) \cdot p(\vec{y})$

(2) Sum rule (marginalization property).
$$p(\vec{x}) = \begin{cases} \sum_{\vec{y} \in Y} p(\vec{x}, \vec{y}), & \text{if } Y \text{ is a discrete set} \\ \int_Y p(\vec{x}, \vec{y}), & \text{if } Y \text{ is a continuous set} \end{cases}$$
where $Y$ stands for the states of the target space of random variable $y$.
Generally speaking, considering $\vec{x} = [x_1, \dots, x_D]^T$
$$p(x_i) = \int p(x_1, \dots, x_D) dx_{\setminus i} \quad \left( \begin{array}{l} \text{integration over all dim} \\ \text{called all except } i \\ \text{except for } x_i \end{array} \right)$$

(3) Bayes' Theorem
$$p(\vec{x}|\vec{y}) = \frac{p(\vec{y}|\vec{x}) \cdot p(\vec{x})}{p(\vec{y})}$$
$\underbrace{\text{posterior}}_{\checkmark}$ $\underbrace{\text{likelihood}}_{\text{<}}$ $\underbrace{\text{prior}}_{\text{<}}$ $\underbrace{\text{evidence}}_{\text{<}}$

① posterior: probability of $\vec{x}$ having observed $\vec{y}$
② Likelihood: The probability of $\vec{y}$ if we were to know the latent variable $\vec{x}$ (likelihood of $\vec{x}$ given $\vec{y}$ / probability of $\vec{y}$ given $\vec{x}$)
③ prior: prior knowledge of $\vec{x}$ before observing data $\vec{y}$

Note: Evidence / Marginal Likelihood.
Discrete: $p(\vec{y}) := \sum_{\vec{x} \in \mathcal{X}} p(\vec{y}|\vec{x}) \cdot p(\vec{x})$
Continuous: $p(\vec{y}) = \int_{\vec{x} \in \mathcal{X}} p(\vec{y}|\vec{x}) p(\vec{x}) d\vec{x}$
$\left. \begin{array}{l} \\ \\ \end{array} \right\} = \mathbb{E}_x [p(\vec{y}|\vec{x})]$

## page 3

Exercise: $P(x,y)$ of two discrete random variable $X, Y$

| $Y$ \ $X$ | $x_1$ | $x_2$ | $x_3$ | $x_4$ |
|---|---|---|---|---|
| $y_1$ | 0.01 | 0.02 | 0.03 | 0.2 |
| $y_2$ | 0.05 | 0.1 | 0.05 | 0.27 |
| $y_3$ | 0.1 | 0.05 | 0.03 | 0.09 |

compute conditional distribution $P(y|X=x_4)$

$$P(x_4) = P(x_4, y_1) + P(x_4, y_2) + P(x_4, y_3) = 0.2 + 0.27 + 0.09 = 0.56$$
$$= \sum_{y \in Y} P(x_4, y)$$
$$P(y_1 | X=x_4) = \frac{P(y_1, x_4)}{P(x_4)} = \frac{0.2}{0.56}$$
$$P(y_2 | X=x_4) = \frac{P(y_2, x_4)}{P(x_4)} = \frac{0.27}{0.56}$$
$$P(y_3 | X=x_4) = \frac{P(y_3, x_4)}{P(x_4)} = \frac{0.09}{0.56}$$

2. Expectation

1) Expected value:
Def: The expected value of a function: $g: \mathbb{R} \to \mathbb{R}$ of a random variable $x \sim p(x)$. is
$$E_x[g(x)] = \int_{x \in \mathcal{X}} g(x) \cdot p(x) dx \quad \text{(continuous case)}$$
or $E_x[g(x)] = \sum_{x \in \mathcal{X}} g(x) p(x)$

Note: Multivariable: $X = [x_1, \dots, x_D]^T$, the expected value (element-wise)
$$E_x[g(x)] = \begin{bmatrix} E_{x_1}[g(x_1)] \\ \vdots \\ E_{x_D}[g(x_D)] \end{bmatrix} \in \mathbb{R}^D, \text{ with } E_{x_d}: d=1, \dots, D.$$
taking the expectation w.r.t, $x_d$, i.e. $d$th element of $x$

## page 4

3. Mean.

For $\vec{X} = [X_1, \dots, X_D] \in \mathbb{R}^D$

$$E_{\vec{X}}[\vec{X}] = \begin{bmatrix} E_{X_1}(X_1) \\ \vdots \\ E_{X_D}(X_D) \end{bmatrix} \in \mathbb{R}^D, \text{ where.}$$

① $E_{X_d}(X_d) = \int_X x_d p(x_d) dx_d$, if $X$ is a continuous Random Variable.

② $E_{X_d}(X_d) = \sum_{x_i \in X} x_i p(X_d = x_i)$, if $X$ is a discrete random variable.

with $d = 1, \dots, D$

4. Linear of Expectation.

Let $f(\vec{x}) = a g(\vec{x}) + b h(\vec{x})$, for $a, b \in \mathbb{R}$, and $\vec{X} \in \mathbb{R}^D$

$E_X[f(\vec{x})] = \int_X f(\vec{x}) \cdot p(\vec{x}) d\vec{x}$

$= \int_X (a g(\vec{x}) + b h(\vec{x})) p(\vec{x}) d\vec{x}$

$= a \int_X g(\vec{x}) p(\vec{x}) d\vec{x} + b \int_X h(\vec{x}) p(\vec{x}) d\vec{x}$

$= a E_X(g(\vec{x})) + b E_X[h(\vec{x})]$

if $\vec{x} \in X$ (discrete case).

$E_X[f(\vec{x})] = a E_X[g(\vec{x})] + b E_X[h(\vec{x})]$

Mean or Expected value describes what could be the outcome of the random variable, in average. Meanwhile, Variance shows how the actual outcome deviate from the mean.

## page 5

5. Variance-

Def: The variance of random variable $X$ with states $\vec{x} \in \mathbb{R}^D$
and the mean $\vec{\mu} \in \mathbb{R}^D$ is

$$V_x[\vec{x}] := E_x[(\vec{x} - \vec{\mu})(\vec{x} - \vec{\mu})^T]$$

$$= E_x[\vec{x}\vec{x}^T - \vec{x}\vec{\mu}^T - \vec{\mu}\vec{x}^T + \vec{\mu}\vec{\mu}^T]$$

$$= E_x[\vec{x}\vec{x}^T] - E_x[\vec{x}\vec{\mu}^T] - E_x[\vec{\mu}\vec{x}^T] + E_x[\vec{\mu}\vec{\mu}^T]$$

$$= E_x[\vec{x}\vec{x}^T] - E_x[\vec{x}]\vec{\mu}^T - \vec{\mu}E_x[\vec{x}^T] + E_x[\vec{\mu}]E_x[\vec{\mu}^T]$$

$$= E_x[\vec{x}\vec{x}^T] - E_x[\vec{x}]E_x[\vec{x}^T] - E_x[\vec{x}]E_x[\vec{x}^T] + E_x[\vec{x}]E_x[\vec{x}^T]$$

$$\checkmark = \boxed{E_x[\vec{x}\vec{x}^T] - E_x[\vec{x}]E_x[\vec{x}]^T}$$

Let $Cov_x[x_i, x_j] = E_{x_i, x_j}[x_i x_j] - E_{x_i}[x_i]E_{x_j}[x_j]$

$$V_x[\vec{x}] = \begin{bmatrix} Cov[x_1, x_1] & Cov[x_1, x_2] & \cdots & Cov[x_1, x_D] \\ Cov[x_2, x_1] & Cov[x_2, x_2] & \cdots & Cov[x_2, x_D] \\ \vdots & \vdots & \ddots & \vdots \\ Cov[x_D, x_1] & Cov[x_D, x_2] & \cdots & Cov[x_D, x_D] \end{bmatrix} \implies \text{Covariance matrix}$$

Note: For a multivariate random variable, the variance describes
the relations between individual dimensions of the random variable
$\implies$ What if one would like to describe how dependent random
variables are to one another?

6. Covariance

① Def: Consider two multivariate random variable $X$ and $Y$ with
states $\vec{x} \in \mathbb{R}^D$ and $\vec{y} \in \mathbb{R}^E$, respectively, the covariance between
$X$ and $Y$ is defined as

$$Cov[\vec{x}, \vec{y}] = E[\vec{x}\vec{y}^T] - E[\vec{x}]E[\vec{y}]^T = Cov[\vec{y}, \vec{x}]^T \in \mathbb{R}^{D \times E}$$

② correlation: The correlation between two random variables $X$ and $Y$, is

$$corr[x, y] := \frac{Cov[x, y]}{\sqrt{V[x]V[y]}} \in [-1, 1] \begin{cases} > 0, \text{ positive correlation} \\ < 0, \text{ negative correlation} \end{cases}$$

## page 6

Note : Both covariance and correlation characterize how two random variables are related.

Graphical illustration -

① $y \uparrow$ 
 II | I
 ---+--- $E_x$ → x
 III| IV
 $E_y$

② $y \uparrow$
 II | I
 ---+--- $E_x$ → x
 III| IV
 $E_y$

① $E[(X-E_x)(Y-E_y)] > 0$
② $E[(X-E_x)(Y-E_y)] < 0$

Region I: $X > E_x \quad Y > E_y \quad (X - E[X])(Y - E[Y]) \ge 0$
Region II: $X < E_x, Y > E_y \quad (X - E[X])(Y - E[Y]) < 0$
Region III: $X < E_x, Y < E_y \quad (X - E_x)(Y - E_y) \ge 0$
Region IV: $X > E_x, Y < E_y, \quad (X - E_x)(Y - E_y) < 0$

7. Empirical Means and Covariances. ✓

Def: Consider a set of data $\{\vec{x}_i \in \mathbb{R}^D, i=1, \dots, N\}$

empirical mean: $\bar{\vec{x}} := \frac{1}{N} \sum_{i=1}^N \vec{x}_i \in \mathbb{R}^D$

empirical covariance: $\hat{\Sigma} := \frac{1}{N} \sum_{i=1}^N (\vec{x}_i - \bar{\vec{x}})(\vec{x}_i - \bar{\vec{x}})^T \in \mathbb{R}^{D \times D}$

$\begin{cases}
V_x[\vec{x}] = E_x[(x-\mu)(x-\mu)^T] \overset{1-D}{=} E[(x-\mu)^2] \\
1-D: V_x[x] = E_x[(x^2)] - (E_x[x])^2 \\
\qquad \qquad = \frac{1}{N} \sum_{i=1}^N x_i^2 - \left(\frac{1}{N} \sum_{i=1}^N x_i\right)^2
\end{cases}$

8. Basic Rules for Expectation and Variance

Consider Two random variable X, Y, with state $\vec{x}, \vec{y} \in \mathbb{R}^D$, Then

(1) $E[\vec{x} \pm \vec{y}] = E[\vec{x}] \pm E[\vec{y}]$.

Proof: (Discrete case): $E[X+Y] = \sum_{i,j} (\vec{x}_i + \vec{y}_j) P(X=\vec{x}_i, Y=\vec{y}_j)$
$= \sum_{i,j} \vec{x}_i P(X=\vec{x}_i, Y=\vec{y}_j) + \sum_{i,j} \vec{y}_j P(X=\vec{x}_i, Y=\vec{y}_j)$
$= \sum_i \vec{x}_i \sum_j P(X=x_i, Y=y_j) + \sum_j \vec{y}_j \sum_i P(X=x_i, Y=y_j)$
$\qquad \qquad \underline{P(X=x_i)} \qquad \qquad \qquad \underline{P(Y=y_j)}$
$= \sum_i x_i P(X=x_i) + \sum_j y_j P(Y=y_j) = \boxed{E[X]} + \boxed{E[Y]}$
$\qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \qquad \boxed{E_x[x]}$

## page 7

② $V[X+Y] = V[X] + V[Y] \pm Cov[X,Y] \pm Cov[Y,X]$

$V[X+Y] = E\left[ ((X+Y) - E[X+Y])^2 \right]$
$= E\left[ ((X-E[X]) + (Y-E[Y]))^2 \right]$
$\left( (X-E[X]) + (Y-E[Y]) \right)^2$
$= (X-E[X])^2 + 2(X-E[X])(Y-E[Y]) + (Y-E[Y])^2$
$\Rightarrow E\left[ (X-E[X])^2 \right] + 2E\left[ (X-E[X])(Y-E[Y]) \right] + E\left[ (Y-E[Y])^2 \right]$
$\quad\quad\quad V[X] \quad\quad\quad\quad\quad\quad Cov[X,Y] \quad\quad\quad\quad\quad\quad V[Y]$

$\Rightarrow$ Let $y = A\vec{x} + \vec{b} \quad, \quad \Sigma := V_X[\vec{x}] \quad, \quad \vec{b} \in \mathbb{R}^p, \text{ constant}$

(3) $E_Y[\vec{y}] = E_X[A\vec{x} + \vec{b}] = A E_X[\vec{x}] + \vec{b}$
$V_Y[\vec{y}]$
(4) $V_Y[\vec{y}] = V_X[A\vec{x} + \vec{b}] \stackrel{\text{①}}{=} V_X[A\vec{x}] \stackrel{\text{②}}{=} A V_X[\vec{x}] A^T = A \Sigma A^T$

$V_X(\vec{b}) = E[\vec{b}\vec{b}^T] - E[\vec{b}] \cdot E[\vec{b}]^T = \vec{b}\vec{b}^T - \vec{b}\vec{b}^T = \vec{0}$
$Cov(\vec{x}, \vec{b}) = E[\vec{x}\vec{b}^T] - E[\vec{x}] E[\vec{b}]^T = E[\vec{x}]\vec{b}^T - E[\vec{x}]\vec{b}^T = 0$
$\Rightarrow V_X[A\vec{x}+\vec{b}] = V_X[A\vec{x}] + V_X[\vec{b}] + Cov(\vec{x},\vec{b}) + Cov(\vec{b},\vec{x}) = V_X[A\vec{x}]$

② $V_X[A\vec{x}] = E_X[(A\vec{x})(A\vec{x})^T] - E_X[A\vec{x}] \cdot E_X[A\vec{x}]^T \quad (Def.)$
$= E_X[A\vec{x}\vec{x}^T A^T] - A E_X[\vec{x}] E_X[\vec{x}]^T A^T$
$= A E_X[\vec{x}\vec{x}^T] A^T - A E_X[\vec{x}] \cdot E_X[\vec{x}]^T A^T$
$= A \left( E_X[\vec{x}\vec{x}^T] - E_X[\vec{x}] \cdot E_X[\vec{x}]^T \right) A^T = A \Sigma A^T$
$\quad\quad\quad\quad\quad V_X[\vec{x}]$

(5) $Cov(\vec{x}, \vec{y}) = \Sigma A^T$
$\quad\quad\quad\quad\quad\quad \mu = E[\vec{x}]$
$= Cov(\vec{x}, A\vec{x}+\vec{b}) = \Sigma A^T$
$Cov(\vec{x}, A\vec{x}+\vec{b}) = E_X[\vec{x}(A\vec{x}+\vec{b})^T] - E_X[\vec{x}] E_X[A\vec{x}+\vec{b}]^T$
$= E_X[\vec{x}\vec{x}^T A^T + \vec{x}\vec{b}^T] - \vec{\mu} \cdot (A\vec{\mu}+\vec{b})^T$
$= E_X[\vec{x}\vec{x}^T]A^T + E_X[\vec{x}\vec{b}^T] - \vec{\mu}\vec{\mu}^T A^T - \vec{\mu}\vec{b}^T$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad 0$
$= E_X[\vec{x}\vec{x}^T]A^T - \vec{\mu}\vec{\mu}^T A^T = (E_X[\vec{x}\vec{x}^T] - E_X[\vec{x}] \cdot E_X[\vec{x}]^T) A^T$
$= \Sigma A^T$

9. Statistical Independence

## page 8

(1) Two random variables X, Y are statistically independent
$$\iff p(\check{x}, \check{y}) = p(\check{x}) p(\check{y}) \ \checkmark$$
★
reversely
NOT
true
$$
\begin{cases}
\Rightarrow p(\check{y} \mid \check{x}) = p(\check{y}) \ \text{①} \\
\Rightarrow p(\check{x} \mid \check{y}) = p(\check{x}) \ \text{②} \\
\Rightarrow Cov_{X,Y}(\check{x}, \check{y}) = \vec{0} \ \text{③} \Rightarrow V_{X,Y}[\check{x} + \check{y}] = V_X[\check{x}] + V_Y[\check{y}]
\end{cases}
$$

(2) Two random variables X, Y are conditionally independent
given Z $\iff p(\check{x}, \check{y} \mid \check{z}) = p(\check{x} \mid \check{z}) \cdot p(\check{y} \mid \check{z})$ for any $z \in Z$

Note: $p(\check{x}, \check{y}) = p(\check{x} \mid \check{y}) \cdot p(\check{y}) \Rightarrow p(\check{x}, \check{y} \mid \check{z}) = p(\check{x} \mid \check{y}, \check{z}) \cdot p(\check{y} \mid \check{z})$

Summary:
probability
$\begin{cases}
\text{Basic concepts} \begin{cases} \text{Sample space, Event space} \\ \text{Target Space, Probability, Distribution} \end{cases} \\
\text{Sum Rule (marginalization property)} \\
\text{Product Rule} \implies \text{Bayes' Thm} \\
\text{Expectation} \implies \text{Mean} \\
\text{Variance} \implies \text{Covariance} \implies \text{Correlation} \\
\text{Independence}
\end{cases}$
Sec. 6.1 - 6.4

(1). Gaussian Distribution.
(1) Univariate: mean $\mu$, Variance $\sigma$
probability density function:
$$p(x \mid \mu, \sigma) = \frac{1}{\sqrt{2\pi}\sigma} \exp\left(-\frac{(x-\mu)^2}{2\sigma}\right)$$
(2) Multivariate: mean $\vec{\mu}$, covariance matrix
$$\Sigma = V_x[\vec{x}] = Cov_x[\vec{x}, \vec{x}]$$

## page 9

✓ $p(\vec{x} \mid \vec{\mu}, \Sigma) = (2\pi)^{-\frac{D}{2}} \cdot \det(\Sigma)^{-\frac{1}{2}} \exp\left(-\frac{1}{2} (\vec{x}-\vec{\mu})^T \Sigma^{-1} (\vec{x}-\vec{\mu})\right)$
for $\vec{x} \in \mathbb{R}^D$ $p(\vec{x}) = \mathcal{N}(\vec{x} \mid \vec{\mu}, \Sigma)$ or $X \sim \mathcal{N}(\vec{\mu}, \Sigma)$ -

(3) Marginal and Conditionals
Let X, Y be two multivariate Gaussian variables
① Concatenate $[\vec{x}^T, \vec{y}^T]^T$ (concatenation is Gaussian).
$p(\vec{x}, \vec{y}) = \mathcal{N}\left( \begin{bmatrix} \vec{\mu}_x \\ \vec{\mu}_y \end{bmatrix}, \begin{bmatrix} \Sigma_{xx} & \Sigma_{xy} \\ \Sigma_{yx} & \Sigma_{yy} \end{bmatrix} \right)$
where $\Sigma_{xx} = \text{cov}[\vec{x},\vec{x}]$, $\Sigma_{yy} = \text{cov}[\vec{y},\vec{y}]$, $\Sigma_{xy} = \text{cov}[\vec{x},\vec{y}]$
② Conditional distribution $p(\vec{x} \mid \vec{y})$ is also Gaussian.
$p(\vec{x} \mid \vec{y}) = \mathcal{N}(\vec{\mu}_{x|y}, \Sigma_{x|y})$
where $\vec{\mu}_{x|y} = \vec{\mu}_x + \Sigma_{xy} \Sigma_{yy}^{-1} (\vec{y} - \vec{\mu}_y)$, $\Sigma_{x|y} = \Sigma_{xx} - \Sigma_{xy} \Sigma_{yy}^{-1} \Sigma_{yx}$
③ Marginal is still gaussian distribution.
$p(\vec{x}) = \int p(\vec{x}, \vec{y}) dy = \mathcal{N}(\vec{x} \mid \vec{\mu}_x, \Sigma_{xx})$
$\Rightarrow$ See Example 6.6
(4) Sum and Linear Transformation of Gaussian.
① Sum: X, Y: independent Gaussian random variables
$X \sim \mathcal{N}(\vec{\mu}_x, \Sigma_x)$ $Y \sim \mathcal{N}(\vec{\mu}_y, \Sigma_y)$
$X+Y \sim \mathcal{N}(\vec{\mu}_x + \vec{\mu}_y, \Sigma_x + \Sigma_y)$
② Linear Combination:
a) univariate: $p(ax+by) = \mathcal{N}(a\mu_x + b\mu_y, a^2\Sigma_x + b^2\Sigma_y)$
b) Multivariate: $X \sim \mathcal{N}(\vec{\mu}, \Sigma)$ $\vec{y} = A\vec{x}$

## page 10

$Y \sim \mathcal{N}(A\vec{\mu}, A\Sigma A^T)$

Application: obtaining samples from a multivariate $\mathcal{N}(\vec{\mu}, \Sigma)$
leveraging a sampler $\mathcal{N}(\vec{0}, I)$
Step 1: get a sample from $\vec{X} \sim \mathcal{N}(\vec{0}, I)$
Step 2: Compute $\vec{Y} = A\vec{X} + \vec{\mu}$, with $AA^T = \Sigma$ positive definite.
decompose $\Sigma$ using
e.g. cholesky decomposition

---

③ Mixture of two univariate Gaussian densities functions
$p_1(x) = \mathcal{N}(\mu_1, \sigma_1)$, $p_2(x) = \mathcal{N}(\mu_2, \sigma_2)$, $0 < \alpha < 1$
consider $p(x) = \alpha p_1(x) + (1-\alpha) p_2(x)$
Mean: $E[X] = \alpha \mu_1 + (1-\alpha) \mu_2$
$V[X] = [\alpha \sigma_1 + (1-\alpha) \sigma_2] + \left( [\alpha \mu_1^2 + (1-\alpha) \mu_2^2] - [\alpha \mu_1 + (1-\alpha) \mu_2]^2 \right)$

Proof: $V_x[X] = E_x[X^2] - (E_x[X])^2$
① $E_x[X] = \int_{-\infty}^{+\infty} x p(x) dx = \int_{-\infty}^{+\infty} (\alpha x p_1(x) + (1-\alpha) x p_2(x)) dx$
$= \alpha \int_{-\infty}^{+\infty} x p_1(x) dx + (1-\alpha) \int_{-\infty}^{+\infty} x p_2(x) dx = \alpha \mu_1 + (1-\alpha) \mu_2$ ①

② $E_x[X^2] = \int_{-\infty}^{+\infty} x^2 p(x) dx = \int_{-\infty}^{+\infty} (\alpha x^2 p_1(x) + (1-\alpha) x^2 p_2(x)) dx$
$= \alpha \int_{-\infty}^{+\infty} x^2 p_1(x) dx + (1-\alpha) \int_{-\infty}^{+\infty} x^2 p_2(x) dx$
$= \alpha (\mu_1^2 + \sigma_1) + (1-\alpha) (\mu_2^2 + \sigma_2)$ ②

$V_x[X] = E_x[X^2] - (E_x[X])^2$

## page 11

$$= \alpha (\mu_1^2 + \sigma_1) + (1-\alpha)(\mu_2^2 + \sigma_2) - (\alpha\mu_1 + (1-\alpha)\mu_2)^2$$
$$= \alpha\sigma_1 + (1-\alpha)\sigma_2 + (\alpha\mu_1^2 + (1-\alpha)\mu_2^2 - [\alpha\mu_1 + (1-\alpha)\mu_2]^2)$$

Section 6.5.
More different distributions Section 6.6. self-study.
How to transform known distribution to another new distribution? $\rightarrow$ Section 6.7 self-study.