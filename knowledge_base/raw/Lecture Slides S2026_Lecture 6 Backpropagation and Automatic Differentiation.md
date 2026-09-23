# Lecture Slides S2026\Lecture 6 Backpropagation and Automatic Differentiation.pdf

## page 1

Vector Calculus: Back-propagation & Automatic Differentiation.

[Diagram of a neural network with layers of nodes and connections, labeled with $(\ell-1)$-th layer, $\ell$-th layer, $(\ell+1)$-th layer]

$L$: number of layer (hidden layer and output layer)
$M_\ell$: number of neurons in the $\ell$-th layer.
$f_\ell$: activation function in the $\ell$-th layer
$W^{(\ell)} \in \mathbb{R}^{M_\ell \times M_{(\ell-1)}}$: weight matrix from the $(\ell-1)$-th layer to the $\ell$-th layer.
$\vec{b}^{(\ell)} \in \mathbb{R}^{M_\ell}$: $(\ell-1)$-th - $\ell$-th layer bias
$\vec{z}^{(\ell)} \in \mathbb{R}^{M_\ell}$: input to the $\ell$-th layer of neuron.
(activation)
$\vec{a}^{(\ell)} \in \mathbb{R}^{M_\ell}$: output of the $\ell$-th layer
(net activation).

Consider $\mathcal{L}(\vec{y}, \hat{\vec{y}})$ lost function to be minimized, note that
$$ \vec{y} = (f_L \circ f_{L-1} \circ \dots \circ f_1)(\vec{x}) = f_L(f_{L-1}(f_{L-2}(\dots (f_1(\vec{x}))) \dots)) $$
$\vec{x}$: input to the NN,
$\vec{y}$: output of the NN
$f_\ell$: activation function, $\ell \in [1, L]$, with $f_\ell(W^{(\ell)}\vec{a}^{(\ell-1)} + \vec{b}^{(\ell)})$ in the $\ell$-th layer.

Common activation function
[Graph of a sigmoid curve with axes]
Sigmoid (S-shape curve)
(Saturation on both side)
\begin{cases}
\text{logistic}: \sigma(x) = \frac{1}{1 + e^{-x}} \\
\text{Tanh}: \tanh(x) = \frac{e^x - e^{-x}}{e^x + e^{-x}}
\end{cases}
[Graph of ReLU, Tanh, and Sigmoid curves with axes]

ReLU (rectified function)
\begin{cases}
\text{original } ReLU(x) = \max(0, x) \\
\text{softplus}(x) = \log(1 + e^x) \\
\text{maxout}(\vec{x}) = \max_{k \in [1, n]} (x_k) \\
\quad \vec{x} \in \mathbb{R}^n
\end{cases}

Ultimate goal: obtain matrix $W^{(\ell)}$ and vector $\vec{b}^{(\ell)}$ for each layer
$\Rightarrow$ partial derivative of $\mathcal{L}(\vec{y}, \hat{\vec{y}})$ w.r.t. $W^{(\ell)}$ and $\vec{b}^{(\ell)}$.
i.e., need to compute $\frac{\partial \mathcal{L}(\vec{y}, \hat{\vec{y}})}{\partial W^{(\ell)}}$ and $\frac{\partial \mathcal{L}(\vec{y}, \hat{\vec{y}})}{\partial \vec{b}^{(\ell)}}$ for any $\ell \in [1, L]$.
$\Rightarrow$ backpropagation.

1. Backpropagation:
For each layer, $\vec{a}^{(\ell)} = f_\ell(\vec{z}^{(\ell)}) = f_\ell(W^{(\ell)}\vec{a}^{(\ell-1)} + \vec{b}^{(\ell)})$, then

## page 2

$$
\frac{\partial L(y, \hat{y})}{\partial W_{ij}^{(l)}} = \frac{\partial L(y, \hat{y})}{\partial \vec{z}^{(l)}} \cdot \frac{\partial \vec{z}^{(l)}}{\partial W_{ij}^{(l)}} \quad (w.r.t. \text{ each element in } W)
$$
$$
\underbrace{1 \times 1}_{\text{}} \quad \underbrace{1 \times M_l}_{\text{}} \quad \underbrace{M_l \times 1}_{\text{}}
$$

