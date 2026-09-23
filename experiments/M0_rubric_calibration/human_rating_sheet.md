# M0 人工盲评表

**怎么用**：这份表不用全做完。Part A 的前 4 对（A1/A2/A3/B1）最关键，做完就能和 LLM 评判者算出一致性；有余力再往后做。

**唯一要求**：不要猜"哪个是被改坏的"。如果两个回答你看不出差别，就写"差不多"——那本身就是重要的结果（说明这个条目人判不出来）。

条目速查：

```
A1 定位与意图｜A2 分阶段步进｜A3 推理链完整、关系显式｜B1 无冗余与填充
B2 范围相称｜C1 符号与术语卫生｜C2 前置桥接｜C3 给出理由，而非仅步骤
```

---

## Part A｜成对比较

每对里，两个回答**内容基本相同**，但其中一个被定向注入了一处缺陷。顺序已随机。请回答三个问题。

### A-1

**问题**：为什么梯度要写成行向量？课件里专门问了这个问题，我还是没懂。

**左**：

关键原因：**这是本课程对“导数/Jacobian”的约定。把 scalar-valued function 的导数写成行向量，链式法则可以直接用矩阵乘法，不需要额外转置。**

看课件里的 case 1：  
设 \(f:\mathbb{R}^2\to\mathbb{R}\)，而 \(x_1(t),x_2(t):\mathbb{R}\to\mathbb{R}\)。链式法则给出

\[
\frac{df}{dt}
=
\frac{\partial f}{\partial x_1}\frac{dx_1}{dt}
+
\frac{\partial f}{\partial x_2}\frac{dx_2}{dt}.
\]

如果令

\[
\frac{\partial f}{\partial \vec{x}}
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1} & \frac{\partial f}{\partial x_2}
\end{bmatrix}
\quad (1\times 2 \text{ row}),
\qquad
\frac{d\vec{x}}{dt}
=
\begin{bmatrix}
\frac{dx_1}{dt}\\
\frac{dx_2}{dt}
\end{bmatrix}
\quad (2\times 1 \text{ column}),
\]

那么

\[
\frac{df}{dt}
=
\frac{\partial f}{\partial \vec{x}}
\frac{d\vec{x}}{dt}.
\]

可以直接乘：\((1\times 2)(2\times 1)=1\times 1\)。

如果 \(\frac{\partial f}{\partial \vec{x}}\) 写成列向量 \((2\times 1)\)，那就必须写成

\[
\frac{df}{dt}
=
\left(\frac{\partial f}{\partial \vec{x}}\right)^T
\frac{d\vec{x}}{dt},
\]

多了一个转置。课件选择行向量，就是为了避免这个转置。

再看 case 2：  
若 \(x_1(s,t),x_2(s,t)\)，令 \(\vec{\theta}=[s,t]\)，则

\[
\frac{\partial f}{\partial \vec{\theta}}
=
\frac{\partial f}{\partial \vec{x}}
\frac{\partial \vec{x}}{\partial \vec{\theta}}
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1} & \frac{\partial f}{\partial x_2}
\end{bmatrix}
\begin{bmatrix}
\frac{\partial x_1}{\partial s} & \frac{\partial x_1}{\partial t}\\
\frac{\partial x_2}{\partial s} & \frac{\partial x_2}{\partial t}
\end{bmatrix}
=
\begin{bmatrix}
\frac{\partial f}{\partial s} & \frac{\partial f}{\partial t}
\end{bmatrix}.
\]

维度是 \((1\times 2)(2\times 2)=1\times 2\)，仍然不需要转置。

从 total derivative 的角度看也是一样：

\[
df_a
=
\sum_{i=1}^n
\frac{\partial f}{\partial x_i}(a)\,dx_i
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1} & \cdots & \frac{\partial f}{\partial x_n}
\end{bmatrix}
\begin{bmatrix}
dx_1\\
\vdots\\
dx_n
\end{bmatrix}.
\]

也就是说，\(df\) 是一个从 \(\mathbb{R}^D\) 到 \(\mathbb{R}\) 的线性映射，它自然表示为“行向量乘列向量”。

所以课件总结为：

\[
\begin{aligned}
f:\mathbb{R}^D\to\mathbb{R}
&\Rightarrow \text{gradient is } 1\times D \text{ row vector},\\
f:\mathbb{R}\to\mathbb{R}^E
&\Rightarrow \text{gradient is } E\times 1 \text{ column vector},\\
f:\mathbb{R}^D\to\mathbb{R}^E
&\Rightarrow \text{gradient is } E\times D \text{ matrix}.
\end{aligned}
\]

这样定义后，复合函数 \(h=f\circ g\) 的链式法则就是

\[
Dh = Df\,Dg,
\]

维度自动匹配，不需要到处转置。

需要注意：**行向量不是数学上唯一必须的写法，而是一种约定。** 很多教材把 \(\nabla f\) 定义为与 \(\vec{x}\) 同型的列向量。本课程这里说的 “gradient” 更接近 Jacobian/derivative matrix。对于 \(f:\mathbb{R}^D\to\mathbb{R}\)，它的 derivative 是 \(1\times D\) 行向量；如果你想要与 \(\vec{x}\) 同型的列向量，就取它的转置即可。

**右**：

看课件里的 case 1：  
设 \(f:\mathbb{R}^2\to\mathbb{R}\)，而 \(x_1(t),x_2(t):\mathbb{R}\to\mathbb{R}\)。链式法则给出

\[
\frac{df}{dt}
=
\frac{\partial f}{\partial x_1}\frac{dx_1}{dt}
+
\frac{\partial f}{\partial x_2}\frac{dx_2}{dt}.
\]

如果令

\[
\frac{\partial f}{\partial \vec{x}}
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1} & \frac{\partial f}{\partial x_2}
\end{bmatrix}
\quad (1\times 2 \text{ row}),
\qquad
\frac{d\vec{x}}{dt}
=
\begin{bmatrix}
\frac{dx_1}{dt}\\
\frac{dx_2}{dt}
\end{bmatrix}
\quad (2\times 1 \text{ column}),
\]

那么

\[
\frac{df}{dt}
=
\frac{\partial f}{\partial \vec{x}}
\frac{d\vec{x}}{dt}.
\]

可以直接乘：\((1\times 2)(2\times 1)=1\times 1\)。

如果 \(\frac{\partial f}{\partial \vec{x}}\) 写成列向量 \((2\times 1)\)，那就必须写成

\[
\frac{df}{dt}
=
\left(\frac{\partial f}{\partial \vec{x}}\right)^T
\frac{d\vec{x}}{dt},
\]

多了一个转置。课件选择行向量，就是为了避免这个转置。

再看 case 2：  
若 \(x_1(s,t),x_2(s,t)\)，令 \(\vec{\theta}=[s,t]\)，则

\[
\frac{\partial f}{\partial \vec{\theta}}
=
\frac{\partial f}{\partial \vec{x}}
\frac{\partial \vec{x}}{\partial \vec{\theta}}
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1} & \frac{\partial f}{\partial x_2}
\end{bmatrix}
\begin{bmatrix}
\frac{\partial x_1}{\partial s} & \frac{\partial x_1}{\partial t}\\
\frac{\partial x_2}{\partial s} & \frac{\partial x_2}{\partial t}
\end{bmatrix}
=
\begin{bmatrix}
\frac{\partial f}{\partial s} & \frac{\partial f}{\partial t}
\end{bmatrix}.
\]

