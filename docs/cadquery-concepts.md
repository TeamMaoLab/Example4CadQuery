# CadQuery 核心概念 (Concepts)

> **说明**: 本文档整理自 CadQuery 官方文档的 Concepts 部分，用于学习和参考。  
> **官方文档**: https://cadquery.readthedocs.io/en/latest/primer.html

## 1. 3D BREP 拓扑概念

在讨论 CadQuery 之前，了解 3D CAD 拓扑结构是有意义的。CadQuery 是基于 OpenCascade 内核的，该内核使用边界表示法 (BREP) 来定义对象。这意味着对象是由其封闭曲面定义的。

在 BREP 系统中，这些基本构造块用于定义形状（按层级结构向上）：
- **vertex (顶点)**: 空间中的一个点。
- **edge (边)**: 沿着特定路径（称为曲线）连接两个或多个顶点。
- **wire (线)**: 连接在一起的边的集合。
- **face (面)**: 封闭曲面的边或线的集合。
- **shell (壳)**: 沿其部分边缘连接在一起的面的集合。
- **solid (实体)**: 具有封闭内部的壳。
- **compound (组合体)**: 实体的集合。

使用 CadQuery 时，所有这些对象都会被创建，希望能以最少的工作量完成。在实际的 CAD 内核中，还涉及另一组几何构造。例如，一个弧形边将在其下方保存一个完整圆的底层曲线引用，每个线性边在其下方保存一条线的方程。CadQuery 为您屏蔽了这些构造。

## 2. CadQuery API 层级

深入了解 CadQuery 后，您可能会发现自己在处理 CadQuery API 可以返回的不同类型对象时感到有些困惑。本章旨在解释这个主题，并提供有关底层实现和内核层的背景知识，以便您能够利用更多的 CadQuery 功能。

CadQuery 由 4 个不同的 API 组成，它们相互实现。

1.  **The Fluent API (流畅 API)**
    -   `Workplane` 类及其所有方法定义了 Fluent API。这是您开始使用 CadQuery 时所使用的内容，也是您大部分时间会看到的内容。它相当易于使用，并为您简化了很多事情。
    -   `Sketch` 类。
    -   `Assembly` 类。
2.  **The Direct API (直接 API)**
    -   `Shape` 类。
3.  **The Geometry API (几何 API)**
    -   `Vector` 类。
    -   `Plane` 类。
    -   `Location` 类。
4.  **The OCCT API (OpenCascade 技术 API)**
    -   OCCT API 是 CadQuery 的最低层。Direct API 构建于 OCCT API 之上，OCCT API 在 CadQuery 中通过 OCP 提供。OCP 是 CadQuery 使用的 OCCT C++ 库的 Python 绑定。这意味着您可以 (几乎) 访问所有 OCCT C++ 库。使用 OCCT API 可以为您的设计提供最大的灵活性和控制力，但它非常冗长且难以使用。您需要对不同的 C++ 库有很强的了解才能实现您想要的功能。

### 2.1 The Fluent API (流畅 API)

所谓 Fluent API，就是您刚开始使用 CadQuery 时所接触的内容，`Workplane` 类及其所有方法定义了 Fluent API。这是您将最常使用和看到的 API，它使用起来相当容易，并且为您简化了很多事情。一个经典的例子是：
```python
part = Workplane("XY").box(1, 2, 3).faces(">Z").vertices().circle(0.5).cutThruAll()
```
在这里，我们创建一个 `Workplane` 对象，然后在其上调用几个方法来创建我们的零件。可以将 Fluent API 看作是您的零件对象，而它所有的方法都是将影响您的零件的操作。通常，您会从一个空的 `Workplane` 开始，然后通过调用 `Workplane` 方法添加更多特征。

这种层级结构的操作修改零件在 CadQuery 代码中使用的传统代码风格中得到了很好的体现。使用 CadQuery Fluent API 编写的代码通常看起来像这样：
```python
part = Workplane("XY").box(1, 2, 3).faces(">Z").vertices().circle(0.5).cutThruAll()
```
或者像这样：
```python
part = Workplane("XY")
part = part.box(1, 2, 3)
part = part.faces(">Z")
part = part.vertices()
part = part.circle(0.5)
part = part.cutThruAll()
```
**注意**: 虽然第一种代码风格是人们的默认选择，但需要注意的是，当您像这样编写代码时，它等效于将其写在一行上。这使得调试更加困难，因为您无法逐步可视化每个操作步骤，而 CQ-Editor 调试器等功能则提供了这种可视化。

