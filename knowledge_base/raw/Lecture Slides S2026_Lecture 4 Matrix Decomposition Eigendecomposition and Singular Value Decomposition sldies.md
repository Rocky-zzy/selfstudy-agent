# Lecture Slides S2026\Lecture 4 Matrix Decomposition Eigendecomposition and Singular Value Decomposition sldies.pdf

## page 1

Matrix Decomposition: Eigendecomposition and singular value decomposition.

$\vec{x}$ -> [diagram: input nodes with arrows crossing to output nodes] -> $\vec{y}$ 
$\vec{y} = W\vec{x} + \vec{b}$

observation: ① for some $W$, some small deviation in $\vec{x}$ 
$\quad\quad\quad\quad\quad\quad$ $\Rightarrow$ large change in output ($\vec{y}$) 
$\quad\quad\quad\quad$ ② for some $W$, small deviation in $\vec{x}$ results in [unreadable] deviation in $\vec{y}$ 
$\quad\quad$ $\Rightarrow$ how $W$ effect the input-output relation 
$\quad$ $\Rightarrow$ Eigendecomposition and Singular-value decomposition.

---

1. Eigenvalue and eigenvector.

Def: Let $A \in \mathbb{R}^{n \times n}$ be a square matrix, then 1) $\lambda \in \mathbb{R}$ is an eigenvalue of $A$ and $\vec{x} \in \mathbb{R}^n \setminus \{\vec{0}\}$ is the corresponding eigenvector of $A$, if 
$$A\vec{x} = \lambda\vec{x}$$

Remark 1: $\vec{x}$ is a particular direction in space s.t. the linear transformation from $\vec{x}$ to $A\vec{x}$ is equivalent to stretching the vector $\vec{x}$ with parameter $\lambda$

Special case: Diagonal matrix (only stretching effect). 
$$A_{diag} = \begin{bmatrix} \lambda_1 & & \\ & \ddots & \\ & & \lambda_n \end{bmatrix} \quad A_{diag}\vec{x} = \begin{bmatrix} \lambda_1 x_1 \\ \vdots \\ \lambda_n x_n \end{bmatrix}, \quad \vec{x} = [x_1, \dots, x_n]^T$$ 
(larger $\lambda_i$, $i \in [1, n]$, larger change in output)

Remark 2: suppose that $\vec{x}$ is an eigenvector of $A$ w.r.t the eigenvalue $\lambda$, we have $A(c\vec{x}) = cA\vec{x} = \lambda(c\vec{x})$, for any $c \in \mathbb{R} \setminus \{0\} \Rightarrow c\vec{x}$ is also eigenvector.

Computation of eigenvalue 
Theorem: $\lambda \in \mathbb{R}$ is an eigenvalue of $A \in \mathbb{R}^{n \times n}$ iff $\lambda$ is a root of the characteristic polynomial of $A$. 
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad$ $\downarrow P_A(\lambda)$

Def. characteristic polynomial.

## page 2

For $\lambda \in \mathbb{R}$ and a square $A \in \mathbb{R}^{n \times n}$, the characteristic polynomial is defined as

$$\leftarrow \text{identity matrix}$$

$$p_A(\lambda) := \det(A - \lambda I)$$
$$= (-1)^n (\lambda - \lambda_1) \cdots (\lambda - \lambda_n) \quad \Rightarrow \ \lambda \text{ s.t } p_A(\lambda) = 0 \text{ root of C.P.}$$
$$= c_0 + c_1\lambda + \cdots + c_{n-1}\lambda^{n-1} + (-1)^n \lambda^n$$

note: $c_0 = \det(A) = \lambda_1 \cdots \lambda_n$ $c_{n-1} = (-1)^{n-1} \cdot tr(A)$
$= (-1)^{n-1}(\lambda_1 + \cdots + \lambda_n)$

trace = sum of eigenvalue

Remark: Formal definition and intuition of det and trace
$\Rightarrow$ Theorems 4.10 / 4.17 and discussion for Figure 4.6.

Special cases

