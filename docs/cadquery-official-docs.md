# CadQuery 官方文档整理

> **说明**: 本文档整理自 CadQuery 官方文档，用于学习和参考。  
> **官方文档**: https://cadquery.readthedocs.io/en/latest/

---

## 1. CadQuery 简介

### 什么是 CadQuery
CadQuery 是一个直观、易用的 Python 库，用于构建参数化 3D CAD 模型。

### 主要目标
- 使用接近人类描述方式的脚本构建模型
- 创建可由最终用户轻松定制的参数化模型
- 输出高质量 CAD 格式（STEP、AMF、3MF）以及传统 STL
- 提供非专有的纯文本模型格式，仅需网络浏览器即可编辑和执行

### 技术基础
- 基于 OCP（OpenCascade Python 绑定）
- 使用开源的 OpenCascade 建模内核

---

## 2. CadQuery vs OpenSCAD 对比分析

### 概述
CadQuery 和 OpenSCAD 都是开源的、基于脚本的参数化模型生成器，但 CadQuery 具有几个关键优势。

### CadQuery 的关键优势

#### 2.1 使用标准编程语言
- **语言**: 使用 Python 作为脚本语言
- **优势**: 可以利用 Python 丰富的生态系统，包括许多标准库和 IDE
- **影响**: 开发者可以使用熟悉的工具和库，提高开发效率

#### 2.2 更强大的 CAD 内核
- **内核**: 基于 OpenCascade (OCC)
- **对比**: OpenCascade 比 OpenSCAD 使用的 CGAL 强大得多
- **支持功能**:
  - NURBS (非均匀有理B样条)
  - 样条线 (splines)
  - 曲面缝合 (surface sewing)
  - STL 修复
  - STEP 导入/导出
  - 其他复杂操作
- **基础**: 除了 CGAL 支持的标准 CSG 操作外，还支持更多高级功能

#### 2.3 导入/导出能力
- **支持格式**: STEP 和 DXF
- **核心优势**: 可以从 CAD 软件创建的 STEP 模型开始，然后添加参数化特征
- **对比**: OpenSCAD 也可以使用 STL，但 STL 是有损格式
- **应用**: 支持在现有 CAD 模型基础上进行参数化设计

#### 2.4 更少的代码和更简单的脚本
- **代码量**: CadQuery 脚本通常需要更少的代码来创建大多数对象
- **原因**: 可以基于其他特征、工作平面、顶点等位置来定位特征
- **效果**: 提高代码的可读性和维护性

#### 2.5 更好的性能
- **构建速度**: CadQuery 脚本可以比 OpenSCAD 更快地构建 STL、STEP、AMF 和 3MF 文件
- **效率**: 在处理复杂模型时性能优势更明显

### 总结
CadQuery 通过使用 Python 语言、强大的 OpenCascade 内核、支持高质量格式导入导出、简洁的代码语法以及优秀的性能，为参数化 CAD 建模提供了一个现代化、高效的解决方案。相比 OpenSCAD，CadQuery 更适合复杂的工程应用和专业级 CAD 建模需求。

---

## 3. CadQuery 的设计理念

### 库与 GUI 分离
- CadQuery 是一个无 GUI 的库，专为程序化创建 3D 模型而设计
- 适用于各种工程和科学应用
- 可选的 GUI 解决方案：
  - **CQ-editor**: 基于 Qt 的 GUI
  - **jupyter-cadquery**: Jupyter 扩展

### jQuery 灵感
CadQuery 受 jQuery 启发，具有以下特点：
- 流畅的 API，创建清晰易读的代码
- 能够与其他 Python 库一起使用
- 清晰完整的文档，包含大量示例

---

## 4. 官方示例实践

### 示例 1：QuickStart 轴承座（官方第一个例子）

#### 完整代码
```python
import cadquery as cq

# 参数定义
height = 60.0    # 高度
width = 80.0     # 宽度
thickness = 10.0 # 厚度
diameter = 22.0  # 轴承孔直径
padding = 12.0   # 边距（孔距离边缘的距离）

# 创建轴承座模型
result = (
    cq.Workplane("XY")
    .box(height, width, thickness)           # 创建基础板块
    .faces(">Z")                            # 选择顶面
    .workplane()                            # 在顶面创建工作平面
    .hole(diameter)                         # 在中心钻轴承孔
    .faces(">Z")                            # 再次选择顶面
    .workplane()                            # 创建新的工作平面
    .rect(height - padding, width - padding, forConstruction=True)  # 绘制构造矩形
    .vertices()                             # 选择矩形顶点（四个角）
    .cboreHole(2.4, 4.4, 2.1)              # 在四个角创建沉头孔
    .edges("|Z")                            # 选择所有平行于Z轴的边
    .fillet(2.0)                            # 添加圆角
)

# 导出模型
cq.exporters.export(result, "bearing_block.stl")
cq.exporters.export(result.section(), "bearing_block.dxf")
cq.exporters.export(result, "bearing_block.step")
```

#### 代码解析
1. **参数定义**: 使用变量控制模型尺寸，实现参数化设计
2. **基础板块**: `cq.Workplane("XY").box()` 创建矩形基础
3. **选择器应用**: 
   - `.faces(">Z")` 选择顶面
   - `.vertices()` 选择顶点
   - `.edges("|Z")` 选择边
4. **工作平面**: `.workplane()` 在选定面上创建新的工作平面
5. **构造几何**: `forConstruction=True` 创建辅助几何体
6. **链式调用**: 通过方法链构建复杂模型

#### 模型特性
- **尺寸**: 60 x 80 x 10 mm
- **轴承孔**: 22 mm 直径（适用于 608 轴承）
- **固定孔**: 四个 M2 沉头孔
- **圆角**: 2mm 半径边缘圆角

#### 导出格式
- **STL**: 3D 打印格式
- **DXF**: 2D CAD 格式
- **STEP**: 高质量 3D CAD 格式

#### 本地实现
- **代码模块**: `app/quickstart/bearing_block.py`
- **模块导入**: `from app.quickstart import bearing_block`
- **输出文件**: `output/quickstart/` 目录
- **状态**: ✅ 已成功实现并验证
- **运行方式**: 
  - 直接运行: `uv run app/quickstart/bearing_block.py`
  - 模块导入: `python -m app.quickstart.bearing_block`

### 示例 2：简单带孔平板
```python
thickness = 0.5
width = 2.0
result = Workplane("front").box(width, width, thickness).faces(">Z").hole(thickness)
```

---

**整理日期**: 2025-08-06  
**最后更新**: 2025-08-06  
**维护者**: AI助手与人工监督