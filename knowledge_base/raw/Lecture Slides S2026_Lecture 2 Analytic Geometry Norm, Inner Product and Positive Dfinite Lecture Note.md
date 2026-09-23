# Lecture Slides S2026\Lecture 2 Analytic Geometry Norm, Inner Product and Positive Dfinite Lecture Note.pdf

## page 1

Analytic Geometry 1: Norm, Inner Product and Positive definite

Data set
input , output

[Diagram: Three horizontal layers of open circles connected by arrows from left to right, labeled below as "DNN".]
① predict "unseen" data,
goal → prediction closed to the truth
⇒ $\|y - \hat{y}\|$ as small as possible
true value predicted value
① $\|\cdot\|$ norm
② distance between $y$ and $\hat{y}$

1. Norm
Def. A norm on a vector space $V$ is a function
$\|\cdot\| : V \mapsto \mathbb{R}$
such that for any $\lambda \in \mathbb{R}$ and $\vec{x}, \vec{y} \in V$, s.t. the following hold:
(1) $\|\lambda \vec{x}\| = |\lambda| \cdot \|\vec{x}\|$ absolute homogeneous
(2) $\|\vec{x} + \vec{y}\| \leq \|\vec{x}\| + \|\vec{y}\|$ : triangle inequality
[Diagram: two vectors $\vec{x}$ and $\vec{y}$ forming a triangle with $\vec{x}+\vec{y}$.]
(3) $\|\vec{x}\| \geq 0$ , and $\|\vec{x}\| = 0 \iff \vec{x} = \vec{0}$ : positive definite
iff

Example: (1) $l_1$-norm (Manhattan Norm)
For $x \in \mathbb{R}^n$ $\|x\|_1 := \sum_{i=1}^n |x_i|$
[Diagram: A diamond shape on a coordinate plane with axes $x_1$ and $x_2$. The vertices are at $(1,0)$, $(0,1)$, $(-1,0)$, and $(0,-1)$. Labeled $\|x\|_1 = 1$.]
(2) $l_2$-norm (Euclidean Norm)
For $x \in \mathbb{R}^n$, $\|x\|_2 = \sqrt{\sum_{i=1}^n x_i^2} = \sqrt{x^T x}$
[Diagram: A circle centered at the origin on a coordinate plane with axes $x_1$ and $x_2$. Labeled $\|x\|_2 = 1$.]

2. General Inner product
① Dot product: for $\vec{x}, \vec{y} \in \mathbb{R}^n$, $\vec{x}^T \vec{y} = \sum_{i=1}^n x_i y_i$
② Bilinear mapping $f$
Def: Given a vector space $V$. For all $\vec{x}, \vec{y} \in V$ , $\lambda, \varphi \in \mathbb{R}$,
$f(\cdot, \cdot) : V \times V \mapsto \mathbb{R}$ is a bilinear map
1) $f(\lambda \vec{x} + \varphi \vec{y}, \vec{z}) = \lambda f(\vec{x}, \vec{z}) + \varphi f(\vec{y}, \vec{z})$ (linear in 1st argument)
2) $f(\vec{x}, \lambda \vec{y} + \varphi \vec{z}) = \lambda f(\vec{x}, \vec{y}) + \varphi \cdot f(\vec{x}, \vec{z})$ (linear in 2nd argument)
③ Symmetric.
Let $V$ be a vector space and $f: V \times V \mapsto \mathbb{R}$ be a bilinear

## page 2

mapping. Then $f$ is symmetric if $f(\vec{x}, \vec{y}) = f(\vec{y}, \vec{x})$
$\Rightarrow$ the order of argument does not matters.
(次序)

④ positive definite.
Let $V$ be a vector space and $f: V \times V \mapsto \mathbb{R}$ be a bilinear mapping.
Then $f$ is positive definite if $\forall \vec{x} \in V \setminus \{\vec{0}\}$, we have
$f(\vec{x}, \vec{x}) > 0$ and $f(\vec{0}, \vec{0}) = 0$ (always non-negative)

