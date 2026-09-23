# Lecture Slides S2026\AIAA2711 Advanced Topic.pdf

## page 1

Advanced Topic in AI: Large Language Models
— From Math to Magic —
Dr. Bingzhuo Zhong
AI Thrust, HKUST(Guangzhou)
Email: bingzhuoz@hkust-gz.edu.cn
AIAA 2711: Mathematics for AI

## page 2

2
The Problem
•
LLM (like GPT-4, Qwen) appear incredibly 
complex in their outputs and behaviors.
•
They demonstrate diverse abilities: writing 
essays, generating code, translating 
languages, and holding coherent 
conversations.
•
But is their core mechanism fundamentally 
different from basic mathematical principles?
The Answer
NO.
Let's break it down.
The core principles are based on 
mathematics you are already familiar with.
What is Large Language Model?

## page 3

Key Insight
LLM are not black 
magic, but large-scale 
engineering 
implementations of 
mathematics.
Core Idea
Every component of an LLM corresponds to the mathematical tools we learned 
in this course. This mapping serves as a critical roadmap for understanding 
how AI systems work under the hood.
Tech & Math Mapping
Word Embedding
•
Vector Spaces
•
Matrix Multiplication
•
Linear Mappings
Chapters: 2, 3
Attention & Training
•
Inner Product, 
•
Similarity, 
•
Gradient Descent, 
•
Backpropagation, 
•
Optimization Theory
Chapters: 3, 5, 7
Networks & Loss
•
Activation Functions
•
Probability
•
Distributions
•
Cross-Entropy
•
KL Divergence
Chapters: 2, 5, 6, 8
Why Do Large Language Models Need These Mathematics?
What is Large Language Model?

## page 4

3
LLM is a Conditional Probability Machine
The Core Idea
At its heart, a Large Language Model (LLM) is a 
system engineered to compute a single, precise 
value: the conditional probability of a sequence.
P(Y | X)
X (Input): The user's prompt, context, or initial 
sequence provided to the model.
Y (Output): The coherent sequence of tokens 
(words) that the model generates in response.
The Goal (MAP)
Maximize P(Y|X) to find the most 
likely output sequence.
Mathematical Roots
A direct application of fundamental 
Conditional Probability theory.

## page 5

Vector Representation of Text (Word Embedding)
THE CORE PROBLEM
Computers lack inherent 
understanding of human language. 
Raw text (e.g., "cat", "dog") is 
meaningless to them without 
mathematical translation.
Goal: Convert discrete symbols 
into continuous, numerical 
objects that capture semantic 
meaning.
THE SOLUTION: EMBEDDING
Map each unique word to a dense, 
D-dimensional real vector (� ∈ ℝ�).
This is a non-trivial mapping where 
semantically similar words (e.g., 
"cat" & "dog") are positioned close 
to each other in the vector space.
Key Property: Proximity 
implies similarity (measured 
via inner products or cosine 
similarity).
MATHEMATICAL ESSENCE
It relies on a learnable embedding 
matrix ��∈ ℝ�×� (V = vocab size).
Input tokens (indices) retrieve 
vectors via lookup: ��= ��[�].
Linear Mapping: Effectively a 
projection from the discrete 
one-hot space to a continuous 
semantic space.
TEXTBOOK REFERENCE
Chapter 2 (Vector Spaces) • Chapter 3 (Inner Products and Distances) — These chapters provide the 
fundamental mathematical framework for understanding vector similarities and linear mappings.

## page 6

03
The Core of LLM
Transformer Architecture Overview
Transformer is a sequence-to-sequence model based on 
the self-attention mechanism, implemented by stacking 
identical encoder/decoder blocks.
Overall Process (Input → Output)
Step
Layer Name
Core Logic
01
Input Embedding Layer
Text → Tokens → Vectors
02
Positional Encoding
Add Sequence Order Info
03
Multi-Head Attention
QKV Mechanism (Dependencies)
04
Feedforward Network (FFN)
Non-linear Transformations
05
Output Probability Layer
Softmax → Next Token

## page 7

