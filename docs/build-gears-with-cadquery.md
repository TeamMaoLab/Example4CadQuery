# 使用CadQuery构建齿轮 (Build Gears with CadQuery)

## 1. 齿轮概述 (Gears Overview)

### 1.1 齿轮主要类型、特点和典型应用

#### 1.1.1 直齿轮 (Spur Gear)
- **特点**: 齿轮齿平行于齿轮轴线。结构简单、成本低，但运行时噪音较大，尤其在高速下。用于传递平行轴之间的动力。
- **应用**: 手动变速箱、洗衣机、螺杆驱动器、钟表、玩具。

#### 1.1.2 斜齿轮 (Helical Gear)
- **特点**: 齿轮齿与齿轮轴线成一定角度（螺旋角）。运行更平稳、更安静，适合高速应用。接触线较长，可承受更大载荷。会产生轴向推力，需要推力轴承。
- **应用**: 汽车变速器（常用于高速轴）、工业机械、船舶传动装置。

#### 1.1.3 伞齿轮 (Bevel Gear)
- **特点**: 用于传递相交轴（通常是90度）之间的动力。齿轮是锥形的。根据齿形可分为直齿、斜齿或弧齿。
- **应用**: 差速器、手钻、机车驱动轮、通风系统。

#### 1.1.4 蜗轮蜗杆 (Worm Gear)
- **特点**: 由蜗杆和蜗轮组成，用于传递交错轴（通常为90度）之间的动力。减速比高，具有自锁特性（在某些配置下）。
- **应用**: 起重机、电梯、转向机构、张力控制系统、减速电机。

#### 1.1.5 齿条和小齿轮 (Rack and Pinion)
- **特点**: 小齿轮是圆形齿轮，齿条是直线。将旋转运动转换为直线运动（反之亦然）。
- **应用**: 汽车转向系统、机床进给机构、千斤顶、线性执行器。

#### 1.1.6 行星齿轮 (Planetary Gear)
- **特点**: 由太阳轮、行星齿轮和内齿轮环组成。结构紧凑，可实现高减速比或增速比。效率高，承载能力强。能够实现运动的合成或分解。
- **应用**: 自动变速箱、轮毂电机、工业机器人、风力涡轮机齿轮箱。

#### 1.1.7 人字齿轮 (Herringbone Gear)
- **特点**: 类似于两个方向相反的斜齿轮组合。消除了轴向推力。运行平稳、噪音低。制造复杂，成本较高。
- **应用**: 重型机械、船舶推进系统、发电厂。

### 1.2 齿轮设计相关标准

齿轮设计和制造遵循一系列国际和国家标准，以确保互换性和性能。常见的标准体系包括：
- **ISO (International Organization for Standardization)**: 国际标准化组织标准，如 ISO 1328（圆柱齿轮精度）、ISO 6336（齿轮承载能力计算）等。
- **AGMA (American Gear Manufacturers Association)**: 美国齿轮制造商协会标准，如 AGMA 2000（齿轮精度）、AGMA 2101（齿轮设计）等。
- **DIN (Deutsches Institut für Normung)**: 德国标准化学会标准，如 DIN 3960（齿轮几何计算）、DIN 3967（齿轮精度）等。
- **JIS (Japanese Industrial Standards)**: 日本工业标准，如 JIS B 1701（齿轮精度）、JIS B 1702（齿轮强度计算）等。

选择合适的齿轮类型和遵循相关标准对于确保齿轮传动系统的性能、可靠性和寿命至关重要。

## 2. 齿轮设计原理与参数详解

### 2.1 齿轮基本概念与术语

