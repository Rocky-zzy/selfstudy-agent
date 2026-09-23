# Lecture Slides S2026\Lecture 7 Optimization Gradient decent and constrained optimization.pdf

## page 1

lecture 7. Optimization : Gradient descent and constrained optimization

Loss function $L(y, \hat{y})$ to be minimized.

$\frac{\partial L(y, \hat{y})}{\partial W^{(l)}} , \frac{\partial L(y, \hat{y})}{\partial b^{(l)}} \Rightarrow$ searching direction

$\Rightarrow$ numerical optimization technique for searching strategy.

Remark: ① assuming that the objective function ( loss function ) is differentiable.
② mainly focus on "minimization" objectives.

Example: consider the loss function $l(x) = x^4 + 7x^3 + 5x^2 - 17x + 3$
The gradient: $\frac{dl(x)}{dx} = 4x^3 + 21x^2 + 10x - 17 \quad \frac{d^2l(x)}{dx^2} = 12x^2 + 42x + 10.$

$\frac{dl(x)}{dx} = 0$
$x_1 = -4.5 \quad d^2l(x)/dx^2 = 69$
$x_2 = -1.4 \quad d^2l(x)/dx^2 = -25.282 - (1-$st derivative decreases)
$x_3 = 0.7 \quad d^2l(x)/dx^2 = 299.88. \Rightarrow$ (local maximum).

$\Rightarrow$ start at some $x_0$, negative gradient leads us to some (local) minimum
$\Rightarrow$ Hence: minimization of the objective $\Rightarrow$ gradient descent
maximization of the objective $\Rightarrow$ gradient ascent

1. Unconstrained optimization

Problem: Solving the minimum of a real-valued function.

$\min_{\vec{x} \in \mathbb{R}^d} f(\vec{x})$
where $f: \mathbb{R}^d \rightarrow \mathbb{R}$ being a differentiable objective function

Solution: starting from a particular location $x_0$, searching is iteratively done by
$\gamma > 0$, step-size (learning rate).
$\star \quad \vec{x}_{t+1} = \vec{x}_t - \gamma (\nabla f(\vec{x}_t))^T$

Goal: $f(\vec{x}_0) \geq f(\vec{x}_1) \geq \dots \dots$ converge to a local minimum.

Remark: The gradient points in a direction orthogonal to the contour lines of the function.

## page 2

Let : $\vec{y}(t) = [x(t)\ \ y(t)] \in \mathbb{R}^2$ being curve.

[figure: plot with horizontal axis $x(t)$ and vertical axis $y(t)$; a closed oval curve labeled $f(y(t)) = C$; red annotations $dy$ and $\partial_y f$ beside a point on the curve]

contain: $f(y(t)) = C$, $C \in \mathbb{R}$ is a constant.

$$\frac{df}{dt} = 0 \quad \checkmark$$

Meanwhile:
$$\frac{df}{dt} = \frac{df}{dy}\cdot\frac{dy}{dt} = \begin{bmatrix}\frac{\partial f}{\partial x} & \frac{\partial f}{\partial y}\end{bmatrix}\begin{bmatrix}\frac{\partial x}{\partial t}\\[4pt]\frac{\partial y}{\partial t}\end{bmatrix} = \langle \nabla f,\ \vec{y}\,\rangle$$
(red) $= 0$

2. Configuration of step-size.

General idea: adaptive gradient descent instead of fixed-size.

$\Rightarrow$ rescale the step-size at each iteration:

① Function value $\uparrow$ after a gradient step
$\rightarrow$ undo, step-size $\downarrow$

② function value $\downarrow$ after a gradient step
$\rightarrow$ try to increase the step-size

[figure: sketch of a curve $f$ with a starting point $x_0$ and successive points along a descent path]

3. Gradient descent with momentum.

Motivation: The convergence of gradient descent could be slow due to the curvature of the optimization surface:

Example: Valley-shape surface
$\rightarrow$ curved in one direction flat in another.

[figure: sketch of a steep V-shaped valley]

## page 3

Idea: Extra memory for the gradient descent
$\Delta x_t = x_t - x_{t-1}$

consider $\alpha \in [0, 1]$.

$$\boxed{\vec{x}_{t+1} = \vec{x}_t - \gamma_t \left(\nabla f\right)(\vec{x}_t)^T + \alpha\,\Delta x_t}$$

