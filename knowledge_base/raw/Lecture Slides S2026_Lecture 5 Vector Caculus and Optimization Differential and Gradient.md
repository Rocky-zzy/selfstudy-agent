# Lecture Slides S2026\Lecture 5 Vector Caculus and Optimization Differential and Gradient.pdf

## page 1

Lecture 5. Vector Calculus and Optimization: Differential and Gradient

$\vec{y} = W\vec{x} + \vec{b}$ we would like to obtain $W$, which is trainable parameter such that $\|y - \hat{y}\|$ is minimal.
$\Rightarrow$ how to search?

General idea: along directions that gradient decaying.

① how to compute gradient?
② how to go along the direction of gradient descent?

1. Differentiation of univariant functions.

(1) Basic Concept: derivative.

Def: Consider a univariant function $y = f(x)$, $x, y \in \mathbb{R}$. $\mathbb{R} \rightarrow \mathbb{R}$

[Graph of a curve with axes $x$ and $y$. Points labeled $f(x_0)$ and $f(x_0 + \delta x)$. The differences are marked as $\delta x$ and $\delta y$.]

Different Quotient.
$$ \frac{\delta y}{\delta x} := \frac{f(x + \delta x) - f(x)}{\delta x} $$
$\delta x \rightarrow 0$ $\Rightarrow$
Derivative
$$ \frac{df}{dx} := \lim_{\delta x \rightarrow 0} \frac{f(x + \delta x) - f(x)}{\delta x} $$

Some common rule for derivative.
① $f(x) = x^n$, $f'(x) = n x^{n-1}$; ② $f(x) = \sin x$, $f'(x) = \cos x$
③ $f(x) = \cos x$, $f'(x) = -\sin x$; ④ $f(x) = e^x$, $f'(x) = e^x$
⑤ $f(x) = \ln x = \log_e x$, $f'(x) = \frac{1}{x}$

(2) Chain rule for derivative.
① $(f(x)g(x))' = f'(x)g(x) + f(x)g'(x)$
② $\left(\frac{f(x)}{g(x)}\right)' = \frac{f'(x)g(x) - f(x)g'(x)}{(g(x))^2}$
③ $(g(f(x)))' = (g \circ f)'(x) = g'(f(x)) \cdot f'(x)$

Example: $h(x) = (2x+1)^4 \quad \frac{dh(x)}{dx}$
Let $f(x) = 2x+1$, $g(f) = f^4$
$f'(x) = 2 \quad g'(f) = 4f^3 \Rightarrow h'(x) = g'(f(x)) \cdot f'(x)$
$= 4f^3 \cdot 2 = 4(2x+1)^3 \cdot 2$
$= 8(2x+1)^3$

## page 2

2. Partial differential & gradients

Consider a function $f: \mathbb{R}^n \to \mathbb{R}$ (requires derivative to function of several variables)

(1) Def. Partial Derivative:

For a function $f: \mathbb{R}^n \to \mathbb{R}$ and $\vec{x} \in \mathbb{R}^n$ of $n$ variable $x_1, \dots, x_n$

the partial derivatives are:

① $\left[\dfrac{\partial f}{\partial x_1}\right] = \lim_{h \to 0} \dfrac{f(x_1+h,\, x_2,\, x_3,\, \dots,\, x_n) - f(\vec{x})}{h}$

$\vdots$

$\left[\dfrac{\partial f}{\partial x_n}\right] = \lim_{h \to 0} \dfrac{f(x_1,\, x_2,\, \dots,\, x_n+h) - f(\vec{x})}{h}$

$\implies \nabla_{\vec{x}} f = \dfrac{df}{d\vec{x}} = \left[\dfrac{\partial f(\vec{x})}{\partial x_1} \quad \dfrac{\partial f(\vec{x})}{\partial x_2} \quad \cdots \quad \dfrac{\partial f(\vec{x})}{\partial x_n}\right] \in \mathbb{R}^{1 \times n}$ (row vector)

$\vec{x} = [x_1 \cdots x_n]^T$

(2) Chain rule for differentiation

① $\dfrac{\partial}{\partial \vec{x}}\left(f(\vec{x}) \cdot g(\vec{x})\right) = \dfrac{\partial f}{\partial \vec{x}} g(x) + f(x)\dfrac{\partial g}{\partial \vec{x}}$

