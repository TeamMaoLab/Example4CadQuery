#!/usr/bin/env python3
"""
CadQuery 轴承座示例
==================

官方 QuickStart 教程中的第一个例子 - 参数化轴承座模型

来源：https://cadquery.readthedocs.io/en/latest/quickstart.html

这是一个完整的参数化轴承座，包含：
- 中心轴承孔（22mm 直径，适用于 608 轴承）
- 四个 M2 沉头孔（位于四个角）
- 边缘圆角（2mm 半径）

学习要点：
- 工作平面 (Workplane) 的使用
- 链式调用构建模型
- 选择器 (faces, edges, vertices) 的应用
- 参数化设计方法
- 多格式导出功能
"""

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

# 显示模型（在 CQ-editor 中使用）
# show_object(result)

# 在命令行环境中，我们直接导出模型
print("正在导出模型...")

# 定义输出目录（相对于项目根目录）
import os
from pathlib import Path

# 获取项目根目录的绝对路径
project_root = Path(__file__).parent.parent.parent
output_dir = project_root / "output" / "quickstart"

# 确保输出目录存在
output_dir.mkdir(parents=True, exist_ok=True)

# 导出为不同格式
try:
    cq.exporters.export(result, f"{output_dir}/bearing_block.stl")
    print(f"✓ STL 文件导出成功: {output_dir}/bearing_block.stl")
except Exception as e:
    print(f"✗ STL 导出失败: {e}")

try:
    cq.exporters.export(result.section(), f"{output_dir}/bearing_block.dxf")
    print(f"✓ DXF 文件导出成功: {output_dir}/bearing_block.dxf")
except Exception as e:
    print(f"✗ DXF 导出失败: {e}")

try:
    cq.exporters.export(result, f"{output_dir}/bearing_block.step")
    print(f"✓ STEP 文件导出成功: {output_dir}/bearing_block.step")
except Exception as e:
    print(f"✗ STEP 导出失败: {e}")

# 导出模型（如果需要）
# cq.exporters.export(result, "bearing_block.stl")
# cq.exporters.export(result.section(), "bearing_block.dxf")
# cq.exporters.export(result, "bearing_block.step")

print("轴承座模型创建完成!")
print(f"尺寸: {height} x {width} x {thickness} mm")
print(f"轴承孔直径: {diameter} mm")
print(f"沉头孔: M2 (孔径2.4mm, 沉头直径4.4mm, 沉头深度2.1mm)")