$$
\frac{1}{M_e} \frac{\partial L(y, \hat{y})}{\partial \vec{b}^{(l)}} = \frac{1}{M_e} \frac{\partial L(y, \hat{y})}{\partial \vec{z}^{(l)}} \cdot \frac{\partial \vec{z}^{(l)}}{\partial \vec{b}^{(l)}} \quad (w.r.t. \text{ each } \vec{b})
$$
$$
\underbrace{1 \times M_e}_{\text{}} \quad \underbrace{1 \times M_e}_{\text{}} \quad \underbrace{M_e \times M_e}_{\text{}}
$$

① Computation of $\frac{\partial \vec{z}^{(l)}}{\partial W_{ij}^{(l)}} \in \mathbb{R}^{M_e \times 1}$

$$
\frac{\partial \vec{z}^{(l)}}{\partial W_{ij}^{(l)}} = 
\begin{bmatrix}
\frac{\partial z_1^{(l)}}{\partial W_{ij}^{(l)}} \\
\vdots \\
\frac{\partial z_2^{(l)}}{\partial W_{ij}^{(l)}} \\
\vdots \\
\frac{\partial z_{M_e}^{(l)}}{\partial W_{ij}^{(l)}}
\end{bmatrix}
=
\begin{bmatrix}
0 \\
\vdots \\
\frac{\partial (W_{i,:}^{(l)} \vec{a}^{(l-1)} + \vec{b}^{(l)})}{\partial W_{ij}^{(l)}} \\
\vdots \\
0
\end{bmatrix}
=
\begin{bmatrix}
0 \\
\vdots \\
a_j^{(l-1)} \\
\vdots \\
0
\end{bmatrix}
= \Pi_i (a_j^{(l-1)})
$$

*[Red text next to the vector:]*
$\leftarrow$ i-th element
*[Text below the vector:]*
if
the i-th element
is $a_j^{(l-1)}$, 0
otherwise.

② Computation of $\frac{\partial \vec{z}^{(l)}}{\partial \vec{b}^{(l)}} \in \mathbb{R}^{M_e \times M_e}$.

since $\vec{z}^{(l)} = W^{(l)} \cdot \vec{a}^{(l-1)} + \vec{b}^{(l)} \Rightarrow \frac{\partial \vec{z}^{(l)}}{\partial \vec{b}^{(l)}} = I_{M_e}$ ✓
with $I_{M_e}$ being an $M_e \times M_e$ identity matrix.

③ Computation of $\frac{\partial L(y, \hat{y})}{\partial \vec{z}^{(l)}}$.

Note: representing the influence of the $l$-th layer of neurons on the final loss (we call it error term of the $l$-th layer) denoted by $\vec{\delta}^{(l)} := \frac{\partial L(y, \hat{y})}{\partial \vec{z}^{(l)}} \in \mathbb{R}^{1 \times M_e}$.

## page 3

$$
\vec{\delta}^{(\ell)} = \frac{\partial L(\vec{y}, \hat{\vec{y}})}{\partial \vec{z}^{(\ell+1)}} \cdot \frac{\partial \vec{z}^{(\ell+1)}}{\partial \vec{a}^{(\ell)}} \cdot \frac{\partial \vec{a}^{(\ell)}}{\partial \vec{z}^{(\ell)}}
$$
$1 \times M_\ell$ 
$\vec{\delta}^{(\ell+1)}$ 
$1 \times M_{\ell+1}$ 
$M_{\ell+1} \times M_\ell$ 
$M_\ell \times M_\ell$ ✓

since $\vec{z}^{(\ell+1)} = W^{(\ell+1)} \vec{a}^{(\ell)} + b^{(\ell+1)}$ 
$$\implies \frac{\partial \vec{z}^{(\ell+1)}}{\partial \vec{a}^{(\ell)}} = W^{(\ell+1)}$$

additionally, since $\vec{a}^{(\ell)} = f_\ell(\vec{z}^{(\ell)})$ 
$$\implies \frac{\partial \vec{a}^{(\ell)}}{\partial \vec{z}^{(\ell)}} = \frac{\partial f_\ell(\vec{z}^{(\ell)})}{\partial \vec{z}^{(\ell)}} = \text{diag}\left(f'_{\ell,1}(\vec{z}^{(\ell)}), \dots, f'_{\ell,M_\ell}(\vec{z}^{(\ell)})\right)$$