2-D: $\det\left(\begin{bmatrix} a & b \\ c & d \end{bmatrix}\right) = \begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc$
$\qquad\qquad\qquad\qquad\qquad\qquad\qquad$ cofactor of $a_v$

3-by-3: $\det\left(\begin{pmatrix} a_{11} & a_{12} & a_{13} \\ a_{21} & a_{22} & a_{23} \\ a_{31} & a_{32} & a_{33} \end{pmatrix}\right) = (-1)^{1+1} a_{11} M_{11} + (-1)^{1+2} a_{12} M_{12} + (-1)^{1+3} a_{13} M_{13}$

$$= a_{11}\begin{vmatrix} a_{22} & a_{23} \\ a_{32} & a_{33} \end{vmatrix} - a_{12}\begin{vmatrix} a_{21} & a_{23} \\ a_{31} & a_{33} \end{vmatrix} + a_{13}\begin{vmatrix} a_{21} & a_{22} \\ a_{31} & a_{32} \end{vmatrix}$$

Example $A = \begin{bmatrix} 3 & 0 \\ 8 & -1 \end{bmatrix}$

Eigenvalue $\det(A - \lambda I) = \begin{vmatrix} 3 - \lambda & 0 \\ 8 & -1 - \lambda \end{vmatrix} = 0$
$= (3 - \lambda)(-1 - \lambda) = 0 \quad \lambda_1 = 3 \quad \lambda_2 = -1$

Eigenvector: $A\vec{x} = \lambda \vec{x}$

① $\lambda_1$: $\begin{bmatrix} 3 & 0 \\ 8 & -1 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = 3\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} \Rightarrow 3x_1 = 3x_1$
$\qquad\qquad\qquad\qquad\qquad\ \ \Rightarrow 8x_1 - x_2 = 3x_2$
$\qquad\qquad\qquad\qquad\qquad\ \ \Rightarrow 8x_1 = 4x_2 \Rightarrow x_2 = 2x_1 \quad \vec{x} = \begin{bmatrix} 1 \\ 2 \end{bmatrix}$

② $\lambda_2$: $\begin{bmatrix} 3 & 0 \\ 8 & -1 \end{bmatrix}\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = -1\begin{bmatrix} x_1 \\ x_2 \end{bmatrix} \Rightarrow 3x_1 = -x_1 \Rightarrow x_1 = 0$
$\qquad\qquad\qquad\qquad\qquad\ \ 8x_1 - x_2 = -x_2$
$\qquad\qquad\qquad\qquad\qquad\ \ x_2 \text{ can be anything} \Rightarrow \vec{x} = \begin{bmatrix} 0 \\ 1 \end{bmatrix}$

Equivalent statement

① $\lambda$ is an eigenvalue of $A$: ② $\exists \vec{x} \neq \vec{0}$, s.t. $(A - \lambda I_n)\vec{x} = \vec{0}$
③ $\text{rank}(A - \lambda I_n) < n$ ; ④ $\det(A - \lambda I_n) = 0$

Several notions about eigenvalue and eigenvector

① Algebraic Multiplicity: Consider $A \in \mathbb{R}^{n \times n}$ with eigenvalue $\lambda_i$, the algebraic multiplicity is the number of times the root appear in the characteristic polynomial, denoted by $am(\lambda_i)$

## page 3

**Example:** 
$$A = \begin{bmatrix} 3 & 2 & 2 \\ 2 & 3 & 2 \\ 2 & 2 & 3 \end{bmatrix} \quad p_A(\lambda) = -(\lambda - 1)^2(\lambda - 7)$$
$\text{am}(\lambda = 1) = 2$ 
$\text{repeated eigenvalue}$ 
$\lambda_1 = 1 \quad \lambda_2 = -7$ 
$\lambda_3 = 1$

2. **Eigenspectrum (Spectrum):** the set of all eigenvalue

