#!/usr/bin/env python3
"""
CadQuery 可视化示例
==================

演示如何使用 CadQuery 的可视化功能直接打开窗口查看 3D 模型

来源：CadQuery 官方文档可视化部分
https://cadquery.readthedocs.io/en/latest/vis.html

使用方法：
    # 直接运行，会弹出 3D 查看窗口
    uv run app/quickstart/visualization_example.py
    
    # 或者在 Python 交互环境中导入使用
    from app.quickstart.visualization_example import create_model
    model = create_model()
"""

from cadquery import *
from cadquery.vis import show

def create_model():
    """
    创建一个示例模型：带圆角的半球壳
    
    返回：
        cadquery 对象：包含半球壳的模型
    """
    # 创建一个球体，保留下半部分
    w = Workplane().sphere(1).split(keepBottom=True)
    # 减去一个较小的内部球体，形成壳体
    w = w - Workplane().sphere(0.5)
    # 对顶面进行圆角处理
    r = w.faces('>Z').fillet(0.1)
    
    return r

def main():
    """
    主函数：创建模型并显示 3D 查看窗口
    """
    print("正在创建模型...")
    model = create_model()
    
    print("正在打开 3D 查看窗口...")
    print("提示：关闭窗口后程序会继续执行")
    
    # 显示模型，alpha=0.5 设置透明度
    show(model, alpha=0.5)
    
    print("3D 查看窗口已关闭")

if __name__ == "__main__":
    main()