$$\implies \vec{\delta}^{(\ell)} = \frac{\partial L(\vec{y}, \hat{\vec{y}})}{\partial \vec{z}^{(\ell+1)}} \cdot \frac{\partial \vec{z}^{(\ell+1)}}{\partial \vec{a}^{(\ell)}} \cdot \frac{\partial \vec{a}^{(\ell)}}{\partial \vec{z}^{(\ell)}}$$
$$= \vec{\delta}^{(\ell+1)} \cdot W^{(\ell+1)} \cdot \text{diag}(\quad)$$

$f_\ell$: if the activation function is the same in the $\ell$-th layer 
$$\vec{\delta}^{(\ell)} = \vec{\delta}^{(\ell+1)} \cdot W^{(\ell+1)} \cdot \text{diag}\left(f'_\ell(\vec{z}^{(\ell)}), \dots, f'_\ell(\vec{z}^{(\ell)})\right)$$
$$= f'_\ell(\vec{z}^{(\ell)}) \odot \left(\vec{\delta}^{(\ell+1)} \cdot W^{(\ell+1)}\right)$$

$\odot$: Hadamard product: 
elementwise product

## page 4

Def: $A, B \in \mathbb{R}^{m \times n} \quad [A \odot B]_{mn} = a_{mn} \cdot b_{mn}$

$a_{mn}$ : $(m,n)$-th element in $A$

$b_{mn}$ : $(m,n)$-th element in $B$

$c \in \mathbb{R}, \ A \in \mathbb{R}^{m \times n}, \ [c \odot A]_{mn} = c a_{mn}$

$\Rightarrow \frac{\partial \mathcal{L}(\vec{y}, \hat{y})}{\partial W^{(e)}_{ij}} = \left[ \delta_1^{(e)} \cdots \delta_{M_e}^{(e)} \right] \begin{bmatrix} 0 \\ \vdots \\ a_j^{(e-1)} \\ \vdots \\ 0 \end{bmatrix} = \delta_i^{(e)} \cdot a_j^{(e-1)}$

$\underbrace{\hspace{2cm}}_{\vec{\delta}^{(e)}}$

Remark: $\vec{a} \in \mathbb{R}^M, \ \vec{b} \in \mathbb{R}^N$

with $\vec{a} = [a_1, \dots, a_M]^T$

$\vec{b} = [b_1, \dots, b_N]^T$

the $(i,j)$-th element of the outer product between $\vec{\delta}^{(e)}$ and $\vec{a}^{(e-1)}$

$\vec{a} \otimes \vec{b} = \begin{bmatrix} a_1 b_1 & a_1 b_2 & \cdots & a_1 b_N \\ a_2 b_1 & a_2 b_2 & \cdots & a_2 b_N \\ \vdots & \vdots & & \vdots \\ a_M b_1 & a_M b_2 & \cdots & a_M b_N \end{bmatrix} = \vec{a} \vec{b}^T$, with $[\vec{a} \otimes \vec{b}]_{mn} = a_m b_n$.

$\Rightarrow \left[ \frac{\partial \mathcal{L}(\vec{y}, \hat{y})}{\partial W^{(e)}} \right]_{ij} = \left[ \vec{\delta}^{(e)} \otimes \vec{a}^{(e-1)} \right]_{ij} \Rightarrow \frac{\partial \mathcal{L}(\vec{y}, \hat{y})}{\partial W^{(e)}} = \vec{\delta}^{(e)} \cdot \vec{a}^{(e-1)T}$

Moreover

$\frac{\partial \mathcal{L}(\vec{y}, \hat{y})}{\partial \vec{b}^{(e)}} = \frac{\partial \mathcal{L}(\vec{y}, \hat{y})}{\partial \vec{z}^{(e)}} \cdot \frac{\partial \vec{z}^{(e)}}{\partial \vec{b}^{(e)}} = \left[ \delta_1^{(e)}, \cdots, \delta_{M_e}^{(e)} \right] \cdot \begin{bmatrix} 1 \\ \vdots \\ 1 \end{bmatrix} = \vec{\delta}^{(e)} \in \mathbb{R}^{1 \times M_e}$

$\underbrace{\hspace{2cm}}_{M_e \times M_e}$

## page 5

Summarize: procedure for training with backpropagation

(1) select data from the training set $(\vec{x}^{(n)}, \vec{y}^{(n)})$

(2) Feed forward computation of each activation $\vec{z}^{(l)}$ and the next activation $\vec{a}^{(l)}$