3. **Eigenspace.** the set of all eigenvectors of $A$ associated with $\lambda$ spans the Eigenspace of $A$ (denote by $E_\lambda$). 
associated with $\lambda_1 = 1$, $\vec{x}_1 = \begin{bmatrix} -1 \\ 1 \\ 0 \end{bmatrix}$, $\vec{x}_2 = \begin{bmatrix} -1 \\ 0 \\ 1 \end{bmatrix}$, $E_{\lambda_1} = \text{span}(\vec{x}_1, \vec{x}_2)$ 
$\lambda_2 = 7$, $\vec{x}_3 = \begin{bmatrix} 1 \\ 1 \\ 1 \end{bmatrix} \implies E_{\lambda_2} = \text{span}(\vec{x}_3)$.

4. **Geometric multiplicity:** $\text{gm}(\lambda) := \dim(E_\lambda)$ 
remark: for any eigenvalue $\lambda$, $\text{gm}(\lambda) \le \text{am}(\lambda)$

5. **defective matrix:** A square matrix $A \in \mathbb{R}^{n \times n}$ is defective if it processes fewer than $n$ linear independent eigenvector.

**Theorem (distinct eigenvalue)** The eigenvectors $\vec{x}_1, \dots, \vec{x}_n$ of a matrix $A \in \mathbb{R}^{n \times n}$ with $n$ distinct eigenvalue $\lambda_1, \dots, \lambda_n$ are linearly independent.

**Corollary:** A defective matrix has at least one eigenvalue $\lambda$, with $\text{am}(\lambda) > 1$, $\text{am}(\lambda) > \text{gm}(\lambda)$

**Theorem 2.** If $A$ is symmetric, the eigenvectors to different eigenvalue are orthogonal.

**Proof:** Consider $\lambda, \mu \in \mathbb{R}$, with $\lambda \ne \mu$, and two vectors $\vec{v}, \vec{w} \in V$ 
s.t. $A\vec{v} = \lambda \vec{v}$, $A\vec{w} = \mu \vec{w}$, consider dot product: $\langle \cdot, \cdot \rangle$ 
$\lambda \langle \vec{v}, \vec{w} \rangle = \langle \lambda \vec{v}, \vec{w} \rangle = \langle A\vec{v}, \vec{w} \rangle = (A\vec{v})^T \vec{w} = \vec{v}^T A^T \vec{w} = \langle \vec{v}, A^T \vec{w} \rangle = \langle \vec{v}, A\vec{w} \rangle$ 
$= \langle \vec{v}, \mu \vec{w} \rangle = \mu \langle \vec{v}, \vec{w} \rangle \quad \text{note that } \lambda \ne \mu \implies \langle \vec{v}, \vec{w} \rangle = 0$ 
$\implies \vec{v} \perp \vec{w} \quad \langle \vec{v}, \vec{w} \rangle = 0$

**Theorem 3: (Spectral Theorem)** 
If $A \in \mathbb{R}^{n \times n}$ is symmetric, then there exists an orthonormal basis of the corresponding vector space $V$, which consists of the eigenvector of $A$, and each eigenvalue is real.

**Remark:** for some $\lambda$, $\text{am}(\lambda) = \text{gm}(\lambda) \ge 1 \implies$ Gram-Schmidt algorithm

## page 4

Note: consider two eigenvectors $\vec{x}_1, \vec{x}_2$, associated with $\lambda$ (eigenvalue)
$$A(\alpha \vec{x}_1 + \beta \vec{x}_2) = \alpha \cdot A\vec{x}_1 + \beta A\vec{x}_2 = \alpha \cdot \lambda \vec{x}_1 + \beta \cdot \lambda \vec{x}_2 = \lambda (\alpha \vec{x}_1 + \beta \vec{x}_2)$$
$\Rightarrow$ linear combination of $\vec{x}_1$ & $\vec{x}_2$ is also eigenvector

Theorem 4: Symmetric, positive definite matrices always have positive
real eigenvalue.