维度是 \((1\times 2)(2\times 2)=1\times 2\)，仍然不需要转置。

从 total derivative 的角度看也是一样：

\[
df_a
=
\sum_{i=1}^n
\frac{\partial f}{\partial x_i}(a)\,dx_i
=
\begin{bmatrix}
\frac{\partial f}{\partial x_1} & \cdots & \frac{\partial f}{\partial x_n}
\end{bmatrix}
\begin{bmatrix}
dx_1\\
\vdots\\
dx_n
\end{bmatrix}.
\]

也就是说，\(df\) 是一个从 \(\mathbb{R}^D\) 到 \(\mathbb{R}\) 的线性映射，它自然表示为“行向量乘列向量”。

所以课件总结为：

\[
\begin{aligned}
f:\mathbb{R}^D\to\mathbb{R}
&\Rightarrow \text{gradient is } 1\times D \text{ row vector},\\
f:\mathbb{R}\to\mathbb{R}^E
&\Rightarrow \text{gradient is } E\times 1 \text{ column vector},\\
f:\mathbb{R}^D\to\mathbb{R}^E
&\Rightarrow \text{gradient is } E\times D \text{ matrix}.
\end{aligned}
\]

这样定义后，复合函数 \(h=f\circ g\) 的链式法则就是

\[
Dh = Df\,Dg,
\]

维度自动匹配，不需要到处转置。

需要注意：**行向量不是数学上唯一必须的写法，而是一种约定。** 很多教材把 \(\nabla f\) 定义为与 \(\vec{x}\) 同型的列向量。本课程这里说的 “gradient” 更接近 Jacobian/derivative matrix。对于 \(f:\mathbb{R}^D\to\mathbb{R}\)，它的 derivative 是 \(1\times D\) 行向量；如果你想要与 \(\vec{x}\) 同型的列向量，就取它的转置即可。

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

### A-2

**问题**：Gram–Schmidt 正交化的步骤我背下来了但不太理解，能讲一下它每一步在做什么吗？

**左**：

Gram–Schmidt 的本质可以理解成一句话：

> 每一步都把当前向量中“已经能由前面那些方向表示出来的部分”减掉，只留下与前面所有方向都垂直的新成分。

\[
\vec u_1=\vec b_1
\]

因为还没有任何旧方向，所以第一个向量不用处理，直接作为第一个正交方向。

---

假设前面已经得到相互正交的向量

\[
\vec u_1,\vec u_2,\dots,\vec u_{k-1}.
\]

现在处理原来的基向量 \(\vec b_k\)。

\(\vec b_k\) 可能含有一些已经落在 \(\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})\) 里的分量。我们要把这个分量减掉：

\[
\vec u_k
=
\vec b_k
-
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k).
\]

因为 \(\vec u_i\) 已经两两正交，所以投影可以拆成每个方向上的投影之和：

\[
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k)
=
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

所以实际计算就是：

\[
\vec u_k
=
\vec b_k
-
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

其中

\[
\frac{\vec u_i \vec u_i^T}{\|\vec u_i\|^2}
\]

就是“投影到方向 \(\vec u_i\) 上”的投影矩阵。

也就是说，每一步做的事是：

> 把 \(\vec b_k\) 在旧方向 \(\vec u_1,\dots,\vec u_{k-1}\) 上的影子减掉，剩下的 \(\vec u_k\) 就垂直于所有这些旧方向。

---

对任意 \(j<k\)，检查内积：

\[
\vec u_j^T \vec u_k
=
\vec u_j^T \vec b_k
-
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}
\vec u_j^T \vec u_i.
\]

因为前面已经正交，所以当 \(i\neq j\) 时，\(\vec u_j^T \vec u_i=0\)。只剩 \(i=j\) 那一项：

\[
\vec u_j^T \vec u_k
=
\vec u_j^T \vec b_k
-
\frac{\vec u_j^T \vec b_k}{\|\vec u_j\|^2}\|\vec u_j\|^2
=
0.
\]

所以 \(\vec u_k\) 与所有之前的 \(\vec u_j\) 都正交。

---

Gram–Schmidt 先得到的是正交基：

\[
\vec u_1,\dots,\vec u_n
\]

满足

\[
\vec u_i^T \vec u_j=0 \quad (i\neq j).
\]

如果还想要 orthonormal basis，就做归一化：

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

这样就有

\[
\vec e_i^T \vec e_j=
\begin{cases}
1, & i=j,\\
0, & i\neq j.
\end{cases}
\]

---

例子：

\[
\vec a=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec b=\begin{bmatrix}0\\2\end{bmatrix}.
\]

第一步：

\[
\vec u_1=\vec a=\begin{bmatrix}1\\1\end{bmatrix}.
\]

第二步，把 \(\vec b\) 投影到 \(\vec u_1\) 上：

\[
\frac{\vec a^T \vec b}{\|\vec a\|^2}\vec a
=
\frac{2}{2}
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}1\\1\end{bmatrix}.
\]

然后减掉这个投影：

\[
\vec u_2
=
\vec b-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}0\\2\end{bmatrix}
-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}-1\\1\end{bmatrix}.
\]

验证：

\[
\vec u_1^T \vec u_2
=
\begin{bmatrix}1&1\end{bmatrix}
\begin{bmatrix}-1\\1\end{bmatrix}
=
0.
\]

最后归一化：

\[
\vec e_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec e_2=\frac{1}{\sqrt2}\begin{bmatrix}-1\\1\end{bmatrix}.
\]

---

所以你背的步骤其实对应这个几何动作：

\[
\vec u_1=\vec b_1,
\]

\[
\vec u_k
=
\vec b_k
-
\text{\(\vec b_k\) 在前面所有旧方向上的投影},
\]

最后

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

注：slides 里 \(\vec u_2\) 的公式似乎有个笔误，投影应该作用于 \(\vec b_2\)，即  
\(\vec u_2=\vec b_2-\pi_{\operatorname{span}(\vec u_1)}(\vec b_2)\)。另外例子里 \(\vec a^T\vec b\) 实际是 \(2\)，不是 \(3\)。

**右**：

Gram–Schmidt 的本质可以理解成一句话：

> 每一步都把当前向量中“已经能由前面那些方向表示出来的部分”减掉，只留下与前面所有方向都垂直的新成分。

## 1. 第一步：保留第一个方向

\[
\vec u_1=\vec b_1
\]

因为还没有任何旧方向，所以第一个向量不用处理，直接作为第一个正交方向。

---

## 2. 第 \(k\) 步：减去在旧方向上的投影

假设前面已经得到相互正交的向量

\[
\vec u_1,\vec u_2,\dots,\vec u_{k-1}.
\]

现在处理原来的基向量 \(\vec b_k\)。

\(\vec b_k\) 可能含有一些已经落在 \(\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})\) 里的分量。我们要把这个分量减掉：

\[
\vec u_k
=
\vec b_k
-
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k).
\]

