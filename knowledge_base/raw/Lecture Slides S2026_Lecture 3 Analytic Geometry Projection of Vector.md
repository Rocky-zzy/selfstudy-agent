# Lecture Slides S2026\Lecture 3 Analytic Geometry Projection of Vector.pdf

## page 1

Analytic Geometry 3: Projection of vector.

* In machine learning, there are a lot of high dimensional data. $\longrightarrow$ hard to analyze
* only a few dimension is of interest.
* Try to project the original high-dimensional data on to a lower dimensional space.
* How to project in a correct way

principle component analysis

1. projection : Let $V$ be a vector space and $U \subseteq V$ be a subspace of $V$
A linear mapping $\pi : V \mapsto U$ is called a projection if $\pi^2 = \pi \circ \pi = \pi$
transformation matrix $P_\pi \Rightarrow P_\pi^2 = P_\pi \cdot P_\pi = P_\pi$
Remark: Projecting n times $\iff$ projecting once.

2. Projection onto 1-D space.
(1) $\pi_U(\vec{x})$ is an element $U$ that is closest to $\vec{x}$, i.e.
 1) $\exists \lambda \in \mathbb{R}$, $\pi_U(\vec{x}) = \lambda \vec{b}$, with $\vec{b}$ being the basis vector of $U$
 2) inner product. $\langle \vec{x} - \pi_U(\vec{x}), \vec{b} \rangle = 0$
(2) What is $\lambda$? 1), 2) $\Rightarrow \langle \vec{x} - \lambda \vec{b}, \vec{b} \rangle = 0$
 $\iff \langle \vec{x}, \vec{b} \rangle - \lambda \langle \vec{b}, \vec{b} \rangle = 0$
 $\iff \lambda = \frac{\langle \vec{x}, \vec{b} \rangle}{\langle \vec{b}, \vec{b} \rangle} = \frac{\vec{b}^T \vec{x}}{\vec{b}^T \vec{b}}$
(3) norm of projection $\pi_U(\vec{x})$
 $\| \pi_U(\vec{x}) \| = \| \lambda \vec{b} \| = \| \frac{\vec{b}^T \vec{x}}{\| \vec{b} \|^2} \vec{b} \| = \frac{1}{\| \vec{b} \|^2} \| \vec{b}^T \vec{x} \| \| \vec{b} \| = \frac{\| \vec{b}^T \vec{x} \|}{\| \vec{b} \|}$
 $\| \vec{b}^T \vec{x} \| = \| \vec{b} \| \| \vec{x} \| \cos \theta$
 $\| \pi_U(\vec{x}) \| = | \cos \theta | \| \vec{x} \|$
 bilinear map: $f(\alpha \vec{x} + \beta \vec{y}, \vec{z}) = \alpha f(\vec{x}, \vec{z}) + \beta f(\vec{y}, \vec{z})$
(4) What is $P_\pi$?
 $\pi_U(\vec{x}) = \lambda \vec{b} = \vec{b} \lambda = \vec{b} \cdot \frac{\vec{b}^T \vec{x}}{\| \vec{b} \|^2} \Rightarrow P_\pi = \frac{\vec{b} \vec{b}^T}{\| \vec{b} \|^2}$
 $P_\pi \vec{x}$

3. Projection onto m-dimensional space $(m \ge 1)$
 $\Rightarrow$ extension from 1-D case
(1) $\pi_U(\vec{x})$ is an element on $U$ that is closest to $\vec{x}$
 1) $\exists \lambda_i \in \mathbb{R}, i \in [1, m], \pi_U(\vec{x}) = \sum_{i=1}^m \lambda_i \vec{b}_i$

## page 2

2) inner product $\quad \vec{x}-\pi_U(\vec{x}) \perp \{\vec{b}_1,\, \vec{b}_2,\, \dots \vec{b}_m\}$, i.e.

$$
\begin{cases}
\langle \vec{b}_1,\ \vec{x}-\pi_U(\vec{x})\rangle = \vec{b}_1^{T}\big(\vec{x}-\pi_U(\vec{x})\big) = 0 \\[4pt]
\qquad \vdots \\[4pt]
\langle \vec{b}_m,\ \vec{x}-\pi_U(\vec{x})\rangle = \vec{b}_m^{T}\big(\vec{x}-\pi_U(\vec{x})\big) = 0
\end{cases}
\qquad\text{let } B=\big[\,\vec{b}_1\ \cdots\ \vec{b}_m\,\big]
$$