2. Eigendecomposition.
Let $A \in \mathbb{R}^{n \times n}$, $\lambda_1, \dots, \lambda_n$ being eigenvalue, with the corresponding
eigenvector $\vec{p}_1, \dots, \vec{p}_n$, we have
$$A\vec{p}_1 = \lambda_1 \vec{p}_1$$
$$A\vec{p}_2 = \lambda_2 \vec{p}_2$$
$$\vdots$$
$$A\vec{p}_n = \lambda_n \vec{p}_n$$
$$\Rightarrow A \underbrace{\left[ \vec{p}_1 \cdots \vec{p}_n \right]}_{P} = \underbrace{\left[ \lambda_1 \vec{p}_1 \cdots \lambda_n \vec{p}_n \right]}_{P} = \underbrace{\left[ \vec{p}_1 \cdots \vec{p}_n \right]}_{P} \underbrace{\begin{bmatrix} \lambda_1 & & \\ & \ddots & \\ & & \lambda_n \end{bmatrix}}_{D}$$
$$\Rightarrow AP = PD, \quad \text{if } P \text{ is invertible}$$
$$A = PDP^{-1} \quad (A \text{ is symmetric, } A = PDP^T, \text{Thm 3})$$
$\xrightarrow{\text{Eigendecomposition}}$

Remark: consider $\vec{x} \in \mathbb{R}^n$,
$A \in \mathbb{R}^{n \times n}$ has $n$ linearly independent eigenvectors
$$A\vec{x} = PDP^{-1}\vec{x}$$
① $P^{-1}\vec{x}$: transfer $\vec{x}$ to the column space of $P^{-1}$
(basis change)
, ② $DP^{-1}\vec{x}$: stretching $P^{-1}\vec{x}$ with $D$ (eigenvalue)
③ $PDP^{-1}\vec{x}$: transfer the stretched vector $DP^{-1}\vec{x}$ to
column space of $P$

In particular, $A^k = (PDP^{-1})^k = (PDP^{-1})(PDP^{-1}) \cdots (PDP^{-1}) = PD^kP^{-1}$
$\xrightarrow{I}$
$\rightarrow$ Note: "similar" to pure stretching the vectors, but under different basis
From the perspective of similarity:
A matrix $A \in \mathbb{R}^{n \times n}$ is diagonalizable, if it is similar to a diagonal
matrix $\Rightarrow \exists D \in \mathbb{R}^{n \times n}, D = P^TAP \leftarrow A = PDP^T$