- **齿数 (z)**: 一个齿轮的轮齿总数。
- **模数 (m)**: 齿距 `p` 与圆周率 `π` 的比值，即 `m = p / π`。模数是齿轮几何尺寸计算中最基本的参数，已标准化。单位为毫米 (mm)。
- **压力角 (α)**: 在齿轮啮合过程中，啮合点处的受力方向与该点速度方向之间所夹的锐角。标准压力角为 20°。
- **分度圆**: 齿轮上具有标准模数和标准压力角的圆。其直径 `d = m * z`。
- **齿顶圆**: 通过齿轮各齿顶部的圆。其直径为 `da`。
- **齿根圆**: 通过齿轮各齿槽底部的圆。其直径为 `df`。
- **齿高 (h)**: 齿顶圆与齿根圆之间的径向距离。`h = ha + hf`。
- **齿顶高 (ha)**: 分度圆到齿顶圆的径向距离。
- **齿根高 (hf)**: 分度圆到齿根圆的径向距离。
- **齿厚 (s)**: 在分度圆上，一个轮齿两侧齿廓间的弧长。
- **齿槽宽 (e)**: 在分度圆上，一个齿槽两侧齿廓间的弧长。
- **齿距 (p)**: 在分度圆上，相邻两齿同侧齿廓间的弧长。`p = s + e = π * m`。
- **基圆**: 形成渐开线齿廓的圆。其直径 `db = d * cos(α)`。

### 2.2 直齿轮 (Spur Gear) 设计

#### 2.2.1 几何尺寸计算

对于标准直齿轮（无变位修正），其主要尺寸计算公式如下：
- **分度圆直径 (Pitch Diameter)**: `d = m * z`
- **基圆直径 (Base Diameter)**: `db = d * cos(α) = m * z * cos(α)`
- **齿顶高 (Addendum)**: `ha = ha* * m`。对于标准齿轮，齿顶高系数 `ha*` 通常为 1.0。
- **齿根高 (Dedendum)**: `hf = (ha* + c*) * m`。对于标准齿轮，顶隙系数 `c*` 通常为 0.25。
- **全齿高 (Whole Depth)**: `h = ha + hf = (2 * ha* + c*) * m`
- **齿顶圆直径 (Outside Diameter)**: `da = d + 2 * ha = m * (z + 2 * ha*)`
- **齿根圆直径 (Root Diameter)**: `df = d - 2 * hf = m * (z - 2 * (ha* + c*))`
- **齿距 (Circular Pitch)**: `p = π * m`
- **基圆齿距 (Base Pitch)**: `pb = p * cos(α) = π * m * cos(α)`

#### 2.2.2 齿廓曲线：渐开线 (Involute)

直齿轮的齿廓曲线通常采用渐开线。渐开线的生成方法：
1.  将一条直线（发生线）沿着一个固定的圆（基圆）作纯滚动。
2.  发生线上任一点的轨迹就是该基圆的渐开线。

渐开线具有以下重要性质：
- 发生线在基圆上滚过的长度等于基圆上被滚过的弧长。
- 发生线（即渐开线的法线）始终与基圆相切。
- 渐开线上任一点的法线恒切于基圆。
- 基圆内无渐开线。
- 渐开线的形状取决于基圆的大小。基圆半径越大，渐开线越平直。

#### 2.2.3 啮合特性

- **定传动比**: 一对渐开线齿轮啮合时，其瞬时传动比恒定，等于两基圆半径的反比。
- **可分性**: 实际中心距略有变化时，不影响传动比的恒定性，但会影响齿侧间隙和重合度。

#### 2.2.4 在 CadQuery 中的建模思路

1.  **参数计算**: 根据输入的模数 `m`、齿数 `z`、压力角 `α` 等参数，计算出分度圆、基圆、齿顶圆、齿根圆的直径。
2.  **单个齿形建模**:
    -  在基圆上生成一段渐开线。这可以通过数学计算或近似方法（如多段线）实现。
    -  确定单个齿的有效轮廓。齿的一侧渐开线从基圆开始，到齿顶圆结束；齿的另一侧是相邻齿的渐开线镜像。齿根部分通常用一段圆弧或直线连接。
    -  对齿根部分进行圆角处理，以提高强度。
3.  **齿形复制与阵列**:
    -  将创建好的单个齿形绕齿轮中心轴旋转 `(360 / z)` 度，并复制 `z` 次。
    -  将所有齿形合并成一个齿圈（`Wire` 或 `Face`）。
4.  **创建实体**:
    -  将齿圈拉伸成一个齿轮环（`Solid`）。
    -  创建中心孔和轮毂（如果需要）。
    -  使用布尔运算（并集）将齿轮环与轮毂组合。
5.  **后处理 (可选)**:
    -  添加键槽、油孔等特征。

## 3. 齿轮相关标准摘要

