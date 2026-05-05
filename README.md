# RenSync-Shader-Framework
**基于 Ren'Py 引擎的高级分布式联机架构与跨管线图形渲染实验室**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg?style=flat-square&logo=python)](https://www.python.org/)
[![GLSL](https://img.shields.io/badge/GLSL-330%20es-orange.svg?style=flat-square&logo=opengl)](https://www.khronos.org/opengl/)
[![Network](https://img.shields.io/badge/Network-Socket--TCP-green.svg?style=flat-square)](https://docs.python.org/3/library/socket.html)

## 🚀 项目概述
通过 Python 底层扩展实现了**分布式实时同步系统**，并集成了一套基于 **Raymarching 算法与 SDF 物理建模**的高级着色器管线。

---

## 🛠️ 技术核心 (Technical Excellence)

### 1. 高级渲染管线与光影实验室 (Advanced Rendering)
通过 `renpy.register_shader` 直接控制 GPU，实现了多项图形学领域的高级技术：
*   **Raymarching 实时海洋渲染 (Realistic Ocean)**：
    *   利用射线步进算法渲染动态 3D 海面，支持**多层波浪叠加 (Gerstner Waves)**。
    *   **PBR 物理模拟**：集成 **Fresnel（菲涅尔效应）** 混合反射、**ACES Tonemapping** 色调映射以及自适应大气散射模型。
    *   **Kuroshio（黑潮）调色**：通过 Beer-Lambert 吸收定律变体实现深色水体与强高光的对比表现。
*   **程序化 Sci-Fi HUD 绘制**：
    *   基于 **SDF (符号距离场)** 纯数学定义 UI 元素，摆脱纹理依赖，实现无限分辨率的几何 UI。
    *   包含动态数字解算、极坐标变换箭头、以及基于齐次矩阵旋转的雷达扫描视觉。
*   **复杂图层混合**：实现了 CyberTunnel、分形噪声 (Fractal) 及 UV 空间扰动驱动的折射雨滴效果。

### 2. 程序化粒子发射系统 (Procedural Particle System)
*   **随机轨迹建模**：基于 Python 构建粒子发射器，利用随机种子生成非对称的扩散轨迹（Stochastic Trajectory）。
*   **多维插值控制**：利用 Ren'Py `transform` 的 `parallel` 机制，通过数学曲线控制粒子的**加速度上升、阻尼感横向扩散、以及动态旋转偏移**。
*   **自适应性能分配**：支持动态调整粒子密度与生命周期，平衡视觉华丽度与渲染帧率。

### 3. 分布式联机与状态同步 (C/S Architecture)
*   **网络引擎**：基于 Python `socket` 实现，采用多线程异步 IO 模型处理 TCP 报文。
*   **状态仲裁机制**：实现了主机权威（Host Authority）逻辑，解决跨网络分布式环境下的角色竞态冲突。
*   **实时事件总线**：报文通过线程安全队列缓冲，配合主线程周期性轮询（Polling）实现逻辑一致性。

### 4. 向量驱动的动态 UI
*   **动态雷达图渲染器**：继承 `renpy.Displayable`，利用向量运算在底层 Canvas 上实时渲染多维属性变化，支持平滑的插值过渡。