因为 \(\vec u_i\) 已经两两正交，所以投影可以拆成每个方向上的投影之和：

\[
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k)
=
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

所以实际计算就是：

\[
\vec u_k
=
\vec b_k
-
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

其中

\[
\frac{\vec u_i \vec u_i^T}{\|\vec u_i\|^2}
\]

就是“投影到方向 \(\vec u_i\) 上”的投影矩阵。

也就是说，每一步做的事是：

> 把 \(\vec b_k\) 在旧方向 \(\vec u_1,\dots,\vec u_{k-1}\) 上的影子减掉，剩下的 \(\vec u_k\) 就垂直于所有这些旧方向。

---

## 3. 为什么减完就正交？

对任意 \(j<k\)，检查内积：

\[
\vec u_j^T \vec u_k
=
\vec u_j^T \vec b_k
-
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}
\vec u_j^T \vec u_i.
\]

因为前面已经正交，所以当 \(i\neq j\) 时，\(\vec u_j^T \vec u_i=0\)。只剩 \(i=j\) 那一项：

\[
\vec u_j^T \vec u_k
=
\vec u_j^T \vec b_k
-
\frac{\vec u_j^T \vec b_k}{\|\vec u_j\|^2}\|\vec u_j\|^2
=
0.
\]

所以 \(\vec u_k\) 与所有之前的 \(\vec u_j\) 都正交。

---

## 4. 最后为什么要归一化？

Gram–Schmidt 先得到的是正交基：

\[
\vec u_1,\dots,\vec u_n
\]

满足

\[
\vec u_i^T \vec u_j=0 \quad (i\neq j).
\]

如果还想要 orthonormal basis，就做归一化：

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

这样就有

\[
\vec e_i^T \vec e_j=
\begin{cases}
1, & i=j,\\
0, & i\neq j.
\end{cases}
\]

---

## 5. 用一个例子看

例子：

\[
\vec a=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec b=\begin{bmatrix}0\\2\end{bmatrix}.
\]

第一步：

\[
\vec u_1=\vec a=\begin{bmatrix}1\\1\end{bmatrix}.
\]

第二步，把 \(\vec b\) 投影到 \(\vec u_1\) 上：

\[
\frac{\vec a^T \vec b}{\|\vec a\|^2}\vec a
=
\frac{2}{2}
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}1\\1\end{bmatrix}.
\]

然后减掉这个投影：

\[
\vec u_2
=
\vec b-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}0\\2\end{bmatrix}
-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}-1\\1\end{bmatrix}.
\]

验证：

\[
\vec u_1^T \vec u_2
=
\begin{bmatrix}1&1\end{bmatrix}
\begin{bmatrix}-1\\1\end{bmatrix}
=
0.
\]

最后归一化：

\[
\vec e_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec e_2=\frac{1}{\sqrt2}\begin{bmatrix}-1\\1\end{bmatrix}.
\]

---

所以你背的步骤其实对应这个几何动作：

\[
\vec u_1=\vec b_1,
\]

\[
\vec u_k
=
\vec b_k
-
\text{\(\vec b_k\) 在前面所有旧方向上的投影},
\]

最后

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

注：slides 里 \(\vec u_2\) 的公式似乎有个笔误，投影应该作用于 \(\vec b_2\)，即  
\(\vec u_2=\vec b_2-\pi_{\operatorname{span}(\vec u_1)}(\vec b_2)\)。另外例子里 \(\vec a^T\vec b\) 实际是 \(2\)，不是 \(3\)。

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

### A-3

**问题**：特征多项式 $p_A(\lambda)$ 是怎么定义的？为什么它的根就是特征值？

**左**：

对 square matrix \(A \in \mathbb{R}^{n \times n}\)，特征多项式定义为

\[
p_A(\lambda) := \det(A-\lambda I),
\]

其中 \(I\) 是 \(n\times n\) 的 identity matrix。也就是说，把矩阵 \(A\) 的每个对角线元素都减去 \(\lambda\)，再取 determinant，得到的就是关于 \(\lambda\) 的多项式。

展开后，它是一个 \(n\) 次多项式，例如：

\[
p_A(\lambda)=c_0+c_1\lambda+\cdots+c_{n-1}\lambda^{n-1}+(-1)^n\lambda^n.
\]

它的根就是满足

\[
p_A(\lambda)=0
\]

的 \(\lambda\)。

为什么它的根就是特征值？因为特征值的定义是：\(\lambda\) 是 \(A\) 的特征值，当且仅当存在非零向量 \(\vec{x}\neq \vec{0}\)，使得

\[
A\vec{x}=\lambda \vec{x}.
\]

移项得

\[
A\vec{x}-\lambda \vec{x}=\vec{0},
\]

即

\[
(A-\lambda I)\vec{x}=\vec{0}.
\]



\[
\det(A-\lambda I)=0.
\]

但根据定义，

\[
\det(A-\lambda I)=p_A(\lambda).
\]

所以：

\[
\lambda \text{ 是 } A \text{ 的特征值}
\iff
\det(A-\lambda I)=0
\iff
p_A(\lambda)=0
\iff
\lambda \text{ 是特征多项式 } p_A \text{ 的根}.
\]

反过来也成立：如果 \(p_A(\lambda)=0\)，那么 \(\det(A-\lambda I)=0\)，所以 \(A-\lambda I\) singular，于是存在非零向量 \(\vec{x}\) 使 \((A-\lambda I)\vec{x}=\vec{0}\)，也就是 \(A\vec{x}=\lambda \vec{x}\)。因此 \(\lambda\) 是特征值。

这和讲义中的等价说法一致：

\[
\lambda \text{ 是 eigenvalue}
\iff
\exists \vec{x}\neq \vec{0},\ (A-\lambda I_n)\vec{x}=\vec{0}
\iff
\operatorname{rank}(A-\lambda I_n)<n
\iff
\det(A-\lambda I_n)=0.
\]

因此，特征多项式的根正好就是矩阵 \(A\) 的特征值。

**右**：

对 square matrix \(A \in \mathbb{R}^{n \times n}\)，特征多项式定义为

\[
p_A(\lambda) := \det(A-\lambda I),
\]

其中 \(I\) 是 \(n\times n\) 的 identity matrix。也就是说，把矩阵 \(A\) 的每个对角线元素都减去 \(\lambda\)，再取 determinant，得到的就是关于 \(\lambda\) 的多项式。

展开后，它是一个 \(n\) 次多项式，例如：

\[
p_A(\lambda)=c_0+c_1\lambda+\cdots+c_{n-1}\lambda^{n-1}+(-1)^n\lambda^n.
\]

它的根就是满足

\[
p_A(\lambda)=0
\]

的 \(\lambda\)。

为什么它的根就是特征值？因为特征值的定义是：\(\lambda\) 是 \(A\) 的特征值，当且仅当存在非零向量 \(\vec{x}\neq \vec{0}\)，使得

\[
A\vec{x}=\lambda \vec{x}.
\]

移项得

\[
A\vec{x}-\lambda \vec{x}=\vec{0},
\]

即

\[
(A-\lambda I)\vec{x}=\vec{0}.
\]