$$\pi_U(\vec{x})=\sum_{i=1}^{m}\lambda_i\vec{b}_i = B\vec{\lambda}\qquad \vec{\lambda}=[\lambda_1,\ \lambda_2\ \cdots\ \lambda_m]^{T}$$

$$\vec{b}_1^{T}\big(\vec{x}-B\vec{\lambda}\big)=0$$
$$\qquad\vdots$$
$$\vec{b}_m^{T}\big(\vec{x}-B\vec{\lambda}\big)=0$$

$$\Rightarrow\quad
\begin{bmatrix}
\vec{b}_1^{T}\\
\vdots\\
\vec{b}_m^{T}
\end{bmatrix}
\big[\vec{x}-B\vec{\lambda}\big]=\vec{0}
\iff\ B^{T}\big(\vec{x}-B\vec{\lambda}\big)=\vec{0}$$

$$\iff\ B^{T}\vec{x}=\underline{B^{T}B}\,\lambda$$

since $B$ consists of basis of $U$ (linear independent) $\Rightarrow$ $B$ has full rank.
$B^{T}B$ is invertible $\Rightarrow$ $\lambda=(B^{T}B)^{-1}B^{T}\vec{x}$

$$\Rightarrow\ \pi_U(\vec{x})=B\vec{\lambda}=B\,(B^{T}B)^{-1}B^{T}\vec{x}\quad\Rightarrow\quad \text{projection matrix } P_\pi=B\,(B^{T}B)^{-1}B^{T}$$
$$\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad\qquad=\frac{BB^{T}}{B^{T}B}$$

---
Remark: rank$(A^{T}A)=$ rank$(A)$ for any matrix $A\in\mathbb{R}^{n\times n}$.
According to Rank-Nullity Theorem, for any $A\in\mathbb{R}^{n\times m}$, $\quad A\vec{x}=\vec{0}$
$\qquad\qquad$ rank$(A)$ + nullity$(A)=n$.
we want to show rank$(A)=$ rank$(A^{T}A)$ by showing
$\qquad\qquad$ null$(A)=$ null$(A^{T}A)$ ✓

How to prove set $A=B$ ? $\Rightarrow$ $A\subseteq B$ and $B\subseteq A$

① showing null$(A)\subseteq$ null$(A^{T}A)$
for any $\vec{x}\in$ null$(A)$, we need to show $\vec{x}\in$ null$(A^{T}A)$
$\Rightarrow A\vec{x}=\vec{0}$, one has $A^{T}(A\vec{x})=\vec{0}$ $\Rightarrow$ $A^{T}A\vec{x}=\vec{0}$, $\vec{x}\in$ null$(A^{T}A)$
$\Rightarrow$ null$(A)\subseteq$ null$(A^{T}A)$ (a)

② show null$(A^{T}A)\subseteq$ null$(A)$
for any $\vec{x}\in$ null$(A^{T}A)$, $A^{T}A\vec{x}=\vec{0}$, therefore $\vec{x}^{T}A^{T}A\vec{x}=0=(A\vec{x})^{T}A\vec{x}=\|A\vec{x}\|^2=0$
$\Rightarrow A\vec{x}=\vec{0}$ $\Rightarrow x\in$ null$(A)$ $\Rightarrow$ null$(A^{T}A)\subseteq$ null$(A)$. (b)
(a) (b) $\Rightarrow$ null$(A)=$ null$(A^{T}A)$.

consider any $B$, we need to compute $(B^{T}B)^{-1}$, which is
expensive, unless $B^{T}B=I$, meaning that $B$ contains an
orthonormal basis.

## page 3

2、Gram–Schmidt Orthogonalization

Goal : Transforming a basis $(\vec b_1, \dots, \vec b_n)$ of an n-dimensional vector space $V$ into an orthogonal / orthonormal basis of $V$

[diagram: $\vec u_1 = \vec b_1$; axes labeled $\vec b_1$, $\vec b_2$; arrow "projection"]