(General) Inner product
Def. Consider a vector space $V$ and a mapping $f: V \times V \mapsto \mathbb{R}$
$f$ is called an inner product on $V$, if.
① $f$ is bilinear ; ② $f$ is symmetric ; ③ $f$ is positive definite
In this case, we write $f(\vec{x}, \vec{y})$ as $\langle \vec{x}, \vec{y} \rangle$

3. Property of Inner Product
Consider a vector space $V$, inner product $\langle \cdot, \cdot \rangle : V \times V \mapsto \mathbb{R}$
and an ordered basis $B = [\vec{b}_1, \dots, \vec{b}_n]$
For any $\vec{x}, \vec{y} \in V$, with
$\vec{x} = \sum_{i=1}^n \psi_i \vec{b}_i$ , $\vec{y} = \sum_{j=1}^n \lambda_j \vec{b}_j$ , with suitable $\psi_i, \lambda_j \in \mathbb{R}$
Then $\langle \vec{x}, \vec{y} \rangle = \langle \sum_{i=1}^n \psi_i \vec{b}_i , \sum_{j=1}^n \lambda_j \vec{b}_j \rangle$
$= \sum_{i=1}^n \psi_i \langle \vec{b}_i , \sum_{j=1}^n \lambda_j \vec{b}_j \rangle = \sum_{i=1}^n \psi_i \sum_{j=1}^n \lambda_j \langle \vec{b}_i, \vec{b}_j \rangle$
$= \sum_{i=1}^n \sum_{j=1}^n \psi_i \langle \vec{b}_i, \vec{b}_j \rangle \lambda_j = \hat{x}^T A \hat{y}$
with $\hat{x} := [\psi_1, \dots, \psi_n]^T$ , $\hat{y} = [\lambda_1, \dots, \lambda_n]^T$ , $A = \begin{bmatrix} \langle \vec{b}_1, \vec{b}_1 \rangle & \cdots & \langle \vec{b}_1, \vec{b}_n \rangle \\ \langle \vec{b}_2, \vec{b}_1 \rangle & \cdots & \vdots \\ \vdots & \ddots & \vdots \\ \langle \vec{b}_n, \vec{b}_1 \rangle & \cdots & \langle \vec{b}_n, \vec{b}_n \rangle \end{bmatrix}$

$A$ is symmetric since $\langle \vec{b}_j, \vec{b}_i \rangle = \langle \vec{b}_i, \vec{b}_j \rangle$.

Example: Consider $V = \mathbb{R}^2$ with an inner product
$\langle \cdot, \cdot \rangle : V \times V \mapsto \mathbb{R}$ and an order basis $B = [\vec{g}_1, \vec{g}_2]$ of $V$
where $\vec{g}_1 = [1, 1]^T$ , $\vec{g}_2 = [1, -2]^T$ . Given $\vec{x} = 2\vec{g}_1 + 3\vec{g}_2$

## page 3

$\vec{y} = -\vec{g}_1 + 2\vec{g}_2$ , Compute $\langle \vec{x}, \vec{y} \rangle$ , ( dot product)

Normal Computation $\langle \vec{x}, \vec{y} \rangle = \langle 2\vec{g}_1 + 3\vec{g}_2 , -\vec{g}_1 + 2\vec{g}_2 \rangle$
$= -2\langle \vec{g}_1, \vec{g}_1 \rangle - 3\langle \vec{g}_2, \vec{g}_1 \rangle + 4\langle \vec{g}_1, \vec{g}_2 \rangle + 6\langle \vec{g}_2, \vec{g}_2 \rangle$

$\langle \vec{g}_1, \vec{g}_1 \rangle = 2$ , $\langle \vec{g}_2, \vec{g}_1 \rangle = \langle \vec{g}_1, \vec{g}_2 \rangle = -1$ , $\langle \vec{g}_2, \vec{g}_2 \rangle = 5$