这是一个齐次线性方程组。它有非零解 \(\vec{x}\neq \vec{0}\)，当且仅当系数矩阵 \(A-\lambda I\) 是 singular，即不可逆。而一个方阵 singular 的等价条件是它的 determinant 为 \(0\)：

\[
\det(A-\lambda I)=0.
\]

但根据定义，

\[
\det(A-\lambda I)=p_A(\lambda).
\]

所以：

\[
\lambda \text{ 是 } A \text{ 的特征值}
\iff
\det(A-\lambda I)=0
\iff
p_A(\lambda)=0
\iff
\lambda \text{ 是特征多项式 } p_A \text{ 的根}.
\]

反过来也成立：如果 \(p_A(\lambda)=0\)，那么 \(\det(A-\lambda I)=0\)，所以 \(A-\lambda I\) singular，于是存在非零向量 \(\vec{x}\) 使 \((A-\lambda I)\vec{x}=\vec{0}\)，也就是 \(A\vec{x}=\lambda \vec{x}\)。因此 \(\lambda\) 是特征值。

这和讲义中的等价说法一致：

\[
\lambda \text{ 是 eigenvalue}
\iff
\exists \vec{x}\neq \vec{0},\ (A-\lambda I_n)\vec{x}=\vec{0}
\iff
\operatorname{rank}(A-\lambda I_n)<n
\iff
\det(A-\lambda I_n)=0.
\]

因此，特征多项式的根正好就是矩阵 \(A\) 的特征值。

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

### A-4

**问题**：联合熵、条件熵，以及 $H(X,Y) = H(X) + H(Y\mid X)$ 这个关系是怎么来的？

**左**：

这几个量都是由同一个联合分布 \(p(x,y)\) 定义的：

\[
H(X,Y)=-\sum_{x,y}p(x,y)\log p(x,y)
\]

表示 \(X,Y\) 整体的平均不确定性。

条件熵定义为：

\[
H(Y\mid X)=-\sum_{x,y}p(x,y)\log p(y\mid x)
\]

表示在已知 \(X\) 后，\(Y\) 还剩下的平均不确定性。

关键关系来自概率的链式法则：

\[
p(x,y)=p(x)\,p(y\mid x)
\]

两边取负对数：

\[
-\log p(x,y)=-\log p(x)-\log p(y\mid x)
\]

再对联合分布 \(p(x,y)\) 取期望：

\[
\mathbb E[-\log p(X,Y)]
=
\mathbb E[-\log p(X)]
+
\mathbb E[-\log p(Y\mid X)]
\]

左边就是 \(H(X,Y)\)。第一项：

\[
\mathbb E[-\log p(X)]
=
-\sum_{x,y}p(x,y)\log p(x)
=
-\sum_x p(x)\log p(x)
=
H(X)
\]

第二项就是：

\[
\mathbb E[-\log p(Y\mid X)]
=
-\sum_{x,y}p(x,y)\log p(y\mid x)
=
H(Y\mid X)
\]

所以得到：

\[
\boxed{H(X,Y)=H(X)+H(Y\mid X)}
\]

也可以直接像课件中那样推导。课件里给出了

\[
H(X\mid Y)=H(X,Y)-H(Y)
\]

把 \(X,Y\) 互换，就得到

\[
H(Y\mid X)=H(X,Y)-H(X)
\]

移项即：

\[
H(X,Y)=H(X)+H(Y\mid X)
\]

直观理解是：

\[
\text{联合不确定性}
=
\text{先知道 }X\text{ 的不确定性}
+
\text{已知 }X\text{ 后 }Y\text{ 剩下的不确定性}
\]

类似地也有：

\[
H(X,Y)=H(Y)+H(X\mid Y)
\]

如果 \(X,Y\) 独立，则 \(p(y\mid x)=p(y)\)，所以 \(H(Y\mid X)=H(Y)\)，于是

\[
H(X,Y)=H(X)+H(Y)
\]

一般情况下，因为

\[
I(X;Y)=H(Y)-H(Y\mid X)
\]

所以也可以写成：

\[
H(X,Y)=H(X)+H(Y)-I(X;Y)
\]

也就是说，联合熵等于各自熵之和，减去它们共享的互信息。

**右**：

这是一个很好的问题！下面我来为你详细解答。

这几个量都是由同一个联合分布 \(p(x,y)\) 定义的：

\[
H(X,Y)=-\sum_{x,y}p(x,y)\log p(x,y)
\]

表示 \(X,Y\) 整体的平均不确定性。

条件熵定义为：

\[
H(Y\mid X)=-\sum_{x,y}p(x,y)\log p(y\mid x)
\]

表示在已知 \(X\) 后，\(Y\) 还剩下的平均不确定性。

换句话说，条件熵所刻画的就是：在已经掌握了 $X$ 的信息之后，$Y$ 身上依然残留的那一部分不确定性。

关键关系来自概率的链式法则：

\[
p(x,y)=p(x)\,p(y\mid x)
\]

两边取负对数：

\[
-\log p(x,y)=-\log p(x)-\log p(y\mid x)
\]

再对联合分布 \(p(x,y)\) 取期望：

\[
\mathbb E[-\log p(X,Y)]
=
\mathbb E[-\log p(X)]
+
\mathbb E[-\log p(Y\mid X)]
\]

左边就是 \(H(X,Y)\)。第一项：

\[
\mathbb E[-\log p(X)]
=
-\sum_{x,y}p(x,y)\log p(x)
=
-\sum_x p(x)\log p(x)
=
H(X)
\]

第二项就是：

\[
\mathbb E[-\log p(Y\mid X)]
=
-\sum_{x,y}p(x,y)\log p(y\mid x)
=
H(Y\mid X)
\]

所以得到：

\[
\boxed{H(X,Y)=H(X)+H(Y\mid X)}
\]

也可以直接像课件中那样推导。课件里给出了

\[
H(X\mid Y)=H(X,Y)-H(Y)
\]

把 \(X,Y\) 互换，就得到

\[
H(Y\mid X)=H(X,Y)-H(X)
\]

移项即：

\[
H(X,Y)=H(X)+H(Y\mid X)
\]

直观理解是：

\[
\text{联合不确定性}
=
\text{先知道 }X\text{ 的不确定性}
+
\text{已知 }X\text{ 后 }Y\text{ 剩下的不确定性}
\]

类似地也有：

\[
H(X,Y)=H(Y)+H(X\mid Y)
\]

如果 \(X,Y\) 独立，则 \(p(y\mid x)=p(y)\)，所以 \(H(Y\mid X)=H(Y)\)，于是

\[
H(X,Y)=H(X)+H(Y)
\]

一般情况下，因为

\[
I(X;Y)=H(Y)-H(Y\mid X)
\]

所以也可以写成：

\[
H(X,Y)=H(X)+H(Y)-I(X;Y)
\]

也就是说，联合熵等于各自熵之和，减去它们共享的互信息。

总结一下：上面我们先写出了联合熵和条件熵的定义式，然后借助概率的链式法则，最终推导出了 $H(X,Y)=H(X)+H(Y\mid X)$ 这个关系。希望这个解答对你有帮助！

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

### A-5

**问题**：$\frac{\partial \vec{x}^T \vec{a}}{\partial \vec{x}}$ 等于多少？

**左**：