### 2.2 The Direct API (直接 API)

虽然 Fluent API 提供了大部分功能，但您可能会遇到需要额外灵活性或需要处理低级对象的场景。

直接 API 是 Fluent API 在幕后调用的 API。这 9 个拓扑类及其方法组成了直接 API。这些类实际上包装了等效的 Open CASCADE Technology (OCCT) 类。这 9 个拓扑类是：
- `Shape`
- `Compound`
- `CompSolid`
- `Solid`
- `Shell`
- `Face`
- `Wire`
- `Edge`
- `Vertex`

每个类都有自己的方法来创建和/或编辑其各自类型的形状。您也可以使用 freefuncapi 来创建和修改形状。正如在概念中已经解释的那样，拓扑类中也存在某种层次结构。线由几条边组成，而边又由几个顶点组成。这意味着您可以自下而上地创建几何体，并对其拥有大量控制权。

例如，我们可以这样创建一个圆形面：

```python
circle_wire = Wire.makeCircle(10, Vector(0, 0, 0), Vector(0, 0, 1))
circular_face = Face.makeFromWires(circle_wire, [])
```
**注意**: 在 CadQuery (和 OCCT) 中，所有的拓扑类都是形状，`Shape` 类是最抽象的拓扑类。拓扑类继承 `Mixin3D` 或 `Mixin1D`，它们为继承它们的类提供共享的附加方法。

直接 API 顾名思义，不提供父子数据结构，而是每个方法调用直接返回指定拓扑类型的对象。它比 Fluent API 更冗长，使用起来也更繁琐，但由于它提供了更多的灵活性（您可以处理面，这是 Fluent API 无法做到的），有时它比 Fluent API 更方便。

### 2.3 The OCCT API (OpenCascade 技术 API)

