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

### QuickStart 示例实现

官方 QuickStart 教程中的示例已在本地实现并模块化组织：

#### 示例 1：轴承座模型（官方第一个例子）
- **代码位置**: `app/quickstart/bearing_block.py`
- **输出文件**: `output/quickstart/` 目录
- **功能**: 参数化 608 轴承座，包含中心孔、沉头孔和圆角
- **运行方式**: 
  - 导出文件: `uv run app/quickstart/bearing_block.py`
  - 可视化查看: `uv run app/quickstart/bearing_block.py --view`
  - 同时导出和查看: `uv run app/quickstart/bearing_block.py --both`
  - 模块导入: `from app.quickstart import bearing_block`

**运用的 CadQuery 能力：**
- **工作平面 (Workplane)**: 使用 `cq.Workplane("XY")` 创建 2D 工作平面作为建模基础
- **基础几何体创建**: 使用 `.box()` 方法创建矩形基础板块
- **选择器系统**: 
  - `.faces(">Z")` 选择 Z 轴正方向的顶面
  - `.vertices()` 选择构造矩形的顶点
  - `.edges("|Z")` 选择所有平行于 Z 轴的边
- **工作平面切换**: 使用 `.workplane()` 在选定面上创建新的工作平面
- **孔操作**: 
  - `.hole()` 创建通孔
  - `.cboreHole()` 创建沉头孔
- **构造几何**: 使用 `forConstruction=True` 创建辅助几何体，不参与最终实体
- **圆角操作**: 使用 `.fillet()` 对选定边进行圆角处理
- **链式调用**: 通过方法链式调用构建复杂模型，代码简洁易读
- **参数化设计**: 使用变量控制所有尺寸，便于修改和定制
- **多格式导出**: 支持 STL、DXF、STEP 三种格式的文件导出
- **3D 可视化**: 使用 `show()` 函数直接打开 3D 查看窗口

#### 示例 2：可视化查看模型
- **代码位置**: `app/quickstart/visualization_example.py`
- **功能**: 演示如何使用 `show()` 函数直接打开 3D 查看窗口
- **关键代码**: 
  ```python
  from cadquery.vis import show
  show(model, alpha=0.5)  # alpha 设置透明度
  ```
- **运行方式**: `uv run app/quickstart/visualization_example.py`

**运用的 CadQuery 能力：**
- **球体创建**: 使用 `.sphere()` 方法创建球体几何体
- **布尔运算**: 
  - 使用 `.split(keepBottom=True)` 分割球体并保留下半部分
  - 使用 `-` 操作符进行差集运算，创建壳体结构
- **选择器应用**: `.faces('>Z')` 选择 Z 轴正方向的面进行圆角处理
- **圆角操作**: 使用 `.fillet()` 对选定面进行圆角处理
- **3D 可视化**: 
  - 使用 `from cadquery.vis import show` 导入可视化模块
  - 使用 `show(model, alpha=0.5)` 打开 3D 查看窗口，alpha 参数控制透明度
- **复杂几何体构造**: 通过球体的分割和布尔运算创建复杂的半球壳结构
- **模块化编程**: 将模型创建逻辑封装在函数中，便于复用和测试

#### 示例 3：简单带孔平板
```python
thickness = 0.5
width = 2.0
result = Workplane("front").box(width, width, thickness).faces(">Z").hole(thickness)
```

**运用的 CadQuery 能力：**
- **工作平面定位**: 使用 `Workplane("front")` 在前面创建工作平面
- **基础几何体**: 使用 `.box()` 创建立方体
- **选择器操作**: 使用 `.faces(">Z")` 选择顶面
- **孔操作**: 使用 `.hole()` 在选定面上创建通孔
- **链式调用**: 单行代码完成从创建到打孔的完整操作
- **参数化设计**: 使用变量控制尺寸，便于修改

> **提示**: 所有官方示例的详细代码、解析和说明请参考对应的代码文件中的注释。代码文件包含完整的实现、学习要点和使用说明。

---

## 5. 核心概念 (Concepts)

CadQuery 的核心概念已单独整理至 `docs/cadquery-concepts.md` 文件中，以方便查阅。

---

## 6. Workplane 与 Sketch 模块 (简要记录)

由于对 Workplane 和 Sketch 模块的理解尚不深入，此处仅进行简要记录，供后续学习参考。

### 6.1 Workplane (工作平面)
- **核心作用**: 代表空间中的一个平面，是大多数建模操作的基准。拥有中心点和局部坐标系。
- **常见用法**:
  - 作为建模起点 (如 `Workplane("XY")`)。
  - 通过选择实体上的面来创建新的工作平面 (如 `.faces(">Z").workplane()`)。
  - 在其上进行 2D 绘图，然后拉伸/旋转等操作生成 3D 特征。