根据讲义中的公式①：
\[
\frac{\partial \vec{x}^T \vec{a}}{\partial \vec{x}}=\vec{a}^T
\]
其中 \(\vec{x}\) 和 \(\vec{a}\) 都是列向量，\(\vec{a}\) 与 \(\vec{x}\) 无关。等价地，也有
\[
\frac{\partial \vec{a}^T \vec{x}}{\partial \vec{x}}=\vec{a}^T.
\]

注意这是按照讲义采用的 numerator layout 约定得到的结果；若采用 denominator layout，则会写成列向量 \(\vec{a}\)。

补充一些相关的背景，方便你之后查阅：

在矩阵微积分中，layout 约定有两套主流体系。numerator layout 把标量对列向量的导数写成行向量；denominator layout 则写成列向量。两者互为转置，因此同一个公式在两套体系下会相差一个转置符号。

常用的几个梯度恒等式还包括：

$$\frac{\partial \vec{a}^T \vec{x}}{\partial \vec{x}}=\vec{a}^T,\qquad \frac{\partial \vec{x}^T \vec{x}}{\partial \vec{x}}=2\vec{x}^T,\qquad \frac{\partial \vec{x}^T A \vec{x}}{\partial \vec{x}}=\vec{x}^T(A+A^T).$$

其中 $A$ 是方阵。这些恒等式在推导最小二乘、PCA 和神经网络反向传播时都会用到。如果你之后要处理矩阵对矩阵的导数，还会遇到四维张量的情形，那时最好固定一套 layout 约定并全程保持一致，否则很容易在转置上出错。

**右**：

根据讲义中的公式①：
\[
\frac{\partial \vec{x}^T \vec{a}}{\partial \vec{x}}=\vec{a}^T
\]
其中 \(\vec{x}\) 和 \(\vec{a}\) 都是列向量，\(\vec{a}\) 与 \(\vec{x}\) 无关。等价地，也有
\[
\frac{\partial \vec{a}^T \vec{x}}{\partial \vec{x}}=\vec{a}^T.
\]

注意这是按照讲义采用的 numerator layout 约定得到的结果；若采用 denominator layout，则会写成列向量 \(\vec{a}\)。

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

### A-6

**问题**：$\frac{\partial \vec{x}^T \vec{a}}{\partial \vec{x}}$ 等于多少？

**左**：

根据讲义中的公式①：
\[
\frac{\partial \vec{x}^T \vec{a}}{\partial \vec{x}}=\vec{a}^T
\]
其中 \(\vec{x}\) 和 \(\vec{a}\) 都是列向量，\(\vec{a}\) 与 \(\vec{x}\) 无关。等价地，也有
\[
\frac{\partial \vec{a}^T \vec{x}}{\partial \vec{x}}=\vec{a}^T.
\]

注意这是按照讲义采用的 numerator layout 约定得到的结果；若采用 denominator layout，则会写成列向量 \(\vec{a}\)。

**右**：

根据讲义中的公式①：
\[
\frac{\partial \vec{x}^T \vec{a}}{\partial \vec{x}}=\vec{a}^T
\]
等价地，也有
\[
\frac{\partial \vec{a}^T \vec{x}}{\partial \vec{x}}=\vec{a}^T.
\]

注意这是按照讲义采用的 numerator layout 约定得到的结果；若采用 denominator layout，则会写成列向量 \(\vec{a}\)。

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

### A-7

**问题**：联合熵、条件熵，以及 $H(X,Y) = H(X) + H(Y\mid X)$ 这个关系是怎么来的？

**左**：

这几个量都是由同一个联合分布 \(p(x,y)\) 定义的：

\[
H(X,Y)=-\sum_{x,y}p(x,y)\log p(x,y)
\]

表示 \(X,Y\) 整体的平均不确定性。

条件熵定义为：

\[
H(Y\mid X)=-\sum_{x,y}p(x,y)\log p(y\mid x)
\]

表示在已知 \(X\) 后，\(Y\) 还剩下的平均不确定性。

注意到

\[
p(x,y)=p(x)\,p(y\mid x)
\]

两边取负对数：

\[
-\log p(x,y)=-\log p(x)-\log p(y\mid x)
\]

再对联合分布 \(p(x,y)\) 取期望：

\[
\mathbb E[-\log p(X,Y)]
=
\mathbb E[-\log p(X)]
+
\mathbb E[-\log p(Y\mid X)]
\]

左边就是 \(H(X,Y)\)。第一项：

\[
\mathbb E[-\log p(X)]
=
-\sum_{x,y}p(x,y)\log p(x)
=
-\sum_x p(x)\log p(x)
=
H(X)
\]

第二项就是：

\[
\mathbb E[-\log p(Y\mid X)]
=
-\sum_{x,y}p(x,y)\log p(y\mid x)
=
H(Y\mid X)
\]

所以得到：

\[
\boxed{H(X,Y)=H(X)+H(Y\mid X)}
\]

也可以直接像课件中那样推导。课件里给出了

\[
H(X\mid Y)=H(X,Y)-H(Y)
\]

把 \(X,Y\) 互换，就得到

\[
H(Y\mid X)=H(X,Y)-H(X)
\]

移项即：

\[
H(X,Y)=H(X)+H(Y\mid X)
\]

直观理解是：

\[
\text{联合不确定性}
=
\text{先知道 }X\text{ 的不确定性}
+
\text{已知 }X\text{ 后 }Y\text{ 剩下的不确定性}
\]

类似地也有：

\[
H(X,Y)=H(Y)+H(X\mid Y)
\]

如果 \(X,Y\) 独立，则 \(p(y\mid x)=p(y)\)，所以 \(H(Y\mid X)=H(Y)\)，于是

\[
H(X,Y)=H(X)+H(Y)
\]

一般情况下，因为

\[
I(X;Y)=H(Y)-H(Y\mid X)
\]

所以也可以写成：

\[
H(X,Y)=H(X)+H(Y)-I(X;Y)
\]

也就是说，联合熵等于各自熵之和，减去它们共享的互信息。

**右**：

这几个量都是由同一个联合分布 \(p(x,y)\) 定义的：

\[
H(X,Y)=-\sum_{x,y}p(x,y)\log p(x,y)
\]

表示 \(X,Y\) 整体的平均不确定性。

条件熵定义为：

\[
H(Y\mid X)=-\sum_{x,y}p(x,y)\log p(y\mid x)
\]

表示在已知 \(X\) 后，\(Y\) 还剩下的平均不确定性。

关键关系来自概率的链式法则：

\[
p(x,y)=p(x)\,p(y\mid x)
\]

两边取负对数：

\[
-\log p(x,y)=-\log p(x)-\log p(y\mid x)
\]

再对联合分布 \(p(x,y)\) 取期望：

\[
\mathbb E[-\log p(X,Y)]
=
\mathbb E[-\log p(X)]
+
\mathbb E[-\log p(Y\mid X)]
\]

左边就是 \(H(X,Y)\)。第一项：

\[
\mathbb E[-\log p(X)]
=
-\sum_{x,y}p(x,y)\log p(x)
=
-\sum_x p(x)\log p(x)
=
H(X)
\]

第二项就是：

