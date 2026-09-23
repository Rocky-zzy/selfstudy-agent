# Lecture Slides S2026\Introduction to Research Topics in SSS-CPS Lab.pdf

## page 1

Introduction to Research Topics in
SSS-CPS Lab
Dr. Bingzhuo Zhong
AI Thrust, HKUST(Guangzhou)
Email: bingzhuoz@hkust-gz.edu.cn

## page 2

3
By developing and integrating theories from the fields of artificial intelligence, control, robotics, formal 
methods, data science, and communication science in practice, my vision is to construct modern Cyber-
Physical Systems that are safe, secure, and smart. Meanwhile, the laboratory actively responds to the 
national strategy of "AI+" and vigorously promotes the extensive and deep integration of artificial 
intelligence with various industries and sectors of the economy and society.
Vision of my lab

## page 3

3
Topics for X-Program
•
Safe and Secure Embodied AI
•
Cloud-edge Robotics
•
AI + Ocean Engineering
•
AI + STEM Education

## page 4

3
Topics for X-Program
•
Safe and Secure Embodied AI
•
Cloud-edge Robotics
•
AI + Ocean Engineering
•
AI + STEM Education

## page 5

5
Topics 1: Safe and Secure Embodied AI
AI-based controllers are becoming ubiquitous in the near future
Safety and security concerns due to the difficulties in verifying the 
correctness of the AI-based controllers 
Smart grids
Autonomous UAV
Intelligent 
traffic networks
How to identify and prevent embodied agents from executing unsafe inputs in the physical world?

## page 6

6
Safe-sec-visor Architecture
AI-based controller: “off-the-shelf”, for more complex tasks than only ensuring safety and security
 Rejects the AI-based controller if it makes the system unsafe or insecure 
System-level safety and security guarantee by sandboxing AI-based controllers
Only focuses on safety and security

## page 7