- **关键概念**:
  - **The Stack (堆栈)**: 每次操作返回新的 Workplane 对象，形成父子链，可使用 `.end()` 回退。
  - **Chaining (链式调用)**: 方法返回 Workplane 对象，支持流畅的链式语法。
  - **The Context Solid (上下文实体)**: 自动跟踪和组合特征到第一个创建的实体上。
  - **Iteration (迭代)**: 许多方法会自动对堆栈中的每个元素进行操作。
  - **Selectors (选择器)**: 用于选择顶点、边、面等特征。

### 6.2 Sketch (草图)
- **核心作用**: 提供更灵活的 2D 草图绘制能力，可与 Workplane 集成用于生成 3D 模型。
- **主要 API**:
  - **Face-based API**: 通过构建面并进行布尔运算来创建草图。
  - **Edge-based API**: 通过绘制线段、圆弧等边来构建草图，最后需 `assemble()`。
  - **Constraint-based API (实验性)**: 使用几何约束来定义草图。
- **与 Workplane 集成**:
  - 可以在 Workplane 链式调用中就地创建草图 (`.sketch()...finalize()`)。
  - 可以将已创建的草图对象放置到 Workplane 上 (`.placeSketch()`)。
  - 支持使用草图进行 `extrude`, `revolve`, `sweep`, `cut`, `loft` 等操作。
- **其他功能**:
  - 支持凸包 (Convex Hull) 构建 (实验性)。
  - 支持偏移 (Offset) 操作。
  - 支持导出和从 DXF 导入。

---

## 7. Assemblies (装配) 模块 (简要记录)

由于对 Assemblies 模块的理解尚不深入，此处仅进行简要记录，供后续学习参考。

### 7.1 核心概念
- **Assembly 类**: 用于将简单的模型组合成复杂、可能嵌套的装配体。
- **组成**: 一个装配体由多个子部件 (parts) 组成，每个子部件都有其相对父部件的位置 (`loc`) 和可选的颜色 (`color`)。

### 7.2 基本用法
- **创建**: `assy = Assembly(part, loc=Location(...), name="part_name")`
- **添加部件**: `assy.add(part, loc=Location(...), name="child_name", color=Color(...))`
- **导出**: 支持导出为 STEP 文件或 OCCT XML 格式。

### 7.3 约束 (Constraints)
- **目的**: 使用约束来定义组件之间的关系，可以创建完全参数化的装配。约束比直接指定位置更灵活，当参数改变时，求解器 (`solve()`) 会自动重新计算部件的最终位置。
- **常用约束类型**:
  - **Axis**: 使两个法向量或切向量共线或成指定角度。常用于对齐面。
  - **Point**: 使两个点（或特征的中心）重合或相距指定距离。
  - **Plane**: `Axis` 和 `Point` 约束的组合，常用于“贴合”两个面。
  - **PointInPlane**: 将一个点约束在另一个对象定义的平面内。
  - **PointOnLine**: 将一个点约束在另一个对象定义的线上。
  - **FixedPoint**: 固定一个点的位置。
  - **FixedRotation**: 固定一个对象的旋转角度。
  - **FixedAxis**: 固定一个对象的法向量或切向量方向。
- **定义约束**: `assy.constrain("part1@selector1", "part2@selector2", "ConstraintType", param=value)`
- **求解**: `assy.solve()`

### 7.4 选择器 (Selectors) 与标签 (Tags)
- 在装配体约束中，选择器的语法类似 `"part_name@faces@>Z"` 或 `"part_name?tag_name"`。
- 可以在创建部件时使用 `tag()` 方法为特征（如面、边、顶点）添加标签，以便在约束中引用。

---

## 8. CadQuery Cheatsheet 功能速查表

根据 CadQuery 官方 Cheatsheet 整理的主要功能和函数。

### 8.1 3D 建模 (3D Construction)

| 类别 | 函数名 | 简要说明 |
| :--- | :--- | :--- |
| **基本体 (Primitives)** | `box(length, width, height)` | 创建长方体 |
| | `sphere(radius)` | 创建球体 |
| | `cylinder(height, radius)` | 创建圆柱体 |
| | `text(txt, fontsize, distance)` | 创建文字形状 |
| **增料操作 (Additive)** | `extrude(until)` | 拉伸 2D 形状 |
| | `revolve(angleDegrees)` | 旋转 2D 形状 |
| | `loft(ruled)` | 放样多个 2D 形状 |
| | `sweep(path, isFrenet, transitionMode)` | 沿路径扫掠 2D 形状 |
| | `union(shape)` | 并集操作 |
| **减料操作 (Subtractive)** | `cutBlind(until)` | 盲切除 3D 形状 |
| | `cutThruAll()` | 通切除 3D 形状 |
| | `hole(diameter, depth)` | 创建孔 |
| | `cut(shape)` | 差集操作 |
| **修改操作 (Modify)** | `fillet(radius)` | 圆角 |
| | `chamfer(length)` | 倒角 |
| | `shell(thickness)` | 抽壳 |
| | `intersect(shape)` | 交集操作 |