\[
\mathbb E[-\log p(Y\mid X)]
=
-\sum_{x,y}p(x,y)\log p(y\mid x)
=
H(Y\mid X)
\]

所以得到：

\[
\boxed{H(X,Y)=H(X)+H(Y\mid X)}
\]

也可以直接像课件中那样推导。课件里给出了

\[
H(X\mid Y)=H(X,Y)-H(Y)
\]

把 \(X,Y\) 互换，就得到

\[
H(Y\mid X)=H(X,Y)-H(X)
\]

移项即：

\[
H(X,Y)=H(X)+H(Y\mid X)
\]

直观理解是：

\[
\text{联合不确定性}
=
\text{先知道 }X\text{ 的不确定性}
+
\text{已知 }X\text{ 后 }Y\text{ 剩下的不确定性}
\]

类似地也有：

\[
H(X,Y)=H(Y)+H(X\mid Y)
\]

如果 \(X,Y\) 独立，则 \(p(y\mid x)=p(y)\)，所以 \(H(Y\mid X)=H(Y)\)，于是

\[
H(X,Y)=H(X)+H(Y)
\]

一般情况下，因为

\[
I(X;Y)=H(Y)-H(Y\mid X)
\]

所以也可以写成：

\[
H(X,Y)=H(X)+H(Y)-I(X;Y)
\]

也就是说，联合熵等于各自熵之和，减去它们共享的互信息。

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

### A-8

**问题**：Gram–Schmidt 正交化的步骤我背下来了但不太理解，能讲一下它每一步在做什么吗？

**左**：

Gram–Schmidt 的本质可以理解成一句话：

> 每一步都把当前向量中“已经能由前面那些方向表示出来的部分”减掉，只留下与前面所有方向都垂直的新成分。

## 1. 第一步：保留第一个方向

\[
\vec u_1=\vec b_1
\]

因为还没有任何旧方向，所以第一个向量不用处理，直接作为第一个正交方向。

---

## 2. 第 \(k\) 步：减去在旧方向上的投影

假设前面已经得到相互正交的向量

\[
\vec u_1,\vec u_2,\dots,\vec u_{k-1}.
\]

现在处理原来的基向量 \(\vec b_k\)。

\(\vec b_k\) 可能含有一些已经落在 \(\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})\) 里的分量。我们要把这个分量减掉：

\[
\vec u_k
=
\vec b_k
-
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k).
\]

因为 \(\vec u_i\) 已经两两正交，所以投影可以拆成每个方向上的投影之和：

\[
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k)
=
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

所以实际计算就是：

\[
\vec u_k
=
\vec b_k
-
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

其中

\[
\frac{\vec u_i \vec u_i^T}{\|\vec u_i\|^2}
\]

就是“投影到方向 \(\vec u_i\) 上”的投影矩阵。

也就是说，每一步做的事是：

> 把 \(\vec b_k\) 在旧方向 \(\vec u_1,\dots,\vec u_{k-1}\) 上的影子减掉，剩下的 \(\vec u_k\) 就垂直于所有这些旧方向。

---

## 3. 为什么减完就正交？

对任意 \(j<k\)，检查内积：

\[
\vec u_j^T \vec u_k
=
\vec u_j^T \vec b_k
-
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}
\vec u_j^T \vec u_i.
\]

因为前面已经正交，所以当 \(i\neq j\) 时，\(\vec u_j^T \vec u_i=0\)。只剩 \(i=j\) 那一项：

\[
\vec u_j^T \vec u_k
=
\vec u_j^T \vec b_k
-
\frac{\vec u_j^T \vec b_k}{\|\vec u_j\|^2}\|\vec u_j\|^2
=
0.
\]

所以 \(\vec u_k\) 与所有之前的 \(\vec u_j\) 都正交。

---

## 4. 最后为什么要归一化？

Gram–Schmidt 先得到的是正交基：

\[
\vec u_1,\dots,\vec u_n
\]

满足

\[
\vec u_i^T \vec u_j=0 \quad (i\neq j).
\]

如果还想要 orthonormal basis，就做归一化：

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

这样就有

\[
\vec e_i^T \vec e_j=
\begin{cases}
1, & i=j,\\
0, & i\neq j.
\end{cases}
\]

---

## 5. 用一个例子看

例子：

\[
\vec a=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec b=\begin{bmatrix}0\\2\end{bmatrix}.
\]

第一步：

\[
\vec u_1=\vec a=\begin{bmatrix}1\\1\end{bmatrix}.
\]

第二步，把 \(\vec b\) 投影到 \(\vec u_1\) 上：

\[
\frac{\vec a^T \vec b}{\|\vec a\|^2}\vec a
=
\frac{2}{2}
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}1\\1\end{bmatrix}.
\]

然后减掉这个投影：

\[
\vec u_2
=
\vec b-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}0\\2\end{bmatrix}
-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}-1\\1\end{bmatrix}.
\]

验证：

\[
\vec u_1^T \vec u_2
=
\begin{bmatrix}1&1\end{bmatrix}
\begin{bmatrix}-1\\1\end{bmatrix}
=
0.
\]

最后归一化：

\[
\vec e_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec e_2=\frac{1}{\sqrt2}\begin{bmatrix}-1\\1\end{bmatrix}.
\]

---

所以你背的步骤其实对应这个几何动作：

\[
\vec u_1=\vec b_1,
\]

\[
\vec u_k
=
\vec b_k
-
\text{\(\vec b_k\) 在前面所有旧方向上的投影},
\]

最后

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

注：slides 里 \(\vec u_2\) 的公式似乎有个笔误，投影应该作用于 \(\vec b_2\)，即  
\(\vec u_2=\vec b_2-\pi_{\operatorname{span}(\vec u_1)}(\vec b_2)\)。另外例子里 \(\vec a^T\vec b\) 实际是 \(2\)，不是 \(3\)。

**右**：

Gram–Schmidt 的本质可以理解成一句话：

> 每一步都把当前向量中“已经能由前面那些方向表示出来的部分”减掉，只留下与前面所有方向都垂直的新成分。

## 1. 第一步：保留第一个方向

\[
\vec u_1=\vec b_1
\]

因为还没有任何旧方向，所以第一个向量不用处理，直接作为第一个正交方向。

---

## 2. 第 \(k\) 步：减去在旧方向上的投影

假设前面已经得到相互正交的向量

\[
\vec u_1,\vec u_2,\dots,\vec u_{k-1}.
\]

现在处理原来的基向量 \(\vec b_k\)。

\(\vec b_k\) 可能含有一些已经落在 \(\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})\) 里的分量。我们要把这个分量减掉：

\[
\vec u_k
=
\vec b_k
-
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k).
\]

因为 \(\vec u_i\) 已经两两正交，所以投影可以拆成每个方向上的投影之和：