② $\dfrac{\partial}{\partial \vec{x}}\left(f(\vec{x}) + g(\vec{x})\right) = \dfrac{\partial f}{\partial \vec{x}} + \dfrac{\partial g}{\partial \vec{x}}$

③ $\dfrac{\partial}{\partial \vec{x}}(g \circ f)(\vec{x}) = \dfrac{\partial g}{\partial f} \cdot \dfrac{\partial f}{\partial \vec{x}}$

④ $\dfrac{\partial}{\partial x}\left(\dfrac{f}{g}\right) = \dfrac{\dfrac{\partial f}{\partial x} g - \dfrac{\partial g}{\partial x} f}{g^2}$

Summary: Similar to 1-D case.
Derivative $\to$ partial derivative

Example: Given $f(x,y) = (x + 2y^3)^2$, compute $\nabla_{\vec{x}} f$.

$g(x,y) = x + 2y^3 \qquad f(g) = g^2$

$\dfrac{\partial f(x,y)}{\partial x} = \dfrac{\partial f}{\partial g} \cdot \dfrac{\partial g}{\partial x} = 2g \cdot \dfrac{\partial}{\partial x}(x + 2y^3)$
$\qquad = 2(x + 2y^3)$

$\dfrac{\partial f(x,y)}{\partial y} = \dfrac{\partial f}{\partial g} \cdot \dfrac{\partial g}{\partial y} = 2g \cdot \dfrac{\partial}{\partial y}(x + 2y^3)$ [annotation: $6y^2$]
$\qquad = 2 \cdot (x + 2y^3) \cdot 6y^2 = 12(x + 2y^3)y^2$

$\nabla_x = \left[2(x + 2y^3) \qquad 12(x + 2y^3) \cdot y^2\right]$

## page 3

Why row vector?

case 1: Consider function $f: \mathbb{R}^2 \to \mathbb{R}$ of variable $x_1, x_2$.
$\cdot x_1(t), x_2(t): \mathbb{R} \to \mathbb{R}$.
$\implies \frac{df}{dt} = \frac{\partial f}{\partial x_1} \cdot \frac{\partial x_1}{\partial t} + \frac{\partial f}{\partial x_2} \cdot \frac{\partial x_2}{\partial t} = \left[ \frac{\partial f}{\partial x_1} \quad \frac{\partial f}{\partial x_2} \right] \begin{bmatrix} \frac{\partial x_1(t)}{\partial t} \\ \frac{\partial x_2(t)}{\partial t} \end{bmatrix}$

case 2: $x_1(s, t), x_2(s, t): \mathbb{R}^2 \to \mathbb{R}$, let $\vec{\theta} = [s, t]$
since $\frac{\partial f}{\partial s} = \frac{\partial f}{\partial x_1} \cdot \frac{\partial x_1}{\partial s} + \frac{\partial f}{\partial x_2} \cdot \frac{\partial x_2}{\partial s}$
$\quad \quad \frac{\partial f}{\partial t} = \frac{\partial f}{\partial x_1} \cdot \frac{\partial x_1}{\partial t} + \frac{\partial f}{\partial x_2} \cdot \frac{\partial x_2}{\partial t}$
$\implies \frac{df}{d\vec{\theta}} = \frac{\partial f}{\partial \vec{x}} \cdot \frac{\partial \vec{x}}{\partial \vec{\theta}} = \left[ \frac{\partial f}{\partial s} \quad \frac{\partial f}{\partial t} \right]$
$\quad \quad \quad \quad \quad \quad \quad \quad \quad = \left[ \frac{\partial f}{\partial x_1} \quad \frac{\partial f}{\partial x_2} \right] \cdot \begin{bmatrix} \frac{\partial x_1}{\partial s} & \frac{\partial x_1}{\partial t} \\ \frac{\partial x_2}{\partial s} & \frac{\partial x_2}{\partial t} \end{bmatrix}$

Reason: row vector representation is more natural without requiring transposing.
$\implies$ total derivative. $df_a = \sum_{i=1}^n \frac{\partial f}{\partial x_i}(a) \cdot dx_i$

So far.
① $f: \mathbb{R}^D \to \mathbb{R}$ : the gradient is a $1 \times D$ row vector.
② $f: \mathbb{R} \to \mathbb{R}^E$ : the gradient is an $E \times 1$ column vector.
③ $f: \mathbb{R}^D \to \mathbb{R}^E$ : the gradient is an $E \times D$ matrix.