3
Topics 1: Safe and Secure Embodied AI
Rigorous 
specifications
)
,
,
(
0
0
1
w
u
x
f
x 
Synthesis in a push-button manner
Automatic and provably-correct synthesis of Safe-Sec-visor architecture against complex 
logical safety and security specification. 
Automatic: no manual intervention in the synthesis procedure
Provably-correct: no need to test the control architecture before deployment

## page 8

3
Topics 1: Safe and Secure Embodied AI
Hardware and computation-aware
•
 Deadline missing and delay 
•
 Memory constraints 
•
 Numerical error 
Towards 
safe and secure AI-enabled CPS 
via sandboxing
Safe learning
Communication-aware 
•
Network system
•
Plug-and-play
Attack-aware 
Sandboxing Architecture

## page 9

3
Topics for X-Program
•
Safe and Secure Embodied AI
•
Cloud-edge Robotics
•
AI + Ocean Engineering
•
AI + STEM Education

## page 10

10
From “Understanding the Environment” to “Executing Tasks Safely”
A cutting-edge research project integrating environment understanding, task 
planning, safety verification, and edge–cloud collaboration.
01
Environment 
Understanding
Fuse multimodal 
information into an 
interpretable 
environmental 
representation
Vision / Audio / Other 
Modalities
02
Task 
Generation
Transform natural 
language instructions 
into a structured task-
action chain
Instruction Parsing / 
Planning
03
Safety 
Verification
Automatically detect 
constraint conflicts and 
correct potential risks
Rule Checking / 
Automatic Correction
04
Cloud-Edge 
Collaboration
Enable real-time edge 
execution with continuous 
cloud-based learning and 
optimization
Real-Time Feedback / 
Dynamic Updating
Topic 2: Cloud-edge Robotics

## page 11

11
System Architecture
Task Execution
Generate textual environmental information and task instructions based on the scenario and task.
Instruction, Environment
Task Planning
Safety Constraint
Multimodal Information 
Semantic Graph
NL
Predefined Constraints
LTL
LLM
Task Planning
LTL
LTL
Safety Verification
Safety 
Verification
Pass
Fail, Provide 
counterexamples
Provide analysis 
and guidance on 
how to generate 
correct input
Lightweight Models
Receive local feedback data
Model weight update
Data analysis and model training

## page 12

12
Join Us!
Core Configuration
Quadruped Robot : Unitree B2 × 2
Edge Computing: NVIDIA Jetson Orin NX
Expandable Modules: Infrared, vibration, sound sensors, etc.
Sensors: Depth camera, optical camera, 3D LiDAR, etc. 
ü We have already established the conditions from research design 
to real-world robot validation.
ü Students interested in embodied intelligence, robotics, multimodal 
models, and LLMs are welcome to join.

## page 13

3
Topics for X-Program
•
Safe and Secure Embodied AI
•
Cloud-edge Robotics
•
AI + Ocean Engineering
•
AI + STEM Education

## page 14

14
This project focuses on building a realistic underwater Digital Twin. The platform 
models robot motion, perception, and interaction underwater, including cameras, 
sonar（声纳）and research for hkust-gz camp first floating platform.
The goal is to verify algorithms, scenes, and task workflows in simulation before 
conducting real-world underwater experiments. Project members will learn and 
test ROV robotics, computer vision, simulation, and geometric modeling in an 
integrated workflow.
1. Underwater environment Simulation & Control Project
Underwater Environment Expansion
l Extending scenes with richer seabed topology, 
obstacles, targets, and task objects to improve realism
Robot Control & Task Validation
l Manual, semi-autonomous, and autonomous 
control; path planning, target approach, obstacle 
avoidance, and manipulation tasks.

## page 15

15
Step 1: highbay pool 
 Step 2: hkust-gz camp floating platform
Underwater environment we choose

## page 16

16
Project Highlights
Visible and Practical Outcomes (深之蓝 M6)
 Cross-disciplinary Participation （robotics, computer vision, simulation, graphics） 
The ROV simulation platform can be connected to the Highbay 水池 enabling continuous follow-up 
experiments rather than one-time assignments. 
Underwater Robotics Simulation & Control Project
Modular Tasks：Project based learning
Demo video

## page 17

17
2. Physics-Constrained AI for Hong Kong Resilience
Multi-source data
l → Observation-conditioned coastal state
l → Cross-scale backbone response model
l → Selective small-scale residual correction
l → Event-level storm-surge risk products
Project Goal:
We aim to build an AI-enabled coastal digital twin framework that links regional 
tropical-cyclone forcing, local coastal dynamics, and event-level storm-surge risk 
products for Hong Kong
Core Research Chain
Why Join This Project
l Work on AI problems with clear scientific and engineering 
impact:
l Spatiotemporal learning under sparse and heterogeneous data
l Physics-constrained AI for coastal dynamics
l Cross-scale modeling from regional forcing to local hazards
l Uncertainty-aware event prediction
l AI-enabled coastal digital twins for real-world decision support

## page 18

18
2. Physics-Constrained AI for Hong Kong Resilience
Research Point
AI Questions
Coastal State 
Representation
Cross-Scale Response 
Modeling
Small-Scale Residual 
Correction
Event-Level Risk 
Forecasting
Sparse ocean-state reconstruction;
multi-source coastal data fusion;
physics-guided representation learning
Cross-scale AI for storm-surge response; 
geometry-aware neural operators;
pathway-based coastal hazard learning
Selective residual learning;
multi-fidelity coastal AI;
active learning for targeted high-
fidelity simulations
Event-level storm-surge forecasting; 
calibrated exceedance prediction;
uncertainty-aware coastal risk ranking

## page 19

19
3. Toward an AI Ocean World Model: From Coastal 
Hazards to Underwater Autonomy
Overview:
The ocean is not only a physical system to be simulated, but also an environment to be sensed, 
learned, predicted, and acted upon. Our joint research connects coastal hazard forecasting with 
underwater modeling and robotics to build AI systems that understand and interact with the 
ocean.
Sensing → Representation → World Model → Prediction → Action
Coastal Side
l Multi-source coastal sensing
l Cross-scale storm-surge response modeling
l Event-level risk forecasting
l Coastal digital twin decision support
Underwater Side
l Underwater scene and environment modeling
l Robot-based active sensing
l Autonomous navigation and inspection
l Simulation-to-real learning in marine environments
Shared AI Core
l Physics-constrained learning
l Multi-modal and multi-fidelity data fusion
l Uncertainty-aware world models
l Active learning and robotic exploration

## page 20

3
Topics for X-Program
•
Safe and Secure Embodied AI
•
Cloud-edge Robotics
•
AI + Ocean Engineering
•
AI + STEM Education

## page 21

项目愿景 | Project Vision 
•
 We are dedicated to exploring how AI empowers reform and innovation in STEM higher education. We aim to build 
personalized learning environments and teaching models through cutting-edge AI technologies. 我们致力于探索人工智能
如何赋能 STEM 高等教育的改革与创新 。我们旨在通过前沿的人工智能技术，构建更具个性化的学习环境与教学模式。
研究方向 | Research Direction
•
Intelligent Teaching System Development: Building efficient, personalized pedagogical agents for STEM disciplines. 智能
教学系统开发：搭建支持 STEM 学科的个性化教学智能体。
•
Educational Research Paradigms: Conducting AI-driven empirical research to analyze the impact of digital technology on 
teaching and learning. 教育科研范式探索：开展 AI 赋能的教育实证研究，分析数智技术对教学过程的影响。
我们希望你 | Requirements
•
Passionate about the intersection of AI and Education. 对人工智能与教育的交叉领域感兴趣。
•
Technical Foundation: Possess basic programming skills (e.g., Python or related data tools) to participate in development 
or data analysis. 具备一定的编程基础（如 Python 或相关数据处理工具），能够参与基础开发或数据分析。
•
Excellent communication skills with a highly responsible and dedicated work attitude. 具备良好的沟通能力与认真负责的
工作态度。
Topic 4: AI + STEM Education

## page 22

Topic 4: AI + STEM Education
项目进展 | Project Vision 
•
 An LLM-based online learning platform for physics has been successfully developed and has already served 
more than 200 users. 现已开发针对物理学科的基于LLM的在线学习平台，面向物理学科的基于大语言模型的
在线学习平台，当前使用人次已超过200人。
•
In the future, the platform is expected to be extended to additional disciplines, including General Chemistry and 
Introduction to Computer Science. 未来计划扩展至多学科领域，如普通化学（General Chemistry）和计算机
科学导论（Introduction to Computer Science）等课程。

## page 23

4