$\Rightarrow \langle \vec{x}, \vec{y} \rangle = -2 \times 2 - 3 \times (-1) + 4(-1) + 6 \times 5 = 25$ .

also $A = \begin{bmatrix} \langle \vec{g}_1, \vec{g}_1 \rangle & \langle \vec{g}_1, \vec{g}_2 \rangle \\ \langle \vec{g}_2, \vec{g}_1 \rangle & \langle \vec{g}_2, \vec{g}_2 \rangle \end{bmatrix} = \begin{bmatrix} 2 & -1 \\ -1 & 5 \end{bmatrix}$

$x = [2, 3]^T$ , $y = [-1, 2]^T$

$x^T A y = \begin{bmatrix} 2 & 3 \end{bmatrix} \begin{bmatrix} 2 & -1 \\ -1 & 5 \end{bmatrix} \begin{bmatrix} -1 \\ 2 \end{bmatrix} = 25$

7. Symmetric and Positive Definite Matrix
Recall the positive definite of a norm, we should have.
$\forall \vec{x} \in V \setminus \{\vec{0}\}$ , $\vec{x}^T A \vec{x} > 0$ , we call a symmetric matrix $A$ satisfying this condition as positive definite matrix.
Moreover, if $\forall \vec{x} \in V \setminus \{\vec{0}\}$ , $\vec{x}^T A \vec{x} \geq 0$ , then $A$ is called symmetric, positive semidefinite.
Theorem 1: For any $A \in \mathbb{R}^{n \times n}$ , $A^T A$ is positive semidefinite
Proof: by definition, for any $\vec{x} \in V$ , $A\vec{x} \in V$ $\vec{x}^T A^T A \vec{x} \geq 0$
$\Rightarrow A^T A \geq 0$
Theorem 2. For any $M \in \mathbb{R}^{n \times n}$ that is symmetric, positive definite , iff there exists $A \in \mathbb{R}^{n \times n}$ with full rank , s.t.
$M = A^T A$

## page 4

Theorem 3. For a real-valued, finite-dimensional vector space $V$ and an ordered basis $B$ of $V$, it holds that:
$\langle \cdot,\cdot \rangle : V \times V \mapsto \mathbb{R}$ is an inner product if and only if there exists a symmetric, positive definite matrix $A \in \mathbb{R}^{n\times n}$ with $\vec{x},\vec{y} \in V$ $\langle \vec{x},\vec{y}\rangle = \vec{x}^T A \vec{y}$, where $\vec{x}$ and $\vec{y}$ are the coordinate representations of $\vec{x},\vec{y}$ with respect to $B$.

Exercise: Consider a positive definite matrix $M \in \mathbb{R}^{n\times n}$, with a vector space $V = \mathbb{R}^n$, prove $\forall \vec{x} \in V$, $\|\vec{x}\|_M := \sqrt{\vec{x}^T M \vec{x}}$ is a norm.

Proof: (Condition 1). Consider $\lambda \in \mathbb{R}$, $\vec{x} \in V$
$\|\lambda \vec{x}\|_M = \sqrt{\lambda^2 \vec{x}^T M \vec{x}} = |\lambda|\sqrt{\vec{x}^T M \vec{x}} = |\lambda| \cdot \|\vec{x}\|_M$ ✓

(Condition2) Consider any $\vec{x}, \vec{y} \in V$
$\|\vec{x} + \vec{y}\|_M = \sqrt{(\vec{x}+\vec{y})^T M (\vec{x}+\vec{y})}$
$= \sqrt{\vec{x}^T M \vec{x} + \vec{x}^T M \vec{y} + \vec{y}^T M \vec{x} + \vec{y}^T M \vec{y}}$
$= \sqrt{\vec{x}^T M \vec{x} + 2\vec{x}^T M \vec{y} + \vec{y}^T M \vec{y}}$
$= \sqrt{\|\vec{x}\|_M^2 + 2\tilde{x}^T \tilde{y} + \|\vec{y}\|_M^2}$
$\le \sqrt{\|\vec{x}\|_M^2 + 2\|\vec{x}\|_M \|\vec{y}\|_M + \|\vec{y}\|_M^2}$
$= \sqrt{\|\vec{x}\|_M^2 + 2\|\vec{x}\|_M \|\vec{y}\|_M + \|\vec{y}\|_M^2}$
$= \sqrt{(\|\vec{x}\|_M + \|\vec{y}\|_M)^2} = \|\vec{x}\|_M + \|\vec{y}\|_M$.