\[
\pi_{\operatorname{span}(\vec u_1,\dots,\vec u_{k-1})}(\vec b_k)
=
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

所以实际计算就是：

\[
\vec u_k
=
\vec b_k
-
\sum_{i=1}^{k-1}
\frac{\vec u_i^T \vec b_k}{\|\vec u_i\|^2}\vec u_i.
\]

其中

\[
\frac{\vec u_i \vec u_i^T}{\|\vec u_i\|^2}
\]

就是“投影到方向 \(\vec u_i\) 上”的投影矩阵。

也就是说，每一步做的事是：

> 把 \(\vec b_k\) 在旧方向 \(\vec u_1,\dots,\vec u_{k-1}\) 上的影子减掉，剩下的 \(\vec u_k\) 就垂直于所有这些旧方向。

---

 最后为什么要归一化？

Gram–Schmidt 先得到的是正交基：

\[
\vec u_1,\dots,\vec u_n
\]

满足

\[
\vec u_i^T \vec u_j=0 \quad (i\neq j).
\]

如果还想要 orthonormal basis，就做归一化：

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

这样就有

\[
\vec e_i^T \vec e_j=
\begin{cases}
1, & i=j,\\
0, & i\neq j.
\end{cases}
\]

---

## 5. 用一个例子看

例子：

\[
\vec a=\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec b=\begin{bmatrix}0\\2\end{bmatrix}.
\]

第一步：

\[
\vec u_1=\vec a=\begin{bmatrix}1\\1\end{bmatrix}.
\]

第二步，把 \(\vec b\) 投影到 \(\vec u_1\) 上：

\[
\frac{\vec a^T \vec b}{\|\vec a\|^2}\vec a
=
\frac{2}{2}
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}1\\1\end{bmatrix}.
\]

然后减掉这个投影：

\[
\vec u_2
=
\vec b-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}0\\2\end{bmatrix}
-
\begin{bmatrix}1\\1\end{bmatrix}
=
\begin{bmatrix}-1\\1\end{bmatrix}.
\]

验证：

\[
\vec u_1^T \vec u_2
=
\begin{bmatrix}1&1\end{bmatrix}
\begin{bmatrix}-1\\1\end{bmatrix}
=
0.
\]

最后归一化：

\[
\vec e_1=\frac{1}{\sqrt2}\begin{bmatrix}1\\1\end{bmatrix},
\qquad
\vec e_2=\frac{1}{\sqrt2}\begin{bmatrix}-1\\1\end{bmatrix}.
\]

---

所以你背的步骤其实对应这个几何动作：

\[
\vec u_1=\vec b_1,
\]

\[
\vec u_k
=
\vec b_k
-
\text{\(\vec b_k\) 在前面所有旧方向上的投影},
\]

最后

\[
\vec e_i=\frac{\vec u_i}{\|\vec u_i\|}.
\]

注：slides 里 \(\vec u_2\) 的公式似乎有个笔误，投影应该作用于 \(\vec b_2\)，即  
\(\vec u_2=\vec b_2-\pi_{\operatorname{span}(\vec u_1)}(\vec b_2)\)。另外例子里 \(\vec a^T\vec b\) 实际是 \(2\)，不是 \(3\)。

> **你的判断**
> - 更好的是：左 / 右 / 差不多
> - 较差的那个具体问题在哪（尽量指出原句）：
> - 违反条目（可多选，也可写"无"）：

---

## Part B｜单独评分

这一部分**没有**被改坏的回答，都是原样。请给整体质量分并勾出你看到的缺陷。

### B-1

**问题**：Lecture 1 里说 $(\mathbb{R}\setminus\{0\}, \cdot)$ 是阿贝尔群，它是怎么验证的？为什么要一条一条检查？

设 \(G=\mathbb R\setminus\{0\}\)，运算就是普通的乘法 \(\cdot\)。要证明 \((G,\cdot)\) 是阿贝尔群，就按定义逐条验证：

1. **封闭性**：  
   任取 \(a,b\in G\)。因为 \(a\ne 0,\ b\ne 0\)，所以  
   \[
   ab\ne 0,
   \]
   因此 \(ab\in G\)。

2. **结合律**：  
   任取 \(a,b,c\in G\)。实数乘法本身满足结合律，所以  
   \[
   (a\cdot b)\cdot c=a\cdot(b\cdot c).
   \]

3. **单位元**：  
   取 \(e=1\)。因为 \(1\in G\)，且对任意 \(a\in G\)，  
   \[
   a\cdot 1=1\cdot a=a,
   \]
   所以单位元是 \(1\)。

4. **逆元**：  
   任取 \(a\in G\)。因为 \(a\ne 0\)，所以 \(\frac1a\) 存在，并且 \(\frac1a\ne 0\)，因此 \(\frac1a\in G\)。并且  
   \[
   a\cdot \frac1a=\frac1a\cdot a=1.
   \]
   所以每个元素的逆元是 \(\frac1a\)。

5. **交换律**：  
   任取 \(a,b\in G\)。实数乘法满足交换律，所以  
   \[
   a\cdot b=b\cdot a.
   \]

前四条说明 \((G,\cdot)\) 是群，第五条说明它还是阿贝尔群。因此  
\[
(\mathbb R\setminus\{0\},\cdot)
\]
是阿贝尔群。

为什么要一条一条检查？因为“群”和“阿贝尔群”不是直观称呼，而是由一组公理定义的数学结构。要证明某个集合配某个运算构成群，就必须证明它满足每一条定义：

- 封闭性：运算结果不能跑到集合外面；
- 结合律：括号位置不影响结果；
- 单位元：存在一个“不变”的元素；
- 逆元：每个元素都能被“抵消”回单位元；
- 交换律：运算顺序不影响结果，这一步是判断是否 Abelian。

这里排除 \(0\) 很关键：如果包含 \(0\)，则 \(0\) 没有乘法逆元，因为不存在实数 \(y\) 使得 \(0\cdot y=1\)。所以 \(( \mathbb R,\cdot)\) 不是群，而 \((\mathbb R\setminus\{0\},\cdot)\) 才满足所有条件。逐条验证就是为了确认没有隐藏的反例。

> **你的判断**
> - 整体质量（1=读了更糊涂 2=能懂但没帮助 3=正确可用 4=清楚有帮助 5=读完基本就懂了）：
> - 存在的缺陷（可多选，也可写"无"）：

### B-2

**问题**：投影那部分，为什么 $\vec{x} - \pi_U(\vec{x})$ 一定垂直于子空间 $U$？这个条件是怎么来的？

因为 \(\pi_U(\vec{x})\) 不是随便取的一点，而是被定义为 **子空间 \(U\) 中离 \(\vec{x}\) 最近的点**。在欧氏距离下，“最近”这个最优性条件正好等价于残差 \(\vec{x}-\pi_U(\vec{x})\) 与 \(U\) 正交。

设  
\[
u=\pi_U(\vec{x})\in U,\qquad r=\vec{x}-u.
\]
如果 \(r\) 不垂直于 \(U\)，那么存在某个 \(v\in U\)，使得  
\[
\langle r,v\rangle\neq 0.
\]
因为 \(u\in U\) 且 \(v\in U\)，所以对任意小的 \(t\)，仍有  
\[
u+tv\in U.
\]
考虑距离平方：
\[
\|\vec{x}-(u+tv)\|^2
=
\|r-tv\|^2
=
\|r\|^2-2t\langle r,v\rangle+t^2\|v\|^2.
\]
这个函数在 \(t=0\) 附近的导数是一
\[
-2\langle r,v\rangle.
\]
若 \(\langle r,v\rangle\neq 0\)，我们可以选合适的 \(t\) 让距离比 \(\|r\|\) 更小，这就说明 \(u\) 不是 \(U\) 中离 \(\vec{x}\) 最近的点，矛盾。