(3) compute error $\vec{\delta}^{(l)}$, $l \in [1, L]$, on each layer via backpropagation

$$\vec{\delta}^{(l)} = \frac{\partial L(\vec{y}, \hat{\vec{y}})}{\partial \vec{z}^{(l)}} = \vec{\delta}^{(l+1)} \cdot \frac{\partial \vec{z}^{(l+1)}}{\partial \vec{a}^{(l)}} \cdot \frac{\partial \vec{a}^{(l)}}{\partial \vec{z}^{(l)}}$$

$$= \vec{\delta}^{(l+1)} \cdot W^{(l+1)} \cdot \text{diag}\left(f'_e(\vec{z}^{(l)}), \cdots, f'_{e, n_l}(\vec{z}^{(l)})\right)$$

for $l \in [1, L-1]$ recursively.

(4) compute gradients of $W^{(l)}$ and $\vec{b}^{(l)}$ for all layer $l$

$$\frac{\partial L(\vec{y}, \hat{\vec{y}})}{\partial W^{(l)}} = \vec{\delta}^{(l)} (\vec{a}^{(l-1)})^{T}, \qquad \frac{\partial L(\vec{y}, \hat{\vec{y}})}{\partial \vec{b}^{(l)}} = \vec{\delta}^{(l)}$$

(5) update $W$ and $\vec{b}$ based on the gradient (to be discussed)

---

2. Vanishing (exploding) gradient.

(1) consider the same activation function in each layer.

$$\vec{\delta}^{(l)} = \vec{f}_e'(\vec{z}^{(l)}) \odot \left(\vec{\delta}^{(l+1)} \cdot W^{(l+1)}\right)$$
*(gradients of the activation function)*

$$\delta^{(l+1)} = \vec{f}_e'(\vec{z}^{(l+1)}) \cdot \vec{\delta}^{(l+2)} \cdot W^{(l+2)}$$

$$\delta^{(l)} = \vec{f}_e'(\vec{z}^{(l)}) \cdot \vec{f}_e'(\vec{z}^{(l+1)}) \cdot \vec{\delta}^{(l+1)} \cdot W^{(l+2)}$$

① if $f'_e(\vec{z}^{(l)}) < 1 \Rightarrow L \uparrow$, $\delta^{(l)} \to 0$ (consider $0.9^{1000} = 4.3 \times 10^{-5}$)
$\Rightarrow$ gradient tends to $0$ (vanishing gradient)

② if $f'_e(\vec{z}^{(l)}) > 1 \Rightarrow L \uparrow$, $\delta^{(l)} \to \infty$ (grow exponentially)
gradient $\to \infty$ (exploding)

solution
- Gradient clipping
- Batch normalization
- Proper Initialization of parameters

## page 6

3. Automatic differentiation.
consider the function
$$f(x) = \sqrt{x^2 + e^{x^2}} + \cos(x^2 + e^{x^2}), \text{ what is the derivative}$$
$$\frac{df}{dx} \text{ evaluated at } x=1$$
Typical solution:
$$\frac{df}{dx} = \left. \frac{2x + 2e^{x^2}}{2\sqrt{x^2 + e^{x^2}}} - \sin(x^2 + e^{x^2})(2x + 2xe^{x^2}) \right|_{x=1}$$
Expensive and even impossible (consider nesting function)
$\Rightarrow$ automatic differentiation over computational graph.
consider
$a = x^2$
$e^{x^2} = b = \exp(a)$
$c = a + b$
$d = \sqrt{c}$
$e = \cos(c)$
$f = d + e$
$\Rightarrow$ computation graph.

$x \rightarrow \boxed{(\cdot)^2} \rightarrow a$
$\quad\quad\quad\quad\quad\quad \nwarrow$
$\quad\quad\quad\quad\quad\quad \boxed{\exp(\cdot)} \rightarrow b$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \searrow$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \boxed{+} \rightarrow c$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \swarrow \searrow$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \boxed{\sqrt{\cdot}} \rightarrow d \quad \boxed{\cos(\cdot)} \rightarrow e$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \searrow \quad \swarrow$
$\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad\quad \boxed{+} \rightarrow f$

derivative for elementary functions:
$$\frac{\partial a}{\partial x} = 2x \quad \frac{\partial b}{\partial a} = \exp(a) \quad \frac{\partial c}{\partial a} = 1 = \frac{\partial c}{\partial b}$$