3. Gradients of vector-valued functions
Considering function $f: \mathbb{R}^n \to \mathbb{R}^m$ with $\vec{x} = [x_1, \dots, x_n]^T \in \mathbb{R}^n$.
The corresponding vector of functions:
$\vec{f}[\vec{x}] = \begin{bmatrix} f_1(\vec{x}) \\ \vdots \\ f_m(\vec{x}) \end{bmatrix} \in \mathbb{R}^m$, with $\vec{f} = [f_1, \dots, f_m]^T$ s.t.
$\quad \quad \quad \quad \quad \quad \quad \quad \quad \quad \quad f_i: \mathbb{R}^n \to \mathbb{R} \quad i=1, \dots, m$
$\frac{\partial \vec{f}}{\partial \vec{x}} = \left[ \frac{\partial \vec{f}(\vec{x})}{\partial x_1} \dots \frac{\partial \vec{f}(\vec{x})}{\partial x_n} \right]$

## page 4

$$= \begin{bmatrix} \frac{\partial f_1(\vec{x})}{\partial x_1} & \cdots & \frac{\partial f_1(\vec{x})}{\partial x_n} \\ \vdots & & \vdots \\ \frac{\partial f_m(\vec{x})}{\partial x_1} & \cdots & \frac{\partial f_m(\vec{x})}{\partial x_n} \end{bmatrix} \in \mathbb{R}^{m \times n}$$

$\leftarrow$ collection of all first-order partial derivative of a vector function $f$
$\Rightarrow$ Jacobian matrix,

Exercise: Given
$$\vec{f}(\vec{x}) = \begin{bmatrix} f_1(x_1, x_2) \\ f_2(x_1, x_2) \end{bmatrix} = \begin{bmatrix} x_1^2 x_2 + x_1 x_2^3 \\ x_1 x_2 + 3 x_2 + 2 x_1 x_2^4 \end{bmatrix} \in \mathbb{R}^{2 \times 1}, \text{ compute } \nabla_{\vec{x}} \vec{f}$$
with $\vec{x} = [x_1, x_2]^T$

$$\nabla_{\vec{x}} \vec{f} = \begin{bmatrix} \frac{\partial f_1(x_1, x_2)}{\partial x_1} & \frac{\partial f_1(x_1, x_2)}{\partial x_2} \\ \frac{\partial f_2(x_1, x_2)}{\partial x_1} & \frac{\partial f_2(x_1, x_2)}{\partial x_2} \end{bmatrix} = \begin{bmatrix} 2x_2 x_1 + x_2^3 & x_1^2 + 3x_1 x_2^2 \\ x_2 + 2x_2^4 & x_1 + 3 + 8x_1 x_2^3 \end{bmatrix}$$

$$\frac{\partial f_1(x_1, x_2)}{\partial x_1} = 2x_2 x_1 + x_2^3 \qquad \frac{\partial f_1(x_1, x_2)}{\partial x_2} = x_1^2 + 3x_1 x_2^2$$
$$\frac{\partial f_2(x_1, x_2)}{\partial x_1} = x_2 + 2x_2^4 \qquad \frac{\partial f_2(x_1, x_2)}{\partial x_2} = x_1 + 3 + 8x_1 x_2^3$$