$\Rightarrow$ Cholesky Decomposition (Symmetric, positive definite matrix
Sec. 4.3

## page 5

3. Singular Value Decomposition.

$$A \in \mathbb{R}^{m \times n} \quad \text{rank}(A) = r \leq \min(m, n)$$

[Diagram showing matrix factorization: $A$ ($m \times n$) = $U$ ($m \times m$) $\Sigma$ ($m \times n$) $V^T$ ($n \times n$), with a pointer to $\Sigma$ showing a diagonal matrix with $\sigma_1 \dots \sigma_r$ and zeros elsewhere. Text "any matrix!" is written next to the diagram.]

* $U \in \mathbb{R}^{m \times m}$ with orthogonal column vectors $\vec{u}_i, i = 1, \dots, m$
* $V \in \mathbb{R}^{n \times n}$ ------------------ $\vec{v}_j, j = 1, \dots, n$
* $\Sigma \in \mathbb{R}^{m \times n}$, with $\Sigma_{ii} = \sigma_i \geq 0$, $\Sigma_{ij} = 0$, with $i \neq j$.
 * $\sigma_1 \geq \sigma_2 \geq \dots \geq \sigma_r \geq 0 \leftarrow$ singular value.
 * $\vec{u}_i$: left-singular vectors $\quad$ $\vec{v}_j$: right-singular vectors

---

Relation with eigendecomposition.

For symmetric, positive definite matrix $S$
Eigendecomposition: $S = P D P^{-1} = P D P^T$ ($P$ can be orthonormal)
SVD: $S = U \Sigma V^T \quad U = P = V, \quad D = \Sigma$

For symmetric positive definite matrix, SVD and eigendecomposition can be the same, i.e. decompose the matrix (linear transformation) as rotation - scale - rotation.

---

Construction of SVD ($U, \Sigma, V$)
✓ ① construction of $V$ $\quad$ $\leftarrow$ orthonormal.

$A^T A = (U \Sigma V^T)^T (U \Sigma V^T) = V \Sigma^T U^T U \Sigma V^T = V \Sigma^T \Sigma V^T$

$$= V \begin{bmatrix} \sigma_1^2 & & \\ & \ddots & \\ & & \sigma_n^2 \end{bmatrix} V^T$$
$\quad$ $\quad$ $\quad$ $\quad$ $\underbrace{\hspace{2.5cm}}$ Eigendecomposition of $A^T A$

$\Rightarrow V^T = P^T$ (eigenvector of $A^T A$), $\sigma_i^2 = \lambda_i$ (eigenvalue of $A^T A$).

✓ ② construction of $U$.

$A A^T = U \Sigma V^T (U \Sigma V^T)^T = U \Sigma \underbrace{V^T V}_{I} \Sigma^T U^T = U \Sigma \Sigma^T U^T = U \begin{bmatrix} \sigma_1^2 & & \\ & \ddots & \\ & & \sigma_m^2 \end{bmatrix} U^T$

## page 6

$\Rightarrow AA^T$ is symmetric $\Rightarrow$ $U$ contains (orthonormal) eigenvector of $AA^T$
$\sigma_i^2 = \lambda_i$ (eigenvalue of $AA^T$)

$AA^T$ and $A^TA$ have the same eigenvalues (not eigenvectors)
Proof: Consider $A \in \mathbb{R}^{m \times n}$, $\lambda \neq 0$ and $\vec{v}$ being eigenvector of $A^TA$
$A^TA\vec{v} = \lambda\vec{v}$, left multiplication of $A$:
$\star$ $AA^T(A\vec{v}) = A(A^TA\vec{v}) = A(\lambda\vec{v}) = \lambda(A\vec{v})$
$\Rightarrow \lambda$ is the eigenvalue of $AA^T$ with the corresponding eigenvector $A\vec{v}$
$\Rightarrow$ any non-zero eigenvalue $\lambda$ of $A^TA$ is also an eigenvalue of that of $AA^T$
Similarly, consider $\beta \neq 0$ being eigenvalue of $AA^T$, with eigenvector $\vec{u}$, s.t. $AA^T\vec{u} = \beta\vec{u}$, multiplying $A^T$ on both side
$A^T(AA^T\vec{u}) = A^TAA^T\vec{u} = \beta A^T\vec{u} \Rightarrow \beta$ is an eigenvalue of $A^TA$

$\Rightarrow$ $\sigma_1^2 \dots \sigma_n^2$ and $\sigma_1^2 \dots \sigma_m^2$ are consistent

Computational method: ① $A = U\Sigma V^T \Rightarrow AV = U\Sigma V^TV = U\Sigma$
$\Rightarrow$ $A \cdot [\vec{v}_1 \dots \vec{v}_n] = [\vec{u}_1 \dots \vec{u}_m] \begin{bmatrix} \sigma_1 & & \text{\huge0} \\ & \ddots & \\ \text{\huge0} & & \sigma_r \\ & & \end{bmatrix}_{m \times n}$
$m \times n$ $\quad$ $n \times n$
$A\vec{v}_i = \sigma_i\vec{u}_i$, $i=1,\dots,r \Rightarrow \vec{u}_i = \frac{1}{\sigma_i}A\vec{v}_i$
remark: for $i = r+1, \dots, m$, $\vec{u}_i$ can be any unit vector which is perpendicular to $\vec{u}_i$ with $i=1,\dots,r$

Exercise: $A = [2 \quad 1]$, perform SVD
① compute orthonormal eigenvector of $A^TA$.
$A^TA = \begin{bmatrix} 2 \\ 1 \end{bmatrix} [2 \quad 1] = \begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix}$
$\det(A^TA - \lambda I) = \begin{vmatrix} 4-\lambda & 2 \\ 2 & 1-\lambda \end{vmatrix} = (4-\lambda)(1-\lambda) - 4$
$= \lambda^2 - 5\lambda + 4 - 4 = \lambda^2 - 5\lambda = \lambda(\lambda - 5)$
$\lambda_1 = 5, \lambda_2 = 0$

