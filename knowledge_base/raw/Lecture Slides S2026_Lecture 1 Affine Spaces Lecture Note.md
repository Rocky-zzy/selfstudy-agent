# Lecture Slides S2026\Lecture 1 Affine Spaces Lecture Note.pdf

## page 1

Affine space and its generation 1: Vector space and its generation

$W_{ij}$: weight from $x_j$ to $y_i$, $b_i$: weight from $1$ to $y_i$

$$y_1 = W_{11}x_1 + W_{21}x_2 + W_{31}x_3 + b_1$$
$$y_2 = W_{12}x_1 + W_{22}x_2 + W_{32}x_3 + b_2$$
$$y_3 = W_{13}x_1 + W_{23}x_2 + W_{33}x_3 + b_3$$

$\Rightarrow$ compact form:
$$
\begin{bmatrix} y_1 \\ y_2 \\ y_3 \end{bmatrix} =
\begin{bmatrix} W_{11} & W_{21} & W_{31} \\ W_{12} & W_{22} & W_{32} \\ W_{13} & W_{23} & W_{33} \end{bmatrix}
\begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} +
\begin{bmatrix} b_1 \\ b_2 \\ b_3 \end{bmatrix}
$$
$\quad\quad\quad\quad\quad\quad\quad\quad \underbrace{\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad}$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \vec{y} \quad\quad\quad\quad\quad\quad\quad\quad \underbrace{\quad\quad\quad\quad\quad\quad\quad\quad\quad} \quad\quad \underbrace{\quad\quad\quad} \quad\quad \underbrace{\quad\quad}$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad W \quad\quad\quad\quad\quad\quad\quad \vec{x} \quad\quad\quad \vec{b}$

$\Rightarrow \boxed{\vec{y} = W\vec{x} + \vec{b}} \rightarrow$ affine mapping
$\quad\quad\quad\quad \underbrace{\quad\quad\quad\quad\quad\quad\quad\quad}$
$\quad\quad\quad\quad$ linear mapping $\rightarrow$ Vector space

1. Group
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad$ a notation $\quad\quad$ Cartesian product.
Consider a set $G$ and an operation $\otimes : G \times G \rightarrow G$ defined on $G$.
Then $G: (G, \otimes)$ is called a group if the following hold:
$\quad\quad\quad$ for all $\quad$ belongs to
① $\forall x, y \in G \quad x \otimes y \in G$ : The set is closed w.r.t. the operation
② $\forall x, y, z \in G , \quad (x \otimes y) \otimes z = x \otimes (y \otimes z) \quad$ Associativity
③ $\exists e \in G$ s.t. $\forall x \in G , \quad x \otimes e = e \otimes x = x \quad$ Identity element.
④ $\forall x \in G , \exists y \in G$ such that $x \otimes y = y \otimes x = e$. We denote by $x^{-1}$ the inverse element of $x$. Every element has its inverse in its group.
Specifically, $G$ is an Abelian group if.
$\quad$ ① $G$ is a group. ② $\forall x, y \in G , \quad x \otimes y = y \otimes x \quad$ Commutativity

① Example $(\mathbb{R} \setminus \{0\}, \cdot)$ is an Abelian group
proof: ① $\forall a, b \in \mathbb{R} \setminus \{0\} , \quad a \cdot b \in \mathbb{R} \setminus \{0\}$
$\quad\quad$ ② $\forall a, b, c \in \mathbb{R} \setminus \{0\} , \quad (a \cdot b) \cdot c = a \cdot (b \cdot c)$
$\quad\quad$ ③ consider $1 \in \mathbb{R} \setminus \{0\} , \quad \forall a \in \mathbb{R} \setminus \{0\} , \quad a \cdot 1 = 1 \cdot a = a$.
$\quad\quad$ ④ $\forall a \in \mathbb{R} \setminus \{0\} ,$ we have $a \cdot \frac{1}{a} = \frac{1}{a} \cdot a = 1$
$\quad\quad$ ⑤ $\forall a, b \in \mathbb{R} \setminus \{0\} , \quad a \cdot b = b \cdot a$

## page 2

Exercise : $(\mathbb{R}, +)$ is an Abelian Group.

① $\forall a, b \in \mathbb{R}$, $a+b \in \mathbb{R}$
② $\forall a, b, c \in \mathbb{R}$, $(a+b)+c = a+(b+c)$
③ consider $0 \in \mathbb{R}$, $\forall a \in \mathbb{R}$, $a+0 = 0+a = a$.
④ $\forall a \in \mathbb{R}$, we have $a+(-a) = -a+a = 0$
⑤ $\forall a, b \in \mathbb{R}$, $a+b = b+a$