## page 7

$$\frac{\partial d}{\partial c} = \frac{1}{2\sqrt{c}} \qquad \frac{\partial e}{\partial c} = -\sin(c)$$

$$\frac{\partial f}{\partial d} = 1 = \frac{\partial f}{\partial e}$$

$$\frac{\partial f}{\partial c} = \frac{\partial f}{\partial d}\cdot\frac{\partial d}{\partial c} + \frac{\partial f}{\partial e}\cdot\frac{\partial e}{\partial c} = 1\cdot\frac{1}{2\sqrt{c}} + 1\cdot(-\sin c)$$
$$= \frac{1}{2\sqrt{c}} - \sin(c)$$

$$\frac{\partial f}{\partial b} = \frac{\partial f}{\partial c}\cdot\frac{\partial c}{\partial b} = \frac{\partial f}{\partial c}$$

$$\frac{\partial f}{\partial a} = \frac{\partial f}{\partial b}\cdot\frac{\partial b}{\partial a} + \frac{\partial f}{\partial c}\cdot\frac{\partial c}{\partial a} = \frac{\partial f}{\partial b}\cdot\exp(a)$$
$$\qquad\qquad\qquad\qquad\qquad\qquad\qquad + \frac{\partial f}{\partial c}\cdot 1$$

$$\frac{\partial f}{\partial x} = \frac{\partial f}{\partial a}\cdot\frac{\partial a}{\partial x} = \frac{\partial f}{\partial a}\cdot 2x$$
$$= \frac{\partial f}{\partial c}(\exp(a)+1)\cdot 2x$$
$$= \left(\frac{1}{2\sqrt{c}} - \sin c\right)(\exp(a)+1)\cdot 2x$$

$\Big\Downarrow$ one can verify $\qquad\qquad\qquad \Rightarrow$ easy to compute.

$$\frac{\partial f}{\partial x} = \frac{\partial f}{\partial d}\cdot\frac{\partial d}{\partial c}\cdot\frac{\partial c}{\partial b}\cdot\frac{\partial b}{\partial a}\cdot\frac{\partial a}{\partial x} + \frac{\partial f}{\partial d}\cdot\frac{\partial d}{\partial c}\cdot\frac{\partial c}{\partial a}\cdot\frac{\partial a}{\partial x} +$$
$$\quad \frac{\partial f}{\partial e}\cdot\frac{\partial e}{\partial c}\cdot\frac{\partial c}{\partial b}\cdot\frac{\partial b}{\partial a}\cdot\frac{\partial a}{\partial x} + \frac{\partial f}{\partial e}\cdot\frac{\partial e}{\partial c}\cdot\frac{\partial c}{\partial a}\cdot\frac{\partial a}{\partial x}$$

## page 8

Exercise

$f = \frac{1}{\exp(x^2)+x^2}$ compute $\left.\frac{\partial f}{\partial x}\right|_{x=1}$

$x \rightarrow \boxed{(\cdot)^2} \rightarrow a$
$\boxed{\exp(\cdot)} \rightarrow b$
$a, b \rightarrow \boxed{+} \rightarrow c \rightarrow \boxed{1/(\cdot)} \rightarrow f$

$\Rightarrow \frac{\partial f}{\partial x} = \frac{\partial f}{\partial c} \cdot \frac{\partial c}{\partial a} \cdot \frac{\partial a}{\partial x} + \frac{\partial f}{\partial c} \cdot \frac{\partial c}{\partial b} \cdot \frac{\partial b}{\partial a} \cdot \frac{\partial a}{\partial x}$

$= -\frac{1}{c^2} \cdot 1 \cdot 2x + \left(-\frac{1}{c^2}\right) \cdot 1 \cdot \exp(a) \cdot 2x$

$= -\frac{2x}{c^2} (1 + \exp(a))$ , 代入计算

note:
$a = x^2 \quad \frac{\partial a}{\partial x} = 2x$
$b = \exp(a) \quad \frac{\partial b}{\partial a} = e^a$
$c = a + b$
$\frac{\partial c}{\partial a} = 1 = \frac{\partial c}{\partial b}$
$\frac{\partial f}{\partial c} = -\frac{1}{c^2}$

## page 9

[blank page]


## page 10

[blank page]


## page 11

[blank page]


## page 12

[blank page]