### 8.2 2D 绘图 (2D Construction)

| 函数名 | 简要说明 |
| :--- | :--- |
| `rect(xLen, yLen)` | 绘制矩形 |
| `circle(radius)` | 绘制圆 |
| `ellipse(x_radius, y_radius)` | 绘制椭圆 |
| `center(x, y)` | 移动到指定中心点 |
| `moveTo(x, y)` | 移动到绝对坐标 |
| `move(xDist, yDist)` | 相对移动 |
| `lineTo(x, y)` | 绘制直线到指定点 |
| `line(xDist, yDist)` | 绘制相对直线 |
| `polarLine(distance, angle)` | 绘制极坐标直线 |
| `vLine(distance)` | 绘制垂直线 |
| `hLine(distance)` | 绘制水平线 |
| `polyline(listOfXYTuple)` | 绘制折线 |

### 8.3 草图 (Sketching)

| 函数名 | 简要说明 |
| :--- | :--- |
| `rect(w, h)` | 创建矩形 |
| `circle(r)` | 创建圆 |
| `ellipse(a1, a2)` | 创建椭圆 |
| `trapezoid(w, h, a1)` | 创建梯形 |
| `regularPolygon(r, n)` | 创建正多边形 |
| `polygon(pts)` | 创建多边形 |
| `fillet(d)` | 圆角 |
| `chamfer(d)` | 倒角 |
| `finalize()` | 完成草图并返回到 Workplane |

### 8.4 导入/导出 (Import/Export)

| 函数/模块 | 简要说明 |
| :--- | :--- |
| `importers.importDXF(path, tol)` | 导入 DXF 文件 |
| `importers.importStep("path")` | 导入 STEP 文件 |
| `exporters.export(solid, "path/solid.***")` | 导出模型 (支持 svg, step, stl, amf, vrml, json) |

### 8.5 装配 (Assemblies)

| 函数/类 | 简要说明 |
| :--- | :--- |
| `Assembly()` | 创建装配体 |
| `add(obj, loc, color)` | 添加部件 |
| `constrain(***)` | 定义约束 |
| `solve()` | 求解装配 |
| `save("path/assembly.***")` | 保存装配 (支持 step, xml, gltf, vtkjs, vrml) |

### 8.6 选择器字符串修饰符 (Selector String Modifiers)

| 修饰符 | 说明 | 对应选择器类 |
| :--- | :--- | :--- |
| `|` | 平行于指定轴 | `ParallelDirSelector` |
| `#` | 垂直于指定轴 | `PerpendicularDirSelector` |
| `+/-` | 指定轴的正/负方向 | `DirectionSelector` |
| `>` | 指定轴方向的最大值 | `DirectionMinMaxSelector(directionMax=True)` |
| `<` | 指定轴方向的最小值 | `DirectionMinMaxSelector(directionMax=False)` |
| `%` | 指定曲线/曲面类型 | `TypeSelector` |
| **示例** | `.faces(">Z")` 选择 Z 轴正方向的面 |

### 8.7 选择器方法 (Selector Methods)

| 选择器方法 | 对应选择器类 |
| :--- | :--- |
| `faces(selector)` | `NearestToPointSelector(pnt)` |
| `edges(selector)` | `ParallelDirSelector(vector)` |
| `vertices(selector)` | `PerpendicularDirSelector(vector)` |
| `solids(selector)` | `DirectionMinMaxSelector(vector)` |
| `shells(selector)` | `RadiusNthSelector(n)` |
| | `AndSelector(selector, selector)` |
| | `SumSelector(selector, selector)` |
| | `SubtractSelector(selector, selector)` |
| | `InverseSelector(selector)` |

### 8.8 工作平面定位 (Workplane Positioning)

| 函数名 | 简要说明 |
| :--- | :--- |
| `translate(Vector(x, y, z))` | 平移 |
| `rotateAboutCenter(Vector(x, y, z), angleDegrees)` | 绕中心旋转 |
| `rotate(Vector(x, y, z), Vector(x, y, z), angleDegrees)` | 绕指定轴旋转 |
| `workplane(offset, origin)` | 创建新的工作平面 |

### 8.9 命名平面 (Named Planes)

| 名称 | xDir | yDir | zDir |
| :--- | :--- | :--- | :--- |
| `XY` | +x | +y | +z |
| `YZ` | +y | +z | +x |
| `XZ` | +x | +z | -y |
| `front` | +x | +y | +z |
| `back` | -x | +y | -z |
| `left` | +z | +y | -x |
| `right` | -z | +y | +x |
| `top` | +x | -z | +y |
| `bottom` | +x | +z | -y |

---

**整理日期**: 2025-08-06  
**最后更新**: 2025-08-06  
**维护者**: AI助手与人工监督