Example: $(\mathbb{R}, \cdot)$ is not a group
④ for $0 \in \mathbb{R}$, $\nexists a \in \mathbb{R}$, s.t. $a \cdot 0 = 1$ ✓

2. Vector space
A real-valued vector space $V := (v, +, \cdot)$ is a set with two operation:
1) $+ : V \times V \mapsto V$
addition of vectors
2) $\cdot : \mathbb{R} \times V \mapsto V$
multiplication of vector by scalars

where 1) $(V, +)$ is an Abelian group
2) Distributivity (over $\mathbb{R}$) holds:
① $\forall \lambda \in \mathbb{R}$, $\forall \vec{x}, \vec{y} \in V : \lambda \cdot (\vec{x} + \vec{y}) = \lambda \cdot \vec{x} + \lambda \cdot \vec{y}$
② $\forall \lambda, \psi \in \mathbb{R}$, $\forall \vec{x} \in V : (\lambda + \psi) \cdot \vec{x} = \lambda \cdot \vec{x} + \psi \cdot \vec{x}$
3) $\forall \lambda, \psi \in \mathbb{R}$, $\forall \vec{x} \in V$, $\lambda \cdot (\psi \cdot \vec{x}) = (\lambda \psi) \cdot \vec{x}$
4) $\forall \vec{x} \in V : 1 \cdot \vec{x} = \vec{x}$

Space: a set with special structure among elements
operation

3. Vector subspace
Let ① A vector space $V = (v, +, \cdot)$ ; ② $U \subseteq V$ and $U \neq \emptyset$ real subset
Then, $U := (u, +, \cdot)$ is called a vector subspace of $V$, if
① $U$ is a vector space with the operation $+$ and $\cdot$ restriction
to $u \times u$ and $\mathbb{R} \times u$, respectively. $\Rightarrow$ Denote by $U \leq V$

3.1) Linear Combination.
Consider a vector space $V := (v, +, \cdot)$, and a finite number of
vectors $\vec{x}_1, \dots, \vec{x}_k \in V$. Then, every $\vec{v} \in V$ of the form

## page 3

$\vec{v} = \lambda_1 \vec{x}_1 + \lambda_2 \vec{x}_2 + \dots + \lambda_k \vec{x}_k = \sum_{i=1}^{k} \lambda_i \vec{x}_i \in V$

with $\lambda_1, \dots, \lambda_k \in \mathbb{R}$ is a linear combination of vectors $\vec{x}_1, \dots, \vec{x}_k$.

$\Downarrow$ 2) Linear dependency

Consider a vector space $V$, $k>0$, vector $\vec{x}_1, \dots, \vec{x}_k \in V$, and
$\sum_{i=1}^{k} \lambda_i \vec{x}_i = \vec{0}$ for some $\lambda_i \in \mathbb{R}$, $i \in [1, k]$.
*(underlined: zero vector)*

We say $\vec{x}_1, \dots, \vec{x}_k$ are -

① Linearly independent: only trivial solution exists: i.e. $\lambda_1 = \lambda_2 = \dots = \lambda_k = 0$

② Linearly dependent: nontrivial linear combination exists, i.e. $\lambda_i \neq 0$
for some $i \in [1, k]$

3) Spanning / Generating sets

Consider a vector space $V := (V, +, \cdot)$ and a set
$A := \{ \vec{x}_1, \dots, \vec{x}_k \} \subseteq V$, if $\forall \vec{v} \in V$, $\exists \lambda_1, \dots, \lambda_k \in \mathbb{R}$, s.t.

$\vec{v} = \sum_{i=1}^{k} \lambda_i \vec{x}_i$ *(circled: $\lambda_i$)* $\rightarrow$ *(blue: $\lambda_i$: coordinate)*

$\Rightarrow$ $A$ is called a spanning/generating set of $V$, denoted by $\text{Span}(A)$
or $A$ spans $V$.

*(right margin: $\exists$ exists)*

4) minimal generating set (a.k.a. basis)

$A$ is the minimal generating set of $V$, if
① $A$ is a generating set of $V$; ② $\nexists A' \subset A$, s.t. $A'$ spans $V$

Take away
① basis: a minimal set of linear independent vectors that spans $V$
② in general, vectors in a generating set could be linearly dependent
③ Dimension: the number of basis vector, denoted by $\text{dim}(V)$

Affine space and its generation 2: linear mapping affine mapping
Another way to viewing $\underline{W} \vec{x}$, let $\vec{x} := [x_1, x_2, x_3]^T$