最后我们讨论 OCCT API。OCCT API 是 CadQuery 的最底层。直接 API 构建于 OCCT API 之上，OCCT API 在 CadQuery 中通过 OCP 提供。OCP 是 CadQuery 使用的 OCCT C++ 库的 Python 绑定。这意味着您可以 (几乎) 访问所有 OCCT C++ 库。使用 OCCT API 可以为您的设计提供最大的灵活性和控制力，但它非常冗长且难以使用。您需要对不同的 C++ 库有很强的了解才能实现您想要的功能。要获得这些知识，最明显的方法是：
1.  阅读直接 API 源代码，因为它构建于 OCCT API 之上，其中充满了示例用法。
2.  浏览 [C++ 文档](https://dev.opencascade.org/doc/overview/html/)。

**注意**: 导入 OCCT API 特定类的通用方式是 `from OCP.thePackageName import theClassName`。例如，如果您想使用 `BRepPrimAPI_MakeBox` 类。您将按如下方式操作：
```python
from OCP.BRepPrimAPI import BRepPrimAPI_MakeBox
```
包名在文档页面顶部写明。通常它写在类名本身中作为前缀。

### 2.4 在 API 之间转换

虽然这 3 个 API 提供了 3 个不同复杂度和功能的层级，但您可以随意混合使用这 3 个层级。下面介绍了与不同 API 层交互的不同方式。

#### 2.4.1 Fluent API <=> Direct API

以下是获取 Direct API 对象（即拓扑对象）的所有可能性。

您可以结束 Fluent API 调用链并使用 `Workplane.val()` 获取堆栈上的最后一个对象，或者您可以使用 `Workplane.vals()` 获取所有对象。

```python
>>> box = Workplane().box(10, 5, 5)
>>> print(type(box))
<class 'cadquery.cq.Workplane'>
>>> box = Workplane().box(10, 5, 5).val()
>>> print(type(box))
<class 'cadquery.occ_impl.shapes.Solid'>
```

如果您只对获取 Workplane 的上下文实体感兴趣，可以使用 `Workplane.findSolid()`:

```python
>>> part = Workplane().box(10,5,5).circle(3).val()
>>> print(type(part))
<class 'cadquery.cq.Wire'>
>>> part = Workplane().box(10,5,5).circle(3).findSolid()
>>> print(type(part))
<class 'cadquery.occ_impl.shapes.Compound'> # findSolid 的返回类型是 Solid 或 Compound 对象
```

如果您想反向操作，即在 Fluent API 中使用拓扑 API 的对象，您的选择是：

您可以将拓扑对象作为基础对象传递给 `Workplane` 对象。

```python
solid_box = Solid.makeBox(10, 10, 10)
part = Workplane(obj=solid_box) 
# 并且您可以继续在 Fluent API 中进行建模
part = part.faces(">Z").circle(1).extrude(10)
```

您可以使用 `Workplane.newObject()` 将拓扑对象作为 Fluent API 调用链中的新操作/步骤添加：

```python
circle_wire = Wire.makeCircle(1, Vector(0, 0, 0), Vector(0, 0, 1))
box = Workplane().box(10, 10, 10).newObject([circle_wire]) 
# 并且您可以继续建模
box = (box.toPending().cutThruAll()) # 注意 `toPending` 调用，如果您想在后续操作中使用它，这是必需的
```

#### 2.4.2 Direct API <=> OCCT API

Direct API 的每个对象都将其等效的 OCCT 对象存储在其 `wrapped` 属性中。

```python
>>> box = Solid.makeBox(10,5,5)
>>> print(type(box))
<class 'cadquery.occ_impl.shapes.Solid'>
>>> box = Solid.makeBox(10,5,5).wrapped
>>> print(type(box))
<class 'OCP.TopoDS.TopoDS_Solid'>
```

如果您想将 OCCT 对象转换为 Direct API 对象，您只需将其作为参数传递给预期的类：

```python
>>> occt_box = BRepPrimAPI_MakeBox(5,5,5).Solid()
>>> print(type(occt_box))
<class 'OCP.TopoDS.TopoDS_Solid'>
>>> direct_api_box = Solid(occt_box)
>>> print(type(direct_api_box))
<class 'cadquery.occ_impl.shapes.Solid'>
```
**注意**: 您可以将 [此处](https://dev.opencascade.org/doc/refman/html/class_topo_d_s___shape.html) 找到的类型转换为 Direct API。

## 3. Multimethods (多重方法)

CadQuery 使用 [Multimethod](https://coady.github.io/multimethod/) 来允许根据参数类型分发方法调用。一个例子是 `arc()`，其中 `a_sketch.arc((1, 2), (2, 3))` 将被分发到一个方法，而 `a_sketch.arc((1, 2), (2, 3), (3, 4))` 将被分发到另一个方法。为了使 Multimethods 正常工作，您不应使用关键字参数来指定位置参数。例如，您 **不应** 编写 `a_sketch.arc(p1=(1, 2), p2=(2, 3), p3=(3, 4))`，而应使用前面的示例。请注意，CadQuery 会尝试在调度错误时回退到第一个注册的 Multimethod，但最佳实践仍然是在 CadQuery 中不要使用关键字参数来指定位置参数。

## 4. Selectors (选择器)

选择器允许您选择一个或多个特征，以定义新特征。例如，您可以拉伸一个盒子，然后选择顶面作为新特征的位置。或者，您可以拉伸一个盒子，然后选择所有垂直边缘，以便可以对其应用倒角。

您可以使用选择器选择顶点、边、面、实体和线。

将选择器视为您手和鼠标在传统 CAD 系统中构建对象时的等效物。

有关更多信息，请参见 [Selectors](https://cadquery.readthedocs.io/en/latest/apireference.html#selectors)。

## 5. Workplane class (工作平面类)

`Workplane` 类包含当前选定的对象（`objects` 属性中的形状、向量或位置列表）、建模上下文（`ctx` 属性）以及 CadQuery 的 Fluent API 方法。这是用户将实例化的主要类。

有关更多信息，请参见 [API Reference](https://cadquery.readthedocs.io/en/latest/apireference.html#apireference)。

## 6. Assemblies (装配)

简单的模型可以组合成复杂、可能嵌套的装配体。

一个简单的例子如下所示：

```python
from cadquery import *
w = 10
d = 10
h = 10
part1 = Workplane().box(2 * w, 2 * d, h)
part2 = Workplane().box(w, d, 2 * h)
part3 = Workplane().box(w, d, 3 * h)
assy = (
    Assembly(part1, loc=Location(Vector(-w, 0, h / 2)))
    .add(
        part2,
        loc=Location(Vector(1.5 * w, -0.5 * d, h / 2)),
        color=Color(0, 0, 1, 0.5)
    )
    .add(part3, loc=Location(Vector(-0.5 * w, -0.5 * d, 2 * h)), color=Color("red"))
)
```

**注意**: 子部件的位置是相对于其父部件定义的 - 在上面的例子中，`part3` 在全局坐标系中的位置将是 (-5,-5,20)。可以通过这种方式创建具有不同颜色的装配体，并将其导出为 STEP 或本地 OCCT xml 格式。

您可以在此处浏览装配相关的方法：[Assemblies](https://cadquery.readthedocs.io/en/latest/apireference.html#assembly)。

## 7. Assemblies with constraints (带约束的装配)

有时，不希望明确定义组件位置，而是使用约束来获得完全参数化的装配。这可以通过以下方式实现：

```python
from cadquery import *
w = 10
d = 10
h = 10
part1 = Workplane().box(2 * w, 2 * d, h)
part2 = Workplane().box(w, d, 2 * h)
part3 = Workplane().box(w, d, 3 * h)
assy = (
    Assembly(part1, name="part1", loc=Location(Vector(-w, 0, h / 2)))
    .add(part2, name="part2", color=Color(0, 0, 1, 0.5))
    .add(part3, name="part3", color=Color("red"))
    .constrain("part1@faces@>Z", "part3@faces@<Z", "Axis")
    .constrain("part1@faces@>Z", "part2@faces@<Z", "Axis")
    .constrain("part1@faces@>Y", "part3@faces@<Y", "Axis")
    .constrain("part1@faces@>Y", "part2@faces@<Y", "Axis")
    .constrain("part1@vertices@>(-1,-1,1)", "part3@vertices@>(-1,-1,-1)", "Point")
    .constrain("part1@vertices@>(1,-1,-1)", "part2@vertices@>(-1,-1,-1)", "Point")
    .solve()
)
```

这段代码的结果与上一节中的对象相同。额外的好处是，更改参数 `w`, `d`, `h` 时，最终位置将自动计算。诚然，代码很密集，可以使用标签使其更清晰。在构建约束时，可以直接引用标签：

```python
from cadquery import *
w = 10
d = 10
h = 10
part1 = Workplane().box(2 * w, 2 * d, h)
part2 = Workplane().box(w, d, 2 * h)
part3 = Workplane().box(w, d, 3 * h)
part1.faces(">Z").edges("<X").vertices("<Y").tag("pt1")
part1.faces(">X").edges("<Z").vertices("<Y").tag("pt2")
part3.faces("<Z").edges("<X").vertices("<Y").tag("pt1")
part2.faces("<X").edges("<Z").vertices("<Y").tag("pt2")
assy1 = (
    Assembly(part1, name="part1", loc=Location(Vector(-w, 0, h / 2)))
    .add(part2, name="part2", color=Color(0, 0, 1, 0.5))
    .add(part3, name="part3", color=Color("red"))
    .constrain("part1@faces@>Z", "part3@faces@<Z", "Axis")
    .constrain("part1@faces@>Z", "part2@faces@<Z", "Axis")
    .constrain("part1@faces@>Y", "part3@faces@<Y", "Axis")
    .constrain("part1@faces@>Y", "part2@faces@<Y", "Axis")
    .constrain("part1?pt1", "part3?pt1", "Point")
    .constrain("part1?pt2", "part2?pt2", "Point")
    .solve()
)
```

目前实现了以下约束：
- **Axis (轴)**: 两个法向量是反向共线的，或者它们之间的角度（以弧度为单位）等于指定值。可以为所有具有一致法向量的实体定义 - 平面面、线和边。
- **Point (点)**: 两个点是共点的，或者它们之间相隔指定距离。可以为所有实体定义，线、面、实体使用质心，顶点使用顶点位置。
- **Plane (平面)**: `Axis` 和 `Point` 约束的组合。

有关更详细的装配示例，请参见 [Assemblies](https://cadquery.readthedocs.io/en/latest/assy.html#assytutorial)。

---

**整理日期**: 2025-08-06  
**最后更新**: 2025-08-06  
**维护者**: AI助手与人工监督