### 3.1 基础标准

#### ISO 53:1998 (E)
- **标题**: *Cylindrical gears for general engineering and for heavy engineering - Standard basic rack contour*
- **内容**: 定义了用于一般工程和重型工程的圆柱齿轮的标准基本齿条轮廓。它规定了标准压力角为 20°，以及齿顶高系数 `ha* = 1.0` 和顶隙系数 `c* = 0.25`。

#### ISO 54:1996 (E)
- **标题**: *Cylindrical gears - Vocabulary*
- **内容**: 定义了圆柱齿轮相关的术语和定义。

### 3.2 精度标准

#### ISO 1328-1:1995 (E) / ISO 1328-1:2013 (E)
- **标题**: *Cylindrical gears - ISO system of flank tolerance classification - Part 1: Definitions and allowable values of flank deviations relevant to the corresponding flank tolerance classes*
- **内容**: 规定了渐开线圆柱齿轮齿廓公差分类的ISO体系。定义了齿廓偏差（如齿廓总偏差 `Fα`、齿廓形状偏差 `fHα`、齿廓倾斜偏差 `fHβ`）和螺旋线偏差（如螺旋线总偏差 `Fβ`、螺旋线形状偏差 `fHβ`、螺旋线倾斜偏差 `fHβ`）的定义及其允许值。精度等级通常从 0 到 12，数字越小，精度越高。

#### ISO 1328-2:1997 (E) / ISO 1328-2:2013 (E)
- **标题**: *Cylindrical gears - ISO system of flank tolerance classification - Part 2: Definitions and allowable values of deviations relevant to radial composite deviations and radial runout*
- **内容**: 定义了与径向综合偏差和径向跳动相关的偏差的定义和允许值。

#### AGMA 2000-A88 / AGMA 2015-1-A01
- **标题**: *Gear Classification and Inspection Handbook - Tolerances and Measuring Methods for Unassembled Spur and Helical Gears* (AGMA 2000-A88) / *Accuracy Classification System - Radial System* (AGMA 2015-1-A01)
- **内容**: AGMA标准定义了齿轮的精度分类和检验方法。AGMA 2000-A88 是一个较老的标准，定义了从 A0 到 A14 的精度等级。AGMA 2015-1-A01 引入了径向精度分类系统，与ISO标准更接近。

### 3.3 强度计算标准

#### ISO 6336 (所有部分)
- **标题**: *Calculation of load capacity of spur and helical gears*
- **内容**: 这是一套非常重要的系列标准，详细规定了直齿轮和斜齿轮承载能力的计算方法，包括：
    - ISO 6336-1: 基本原则、一般资料、基本公式和计算方法。
    - ISO 6336-2: 齿面接触疲劳强度计算。
    - ISO 6336-3: 齿根弯曲疲劳强度计算。
    - ISO 6336-5: 材料强度。
    - ISO 6336-6: 变速箱的温升计算。
    - 等等。

#### AGMA 2101-D04 / AGMA 2001-D04
- **标题**: *Fundamental Rating Factors and Calculation Methods for Involute Spur and Helical Gear Teeth* (AGMA 2101-D04) / *Design Manual for Parallel Shaft Fine-Pitch Gearing* (AGMA 2001-D04)
- **内容**: AGMA 2101-D04 提供了渐开线直齿轮和斜齿轮轮齿强度校核的基本评级因素和计算方法。AGMA 2001-D04 是细间距平行轴齿轮的设计手册。

### 3.4 其他相关标准

#### DIN 3960:2005-03 / DIN 3967:2005-03
- **标题**: *Tolerances for cylindrical gears - General principles, deviations relevant to flanks, tooth thickness and backlash* (DIN 3960) / *Tolerances for cylindrical gears - Definitions and permissible values of deviations relevant to radial composite deviation and radial runout* (DIN 3967)
- **内容**: 德国标准，与ISO 1328系列标准内容相近，规定了圆柱齿轮的公差、偏差定义和允许值。