$$
\begin{bmatrix}
W_{11} & W_{12} & W_{13} \\
W_{21} & W_{22} & W_{23} \\
W_{31} & W_{32} & W_{33}
\end{bmatrix}
\begin{bmatrix}
x_1 \\
x_2 \\
x_3
\end{bmatrix}
=
\begin{bmatrix}
W_{11}x_1 + W_{12}x_2 + W_{13}x_3 \\
W_{21}x_1 + W_{22}x_2 + W_{23}x_3 \\
W_{31}x_1 + W_{32}x_2 + W_{33}x_3
\end{bmatrix}
=
x_1 \cdot \begin{bmatrix} W_{11} \\ W_{21} \\ W_{31} \end{bmatrix}
+
x_2 \cdot \begin{bmatrix} W_{12} \\ W_{22} \\ W_{32} \end{bmatrix}
+
x_3 \cdot \begin{bmatrix} W_{13} \\ W_{23} \\ W_{33} \end{bmatrix}
$$

*(red underlined: column space of W)*

## page 4

$\Rightarrow$ $\tilde{W}\vec{x}$ is a vector within the span of column vectors of $\tilde{W}$

$\Rightarrow$ $\tilde{W}\vec{x}$ is a linear transformation of $\begin{bmatrix} x_1 \\ x_2 \end{bmatrix}$ from its own space (denoted by $V$) to the column space of $\tilde{W}$ $\Rightarrow$ a mapping from $V$ to $W$

1. Linear mapping
Def (Linear mapping) Given two vector spaces $V, W$,
a mapping $\phi: V \mapsto W$ is a linear mapping if
$\forall \vec{x}, \vec{y} \in V, \forall \lambda, \psi \in \mathbb{R}, \phi(\lambda\vec{x} + \psi\vec{y}) = \lambda\phi(\vec{x}) + \psi\phi(\vec{y})$
Specifically: ① $\lambda = \psi = 1, \phi(x+y) = \phi(x) + \phi(y)$
② $\psi = 0, \lambda = 1, \phi(\lambda\vec{x}) = \lambda\phi(\vec{x})$.

$\Rightarrow$ linear mapping preserves the structure of vector space.
$\Rightarrow$ The order between linear mappings and operations of the vector space can be exchanged.

given $\vec{x} \in V$, $\tilde{W}\vec{x}$ maps $\vec{x}$ to space $W$, let $\vec{x} \in \mathbb{R}^n$
$\tilde{W}\vec{x} \in \mathbb{R}^m$ we denote the number of linearly independent columns of a matrix $W$ by $\text{rank}(W)$, or the rank of $\tilde{W}$

important property: for $\tilde{W} \in \mathbb{R}^{m \times n}$, $\text{rank}(\tilde{W}) = \min\{m, n\}$,
then we say $\tilde{W}$ has full rank.
Three situation (consider $\tilde{W}$ with full rank).

① $\text{rank}(\tilde{W}) = n = m$, space $V$ and $W$ has the same dimension.
we are representing a "same" vector using different coordinate.

[Diagram: three input nodes fully connected to three output nodes, labeled $x$ and $y$]

y (output) has a different interpretation of x (input)

## page 5

② $\operatorname{rank}(\tilde{W}) = n < m$, meaning that $W$ has a higher dimension than $V$, we are mapping the input data to a higher dimensional space (a.k.a. upsampling).

[diagram: network of nodes with inputs labeled $X$ and outputs labeled $y$]

handling data in a lower dimension in a higher dimension

③ $\operatorname{rank}(\tilde{W}) = m < n$, meaning that $W$ has a lower dimension than $V$, we are mapping the input data to a lower dimensional space (a.k.a. downsampling).

dimensionality reduction.
→ handling "the most important" perspective of some high dimensional data.

[diagram: network of nodes with inputs and outputs]

⇒ what if $\tilde{W}$ does not have full rank?
⇒ Some connection are not necessary,
⇒ more property of rank: Session 2.6.2

Exercise: basis change.

Consider vector space $V$ and $W$, and ordered bases
$B = (\tilde{b}_1, \dots, \tilde{b}_n)$, $\tilde{B} = (\tilde{b}'_1, \dots, \tilde{b}'_n)$ of $V$
$C = (\tilde{c}_1, \dots, \tilde{c}_m)$, $\tilde{C} = (\tilde{c}'_1, \dots, \tilde{c}'_m)$ of $W$