$$\vec{x}_{t+1} - \vec{x}_t = \Delta\vec{x}_{t+1} = -\gamma_t\left((\nabla f)(\vec{x}_t)\right)^T + \alpha\,\Delta\vec{x}_t$$
$$= -\sum_{\tau=1}^{t} \boxed{\alpha^{\,t-\tau}\,\gamma_\tau}\left((\nabla f)(\vec{x}_\tau)\right)^T$$
(red annotation: $\gamma_\tau$)

i.e. update the new value according to "accumulated gradient with dynamical rate".

Case 1: direction of recent gradients are consistent:
$|\Delta x_t| \uparrow$ (accelerating the iteration at the beginning)

Case 2: direction of recent gradient diverse: $|\Delta x_t| \downarrow$ (stabilizing the iteration at the late stage) .

4. Stochastic Gradient Descent
Consider the objective function
$$L(\theta) = \sum_{i=1}^{N} L_i(\theta), \text{ with is the sum of losses } L_i$$
incurred by each sample $i$; $\theta$ is the parameter to be optimized.
Target: Find $\theta$ that minimized $L$.

$\Rightarrow$ consider data set $D\{(x,y)\}_i^n$
(blue annotation on $y$: real value; blue annotation on $f$: predicted value for the given $\theta$.)

$$\theta_{t+1} = \theta_t - \gamma_t \sum_{i=1}^{N} \frac{\partial L\left(y^{(i)}, f(x^{(i)}, \theta)\right)}{\partial \theta}$$

Problem: Difficulties for computing the gradient, when.
① Training data set is enormous
② evaluating the sum of gradient is not easy

## page 4

Solution: use **empirical loss** to approximate expected loss
$\uparrow$
an unbiased estimate of the true gradient by randomly select a small, mini-batch of data

Benefit of mini-batch
① quick to estimate
② noisy estimation allows us to get out of some bad local optima
③ good for generalization.

Exercise: Consider $f\left(\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}\right) = \frac{1}{2} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}^T \begin{bmatrix} 2 & 1 \\ 1 & 20 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} - \begin{bmatrix} 5 \\ 3 \end{bmatrix}^T \begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$
run gradient descent and starting at $\vec{x}_0 = \begin{bmatrix} -3 \\ -1 \end{bmatrix}$, what is $\vec{x}_1$ considering $\gamma = 0.085$

Answer: Let $\vec{x} = [x_1 \ x_2]^T$, $f(\vec{x}) = \vec{x}^T M \vec{x} - B \vec{x}$, $\frac{\partial f}{\partial \vec{x}} = \vec{x}^T M - B$
② $\vec{x}_0 = [-3 \ -1]^T$, $\nabla f(\vec{x}_0) = [-3 \ -1] \begin{bmatrix} 2 & 1 \\ 1 & 20 \end{bmatrix} - [5 \ 3]$
$= [-12 \ -26]$.
$\vec{x}_1 = \vec{x}_0 - \gamma (\nabla f(\vec{x}_0))^T = \begin{bmatrix} -3 \\ -1 \end{bmatrix} - 0.085 \begin{bmatrix} -12 \\ -26 \end{bmatrix} = \begin{bmatrix} -1.98 \\ 1.21 \end{bmatrix}$

5. Constrained Optimization.
consider minimizing the objective function.
[Boxed: $\min_{\vec{x}} f(\vec{x})$ primal problem
subject to $g_i(\vec{x}) \leq 0$, for all $i = 1, \dots, m$]
An easy (but not implementation-friendly) unconstrain objective.
[Boxed: $\min_{\vec{x} \in \mathbb{R}^n} J(\vec{x}) := f(\vec{x}) + \sum_{i=1}^m \mathbb{I}(g_i(\vec{x}))$ in which original problem
$\mathbb{I}(z)$ is an infinite step function, i.e. $\mathbb{I}(z) = \begin{cases} 0, & \text{if } z \leq 0 \\ \infty & \text{otherwise} \end{cases}$]

## page 5

only solution with $Z \leq 0$ would be found, but difficult to implement.

Instead, an alternative approach: Lagrange Multiplier

For $\lambda_i \geq 0$, define
$$L(\vec{x}, \vec{\lambda}) := f(\vec{x}) + \sum_{i=1}^m \lambda_i g_i(\vec{x})$$
$$= f(\vec{x}) + \vec{\lambda}^T \vec{g}(\vec{x}),$$
$$\vec{\lambda} = [\lambda_1, \dots, \lambda_m]^T$$
$$\vec{g}(\vec{x}) = [g_1(\vec{x}), \dots, g_m(\vec{x})]^T$$