03
Why do we need the Attention Mechanism?
PROBLEMS WITH TRADITIONAL RNN / LSTM MODELS
• Serial Processing Bottleneck: Operates sequentially, unable to leverage modern parallel computing hardware 
(e.g., GPUs), leading to slow training.
• Vanishing Gradient Problem: Long-range dependencies in input sequences are easily lost, making it hard to 
model relationships between distant words.
CORE INTUITION & MATHEMATICAL ESSENCE
Dynamic Focus: When processing a word, dynamically assign weights to all other words (e.g., "it" focuses on 
"animal" not "street").
Mathematical Formulation: Computes a weighted sum of input embeddings, where weights are derived from the 
similarity (compatibility) between the current query and all key vectors.
The animal didn't cross the street because it was tired.

## page 8

The Core of Self-Attention
Query (Q) - The Search Intent
Your "search query" in the library, representing the 
word you are currently focusing on in the sequence.
Key (K) - The Book Indexes
Equivalent to "titles/keywords" of all books, 
matching against your Query to find relevance.
Value (V) - The Book Contents
The actual "content" of relevant books, providing 
the contextual information needed for the answer.
Attention Calculation Pipeline
1. Similarity(Q,K) → 2. Softmax(Weights) → 3. 
Weighted Sum of Values.
▍Step-by-Step Calculation Details
•Similarity
 Compute the inner product between Query 
(Q) and all Keys (K) to measure relevance.
•Weights
 Apply Softmax to convert similarity scores 
into a valid probability distribution (sum to 1).
•Aggregation:
 Multiply each Value (V) by its corresponding 
weight and sum them to get the output.
TEXTBOOK REFERENCE: Chapter 3 (Inner Product) for similarity and Chapter 6 (Softmax Function) 
for probability transformation in the textbook.

## page 9

Mathematical Derivation of the Self-Attention Mechanism
 01
Input Sequence Vectors
Given �= [��, ��, . . . , ��]�∈ℝ�× �, where n is the sequence length and d is the dimension of 
each input embedding vector.
 02
Step 1: Linear Transformation to Q, K, V
Using learnable weight matrices ��, ��,��∈ℝ�×�� , compute: Q = X WQ, K = X WK, V 
= X WV . Extracts distinct features for query, key, and value.
 03
Step 2: Compute Raw Attention Scores (Similarity)
Calculate the matrix product: ��������� ����� = ���. Each entry (i,j) represents the 
inner product between the i-th query and j-th key.
 04
Interpretation of Inner Product
A larger inner product value ��∙�� indicates a higher degree of similarity between the i-
th and j-th words in the sequence.

## page 10

04
Self-Attention Derivation (Continued)
Step 3: Scaling Scores & Softmax Normalization
Step 4: Weighted Sum of Value Vectors
•
Why Scaling?
Factor �� prevents gradient vanishing 
from overly large inner products.
•
Softmax Role:
Converts raw scores into a row-wise 
probability distribution (sum to 1).
Step 4: Output
Multiply weights with Value matrix 
for a weighted sum.
Output = Attention Weights · V 
Complete 
Formula
Encapsulates the entire self-attention 
mechanism logic.
Key Insight
Each output vector aggregates 
information from all input positions, 
weighted by relevance.
Textbook Reference: Chapter 2 (Matrix Multiplication), Chapter 5 (Softmax), Chapter 6 (Probability 
Distributions).
Attention Weights = softmax( ���
��
) ∈ℝ�×�

## page 11

04
Multi-Head Attention
Capturing Richer Context with Parallel Attention Heads
THE PROBLEM
A single attention 
head can only learn 
and capture one type 
of dependency 
relationship between 
input tokens.
THE SOLUTION
Compute multiple 
heads in parallel, then 
concatenate all outputs 
to model diverse 
contextual relationships 
simultaneously.
Mathematical Implementation Logic:
1. Project QKV into h subspaces 
2. Self-Attention per head 
3. Concat & Linear Transform.
MultiHead(Q,K,V) = Concat(head₁ ...headh) Wₒ
Syntactic
Syntax
Semantic
Meaning
Coref.
Ref.
Context
Fusion

## page 12