Let $A_{\phi}$, $S$, $T$ be transformation from $B$ to $C$, from $\tilde{B}$ to $B$ and from $\tilde{C}$ to $C$, respectively.

## page 6

⇒ transformation matrix $\widetilde{B}$ to $\widetilde{C}$
$$ \widehat{A_\phi} = ? $$
Answer.
[diagram: B → C with A_φ; ↑S ↓T^{-1}; $\widetilde{B}$ → $\widetilde{C}$]

consider $v \in V$ with basis $\widetilde{B}$
$\widetilde{B} \to B : Sv$
$\widetilde{B} \to B \to C : A_\phi Sv$
$\widetilde{B} \to B \to C \to \widetilde{C} : T^{-1}A_\phi Sv$

⇒ $\widehat{A_\phi} = T^{-1}A_\phi S$

Remark 1: Matrices $A_\phi$ and $\widehat{A_\phi}$ are equivalent if there exist regular matrix (i.e. matrix with full rank) $S \in \mathbb{R}^{n \times n}$ and $T \in \mathbb{R}^{m \times m}$ such that $\widehat{A_\phi} = T^{-1}A_\phi S$

Remark 2: Matrices $A_\phi$ and $\widehat{A_\phi}$ are similar if there exist a regular matrix $S \in \mathbb{R}^{n \times n}$, s.t. $\widehat{A_\phi} = S^{-1}A_\phi S$
(Transformation matrix from $\widetilde{B}$ to $B$, and $\widetilde{C}$ to $C$, are the same)

2. Image and kernel
For $\phi: V \to W$ (not restricting to linear mapping), we define
Kernel: $\ker(\phi) := \phi^{-1}(\vec{0}_W) = \{\vec{v} \in V \mid \phi(\vec{v}) = \vec{0}_W\}$
Image: $\text{image}(\phi) = \{\vec{w} \in W \mid \exists \vec{v} \in V, \text{ s.t. } \phi(\vec{v}) = \vec{w}\}$

[diagram: V with ker(φ) inside, W with Im(φ) inside containing $\vec{0}_W$, arrow labeled $\phi: V \to W$]

## page 7

further more: if $\phi$ is a linear transformation with transformation matrix $A$

kernel: $\ker(\phi) := \{ \vec{v} \in V \mid A\vec{v} = \vec{0}_w \}$ Null space

$\Rightarrow$ Capture all possible linear combination of elements in $V$ that produce $\vec{0}_w$

$\text{Image}(\phi) = \{ \vec{w} \in W \mid \exists \vec{v} \in V, \text{ s.t } A\vec{v} = \vec{w} \}$

$\Rightarrow$ span of column vectors of $A$: Column Space

more properties: session 2.7.3 for linear mapping

3. Affine Space

Def. Let $V$ be a vector space, $\vec{x}_0 \in V$, and $U \subseteq V$ be a subspace. Then
$$ \underline{L} = \vec{x}_0 + U := \{ \vec{x}_0 + \vec{u} \mid \vec{u} \in U \} $$
$$ = \{ \vec{v} \in V \mid \exists \vec{u} \in U : \vec{v} = \vec{x}_0 + \vec{u} \} \subseteq V $$

is called affine subspace (or linear manifold) of $V$
$\vec{x}_0$: support point $\quad$ $U$: direction space

Exercise: prove: if $\vec{x}_0 \notin U$, $\vec{0} \notin L$

proof: Suppose $\underline{\vec{x}_0 \notin U}$, but $\vec{0} \in L$, then $\exists \vec{u} \in U$, s.t. $\underline{\vec{x}_0 + \vec{u} = \vec{0}}$
$\Rightarrow \underline{-\vec{x}_0} = \vec{u} \in U$
since $U$ is a vector subspace, the $(\underline{U, +})$ is an Abelian group
therefore, $-\vec{x}_0 \in U$, $\exists \vec{a} \in U$, s.t. $-\vec{x}_0 + \vec{a} = \underline{\vec{0}}$
$\Rightarrow \vec{a} = \underline{\vec{x}_0} \in U$, which is contradictory to $\underline{\vec{x}_0 \notin U}$ $\quad$ ✓

Lemma: if $\vec{x}_0 \notin U$, $L$ is not a vector subspace.

## page 8

**1. Affine mapping**

Given two vector spaces $V, W$, a linear mapping $\phi: V \to W$ and $\vec{a} \in W$, the mapping $\phi': V \to W$ with

$$ \phi'(\vec{x}) = \vec{a} + \phi(\vec{x}) \quad \text{translation vector} $$

is called an affine mapping from $V$ to $W$

Sec 2.4 ~ 2.9