#### JIS B 1701:2009 / JIS B 1702-1:2009 / JIS B 1702-2:2009 / JIS B 1703:2009
- **标题**: *Cylindrical gears - Vocabulary* (JIS B 1701) / *Calculation of load capacity of spur and helical gears - Part 1: Basic principles, general information and basic equations* (JIS B 1702-1) / *Calculation of load capacity of spur and helical gears - Part 2: Calculation of surface durability (pitting)* (JIS B 1702-2) / *Cylindrical gears - Standard basic rack contour* (JIS B 1703)
- **内容**: 日本工业标准，涵盖了齿轮词汇、承载能力计算（弯曲和点蚀）以及标准基本齿条轮廓，与ISO标准体系对应。

## 4. 齿轮建模专题计划

### 4.1 目标

使用 CadQuery 构建一系列参数化齿轮模型，包括但不限于直齿轮、斜齿轮、伞齿轮等。每个模型应能通过调整关键参数（如模数、齿数、压力角等）生成不同规格的齿轮。

### 4.2 项目结构规划

在现有项目结构基础上，增加齿轮相关的目录和模块：

```
Example4CadQuery/
├── app/                
│   ├── gears/               # 齿轮建模代码主目录
│   │   ├── __init__.py      # 包初始化文件
│   │   ├── spur.py          # 直齿轮建模模块
│   │   ├── helical.py       # 斜齿轮建模模块 (后续添加)
│   │   ├── bevel.py         # 伞齿轮建模模块 (后续添加)
│   │   └── ...              # 其他类型齿轮
│   └── ... (其他模块)
├── docs/               
│   ├── gears-design.md      # 齿轮设计原理与参数详解
│   ├── gears-standards.md   # 齿轮相关标准 (ISO, AGMA等) 摘要
│   └── ... (其他文档)
└── output/             
    └── gears/               # 齿轮模型输出目录
        ├── spur/            # 直齿轮输出
        ├── helical/         # 斜齿轮输出 (后续添加)
        ├── bevel/           # 伞齿轮输出 (后续添加)
        └── ...              # 其他类型齿轮输出
```

### 4.3 第一阶段：直齿轮 (Spur Gear) 建模

### 4.3.1 设计文档

详细说明直齿轮设计原理，包括几何参数、尺寸计算公式、渐开线生成原理和在 CadQuery 中的实现思路。

### 4.3.2 标准规范

摘要直齿轮相关的国际和国家标准，包括基础标准、精度标准和强度计算标准，并列出与建模相关的默认参数值。

### 4.3.3 建模代码

创建 `app/gears/spur.py` 模块，用于实现直齿轮的参数化建模。
- **核心函数**: `make_spur_gear(m, z, alpha=20, width=5, ...)`，返回一个 CadQuery `Solid` 或 `Compound` 对象。
- **参数**:
    - `m` (float): 模数。
    - `z` (int): 齿数。
    - `alpha` (float, optional): 压力角 (度)。默认为 20°。
    - `width` (float, optional): 齿宽。默认为 5mm。
    - `hub_diameter` (float, optional): 轮毂直径。默认为 `1.8 * m * sqrt(z)`。
    - `hub_length` (float, optional): 轮毂长度。默认为 `1.2 * m * sqrt(z)`。
    - `clearance` (float, optional): 顶隙系数。默认为 0.25 * m (用于计算 `hf`)。
    - `addendum` (float, optional): 齿顶高系数。默认为 1.0 * m (用于计算 `ha`)。
    - `gear_type` (str, optional): 齿轮类型 ("internal" 或 "external")。默认为 "external"。
- **功能**:
    1.  计算齿轮的各项关键尺寸。
    2.  生成一个齿的渐开线齿廓（2D草图）。
        -  计算基圆。
        -  生成理论渐开线。
        -  确定有效齿廓（考虑齿顶圆和齿根圆）。
        -  添加圆角（在齿根）。
    3.  将单个齿旋转复制 `z` 次，形成完整的齿圈。
    4.  创建中心孔和轮毂（如果是外部齿轮）。
    5.  将齿圈与轮毂（如果存在）进行布尔并集操作，得到最终的齿轮实体。
    6.  （可选）添加键槽。
- **输出**: 一个完整的 3D 齿轮模型对象。

### 4.3.4 运行与测试

实现命令行运行支持、可视化查看功能和参数化运行。

---
**整理日期**: 2025-08-06  
**最后更新**: 2025-08-06  
**维护者**: AI助手与人工监督