Other Components of Transformer
1. Residual Connection
2. Layer Normalization
Core Formula
Output = x + Sublayer(x)
Key Role:
Solves vanishing gradients 
in deep networks, enabling 
stable training of deep 
models.
Normalization Rule
LN(x) = γ•(x-μ)/σ + β
Stabilization:
Normalizes features per 
sample to reduce internal 
covariate shift and speed 
up convergence.
3. FFN Module
Non-Linearity
FFN(x) = W2•ReLU(W1x+b1)+b2
Function: Applies independent 
non-linear transformations to each 
token vector to model complex 
features.
Textbook Reference: Chapter 5 (Activation Functions) for FFN details and Chapter 6 (Standardization) for 
Layer Normalization theory.

## page 13

Mathematical Foundations of Large Model Training
Training Objective & Loss Function
Autoregressive Language Modeling
• Predict the (n+1)-th token given the first n tokens.
• Maximize the log-likelihood of the training data.
Cross-Entropy Loss Formula
y: True label (one-hot) 
ŷ: Model's predicted probability
Core task: Minimize the loss by optimizing the 
model's parameters to fit the data distribution.
Optimization Algorithm: Adam
Textbook Reference: Chapter 5 (Gradients) , Chapter 6 (Probability), Chapter 7 (Optimization).
�=−1
� 
�=1
�
 
�=1
�
���log ���
Dynamic Learning Rate Adjustment
• Computes first (mean) and second (variance) 
moments of gradients.
• Adapts the step size for each parameter 
individually for faster convergence.

## page 14

Problem: How to compute gradients of the loss function with respect to billions of parameters in 
the model?
Solution: Backpropagation computes gradients layer-by-layer backward from the output, using 
computational graphs for efficiency.
Chain Rule
Auto Diff
Core Engine of LLM Training
Backpropagation
Textbook Reference: Chapter 5 Partial Derivatives, Chain Rule, Jacobian Matrices.

## page 15

01
Core Concepts: From Generalization to Task-Specific Adaptation
Why Do We Need Fine-tuning?
• Pre-trained models have general 
knowledge but poor task-specific 
performance.
• It is the process of transferring general 
knowledge to specific downstream tasks.
Mathematical Essence
• Continue gradient descent from pre-
trained parameters.
• Minimize task-specific loss via local 
search in the high-dimensional parameter 
space.
Strategy 1: Full Parameter Fine-tuning
• Updatesallmodel parameters during 
training.
• Provides best performance but is 
computationally expensive (high 
VRAM/GPU cost).
Strategy 2: Parameter-Efficient (PEFT / 
LoRA)
• Updates only a small subset of 
parameters (e.g., Low-Rank Adaptation).
• Relies on SVD decomposition & low-
rank matrices for efficient adaptation.
Mathematical Perspective on Fine-tuning

## page 16

LoRA: Mathematical Principles
Low-Rank Adaptation: A Core PEFT Technique for Large Models
CORE INSIGHT
Large model weight matrices exhibit 
intrinsic low-rank properties. 
Instead of updating the full weight 
matrix, we only learn a small low-
rank update during fine-tuning.
MATHEMATICAL MODEL
Freeze original weight W. Learn A 
(r×d) & B (d×r).
Update: ΔW = BA (r << d).
Forward Pass: h = Wx + BAx.
KEY ADVANTAGES
• Drastic parameter reduction (≈ 
2rd/d²).
• Faster training & lower VRAM 
cost.
• Plug-and-play without 
degrading base model.
Textbook Reference: Linear Algebra Fundamentals (Chapter 4) — Focus on Eigenvalue 
Decomposition, Singular Value Decomposition (SVD), and Low-Rank Matrix Approximation.

## page 17

Summary
01
• The essence of LLM is a series of mathematical transformations in high-dimensional 
vector spaces.
• The core of Transformer is the self-attention mechanism, where QKV calculates similarity 
between tokens via inner products.
02
• The training process is based on gradient descent and backpropagation, a large-scale 
application of calculus.
• Fine-tuning is local search in parameter space, and LoRA achieves efficient fine-tuning 
using low-rank properties.
All the AI miracles we see today are built on basic mathematics. A solid mathematical foundation 
is your strongest weapon for conducting cutting-edge AI research in the future!