Special case: (linear mapping.
Given $\vec{f}(\vec{x}) = A \vec{x}$, $A \in \mathbb{R}^{m \times n}$, $\vec{f}(\vec{x}) \in \mathbb{R}^{m \times 1}$, $\vec{x} \in \mathbb{R}^{n \times 1}$, compute
$$\nabla_{\vec{x}} \vec{f} = \frac{d \vec{f}}{d \vec{x}} \quad \text{Note: } \vec{f} : \mathbb{R}^n \to \mathbb{R}^m \Rightarrow \frac{d \vec{f}}{d \vec{x}} \in \mathbb{R}^{m \times n} = A$$
$$f_i(\vec{x}) = \sum_{j=1}^N A_{ij} x_j \Rightarrow \frac{\partial f_i}{\partial x_j} = A_{ij}$$

4. Gradient of Matrices
[diagram of a neural network node with inputs $x_0, x_1, x_2$ and output $y$]
$y = \sigma(W\vec{x} + \vec{b})$, and we are searching for the "best" $W \Rightarrow$ derivative over matrice $W$

In general, compute the gradient of an $m \times n$ matrix $A$ w.r.t. (with respect to) a $p \times q$ matrix $B$, the Jacobian $J$

## page 5

would be (m×n) x (pxq) (4-dimensional tensor)

Case 1: Gradient of vectors w.r.t. matrices
Consider $\vec{f} = A\vec{x}$, with $\vec{f} \in \mathbb{R}^M$, $A \in \mathbb{R}^{M \times N}$, $\vec{x} \in \mathbb{R}^N$, compute $\frac{df}{dA}$

Answer: $\boxed{\frac{df}{dA}} \in \mathbb{R}^{M \times (M \times N)}$

$$ \frac{d\vec{f}}{dA} = \begin{bmatrix} \frac{\partial \vec{f}}{\partial A_1} \\ \vdots \\ \frac{\partial \vec{f}}{\partial A_m} \end{bmatrix}, \quad \boxed{\frac{\partial f_i}{\partial A} \in \mathbb{R}^{1 \times (M \times N)}} $$

note that: $f_i = \sum_{j=1}^N A_{ij} x_j$, for $i = 1, \dots, m$
Hence, $\frac{\partial f_i}{\partial A_{ig}} \overset{\checkmark}{=} x_g$, $g = 1, \dots, N$, therefore, one has

$$ \frac{\partial f_i}{\partial A_i} = \vec{x}^T \in \mathbb{R}^{1 \times (1 \times N)} \quad \text{and} \quad \frac{\partial f_i}{\partial A_{k \neq i}} = \vec{0}^T \in \mathbb{R}^{1 \times (1 \times N)} $$
$$ \underbrace{\left[ \frac{\partial f_i}{\partial A_{i1}} \cdots \frac{\partial f_i}{\partial A_{iN}} \right]}_{x_1 \quad \quad \quad x_N} \quad \text{the k-th row of A is not related to } f_i $$

$\Rightarrow$ for $i = [1, M]$, $\frac{\partial f_i}{\partial A} = \begin{bmatrix} \vec{0}^T \\ \vec{0}^T \\ \vdots \\ \vec{x}^T \\ \vdots \\ \vec{0}^T \end{bmatrix} \in \mathbb{R}^{1 \times (M \times N)}$ $\Rightarrow \frac{df}{dA} : \text{aggregation of such matrices}$

---

Case 2: Gradient of Matrices w.r.t. Matrices
Consider a matrix $R \in \mathbb{R}^{M \times N}$, $\vec{f}: \mathbb{R}^{M \times N} \to \mathbb{R}^{N \times N}$, with,
$\vec{f}(R) = R^T R := K \in \mathbb{R}^{N \times N}$, compute $\frac{dK}{dR}$.

Answer: $\frac{dK}{dR} \in \mathbb{R}^{(N \times N) \times (M \times N)}$
note that $\frac{\partial K_{pq}}{\partial R} \in \mathbb{R}^{1 \times (M \times N)}$, for all $p, q = 1, \dots, N$.
$K_{pq} = \vec{r}_p^T \vec{r}_q = \sum_{i=1}^M R_{ip} R_{iq}$

$\Rightarrow \frac{\partial K_{pq}}{\partial R_{ij}} = \sum_{i=1}^M \frac{\partial}{\partial R_{ij}} R_{ip} R_{iq} = \delta_{pqij} = \begin{cases} R_{iq} & \text{if } j = p, p \neq q \\ R_{ip} & \text{if } j = q, p \neq q \\ 2 R_{ig} & \text{if } j = p, p = q \Rightarrow R_{ig}^* \\ 0, & \text{otherwise} \end{cases}$

Each entry of the desired gradient $\frac{dK}{dR} \in \mathbb{R}^{(N \times N) \times (M \times N)}$ is $\delta_{pqij}$
for $p, q, j = 1, \dots, N \quad i = 1, \dots, M$.

## page 6

A few more useful identities for computing gradient.

① $\frac{\partial \vec{x}^T \vec{a}}{\partial \vec{x}} = \vec{a}^T = \frac{\partial \vec{a}^T \vec{x}}{\partial \vec{x}}$ ; ② $\frac{\partial \vec{a}^T \vec{x} \vec{b}}{\partial \vec{x}} = \vec{a} \vec{b}^T$ ; ③ $\frac{\partial \vec{x}^T B \vec{x}}{\partial \vec{x}} = \vec{x}^T (B + B^T)$

④ $\frac{\partial}{\partial \vec{s}} (\vec{x} - A\vec{s})^T W (\vec{x} - A\vec{s}) = -2 (\vec{x} - A\vec{s})^T W A$ for symmetric $W$ ✓

reference: The matrix Cookbook by Peterson and Pedersen 2012
for more useful properties

---

5. Taylor series
(1) single variable function: $f: \mathbb{R} \to \mathbb{R}$, $f \in C^\infty$, the Taylor series $f$ at $x_0$ is :
$T_\infty(x) = \sum_{k=0}^\infty \frac{f^{(k)}(x_0)}{k!} (x - x_0)^k$ (to degree $n$: $n$ instead of $\infty$)
$\Rightarrow$ approximating original $f$
*[handwritten blue annotation: infinitely differentiable (smooth)]*
*[handwritten blue annotation next to $x_0=0$: Maclaurin Series]*
*[handwritten blue annotation under $k!$: factorial]*

(2) multivariate Taylor series : Consider a function $f: \mathbb{R}^p \to \mathbb{R}$
which is smooth at $\vec{x}_0$
$f(x) = \sum_{k=0}^\infty \frac{D_{\vec{x}}^k f(\vec{x}_0)}{k!} (\vec{x} - \vec{x}_0)^k$ (to degree $n$: $n$ instead of $\infty$)

$\vec{\delta} = \vec{x} - \vec{x}_0$ $\vec{\delta}^k$ definition?
$\vec{\delta}^k \in \mathbb{R}^{p \times p \times \dots \times p}$ $\vec{\delta}^2 = \vec{\delta} \otimes \vec{\delta} = \vec{\delta} \vec{\delta}^T \Rightarrow \vec{\delta}^2[i,j] = \delta[i]\delta[j]$
 $\vec{\delta}^3 = \vec{\delta} \otimes \vec{\delta} \otimes \vec{\delta} = \vec{\delta}^3 \in \mathbb{R}^{i,j,k} = \delta[i]\delta[j]\delta[k]$

$\Rightarrow D_{\vec{x}}^k f(\vec{x}_0) \vec{\delta}^k = \sum_{i_1=1}^p \dots \sum_{i_k=1}^p D_{\vec{x}}^k f(\vec{x}_0)[i_1, \dots, i_k] \cdot \delta[i_1] \dots \delta[i_k]$

---

(3) linear Approximation of a function around a point $x$
$f(x) = f(\vec{x}_0) + (\nabla_{\vec{x}} f)(\vec{x}_0) (\vec{x} - \vec{x}_0) \Rightarrow$ Taylor series with order 1
$\Rightarrow$ Approximation of the function around a point with linear curve.

Example. Consider a sigmoid-type function : $\tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$
$\tanh'(x) = \frac{(e^x + e^{-x})(e^x + e^{-x}) - (e^x - e^{-x})(e^x - e^{-x})}{(e^x + e^{-x})^2}$

around $x=0$
$g_1(x) = \tanh(0) + x \cdot \tanh'(0)$
$= 0 + x \cdot 1 = x$

*[handwritten diagram: a plot showing $\tanh(x)$ curve (red) passing through origin, and $y=x$ line (black), with axes labeled $y$ and $x$]*
*[handwritten annotations on right:*
$x \to +\infty, \tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}$
$\approx 1$
$x \to -\infty \quad \tanh(x) = \frac{e^{-x} - e^x}{e^{-x} + e^x} = -1$
*]*
*[handwritten annotation near origin: $(0,0)$ and $(0,1)$? actually looks like $(-1,1)$ near left axis]*

Summary:
Taylor series $\to$ linear approximation $\to$ optimization $\to$ searching direction.
$\downarrow$ derivative
$\begin{cases} \mathbb{R} \to \mathbb{R}: \text{derivative} \\ \mathbb{R}^n \to \mathbb{R}: \text{Gradient vector w.r.t a single input} \\ \mathbb{R}^n \to \mathbb{R}^k: \text{Grad. vec. w.r.t. vec.} \\ \mathbb{R}^{m \times n} \to \mathbb{R}^{p \times q}: \text{Grad. mat. w.r.t mat.} \end{cases}$