Then, we can propose the corresponding dual problem

dual $\rightarrow$ problem
$$\max_{\vec{\lambda} \in \mathbb{R}^m} D(\vec{\lambda})$$
subject to $\vec{\lambda} \geq \vec{0}$, with $D(\vec{\lambda}) := \min_{\vec{x} \in \mathbb{R}^d} L(\vec{x}, \vec{\lambda})$
$\vec{\lambda} \geq \vec{0} \iff \lambda_i \geq 0$ for all $i \in \{1, m\}$
$x$: primal variable; $\lambda$: dual variable
unconstrained optimization problem when $\lambda$ is fixed.

Remarks:
① $D(\lambda)$ is easy to solve when $\lambda$ is fixed.
② $L(\vec{x}, \vec{\lambda})$ is affine w.r.t. $\vec{\lambda}$, hence, $D(\lambda) := \min_{\vec{x} \in \mathbb{R}^d} L(\vec{x}, \vec{\lambda})$ is a point-wise minimum of affine function of $\lambda$.
③ The outer problem over $\lambda$ can be solved efficiently ($D(\lambda)$ is concave)

We need Minimax inequality.
For any function $\varphi$ with two arguments $x, y$.
$$\max_y \min_x \varphi(x, y) \leq \min_x \max_y \varphi(x, y)$$

Proof: For any $x_0, y_0$, one can verify
$$\min_x \varphi(x, y_0) \leq \varphi(x_0, y_0) \leq \max_y \varphi(x_0, y) \quad \text{①}$$

Consider $y_0' := \arg\max_y \min_x \varphi(x, y) \quad x_0' := \arg\min_x \max_y \varphi(x, y)$
Since ① holds for any arbitrary $x_0, y_0$
$$\min_x \varphi(x, y_0') \leq \max_y \varphi(x_0', y)$$

## page 6

⇒ $\max_y \min_x g(x,y) \leq \min_x \max_y g(x,y)$

From minimax inequality,
$$ \min_{\vec{x} \in \mathbb{R}^m} \max_{\vec{\lambda} \geq 0} \mathcal{L}(\vec{x}, \vec{\lambda}) \geq \boxed{\max_{\vec{\lambda} \geq 0} \min_{\vec{x} \in \mathbb{R}^m} \mathcal{L}(\vec{x}, \vec{\lambda})} \text{ dual problem} $$