$$\vec u_2 = \vec b_2 - \pi_{\operatorname{span}(\vec b_1)}(\vec b_1)$$

[labels in diagram: $\vec b_1$, $\vec b_2$, $\pi_{\operatorname{span}(\vec b_1)}(\vec b_2)$, "side product"]

Key idea : find a vector that is perpendicular to $\vec u_1$ and $\vec u_2$,

[diagram labels: $\vec b_3$, $\vec u_1$, $\vec u_2$, projection :!, $\pi_{\operatorname{span}(\vec u_1, \vec u_2)}(\vec b_3)$]

$$\vec u_3 = \vec b_3 - \pi_{\operatorname{span}(\vec u_1, \vec u_2)}(\vec b_3) \quad , \quad \text{Let } M = [\vec u_1, \vec u_2]$$

$$= \vec b_3 - M\underset{\lambda I}{(M^T M)^{-1}} M^T \vec b_3 = \vec b_3 - \lambda M M^T \vec b_3$$

or

$$\vec u_3 = \vec b_3 - \frac{\vec u_1 \vec u_1^T}{\|\vec u_1\|^2} \vec b_3 - \frac{\vec u_2 \vec u_2^T}{\|\vec u_2\|^2} \vec b_3 \qquad \text{(can be computed recursively)}$$

$\Rightarrow$ for n-dimensional basis, we obtain a set of orthogonal basis based on $[\vec b_1, \dots, \vec b_n]$ by recursively doing.

$$\vec u_1 = \vec b_1$$

$$\vec u_2 = \vec b_2 - \pi_{\operatorname{span}\{\vec u_1\}}(\vec b_2) = \vec b_2 - \pi_{\vec u_1}(\vec b_2)$$

$$\vdots$$

$$\vec u_k = \vec b_k - \pi_{\operatorname{span}[\vec u_1 \dots \vec u_{k-1}]}(\vec b_k) = \vec b_k - \sum_{i=1}^{k-1} \pi_{\vec u_i}(\vec b_k)$$

then normalize $\vec u_1 \dots \vec u_n$ by

$$\vec e_i = \frac{\vec u_i}{\|\vec u_i\|}$$

Example $\quad \vec a = \begin{bmatrix} 1 \\ 1 \end{bmatrix}, \quad \vec b = \begin{bmatrix} 0 \\ 2 \end{bmatrix}, \quad$ compute an orthonormal basis with Gram–Schmidt orthogonalization.

answer : $\quad \vec u_1 = \vec a = \begin{bmatrix} 1 \\ 1 \end{bmatrix}, \quad \vec u_2 = \vec b - \frac{\vec a \vec a^T}{\|\vec a\|^2} \vec b = \vec b - \frac{\vec a^T \vec b}{\|\vec a\|^2} \vec a$

$$= \begin{bmatrix} 0 \\ 2 \end{bmatrix} - \frac{3}{(\sqrt{2})^2} \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} 0 \\ 2 \end{bmatrix} - \begin{bmatrix} 1 \\ 1 \end{bmatrix} = \begin{bmatrix} -1 \\ 1 \end{bmatrix}$$

## page 4

$$ \vec{u}_1^T \vec{u}_1 = 1 \times 0 + 1 \times (-1) + 1 \times 1 = 0 \quad \vec{u}_1 \perp \vec{u}_2 $$

normalization
$$ \vec{e}_1 = \frac{\vec{u}_1}{\|\vec{u}_1\|} = \frac{[1 \quad 1 \quad 1]^T}{\sqrt{3}} = \begin{bmatrix} 1/\sqrt{3} \\ 1/\sqrt{3} \\ 1/\sqrt{3} \end{bmatrix}, \quad \vec{e}_2 = \frac{\vec{u}_2}{\|\vec{u}_2\|} = \frac{[0 \quad -1 \quad 1]^T}{\sqrt{2}} = \begin{bmatrix} 0 \\ -1/\sqrt{2} \\ 1/\sqrt{2} \end{bmatrix} $$

---

4. Projection onto an affine space