$\|\vec{x}+\vec{y}\|_M \le \|\vec{x}\|_M + \|\vec{y}\|_M$
$\vec{x}^T M^T M \vec{y}$
Let $M = N^T N$
$\tilde{x}' = N\tilde{x}, \tilde{y}' = N\tilde{y}$
$\tilde{x}' =$
$\|\tilde{x}'\| = \|N\tilde{x}\|$
$= \|\vec{x}\|_M$

Condition 3 $\forall \vec{x} \in V$ $\sqrt{\vec{x}^T M \vec{x}} \ge 0$
$\sqrt{\vec{x}^T M \vec{x}} = 0$ if $\vec{x} = \vec{0}$ and if $\sqrt{\vec{x}^T M \vec{x}} = 0$, then $\vec{x} = 0$ ✓

## page 5

Analytic Geometry 2. Distance , angle, orthonormal Basis
Inner product of function.

Fact : Any inner product induces a norm.
$$\|\vec{x}\| = \sqrt{\vec{x}^T M \vec{x}} \quad \text{for some sym. positive definite matrix}$$

Def. Distance.
Consider an inner product space $(V, \langle \cdot, \cdot \rangle)$, Then, the distance between any vectors $\vec{x}, \vec{y} \in V$ is
$$d(\vec{x}, \vec{y}) := \|\vec{x} - \vec{y}\| = \sqrt{\langle \vec{x} - \vec{y}, \vec{x} - \vec{y} \rangle}$$

Remark 1: inner product induced a norm, and distance between two vectors is related to the induced norm,
i.e. the positive definite matrix $(M)$ related to the norm.

Remark 2: different norms correspond to different distance

Consider the length of vector $\vec{x} = [1, 1]^T \in \mathbb{R}^2$ using
(1) Dot product. $x_1 y_1 + x_2 y_2$
(2) $\langle \vec{x}, \vec{y} \rangle := \vec{x}^T \begin{bmatrix} 1 & -0.5 \\ -0.5 & 1 \end{bmatrix} \vec{y} = x_1 y_1 - \frac{1}{2}(x_1 y_2 + x_2 y_1) + x_2 y_2$
$\vec{x} = [x_1, x_2]^T, \vec{y} = [y_1, y_2]^T$

Remark: length a vector is related to the norm selected, length may be different if norm is different

Def: Metric.
The mapping $d: V \times V \mapsto \mathbb{R}$ for which $(\vec{x}, \vec{y})$ maps to $d(\vec{x}, \vec{y})$ is called a metric, which satisfies
1) positive definite: $d(\vec{x}, \vec{y}) \geq 0$ for any $\vec{x}, \vec{y} \in V$, and $d(\vec{x}, \vec{y}) = 0$ iff $\vec{x} = \vec{y}$
2) symmetric property: $d(\vec{x}, \vec{y}) = d(\vec{y}, \vec{x})$ $\forall \vec{x}, \vec{y} \in V$
3) triangular inequality: $d(\vec{x}, \vec{z}) \leq d(\vec{x}, \vec{y}) + d(\vec{y}, \vec{z})$

## page 6

Def Angle

Law of cosine.

$$\|\vec{u} - \vec{v}\|^2 = \|\vec{u}\|^2 + \|\vec{v}\|^2 - 2\|\vec{u}\|\|\vec{v}\|\cos\theta$$