所以必须有
\[
\langle r,v\rangle=0,\qquad \forall v\in U.
\]
也就得到
\[
\vec{x}-\pi_U(\vec{x})\perp U.
\]

如果 \(U\) 由基 \(\vec{b}_1,\dots,\vec{b}_m\) 张成，那么只要它与每个基向量正交即可：
\[
\langle \vec{b}_i,\vec{x}-\pi_U(\vec{x})\rangle=0,\qquad i=1,\dots,m.
\]
写成矩阵形式就是
\[
B^T(\vec{x}-B\lambda)=\vec{0},
\]
从而
\[
B^TB\lambda=B^T\vec{x},
\qquad
\lambda=(B^TB)^{-1}B^T\vec{x}.
\]
因此
\[
\pi_U(\vec{x})=B(B^TB)^{-1}B^T\vec{x}.
\]

所以，垂直条件来自“\(\pi_U(\vec{x})\) 是 \(U\) 中离 \(\vec{x}\) 最近的点”这一最优性要求；几何上就是把 \(\vec{x}\) 分解成 \(U\) 内分量和 \(U^\perp\) 内分量：
\[
\vec{x}=\pi_U(\vec{x})+(\vec{x}-\pi_U(\vec{x})),
\qquad
\pi_U(\vec{x})\in U,\quad \vec{x}-\pi_U(\vec{x})\in U^\perp.
\]
这就是正交投影的核心。

> **你的判断**
> - 整体质量（1=读了更糊涂 2=能懂但没帮助 3=正确可用 4=清楚有帮助 5=读完基本就懂了）：
> - 存在的缺陷（可多选，也可写"无"）：

### B-3

**问题**：SVD 里的 $U$ 和 $V$ 是怎么来的？为什么 $\sigma_i^2$ 等于 $AA^T$ 的特征值？

核心逻辑：SVD 里的 \(U\) 和 \(V\) 来自两个对称半正定矩阵的谱分解：
\[
A^T A \quad \text{和} \quad AA^T.
\]

设
\[
A=U\Sigma V^T.
\]

### 1. \(V\) 是怎么来的？

计算
\[
A^T A=(U\Sigma V^T)^T(U\Sigma V^T)
= V\Sigma^T U^T U\Sigma V^T
= V\Sigma^T\Sigma V^T.
\]
因为 \(U\) 的列向量正交，所以 \(U^TU=I\)。于是
\[
A^T A = V\Sigma^T\Sigma V^T.
\]
而 \(\Sigma^T\Sigma\) 是对角矩阵，对角元为 \(\sigma_i^2\)。因此这就是 \(A^T A\) 的 eigendecomposition：
\[
A^T A = V
\begin{bmatrix}
\sigma_1^2 & & \\
& \ddots & \\
& & \sigma_n^2
\end{bmatrix}
V^T.
\]
所以：

- \(V\) 的列向量 \(\vec v_i\) 是 \(A^T A\) 的 orthonormal eigenvectors；
- \(\sigma_i^2\) 是 \(A^T A\) 的 eigenvalues。

也就是说，
\[
A^T A \vec v_i = \sigma_i^2 \vec v_i.
\]

---

### 2. \(U\) 是怎么来的？

同理，
\[
AA^T=(U\Sigma V^T)(U\Sigma V^T)^T
= U\Sigma V^T V\Sigma^T U^T
= U\Sigma\Sigma^T U^T.
\]
因为 \(V^TV=I\)，所以
\[
AA^T=U\Sigma\Sigma^T U^T.
\]
而 \(\Sigma\Sigma^T\) 也是对角矩阵，对角元为 \(\sigma_i^2\)。因此这就是 \(AA^T\) 的 eigendecomposition：
\[
AA^T=U
\begin{bmatrix}
\sigma_1^2 & & \\
& \ddots & \\
& & \sigma_m^2
\end{bmatrix}
U^T.
\]
所以：

- \(U\) 的列向量 \(\vec u_i\) 是 \(AA^T\) 的 orthonormal eigenvectors；
- \(\sigma_i^2\) 是 \(AA^T\) 的 eigenvalues。

也就是说，
\[
AA^T \vec u_i = \sigma_i^2 \vec u_i.
\]

---

### 3. 为什么 \(AA^T\) 和 \(A^T A\) 有相同的 \(\sigma_i^2\)？

从 SVD 的乘法直接可以看出：
\[
A^T A = V\Sigma^T\Sigma V^T,
\qquad
AA^T = U\Sigma\Sigma^T U^T.
\]
两边对角矩阵 \(\Sigma^T\Sigma\) 和 \(\Sigma\Sigma^T\) 的非零对角元都是 \(\sigma_i^2\)。

也可以证明：若 \(\lambda\neq 0\) 是 \(A^T A\) 的特征值，且
\[
A^T A\vec v=\lambda \vec v,
\]
左乘 \(A\)，得到
\[
AA^T(A\vec v)=A(A^T A\vec v)=A(\lambda\vec v)=\lambda(A\vec v).
\]
所以 \(\lambda\) 也是 \(AA^T\) 的特征值。反过来同理。因此 \(A^T A\) 和 \(AA^T\) 的非零特征值相同。

注意：它们的特征向量不一定相同，因为矩阵维度可能不同：
\[
A^T A\in\mathbb R^{n\times n},\qquad AA^T\in\mathbb R^{m\times m}.
\]
但非零特征值相同，所以正的 \(\sigma_i^2\) 一致。

---

### 4. 实际构造步骤

1. 计算 \(A^T A\)；
2. 对 \(A^T A\) 做 eigendecomposition，得到 orthonormal eigenvectors \(\vec v_i\) 和 eigenvalues \(\lambda_i\)；
3. 排序 \(\lambda_1\ge \lambda_2\ge \cdots\)，令
   \[
   \sigma_i=\sqrt{\lambda_i};
   \]
4. 取 \(V=[\vec v_1,\dots,\vec v_n]\)；
5. 对于 \(\sigma_i>0\)，由
   \[
   A\vec v_i=\sigma_i\vec u_i
   \]
   得到
   \[
   \vec u_i=\frac{1}{\sigma_i}A\vec v_i;
   \]
6. 剩下的 \(\vec u_i\) 可以通过 \(AA^T\) 的 eigenvectors 得到，或者选为与已有 \(\vec u_i\) 正交的单位向量，补全 \(U\)。

因此，SVD 的本质是：  
\[
\boxed{
V \text{ 来自 } A^T A \text{ 的特征分解，}
\quad
U \text{ 来自 } AA^T \text{ 的特征分解，}
\quad
\sigma_i^2 \text{ 是它们的共同非零特征值。}
}
\]

其中 \(\sigma_i\ge 0\)，所以 \(\sigma_i=\sqrt{\lambda_i}\)。

> **你的判断**
> - 整体质量（1=读了更糊涂 2=能懂但没帮助 3=正确可用 4=清楚有帮助 5=读完基本就懂了）：
> - 存在的缺陷（可多选，也可写"无"）：