[Diagram: Left shows a line/plane $L$ spanned by $\vec{b}_1, \vec{b}_2$; a vector $\vec{x}$ projects to $T_L(\vec{x})$ with residual $\vec{x} - \vec{x}_0$. Right shows $U = \text{span}([\vec{b}_1, \vec{b}_2])$ and $L = \vec{x}_0 + U$, projecting $\vec{x} - \vec{x}_0$.]

$$ U = \text{span}([\vec{b}_1, \vec{b}_2]) $$
$$ L = \vec{x}_0 + U $$
step 1: project $\vec{x} - \vec{x}_0$ onto $U$. 
$$ \pi_U(\vec{x} - \vec{x}_0) $$
step 2: Translate $\pi_U(\vec{x} - \vec{x}_0)$ back to $L$ by adding $\vec{x}_0$
$$ \implies \pi_L(\vec{x}) = \vec{x}_0 + \pi_U(\vec{x} - \vec{x}_0) \quad \vec{x}_0 = 0 \quad \vec{x}_0 $$

---

5. Rotation

1) Rotation in $\mathbb{R}^2$. Consider a standard basis $\vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix} \quad \vec{e}_2 = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

[Diagram: Rotation of basis vectors by angle $\theta$.]

$$ \phi(\vec{e}_1) = [\cos\theta, \sin\theta]^T $$
$$ \phi(\vec{e}_2) = [-\sin\theta, \cos\theta]^T $$
$$ P(\theta) = [\phi(\vec{e}_1) \quad \phi(\vec{e}_2)] = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} $$
Rotation matrix

$$ \vec{x} \xrightarrow{\text{rotate } \theta} R(\theta)\vec{x} $$
$$ \vec{e}_1 = \begin{bmatrix} 1 \\ 0 \end{bmatrix} \quad R(\theta)\vec{e}_1 = \begin{bmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{bmatrix} \begin{bmatrix} 1 \\ 0 \end{bmatrix} = \begin{bmatrix} \cos\theta \\ \sin\theta \end{bmatrix} $$

$\implies$ Rotation is a linear mapping

In 2-D case: given rotation angle $\theta$, vector $\vec{x}$.
$$ \vec{x}_{\text{new}} = R(\theta)\vec{x} $$
$\uparrow$ positive direction $\rightarrow$ counter-clock-wise

2) Rotation in $\mathbb{R}^3$

we can consider the rotation of any two dimensional plane about 1-D axis

[Diagram: 3D coordinate system with axes $\vec{e}_1, \vec{e}_2, \vec{e}_3$.]

(1) Rotation about $\vec{e}_1$-axis
$$ R_1(\theta) = [ \phi(\vec{e}_1) \quad \phi(\vec{e}_2) \quad \phi(\vec{e}_3) ] = \begin{bmatrix} 1 & 0 & 0 \\ 0 & \cos\theta & -\sin\theta \\ 0 & \sin\theta & \cos\theta \end{bmatrix} $$

(2) rotating about $\vec{e}_2$-axis
$$ R_2(\theta) = \begin{bmatrix} \cos\theta & 0 & \sin\theta \\ 0 & 1 & 0 \\ -\sin\theta & 0 & \cos\theta \end{bmatrix} $$

(3) rotating about $\vec{e}_3$-axis
$$ R_3(\theta) = \begin{bmatrix} \cos\theta & -\sin\theta & 0 \\ \sin\theta & \cos\theta & 0 \\ 0 & 0 & 1 \end{bmatrix} $$

## page 5

General rotation can be treated as combination of 3 of the basic notation above.

(3) property of rotations.

① preserve distance: $\forall \vec{x}, \vec{y} \in V \quad \| \vec{x} - \vec{y} \| = \| R_\theta(\vec{x}) - R_\theta(\vec{y}) \|$

② preserve angle: angle between $\vec{x}$ and $\vec{y}$ = angle between $R_\theta(\vec{x})$ and $R_\theta(\vec{y})$

③ for $n \geq 3$, rotation matrices are NOT commutative.
$\forall \vec{x} \in \mathbb{R}^n \quad n \geq 3, \quad R(\theta_1)R(\theta_2)\vec{x} \neq R(\theta_2)R(\theta_1)\vec{x}$, in general

Section 3.8 - 3.9