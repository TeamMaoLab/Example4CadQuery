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
- 3D 可视化查看功能

使用方法：
    # 导出文件模式（默认）
    uv run app/quickstart/bearing_block.py
    
    # 可视化查看模式
    uv run app/quickstart/bearing_block.py --view
    
    # 同时导出和查看
    uv run app/quickstart/bearing_block.py --both
"""

import cadquery as cq
from cadquery.vis import show
import sys
from pathlib import Path

def create_bearing_block(height=60.0, width=80.0, thickness=10.0, diameter=22.0, padding=12.0):
    """
    创建轴承座模型
    
    参数:
        height: 高度 (mm)
        width: 宽度 (mm) 
        thickness: 厚度 (mm)
        diameter: 轴承孔直径 (mm)
        padding: 边距 (mm)
    
    返回:
        cadquery 对象: 轴承座模型
    """
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
    return result

def export_model(model, output_dir):
    """
    导出模型到文件
    
    参数:
        model: cadquery 对象
        output_dir: 输出目录路径
    """
    print("正在导出模型...")
    
    # 确保输出目录存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 导出为不同格式
    try:
        cq.exporters.export(model, str(output_dir / "bearing_block.stl"))
        print(f"✓ STL 文件导出成功: {output_dir / 'bearing_block.stl'}")
    except Exception as e:
        print(f"✗ STL 导出失败: {e}")

    try:
        cq.exporters.export(model.section(), str(output_dir / "bearing_block.dxf"))
        print(f"✓ DXF 文件导出成功: {output_dir / 'bearing_block.dxf'}")
    except Exception as e:
        print(f"✗ DXF 导出失败: {e}")

    try:
        cq.exporters.export(model, str(output_dir / "bearing_block.step"))
        print(f"✓ STEP 文件导出成功: {output_dir / 'bearing_block.step'}")
    except Exception as e:
        print(f"✗ STEP 导出失败: {e}")

def view_model(model):
    """
    在 3D 查看窗口中显示模型
    
    参数:
        model: cadquery 对象
    """
    print("正在打开 3D 查看窗口...")
    print("提示：关闭窗口后程序会继续执行")
    
    # 显示模型，设置透明度
    show(model, alpha=0.8)
    
    print("3D 查看窗口已关闭")

def main():
    """
    主函数：解析命令行参数并执行相应操作
    """
    # 解析命令行参数
    view_mode = False
    export_mode = True
    
    if "--view" in sys.argv:
        view_mode = True
        export_mode = False
    elif "--both" in sys.argv:
        view_mode = True
        export_mode = True
    
    # 参数定义
    height = 60.0    # 高度
    width = 80.0     # 宽度
    thickness = 10.0 # 厚度
    diameter = 22.0  # 轴承孔直径
    padding = 12.0   # 边距（孔距离边缘的距离）
    
    print("正在创建轴承座模型...")
    
    # 创建模型
    model = create_bearing_block(height, width, thickness, diameter, padding)
    
    # 根据模式执行操作
    if export_mode:
        # 获取输出目录
        project_root = Path(__file__).parent.parent.parent
        output_dir = project_root / "output" / "quickstart"
        export_model(model, output_dir)
    
    if view_mode:
        view_model(model)
    
    # 打印模型信息
    print("\n轴承座模型创建完成!")
    print(f"尺寸: {height} x {width} x {thickness} mm")
    print(f"轴承孔直径: {diameter} mm")
    print(f"沉头孔: M2 (孔径2.4mm, 沉头直径4.4mm, 沉头深度2.1mm)")
    
    if export_mode and not view_mode:
        print("\n提示: 使用 --view 参数可以打开 3D 查看窗口")
        print("       使用 --both 参数可以同时导出文件和查看模型")

if __name__ == "__main__":
    main()