## page 7

1) $\lambda_1 = 5$
$$\begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = 5 \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} \implies \begin{cases} 4x_1 + 2x_2 = 5x_1 \\ 2x_1 + x_2 = 5x_2 \end{cases} \implies 2x_2 = x_1$$
$\sigma_1^2$ (in red)
$\vec{v}_1 = \begin{bmatrix} 2/\sqrt{5} \\ 1/\sqrt{5} \end{bmatrix}$

2) $\lambda_2 = 0$
$$\begin{bmatrix} 4 & 2 \\ 2 & 1 \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \end{bmatrix} \implies \begin{cases} 4x_1 + 2x_2 = 0 \\ 2x_1 + x_2 = 0 \end{cases} \implies 2x_1 = -x_2$$
$\vec{v}_2 = \begin{bmatrix} -1/\sqrt{5} \\ 2/\sqrt{5} \end{bmatrix}$
$\vec{v}_1 \perp \vec{v}_2$

② $\vec{u}_1 = \frac{1}{\sigma_1} A \vec{v}_1 = \frac{1}{\sqrt{5}} \begin{bmatrix} 2 & 1 \end{bmatrix} \begin{bmatrix} 2/\sqrt{5} \\ 1/\sqrt{5} \end{bmatrix} = 1$
$V^T$

$$A = 1 \times \begin{bmatrix} \sqrt{5} & 0 \end{bmatrix} \begin{bmatrix} 2/\sqrt{5} & 1/\sqrt{5} \\ -1/\sqrt{5} & 2/\sqrt{5} \end{bmatrix}$$

Matrix Approximation

[Diagram of a grid matrix]

- Large matrix, only part of the data is crucial
- consider matrix approximation
- key question: ① how to perform the approximation? ✓
 ② how to quantify the error?

$$A = \begin{bmatrix} \vec{u}_1 \dots \vec{u}_m \end{bmatrix} \begin{bmatrix} \sigma_1 & & \\ & \ddots & \\ & & \sigma_r & \\ & & & \ddots \end{bmatrix} \begin{bmatrix} \vec{v}_1^T \\ \vdots \\ \vec{v}_n^T \end{bmatrix} = \sum_{i=1}^r \sigma_i \vec{u}_i \cdot \vec{v}_i^T \quad \text{outer product}$$
(underbrace $m \times m$ under the left matrix)
$$= \sum_{i=1}^r \sigma_i A_i \quad \text{(circled)} \qquad A_i = \vec{u}_i \cdot \vec{v}_i^T$$
(underbrace $m \times 1$ under $\vec{u}_i$, underbrace $1 \times n$ under $\vec{v}_i^T$)

Approximation up to rank - $k$
$$\hat{A}(k) = \sum_{i=1}^k \sigma_k A_k \quad \text{with } k \le r$$
how good is such an approximation?

Def: (Spectral norm) For $\vec{x} \in \mathbb{R}^n \setminus \{0\}$, the spectral norm of $A \in \mathbb{R}^{m \times n}$ is defined as:
$$\|A\|_2 = \max_{\vec{x} \in \mathbb{R}^n} \frac{\|A \vec{x}\|_2}{\|\vec{x}\|_2}$$

Theorem: $\|A\|_2 = \text{largest singular value } \sigma_1 \text{ of } A$

$\star$ Eckart - Young Theorem

Consider $A \in \mathbb{R}^{m \times n}$ of rank $r$ and let $B \in \mathbb{R}^{m \times n}$ be a matrix of rank $k$. Then for any $k \le r$ with $\hat{A}(k) = \sum_{i=1}^k \sigma_i \vec{u}_i \vec{v}_i^T$, it holds that

① $\hat{A}(k) = \arg\min_{\text{rank}(B)=k} \|A - B\|_2$ (best approximation)

## page 8

② $\|A - \hat{A}(k)\|_2 = \sigma_{k+1}$ Show large is the approximation error.
Sec 4.2 - 4.6