note that $\langle \vec{u} - \vec{v},\ \vec{u} - \vec{v}\rangle = \|\vec{u}\|^2 + \|\vec{v}\|^2 - 2\langle \vec{u}, \vec{v}\rangle$

$$\Rightarrow \langle \vec{u}, \vec{v}\rangle = \|\vec{u}\|\|\vec{v}\|\cos\theta \ \checkmark$$

Assume that $\vec{x} \neq \vec{0}$, $\vec{y} \neq \vec{0}$, then

$$-1 \leq \frac{\langle \vec{x}, \vec{y}\rangle}{\|\vec{x}\|\|\vec{y}\|} \leq 1 \qquad \Rightarrow \cos\theta = \frac{\langle \vec{x}, \vec{y}\rangle}{\|\vec{x}\|\|\vec{y}\|}$$

$\theta \in [0,\pi]$ is called the angle between $\vec{x}$, $\vec{y}$.

$\vec{x} \perp \vec{y} \Rightarrow \langle \vec{x}, \vec{y}\rangle = 0 \Rightarrow \vec{x}$ and $\vec{y}$ are orthogonal.

Furthermore, if $\vec{x}$ and $\vec{y}$ are orthogonal and $\|\vec{x}\| = \|\vec{y}\| = 1$ then $\vec{x}$ and $\vec{y}$ are both orthonormal.

Def. Orthogonal Matrix.

A square matrix $A \in \mathbb{R}^{n \times n}$ is an orthogonal matrix if its columns are orthonormal,

$$A^T A = A A^T = I \quad \text{implies} \quad A^{-1} = A^T$$

$\Rightarrow$ inverse is obtained by simply transposing the matrix.

$$A^T A = \begin{bmatrix} \vec{a}_1^T \\ \vec{a}_2^T \\ \vdots \\ \vec{a}_n^T \end{bmatrix} \begin{bmatrix} \vec{a}_1 & \cdots & \vec{a}_n \end{bmatrix} = \begin{bmatrix} \vec{a}_1^T \vec{a}_1 & \vec{a}_1^T \vec{a}_2 & \cdots & \vec{a}_1^T \vec{a}_n \\ \vec{a}_2^T \vec{a}_1 & - & - & - \\ \vdots & & \ddots & \\ \vec{a}_n^T \vec{a}_1 & - & - & \cdots \ \vec{a}_n^T \vec{a}_n \end{bmatrix} = \begin{bmatrix} 1 & & 0 \\ & \ddots & \\ 0 & & 1 \end{bmatrix}$$

Remark: Transformations by orthogonal matrices do NOT change the length of a vector

$$\|A\vec{x}\|^2 = (A\vec{x})^T A\vec{x} = \vec{x}^T A^T A \vec{x} = \vec{x}^T I \vec{x} = \vec{x}^T \vec{x} = \|\vec{x}\|^2$$

Self learning: orthonormal basis (sec 3.5)
orthonormal complement (sec 3.6)

## page 7

★ Inner product of functions.

Given two functions, $u, v : \mathbb{R} \mapsto \mathbb{R}$, the inner product of $u$ and $v$ is defined as $\langle u, v \rangle := \int_a^b u(x)v(x)dx$, with $a, b < \infty$

A generalization of inner product to infinite number of entries

Remark: norm and orthogonality of a functions (among functions) can also be define in a similar way (sum → integral)

Related concept: convolution of two function.

$u * v\ (t) = \int_0^t f(\tau)g(t-\tau)d\tau$

→ convolutional neural networks → image recognition

Summary:

- general inner product
 - → extended to → convolution, function
 - ← positive definite matrix
 - ↓ induce
 - norm → length
 - → distance (metric)
 - → angle → orthogonal $\xrightarrow{\text{norm}=1}$ orthonormal → orthonormal basis
- $\|y - \hat{y}\|$ minimize sth. within is a norm space (induced by some inner product)