note that if $\vec{\lambda} \geq \vec{0}$, we relaxed the indication functions to a linear function. (linear combination among $g_i(\vec{x})$, $i \in [1,m]$)
$$ \mathcal{L}(\vec{x}, \vec{\lambda}) \leq J(\vec{x}) \text{ } (= f(\vec{x}) + \sum_{i=1}^m I(g_i(\vec{x})) $$
⇒ $J(\vec{x}) = \max_{\vec{\lambda} \geq \vec{0}} \mathcal{L}(\vec{x}, \vec{\lambda})$ consider that the original problem
aim at $\min_{\vec{x} \in \mathbb{R}^m} J(x) \iff \min_{\vec{x} \in \mathbb{R}^m} \max_{\vec{\lambda} \geq 0} \mathcal{L}(\vec{x}, \vec{\lambda})$
⇒ $\max_{\vec{\lambda} \geq 0} \min_{\vec{x} \in \mathbb{R}^m} \mathcal{L}(\vec{x}, \vec{\lambda}) = \max_{\vec{\lambda} \geq 0} D(\lambda) \leq \min_{\vec{x} \in \mathbb{R}^m} \max_{\vec{\lambda} \geq 0} \mathcal{L}(\vec{x}, \vec{\lambda})$
⇒ optimal value of the objective function for the dual problem is a lower bound of that of the original problem.
$\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ $\quad$ ↪ weak duality

Remark: In case equality constraints
$$ h_j(\vec{x}) = 0 \iff \begin{cases} h_j(\vec{x}) \leq 0 \\ -h_j(\vec{x}) \leq 0 \end{cases} $$

In particular:
we define optimal duality gap = $\min_{\vec{x} \in \mathbb{R}^m} \max_{\vec{\lambda} \geq 0} \mathcal{L}(\vec{x}, \vec{\lambda}) - \max_{\vec{\lambda} \geq 0} \min_{\vec{x} \in \mathbb{R}^m} \mathcal{L}(\vec{x}, \vec{\lambda})$

Additionally, optimal duality gap=0 (strong duality holds)
① $g_i(x)$, $i \in [1,m]$ are convex
② $\exists x$, s.t. $g_i(x) = 0 \quad \forall i \in [1,m]$ (Slater's condition)

6. convex programming / optimization
1) Def: Convex Optimization is a class of optimization problems
$$ \min_x f(x) $$
s.t. $g_i(x) \leq 0$, $\forall i \in [1,m]$
with $f(\cdot)$ is a convex function, $g_i(x) \leq 0$, $\forall i \in [1,m]$ form convex set.

## page 7

(2) convex set: A set $C$ is convex if for any $\vec{x}, \vec{y} \in C$, one has $\forall \alpha \in [0, 1]$, $\alpha \vec{x} + (1-\alpha)\vec{y} \in C$

(3) Convex function: A function $f: C \subseteq \mathbb{R}^p \to \mathbb{R}$ is convex if for any $\vec{x}, \vec{y} \in C$
$$\forall \alpha \in [0, 1], \quad f((1-\alpha)\vec{x} + \alpha\vec{y}) \leq (1-\alpha)f(\vec{x}) + \alpha f(\vec{y}) \quad \checkmark$$

① Equivalently, if $f$ is differentiable (i.e. $\nabla f(x)$ exists for all $\vec{x} \in C$) Then $f$ is convex if and only if for all $\vec{x}, \vec{y} \in C$
$$f(\vec{y}) \geq f(\vec{x}) + \nabla f(\vec{x})^T (y - x) \quad \text{(first order condition)}$$

② (second order condition) If $f(x)$ is twice differentiable (i.e. Hessian matrix exists for all $\vec{x} \in C$)

$f: \mathbb{R}^m \to \mathbb{R}$
$\nabla^2 f(x)_{i,j} = \frac{\partial^2 f(x)}{\partial x_i \partial x_j}$
$i=1, \dots, m, j=1, \dots, m$

$f(x)$ is convex $\iff$ $\nabla_x^2 f(x)$ is positive semidefinite

Remark ① for convex loss function in unconstrain optimization, all local minimum are global minimum.
② a concave function is the negative of a convex function.

Theorem. Given nonnegative reals $\alpha_1$ and two convex function $f_1, f_2$ then $\alpha_1 f_1 + (1-\alpha) f_2$ is still convex.
$\alpha \in [0, 1]$

Proof: By definition, $\forall \vec{x}, \vec{y} \in C$
$f_1(\alpha \vec{x} + (1-\alpha)\vec{y}) \leq \alpha f_1(\vec{x}) + (1-\alpha)f_1(\vec{y})$ ①
$f_2(\alpha \vec{x} + (1-\alpha)\vec{y}) \leq \alpha f_2(\vec{x}) + (1-\alpha)f_2(\vec{y})$ ②
$f := f_1 + f_2$
$f(\alpha \vec{x} + (1-\alpha)\vec{y})$
$= f_1(\alpha \vec{x} + (1-\alpha)\vec{y}) + f_2(\alpha \vec{x} + (1-\alpha)\vec{y})$

## page 8

$\leq \alpha f_1(\vec{x}) + (1-\alpha)f_1(\vec{y}) + \alpha f_2(\vec{x}) + (1-\alpha)f_2(\vec{y}) \quad (\text{since } \textcircled{1} \textcircled{2})$

$= \alpha (f_1(\vec{x}) + f_2(\vec{x})) + (1-\alpha)(f_1(\vec{y}) + f_2(\vec{y}))$

$= \alpha f(\vec{x}) + (1-\alpha)f(\vec{y}).$

$\implies f(\alpha \vec{x} + (1-\alpha)\vec{y}) \leq \alpha f(\vec{x}) + (1-\alpha)f(\vec{y}) \implies f_1+f_2 \text{ is convex } \textcircled{3}$

since for any $\gamma \geq 0$ if $f$ is convex, then

$\gamma f((1-\alpha)\vec{x} + \alpha \vec{y}) \leq (1-\alpha)\gamma f(\vec{x}) + \alpha \gamma f(\vec{y}) \implies \gamma f \text{ is convex. } \textcircled{4}$

combining \textcircled{3} \& \textcircled{4}, we have for any $\alpha, \beta \geq 0$ if $f_1$ \& $f_2$ are convex, $\alpha f_1 + \beta f_2$ is convex.

$\star$ Remark: natural extension: nonnegative weight sum of more than two convex function are still convex.

---

7. Linear programming: (special case of convex programming, with all functions are linear)

$\min_{\vec{x} \in \mathbb{R}^n} c^T \vec{x}$

subject to $A\vec{x} \leq \vec{b}$, with $A \in \mathbb{R}^{d \times n}, \vec{b} \in \mathbb{R}^d, \vec{c} \in \mathbb{R}^n$

The Lagrangian.

$\mathcal{L}(\vec{x}, \vec{\lambda}) = c^T \vec{x} + \vec{\lambda}^T (A\vec{x} - \vec{b})$

with $\vec{\lambda} \in \mathbb{R}^m$ is vector of non-negative Lagrange multiplier

$\mathcal{L}(\vec{x}, \vec{\lambda}) = (\vec{c} + A^T \vec{\lambda})^T \vec{x} - \vec{\lambda}^T \vec{b}$

$\checkmark \quad \frac{\partial \mathcal{L}(\vec{x}, \vec{\lambda})}{\partial \vec{x}} = \vec{c} + A^T \vec{\lambda} \quad \text{since for } \min_{\vec{x}} \mathcal{L}(\vec{x}, \vec{\lambda}), \frac{\partial \mathcal{L}(\vec{x}, \vec{\lambda})}{\partial \vec{x}} = 0$

$\implies$ the dual Lagrangian. $D(\vec{\lambda}) = -\vec{\lambda}^T \vec{b}$

Therefore, the dual optimization problem is

$\max_{\vec{\lambda} \in \mathbb{R}^n} -\vec{b}^T \vec{\lambda}$

subject to $\vec{c} + A^T \vec{\lambda} = 0, \vec{\lambda} \geq 0$

## page 9

Remark : ① since linear programming is convex programming
dual problem has the same solution as the
primed one.

② solving the primal problem or dual program
depending on whether m or d is larger.

---

8. Quadratic programming

Consider the case of a convex quadratic objective
function, where the constraints are affine, i.e.

$$\min_{x\in\mathbb{R}^m} \frac{1}{2}\vec{x}^T Q \vec{x} + \vec{c}^{\,T}\vec{x} \qquad \leftarrow \text{primal}$$

subject to $A\vec{x} \le \vec{b}$, where

① $A \in \mathbb{R}^{d\times m}$, $\vec{b} \in \mathbb{R}^d$ and $\vec{c} \in \mathbb{R}^m$

② $Q \in \mathbb{R}^{m\times m}$ being positive definite.

($m$ variables and $d$ linear constraints)

---

The Lagrangian is

$$L(\vec{x},\vec{\lambda}) = \frac{1}{2}\vec{x}^T Q \vec{x} + \vec{c}^{\,T}\vec{x} + \vec{\lambda}^T(A\vec{x} - \vec{b})$$

$$= \frac{1}{2}\vec{x}^T Q \vec{x} + (\vec{c} + A^T\vec{\lambda})^T\vec{x} - \vec{\lambda}^T\vec{b}.$$

consider $\min_{\vec{x}} L(\vec{x},\vec{\lambda})$, $\dfrac{\partial L(\vec{x},\vec{\lambda})}{\partial \vec{x}} = Q\vec{x} + (\vec{c} + A^T\vec{\lambda}) = \vec{0}$

$$\vec{x} = -Q^{-1}(\vec{c} + A^T\vec{\lambda})$$

Therefore substitute it back to $L(\vec{x},\vec{\lambda})$,

$$\Rightarrow D(\vec{\lambda}) = -\frac{1}{2}(\vec{c} + A^T\vec{\lambda})^T Q^{-1}(\vec{c} + A^T\vec{\lambda}) - \vec{\lambda}^T\vec{b}$$

## page 10

dual optimization problem - ✓

$$ \max_{\vec{\lambda} \in \mathbb{R}^d} D(\vec{\lambda}) $$
$$ \text{subject to} \quad \vec{\lambda} \succeq 0 $$

Summary -

Optimization
- unconstrained opt
 - gradient descent
 - ① gradient descent with momentum
 - ② stochastic gradient descent
- constrained opt
 - primal problem
 - dual problem
 - weak duality
 - strong duality ← Slater's condition

set
function
- convex
- linear programming
- quadratic programming

Section 7.1 ~ 7.3.